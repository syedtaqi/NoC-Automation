#Author: TAQI RAZA, CCNP CERTIFIED, NETWORK AUTOMATION ENGINEER
#COPYRIGHT @2020

#!/usr/bin/env python

#PRE-REQUISITE: RUN SCRIPT vlan2Db.py before running this script
#SWITCH AND DATABASE SYNCRONIZATION, USTILIZING NETWORK PROGRAMABILITY TECHNIQUES

from netmiko import ConnectHandler
import mysql.connector
#from pandas.io import sql
#import csv
#import pandas as pd
#import json
#from sqlalchemy import create_engine
#import pymysql
#from sqlalchemy.sql import alias, select


hostname ="localhost"
uname ="root"
pwd="taqi"
dbname ="NETWORK"


myDB = mysql.connector.connect(
        host =hostname,
        user =uname,
        password=pwd,
        database =dbname
)

##DO an IF/ELSE STATEMENT

forDB = raw_input("Add new VLAN Database? Y/N: ")

if forDB == "Y":
        a = raw_input("Choose VLAN ID (2-4094) :")
        b = raw_input("Enter VLAN NAME :")

        Vcursor = myDB.cursor()
        print("Updating Database...")
        vardb = "INSERT INTO VLANS (VLAN, NAME,STATUS,PORT) VALUES (%s, %s, %s, %s)"
        dat = (a, b, 'Active', ' ')
        Vcursor.execute(vardb,dat)
        myDB.commit()
        Vcursor.execute("SELECT*FROM VLANS")
        myresv = Vcursor.fetchall()


        sql = "SELECT VLAN, NAME FROM VLANS WHERE VLAN = %s"
        #Captures new entry as per the user input from the database, and makes fetches info to the switch
        sql_select = (a,)
        Vcursor.execute(sql, sql_select)

        myresult = Vcursor.fetchone()

#Converting tuple into the string, to store in a file
        h = myresult[0]
        strh = ''.join(h)

        hel =  myresult[1]
        strh1 = ''.join(hel)

#Adding string infront of variables, to build a config file for vlan configuration
#Writing lines to a file saved in a directory
        straw = "Vlan "+strh +'\n'
        Joke = "Name " + strh1 +'\n'
        with open("/home/VlanAutomation/DBtoSwitch_Commands", 'w') as out:
                out.writelines([straw, Joke])


#Opening a file
        with open('/home/VlanAutomation/DBtoSwitch_Commands') as fopn:
                command_to_send = fopn.read().splitlines()
#Creating dictionary for Switch

        iosv_l2 = {
        'device_type': 'cisco_ios',
        'ip': '192.168.122.73',
        'username': 'taqi',
        'password': 'cisco',
        }

        all_devices =[iosv_l2]

        #for loop to Update the switch as per the new entry from the Database
        for device in all_devices:
                net_connect = ConnectHandler(**iosv_l2)
                vloutput = net_connect.send_config_set(command_to_send)
        print("Updating Switch....")
        vldata = net_connect.send_config_set("Do Show Vlan Brief")
        print(vldata)

        print("Storing Show Vlan Brief to a file....")
        with open('/home/VlanAutomation/VLAN-Update-Log.txt', 'w' ) as Vlan_Brief1:
                Vlan_Brief1.write(vldata)
                Vlan_Brief1.close()

else:
        print "No Vlan Added"
        print "Exit"

###End of Code

