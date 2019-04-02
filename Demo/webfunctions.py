import pandas as pd
import numpy as np
import mysql.connector
import datetime as dt
import dateutil
config = {
  'host':'mytestservermanipal.mysql.database.azure.com',
  'user':'myadmin@mytestservermanipal',
  'password':'Qwerty123',
  'database':'careplex',
  'ssl_ca':'/Users/pradeepl/Documents/ssl/BaltimoreCyberTrustRoot.crt.pem'
}



def findavg():
    conn = mysql.connector.connect(**config)
    cursor1 = conn.cursor()
    cursor1.execute("select Slot_Time,Bill_Amount,Specialization from careplex.billing_final inner join careplex.slot_db on billing_final.Slot_No = slot_db.Slot_No inner join careplex.user on user.User_ID = slot_db.Doctor_ID where slot_db.Entity_ID ='H0001'")
    rv1 = cursor1.fetchall()
    cursor1.close()
    hospital1= pd.DataFrame(rv1,columns = ["date","amt","Specialization"])
    hospital1['date'] = pd.to_datetime(hospital1['date'])
    li_hospital1=list(hospital1['date'].astype(np.int64) // 10**6)
    li2_hospital1 = list(hospital1['amt'])
    li3_hospital1 = []
    for ch in range(len(li_hospital1)):
        li4 = []
        li4.append(li_hospital1[ch])
        li4.append(li2_hospital1[ch])
        li3_hospital1.append(li4)
############################################################hosital 2  ##################################################################
    conn = mysql.connector.connect(**config)
    cursor2 = conn.cursor()
    cursor2.execute("select Slot_Time,Bill_Amount,Specialization from careplex.billing_final inner join careplex.slot_db on billing_final.Slot_No = slot_db.Slot_No inner join careplex.user on user.User_ID = slot_db.Doctor_ID where slot_db.Entity_ID ='H0002'")
    rv2 = cursor2.fetchall()
    cursor2.close()
    hospital2 = pd.DataFrame(rv2,columns = ["date","amt","Specialization"])
    hospital2['date'] = pd.to_datetime(hospital2['date'])
    li_hospital2=list(hospital2['date'].astype(np.int64) // 10**6)
    li2_hospital2 = list(hospital2['amt'])
    li5_hospital2 = []
    for ch in range(len(li_hospital2)):
        li4 = []
        li4.append(li_hospital2[ch])
        li4.append(li2_hospital2[ch])
        li5_hospital2.append(li4)
#################################################################hospital 3 #######################################################################    
    conn = mysql.connector.connect(**config)
    cursor3 = conn.cursor()
    cursor3.execute("select Slot_Time,Bill_Amount,Specialization from careplex.billing_final inner join careplex.slot_db on billing_final.Slot_No = slot_db.Slot_No inner join careplex.user on user.User_ID = slot_db.Doctor_ID where slot_db.Entity_ID ='H0003'")
    rv3 = cursor3.fetchall()
    cursor3.close()
    hospital3 = pd.DataFrame(rv3,columns = ["date","amt","Specialization"])
    hospital3['date'] = pd.to_datetime(hospital3['date'])
    li_hospital3=list(hospital3['date'].astype(np.int64) // 10**6)
    li2_hospital3 = list(hospital3['amt'])
    li6_hospital3 = []
    for ch in range(len(li_hospital3)):
        li4 = []
        li4.append(li_hospital3[ch])
        li4.append(li2_hospital3[ch])
        li6_hospital3.append(li4)
    
    return li3_hospital1,li5_hospital2,li6_hospital3


def specialization_total_vs_booked(specialization):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("select Slot_Time,Slot_Status,Specialization from careplex.Slot_db inner join careplex.user on  Slot_db.Doctor_ID = user.User_ID")
    rv = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(rv,columns = ['date','Slot_status','specialization'])
    df['date'] = pd.to_datetime(df['date'])
    df2=df.groupby(['specialization',df['date'].dt.month])
    df3=df2['Slot_status'].count()
    df4=df3.to_frame(name="slot_count")
    df4.reset_index()
    d2=dict(df4.groupby(['specialization'])['slot_count'].apply(list))
    df5=df[df['Slot_status']=='BOOKED']
    df6=df5.groupby(['specialization',df['date'].dt.month])
    df7=df6['Slot_status'].count()
    df8=df7.to_frame(name="slot_count")
    df8.reset_index()
    d1=dict(df8.groupby(['specialization'])['slot_count'].apply(list))
    Booked = d1.get(specialization,'NA')
    Total  = d2.get(specialization,'NA')
    send_to_graph = {"Total":Total,"Booked":Booked}
    return send_to_graph

def find_month(front_end):
    # front_end = 'January'
    if front_end == 'January':
        month = 1
    elif front_end == 'February':
        month = 2
    elif front_end == 'March':
        month = 3
    elif front_end == 'April':
        month = 4
    elif front_end == 'May':
        month = 5
    elif front_end == 'June':
        month = 6
    elif front_end == 'July':
        month = 7
    elif front_end == 'August':
        month = 8
    elif front_end == 'September':
        month = 9
    elif front_end == 'October':
        month = 10
    elif front_end == 'November':
        month = 11
    elif front_end == 'December':
        month = 12
    return month

def doctorLabRefer(monthValue):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT  u.User_name, i.Slot_Time, Doctor_ID, Specialization, Inference FROM user u INNER JOIN slot_db s ON u.User_ID = s.Doctor_ID INNER JOIN slot_inference i ON s.Slot_NO = i.Slot_NO WHERE s.Slot_Status = 'BOOKED'")
    slot_status=cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(slot_status,columns = ['username', 'date','doctor_id', 'specialization', 'inference'])
    df['date'] = pd.to_datetime(df['date'])
    df_nd = df.drop(['doctor_id'], axis = 1)
    df_0 = df_nd[df_nd.inference != 'Surgery']

    month = find_month(monthValue)
    df_doc1 = df[df['date'].dt.month == month]
    df_doc1 = df_doc1[df_doc1.inference != 'Surgery']
    df_doc1 = df_doc1.groupby(['doctor_id', 'username'])

    df_doc2 = df_doc1['inference'].count()
    df_doc3 = df_doc2.reset_index()

    doctor_name = list(df_doc3['username'])
    lab_refer = list(df_doc3['inference'])
    d3 = {'doctorName': doctor_name, 'labsReferred': lab_refer}

    #####Department Lab ?Test#####
    

    return d3

def depLabPerformed(monthValue):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT  u.User_name, i.Slot_Time, Doctor_ID, Specialization, Inference FROM user u INNER JOIN slot_db s ON u.User_ID = s.Doctor_ID INNER JOIN slot_inference i ON s.Slot_NO = i.Slot_NO WHERE s.Slot_Status = 'BOOKED'")
    slot_status=cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(slot_status,columns = ['username', 'date','doctor_id', 'specialization', 'inference'])
    df['date'] = pd.to_datetime(df['date'])
    df_nd = df.drop(['doctor_id'], axis = 1)
    df_0 = df_nd[df_nd.inference != 'Surgery']


    month = find_month(monthValue)
    df1 = df_0[df_0['date'].dt.month == month]
    df1 = df1.groupby('specialization')
    df2 = df1['inference'].count()
    df3 = df2.reset_index()

    dept = list(df3['specialization'])
    lab_test_count = list(df3['inference'])
    d1 = {'labTestNames': dept, 'labTestCount': lab_test_count}

    return d1

def testcount():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT  u.User_name, i.Slot_Time, Doctor_ID, Specialization, Inference FROM user u INNER JOIN slot_db s ON u.User_ID = s.Doctor_ID INNER JOIN slot_inference i ON s.Slot_NO = i.Slot_NO WHERE s.Slot_Status = 'BOOKED'")
    slot_status=cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(slot_status,columns = ['username', 'date','doctor_id', 'specialization', 'inference'])
    df['date'] = pd.to_datetime(df['date'])
    df_nd = df.drop(['doctor_id'], axis = 1)
    df_0 = df_nd[df_nd.inference != 'Surgery']

    lab_test_count2 = []
    quarter = [1, 2, 3, 4]
    for i in range(len(quarter)):
      df4 = df_0[df_0['date'].dt.quarter == quarter[i]]
      df4 = df4.groupby('inference')
      df5 = df4['specialization'].count()
      df6 = df5.reset_index()
      
      lab_test_name = list(df6['inference'])
      lab_test_count2.append(list(df6['specialization']))
    d2 = {'labTestName': lab_test_name, 'Q1_labTestCount': lab_test_count2[0], 'Q2_labTestCount': lab_test_count2[1], 'Q3_labTestCount': lab_test_count2[2], 'Q4_labTestCount': lab_test_count2[3]}
    return d2

def location_count(Entity_name):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    if Entity_name == "Apollo Hospital":
        cursor.execute("select Address,Slot_Status from careplex.slot_db inner join careplex.user on slot_db.Patient_ID = user.User_ID inner join careplex.entity on slot_db.Entity_ID=entity.Entity_ID where Entity_Name = 'Apollo Hospital'")
    elif Entity_name == "Fortis Hospital":
        cursor.execute("select Address,Slot_Status from careplex.slot_db inner join careplex.user on slot_db.Patient_ID = user.User_ID inner join careplex.entity on slot_db.Entity_ID=entity.Entity_ID where Entity_Name = 'Fortis Hospital'")
    else:
        cursor.execute("select Address,Slot_Status from careplex.slot_db inner join careplex.user on slot_db.Patient_ID = user.User_ID inner join careplex.entity on slot_db.Entity_ID=entity.Entity_ID where Entity_Name = 'Manipal Hospital'")

    rv = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(rv,columns = ['Address','Count'])
    df2=df.groupby(['Address']).count()
    df3=df2.reset_index()
    # total=df3['Count'].sum()
    df4=df3.set_index('Address').T.to_dict()
   
    return df4

   
