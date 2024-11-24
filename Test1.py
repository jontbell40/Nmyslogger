import mysql.connector
import getopt,sys
import NmysLogger
import time
from enum import Enum


def start()->int:
    """
    Return a integer , 0 success
                         -1 failure
    Simple test, create tables, add one comment to db 1
    """
    nConnect = None
    argument_list = sys.argv[1:]
    options = "c"
    long_options =["create"]
    try:
        arguments, values = getopt.getopt(argument_list,options,long_options)
        for cArgument, cValue in arguments:
            if cArgument in ['-c',"--create"]:
                nConnect=NmysLogger.SqlLogConnection()
                if nConnect.GetConnectedState != None:
                    print("Creating db Table")
                    nConnect.createTables()
                    nConnect.disconnect()
                else:
                    print("Connection not made")
            
            
    except getopt.error as err:
        print(str(err))
        return -1
    
    nConnect = NmysLogger.SqlLogConnection()
    if nConnect != None:
        nConnect.SQLPrintDB1("This is a new test","TSC:43256")
        nConnect.disconnect()
    return 0

if __name__ == "__main__":
    start()
