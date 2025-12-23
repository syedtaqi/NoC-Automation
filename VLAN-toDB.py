#Author: TAQI RAZA, CCNP CERTIFIED, NETWORK AUTOMATION ENGINEER
#COPYRIGHT @2025

#!/usr/bin/env python

from netmiko import ConnectHandler
import mysql.connector
from pandas.io import sql
import csv
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql

#Variables for Database
hostname ="localhost"
uname ="root"
pwd="taqi"
dbname ="NETWORK"

#Dictionary to connect to the Switch
iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.73',
    'username': 'taqi',
    'password': 'cisco',
}

net_connect = ConnectHandler(**iosv_l2)
net_connect.find_prompt()

#IF/ELSE STATEMENTS to Automatically Create/Delete VLANS in a Switch
#Retrieve the Information from the Switch "Show Vlan Brief"
#Store in the directory as a file
#Read a file in  a table format
#Utilized SQLALCHEMY framework to Read a file in a table format, and Migrate the data to the Database
#IF Vlans Deleted, Migrate the updates in the DB Accordingly

VLN = raw_input('Do you want to create Vlans? Y/N ')
if VLN == "Y":
        #Creating VLANS 2-4
        for n in range (2,5):
                print "Creating VLAN " + str(n)
                config_commands = ['vlan ' + str(n), 'name Sales_VLAN'+str(n)]
                output = net_connect.send_config_set(config_commands)
                print output

        #Creating VLANS 6-9
        for n in range (6,10):
                print "Creating VLAN " + str(n)
                config_commands = ['vlan ' + str(n), 'name Finance_VLAN'+str(n)]
                output = net_connect.send_config_set(config_commands)
                print output

        #Retrieve SH VLAN BRIEF INFORMATION to STORE IN A VARIABLE
        outputData = net_connect.send_command('Show vlan brief')


        #print (json.dumps(outputData, indent=3))
#       print(outputData)

        #Open a file, and write Information to file stored in OUTPUTDATA VARIABLE
        with open('/home/VlanAutomation/ShowVlanBrief.txt', 'w' ) as Vlan_Brief1:
                Vlan_Brief1.write(outputData)
                Vlan_Brief1.close()


         #This code is for database
        #Utilizing Pandas framework to read the file
        data = pd.read_csv('/home/VlanAutomation/ShowVlanBrief.txt', skiprows=[2], names =['VLANS'])
#       data.columns = [ "VLAN","NAME", "STATUS"]
        print("Printing DataFrame")

        # bydefault splitting of column is done on the basis of single space.
        dataintocolumns = data.VLANS.str.split(expand=True)
        dataintocolumns.columns = ["VLAN", "NAME", "STATUS", "PORT"]
        print(dataintocolumns)
        #colname = dataintocolumns.columns["VLANS", "NAME", "DESCRIPTION"]


        #creating engine to connect to database, and update/replace the tables within the database:

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        dataintocolumns.to_sql('VLANS', engine, if_exists = 'replace',index=False)


else :
        print 'No Vlan Added'

DELVLN = raw_input('Do you want to delete Vlans? Y/N?')

if DELVLN == "Y" :
        DELVLN2 = raw_input('1. 2-4 or 2. 6-9? ' )
        if DELVLN2 == '1':
                for b in range (2,5):
                        print "Deleting Vlans from 2-4"
                        config_commands = [ 'no vlan ' + str(b)]
                        output1 = net_connect.send_config_set(config_commands)
                        print output1
        elif DELVLN2 == '2' :
                for c in range (6,10):
                        print "Deleting Vlans from 6-9"
                        config_commands = ['no vlan ' + str(c)]
                        output2 = net_connect.send_config_set(config_commands)
                        print output2
        DataDelete = net_connect.send_command('Show vlan brief')
#       print DataDelete


        with open('/home/VlanAutomation/DeletedVlans.txt', 'w') as Del_Vlan_DB:
                Del_Vlan_DB.write(DataDelete)
                Del_Vlan_DB.close()

        dataD = pd.read_csv('/home/VlanAutomation/DeletedVlans.txt', skiprows=[2], names =['VLANS'])



# bydefault splitting is done on the basis of single space.
        dataintocolumnsD = dataD.VLANS.str.split(expand=True)
#       dataintocolumnsD.columns["VLAN" , "NAME", "STATUS", "PORT"]
#        print(dataintocolumnsD)


 #creating engine:
        print("Updating Database...")

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        dataintocolumnsD.to_sql('VLANS', engine, if_exists = 'replace', index=False)



elif DELVLN =="N" :
        print "Vlans not delete"

else :
    print ("Non")




