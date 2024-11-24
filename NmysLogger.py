import mysql.connector
import getopt,sys
import time
from enum import Enum
import LocalConfig as cfg
import Table1Config as table1
import Table2Config as table2
import Table3Config as table3




class SqlLogConnection() :
    """
    Logger class
    """
    __password:str = ""
    __user:str = ""
    __ipaddress:str = ""
    __dataBaseName="netLogger"
    __dbConnection = None
    __dbTable1:str=""
    __testCaseId:str=""
    __productSn:str=""
    __port:int = 0

    def __init__(self)->None:
        self.__ipaddress =  cfg.setup_config["IPAddress"]
        self.__user = cfg.setup_config["user"]
        self.__password = cfg.setup_config["password"]
        self.__dataBaseName = cfg.setup_config["dbName"]
        self.__port = cfg.setup_config["port"]
        self.__productSn = cfg.setup_config["productSn"]
        self.__dbTable1 =cfg.setup_config["tableName1"]
        self.__dbTable2 =cfg.setup_config["tableName2"]
        self.__dbTable3 =cfg.setup_config["tableName3"]
        self.connect()

    def connect(self)->int:
        """
        Return a mysql connection or None on failure
        connect to the db
        """
        try:
            self.__dbConnection = mysql.connector.connect(
            user=self.__user,
            password=self.__password,
            host=self.__ipaddress,
            database=self.__dataBaseName,
            port=self.__port
            )
 
            if self.__dbConnection:
                if self.__dbConnection and self.__dbConnection.is_connected():
                    print("Connected")
                    self.SQLPrintDB1("New Connection","{0}".format(self.__productSn))
                    return 1
            else:
                print('Connection Fail !!!')
                return 0
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return -1 

    def disconnect(self)->None:
        """
        Return none
        Disaconnects from a database
        """
        if self.__dbConnection != None:
            try:
                self.__dbConnection.disconnect()
                self.__dbConnection = None
            except mysql.connector.Error as err:
                print('Error {}'.format(err))
                return
        print("Disconnect")
 

    def createTables(self)->int:
        """
        Return int, 0 on success, -1 on failure
        create tables
        """
        if self.__dbConnection:
            mycursor = self.__dbConnection.cursor()
            # Create table 1
            try:
                mycursor.execute("DROP TABLE {};".format(self.__dbTable1))
            except mysql.connector.Error as err:
                print("Error {}".format(err))
        
            mycursor.execute(table1.defStr.format(self.__dbTable1))
            self.__dbConnection.commit()
            try:
                mycursor.execute("SHOW TABLES")
                for x in mycursor:
                    print("Table {0} Created".format(x))
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
                return -1
        
            # Create table 2
            try:
                mycursor.execute("DROP TABLE {};".format(self.__dbTable2))
            except mysql.connector.Error as err:
                print("Error {}".format(err))
        
            mycursor.execute(table2.defStr.format(self.__dbTable2))
            self.__dbConnection.commit()
            try:
                mycursor.execute("SHOW TABLES")
                for x in mycursor:
                    print("Table {0} Created".format(x))
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
                return -1
            
            # Create table 3
            try:
                mycursor.execute("DROP TABLE {};".format(self.__dbTable3))
            except mysql.connector.Error as err:
                print("Error {}".format(err))
        
            mycursor.execute(table3.defStr.format(self.__dbTable3))
            self.__dbConnection.commit()
            try:
                mycursor.execute("SHOW TABLES")
                for x in mycursor:
                    print("Table {0} Created".format(x))
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
                return -1
        
        return 0

    def GetConnectedState(self):

        # Returns connection value, or none
        
        if self.__dbConnection != None:
            print("Connected")
        else:
            print("Disconnected")

        return self.__dbConnection

    def SQLPrintDB1(self,instr,tsid)->None:
        
        # Returns: None
        # Print function 1 simple print
    
        if self.__dbConnection != None:
            mycursor = self.__dbConnection.cursor()
            mycursor.execute('USE {0};'.format(self.__dataBaseName))

            add_log = ("INSERT INTO netLogger.primaryLog "
                   "(logEntry, UUT, TSID) "
                "VALUES (%s, %s, %s);")

            data_log = [instr,tsid,self.__productSn]
            try: 
                mycursor.execute(add_log,data_log)
                self.__dbConnection.commit()

            except mysql.connector.Error as err:
                print("Error={}",err)


