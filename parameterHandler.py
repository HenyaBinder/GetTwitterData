#########################################################
###       Handle parametersTbl related functions      ###
#########################################################

import connectToMySQL as mySQLDB
import logHandler as log

##
## Function Name: getNumberOfDays
##
## Fetch from parametersTBL the number
## that assigned to the parameter
##
## Parameters:
##      paramName - Name of the parameter
##      days - Overrite the number the defined in the table
##
##
def getNumberOfDays(paramName, days=0):

    try:
        db = mySQLDB.mySqlHandle()

        if (days <= 0):
            results = db.selectDataInParametersTBL(paramName)
            data = list(results[0])

            num_of_days = data[2]
        else:
            num_of_days = days

        db.closeConnection()

        return(num_of_days)

    except Exception as e:
        logger = log.myLogger("parameterHandler", "getNumberOfDays")
        logger.logError("ERROR: {},   Status code: {}.".format(response.text, response.status_code))
        return (days)


