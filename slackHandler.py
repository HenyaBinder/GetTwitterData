
#########################################################
###      Handle Slack Messaging related functions     ###
#########################################################

import requests
import configuration as c
import connectToMySQL as mySQLDB
import logHandler as log
import parameterHandler as p



##
## Function Name: sendMessageToSlack
##
## Send message to Slack
##
## Input parameter:
##      webHook - Messages will be sent to this channel
##      message - Message containt
##
def sendMessageToSlack(webHook, message):
    try:
        if (webHook == ""):
            webhook_url = c.slack_sch_msg_url
        else:
            webhook_url = webHook

        payload = {"text": message}
        response = requests.post(webhook_url,
                                 json=payload,
                                 headers={'Content-Type': 'application/json'}
                                )
    except Exception as e:
        logger = log.myLogger("slackHandler", "sendMessageToSlack")
        logger.logError("ERROR: {},   Status code: {}.".format(response.text, response.status_code))
        return ()




##
## Function Name: createTweetsRemovedMessge
##
## Send message to Slack for all tweets that
#  were deleted in the last "days"
##
## Input parameter:
##      days - Number of days for data range
##
def createTweetsRemovedMessge (days=0):

    # Calculate number of days
    try:
        if (days < 1):
            num_of_days = p.getNumberOfDays(c.removedTweetsMail, days)
        else:
            num_of_days = days

        db = mySQLDB.mySqlHandle()

        # Bring tweet ids for all removed tweets that were updated in last num_of_days
        data = db.selectDataInTweetReportsTbl("logiRemoved = '{}' and reportingDate >= (now() - interval {} day) order by updatedVolDate".
                                              format('Y',num_of_days))
        db.closeConnection()
    except Exception as e:
        logger = log.myLogger("slackHandler", "createTweetsRemovedMessge")
        logger.logError("ERROR: {}".format(str(e)))
        db.closeConnection()
        return()

    # Create Message
    if (len(data) > 0):
        message = ''.join(["\nTweet id *{}* was removed at {}".format(rec[6], rec[17]) for rec in data])
    else:
        message = "*During the last {} days no tweet was deleted*".format(num_of_days)

    # Send message
    sendMessageToSlack(c.slack_sch_msg_url, message)


##
## Function Name: createNewTweetsMessge
##
## Send message to Slack for all new tweets in last "days"
##
## Input parameter:
##      days - Number of days for data range
##
def createNewTweetsMessge (days):

    try:
        # Calculate number of days
        if (days <= 0):
            num_of_days = p.getNumberOfDays(c.newTweetsMail, days)
        else:
            num_of_days = days

        # Bring all new tweets that were created in last num_of_days days
        db = mySQLDB.mySqlHandle()
        data = db.selectDataInTweetReportsTbl("reportingDate >= (now() - interval {} day) order by reportingDate".
                                              format(num_of_days))
        db.closeConnection()

    except Exception as e:
        logger = log.myLogger("slackHandler", "sendMessageToSlack tweets")
        logger.logError("ERROR: {}".format(str(e)))
        db.closeConnection()
        return()

    # Create Message
    if (len(data) > 0):
        message = ''.join(["\nTweet id *{}* was created at {}".format(rec[6], rec[17]) for rec in data])
    else:
        message = "*During the last {} days no antisemitic tweet was founded*".format(num_of_days)

    # Send message
    sendMessageToSlack(c.slack_sch_msg_url, message)

