#!/usr/bin/env python

from netmiko import ConnectHandler
import mysql.connector
from pandas.io import sql
import csv
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.sql import alias, select


#driver = get_network_driver('ios')

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
Vcursor = myDB.cursor()
vardb = "INSERT INTO VLANS (VLAN, NAME,STATUS,PORT) VALUES (%s, %s, %s, %s)"
dat = ('12', 'updatedVLAN', 'Active', ' ')
Vcursor.execute(vardb,dat)
myDB.commit()
Vcursor.execute("SELECT*FROM VLANS")
myresv = Vcursor.fetchall()


sql = "SELECT VLAN, NAME FROM VLANS WHERE VLAN = %s"

sql_select = (12,)
Vcursor.execute(sql, sql_select)

myresult = Vcursor.fetchone()

#Converting Tuple into Strings to store in a file
h = myresult[0]
strh = ''.join(h)

hel =  myresult[1]
strh1 = ''.join(hel)

straw = "Vlan "+strh +'\n'
Joke = "Name " + strh1 +'\n'
with open("/home/VlanAutomation/DBtoSwitch.txt", 'w') as out:
        out.writelines([straw, Joke])

###############################################################
############# CODE IN PROGRESS!!!!
#############
###############################################################

#for x in myresv:
#       print(x)

iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.73',
    'username': 'taqi',
    'password': 'cisco',
}

net_connect = ConnectHandler(**iosv_l2)
net_connect.find_prompt()
#output = net_connect.send_command('show ip int brief')
#print output

VLN = raw_input('Do you want to create Vlans? Y/N ')
if VLN == "Y":

        for n in range (2,5):
                print "Creating VLAN " + str(n)
                config_commands = ['vlan ' + str(n), 'name Sales_VLAN'+str(n)]
                output = net_connect.send_config_set(config_commands)
                print output

        for n in range (6,10):
                print "Creating VLAN " + str(n)
                config_commands = ['vlan ' + str(n), 'name Finance_VLAN'+str(n)]
                output = net_connect.send_config_set(config_commands)
                print output


        outputData = net_connect.send_command('Show vlan brief')
        #print (json.dumps(outputData, indent=3))
#       print(outputData)

#       Vln_ = TorontovL2.get_vlans()
#       print (json.dumps(Vln_, indent=3))

        with open('/home/VlanAutomation/ShowVlanBrief.txt', 'w' ) as Vlan_Brief1:
                Vlan_Brief1.write(outputData)
                Vlan_Brief1.close()


         #This code is for database

        data = pd.read_csv('/home/VlanAutomation/ShowVlanBrief.txt', skiprows=[2], names =['VLANS'])
#       data.columns = [ "VLAN","NAME", "STATUS"]
        print("Printing DataFrame")

# bydefault splitting is done on the basis of single space.
        dataintocolumns = data.VLANS.str.split(expand=True)
        print(dataintocolumns)

 #creating engine:

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        dataintocolumns.to_sql('VLANS', engine, if_exists = 'replace',index=False)



 #       file = open ('/home/VlanAutomation/ShowVlanBrief.txt', 'r')
 #       file_content = file.readlines()[2:]
#       print (file_content)
#       file.close()

#       print "Syncing Database with Switch... "
#       query = ("INSERT INTO VLANS (ID, NAME, STATUS) VALUES (%s, %s, %s)")

        #Split() method is used to splits a string into a list
#       values = [line.split('') for line in file_content

#       query = ("INSERT INTO VLANS (ID, NAME, DESCRIPTION) VALUES (%s, %s, %s)")
#       Vcursor.executemany(query,values)
#       mydb.commit()
#       Vcursor.execute ("SELECT*FROM VLANS")

#       result = cursor.fetchall()
#       for x in result:
#               print(x)

else :
        print 'No Vlan Added'

DELVLN = raw_input('Do you want to delete Vlans? Y/N?')

if DELVLN == "Y" :
        DELVLN2 = raw_input('1. 2-4 or 2. 6-9? ' )
        if DELVLN2 == '1':
                for b in range (2,5):
                        print "Deleting Vlans from 2-5"
                        config_commands = [ 'no vlan ' + str(b)]
                        output1 = net_connect.send_config_set(config_commands)
                        print output1
        elif DELVLN2 == '2' :
                for c in range (6,10):
                        print "Deleting Vlans from 6-10"
                        config_commands = ['no vlan ' + str(c)]
                        output2 = net_connect.send_config_set(config_commands)
                        print output2
        DataDelete = net_connect.send_command('Show vlan brief')
#       print DataDelete


        with open('/home/VlanAutomation/DeletedVlans.txt', 'w') as Del_Vlan_DB:
                Del_Vlan_DB.write(DataDelete)
                Del_Vlan_DB.close()

        dataD = pd.read_csv('/home/VlanAutomation/DeletedVlans.txt', skiprows=[2], names =['VLANS'])
#       data.columns = [ "VLAN","NAME", "STATUS"]
        print("Printing DataFrame")

# bydefault splitting is done on the basis of single space.
        dataintocolumnsD = dataD.VLANS.str.split(expand=True)
        print(dataintocolumnsD)

 #creating engine:

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        dataintocolumnsD.to_sql('VLANS', engine, if_exists = 'replace',index=False)



elif DELVLN =="N" :
        print "Vlans not delete"

else :
    print ("Non")


### USE CASE: UPDATE ENTRY IN MYSQL, and Configure SWITCH with SYNCED ENTRIES



UPDB = raw_input("Do you want to UPDATE your Database Y/N?")

if UPDB == 'Y':

        print("Updating  VLAN Entry in DB:NETWORK..")
        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        engine.execute('INSERT INTO VLANS(0, 1, 2) VALUES ("14","UpdateVLAN", "Active")')



        result = engine.execute('SELECT * FROM VLANS')
        for _r in result:
                 print(_r)


else:
        print("non")
