import gsheetsHandler as gs
import configuration as c
from datetime import datetime, timedelta
import connectToMySQL as m

fromDate = datetime.now() - timedelta(days=10)  # timedelta(10)
toDate = datetime.now()
db = m.mySqlHandle()
wks = gs.connectByName(c.reports_file_name, c.ws_posts)


def updateCat():
    global fromDate
    global wks
    print('fromDate = {}'.format(fromDate))

    gs.categoryUpdate(wks, fromDate,toDate)


def checkExistingRows(date1, date2):
    global db
    print('count rows in db from {},{} = {}'.format(date1, date2, len(db.selectDataInTweetReportsTbl("reportingDate >= '{}' and reportingDate <='{}'".format(date1, date2)))))


def insertFromGSToMySQL():
    global fromDate
    global wks
    global db
    date_str = toDate.strftime("%d-%m-%Y")
    cells = wks.find(pattern=date_str, matchEntireCell=True, cols=[c.gs_date[0], c.gs_date[0]])
    print('count of rows {}'.format(len(cells)))
    if (cells and len(cells) > 0):
        for cell in cells:
            tweetID = wks.get_value(c.gs_tweet_id[1] + str(cell.row))
            rec = db.selectDataInTweetReportsTbl("tweetID='{}'".format(tweetID))
            if(rec and len(rec)==0):
                gs.copyTweetSheetsToMySQL(wks, tweetID)
                print('tweetID {} inserted to the DB'.format(tweetID))


updateCat()
checkExistingRows(fromDate.strftime("%d-%m-%Y"), toDate.strftime("%d-%m-%Y"))
insertFromGSToMySQL()

