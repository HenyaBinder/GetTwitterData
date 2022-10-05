import sys
import pygsheets as gc

gsheets_keys = "{}".format(sys.argv[1])
gsheets_file_name = "{}".format(sys.argv[2])
workbook = "{}".format(sys.argv[3])
tweet_id = "{}".format(sys.argv[4])


# Connect to Google Sheets
gs = gc.authorize(service_account_file=gsheets_keys)
sh = gs.open(gsheets_file_name)
wks = sh.worksheet_by_title(workbook)

cells = wks.find(pattern=str(tweet_id), matchEntireCell=True, cols=[1, 1])

if (len(cells) != 0):
    row_no = cells[0].row
    print("Row Num:", row_no)

    if row_no > 0:
         cell_no = "C" + str(row_no)
         wks.update_value(cell_no, "Removed")
