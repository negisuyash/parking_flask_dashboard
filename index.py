
from flask import Flask,render_template,request,send_file
import pandas as pd



app=Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')



@app.route('/',methods=['POST','GET'])
def index_post():

    searched_query=request.form['keyword']
    df=pd.read_csv("./datasets/parking_points.csv")
    df['name']=df['name'].str.lower()
    df['sector']=df['sector'].str.lower()
    temp_df=df[df['name'].str.contains(searched_query)].append(df[df['sector'].str.contains(searched_query)]).append(df[df['loc'].str.contains(searched_query)])

    result=[]
    for loc,sector,name,sr in zip(temp_df['loc'],temp_df['sector'],temp_df['name'],temp_df['sr']):
        result.append({'sr':str(sr),'loc':loc,'name':name,'sector':sector})
    return render_template('welcome.html',result=result)

@app.route('/delete/<sr_key>')
def delete(sr_key):

    df=pd.read_csv("./datasets/parking_points.csv")
    delete_df=df[df['sr']==int(sr_key)]
    df=df[df['sr']!=int(sr_key)]
    df.to_csv('./datasets/parking_points.csv')
    recovery_system(delete_df)
    return '<alert>SELECTED RECORD DELETED SUCCESSFULLY</alert><br><br><a href="/">go back</a>'

@app.route('/add_parking')
def add():
    return render_template('add_parking.html')


@app.route('/add_parking',methods=['POST','GET'])
def add_parking():

    sector=request.form['sector']
    name=request.form['name']
    loc='['+str(request.form['x'])+','+str(request.form['y'])+']'

    df=pd.read_csv('./datasets/parking_points.csv')
    df=df.append(pd.DataFrame([[sector,name,loc,len(df)]],columns=['sector','name','loc','sr']))
    df.to_csv('./datasets/parking_points.csv')
    return '<alert>RECORD ADDED SUCCESSFULLY</alert><br><br><a href="/add_parking">go back</a>'




def recovery_system(df):
    recover_df=pd.read_csv('./datasets/recovery.csv')
    recover_df=recover_df.append(df)
    recover_df.to_csv('./datasets/recovery.csv')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7000)



