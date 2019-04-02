from flask import Flask, request, json, jsonify
from flask import render_template
from dateutil import parser
import pandas as pd
import mysql.connector
import webfunctions as wb
app = Flask(__name__)
 
# app = Flask(__name__)
config = {
  'host':'mytestservermanipal.mysql.database.azure.com',
  'user':'myadmin@mytestservermanipal',
  'password':'Qwerty123',
  'database':'careplex',
  'ssl_ca':'ssl/BaltimoreCyberTrustRoot.crt.pem'
}
conn = mysql.connector.connect(**config)

@app.route('/', methods = ["POST", "GET"])
def graph():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("select count(careplex.slot_db.Slot_Status), careplex.user.Specialization from careplex.slot_db left join careplex.user on careplex.slot_db.Doctor_ID = careplex.user.User_ID where careplex.slot_db.Slot_Status = 'BOOKED' group by careplex.slot_db.Doctor_ID")
    rv = cursor.fetchall()
    # print(rv)
    patients = []
    specializations = []

    for i in rv:
        patients.append(i[0])
        specializations.append(i[1])
    
    patientsCount = {"Patients" : patients, "Specialize" : specializations }
    pie = {"val":[{'name': 'January', 'y': 16}, {'name': 'February', 'y': 17}, {'name': 'March', 'y': 7}, {'name': 'April', 'y': 20}, {'name': 'May', 'y': 17}, {'name': 'June', 'y': 12}, {'name': 'July', 'y': 13}, {'name': 'August', 'y': 20}, {'name': 'September', 'y': 11}, {'name': 'October', 'y': 17}]}

####################
    # cursor1 = conn.cursor()
    # cursor1.execute("SELECT  u.User_name, i.Slot_Time, Doctor_ID, Specialization, Inference FROM user u INNER JOIN slot_db s ON u.User_ID = s.Doctor_ID INNER JOIN slot_inference i ON s.Slot_NO = i.Slot_NO WHERE s.Slot_Status = 'BOOKED'")
    # slot_status=cursor1.fetchall()
    # df = pd.DataFrame(slot_status,columns = ['username', 'date','doctor_id', 'specialization', 'inference'])
    # df['date'] = pd.to_datetime(df['date'])
    # df_nd = df.drop(['doctor_id'], axis = 1)
    # df_0 = df_nd[df_nd.inference != 'Surgery']
    # # df_0
    # def surgery_count():
    #     df_surgery = df[df.inference == 'Surgery']
    #     df_surgery = df_surgery.groupby(df_surgery['date'].dt.month)
    #     total_surgery = df_surgery.count()
    #     month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    #     surgery_count = list(total_surgery['inference'])
    #     dict_surgery = {'Months': month_list, 'count': surgery_count}
    # # print(dict_surgery)



###################
    return render_template("index.html",j = patientsCount, s = pie)


@app.route('/doctor')
def doctor():
    quar = wb.testcount()
    return render_template("doctor-page.html", q = quar)

@app.route('/revenue')
def revenue():
    h1, h2, h3 = wb.findavg()
    return render_template("revenue-page.html", hospital1 = h1, hospital2 = h2, hospital3 = h3)

@app.route('/specializationVariance', methods=['POST'])
def specializationVariance():
    specValue =  request.form['specialization']
    # print(specValue)
    specialization = specValue
    total_vs_booked=wb.specialization_total_vs_booked(specialization)
    # r = {"va": [12,34,56,7,8,12,34,54,67,11,34,12]}
    return json.jsonify(total_vs_booked)



@app.route('/doctorLabRefer', methods = ['POST'])
def doctorLabRefer():
    month = request.form['monthName']
    doctorLabValues = wb.doctorLabRefer(month)

    return json.jsonify(doctorLabValues)

@app.route('/deptLabPerformed', methods = ['POST'])
def deptLabPerformed():
    month = request.form['monthName1']
    doctorLabValues = wb.depLabPerformed(month)

    return json.jsonify(doctorLabValues)

@app.route('/mapHeat', methods = ['POST'])
def mapHeat():
    hospitalName = request.form['map']
    location=wb.location_count(hospitalName)

    return json.jsonify(location)



if __name__ == "__main__":
    app.run(debug=True)