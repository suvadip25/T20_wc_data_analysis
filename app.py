import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from flask import Flask,request,jsonify,Response
import io
import plotly.graph_objects as go
import plotly.io as pio
import os
pio.templates.default = "plotly_white"


import csv
from os import path, getcwd, environ
import psycopg2
from psycopg2.extras import execute_values


projects =[]
csv_filename = 't20-world-cup-22.csv'
with open(csv_filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        projects.append(row)

#print(projects)
conn = psycopg2.connect(
    database="T20_worldcup", user='postgres',
    password='Arpan@2002', port='5432'
)
cursor = conn.cursor()
columns = projects[0].keys()
query = "INSERT INTO T20_worldcup ({}) VALUES %s".format(','.join(columns))

# # convert projects values to list of lists
values = [[value for value in project.values()] for project in projects]

execute_values(cursor, query, values)
conn.commit()

# Create a cursor object to execute queries


# Execute a SELECT statement to retrieve data from a table
cursor.execute("SELECT * FROM T20_worldcup")
# Get the column names of the table
column_names = [desc[0] for desc in cursor.description]

# Store the column names in a list
columns = column_names

# Fetch the result of the SELECT statement
datas = cursor.fetchall()

# Loop through the rows and print each column(list)
for data in datas:
    j=data

# example list

# convert list to dataframe
df = pd.DataFrame(datas, columns=columns)
# print(df)
def create_app():
    app=Flask(__name__)
    with app.app_context():
        @app.route('/won_after_winning_toss',methods=['GET'])
        def won_after_winning_toss():
        

            df["Match Won By 1st Batting or 2nd"]=''

            d1=pd.DataFrame()
            d1['Whether Team Won by winning Toss']=np.where((df['toss_winner'] == df['winner']),'Yes','No')
            # print(d1)

            col='Whether Team Won by winning Toss'
            count=d1.groupby(col).size()
            #print(type(count))
            d2=pd.DataFrame(count)
            plot=d2.plot.pie(y=0, figsize=(10,10),autopct='%1.1f%%')
            plt.title("Pie Chart to show whether team won by winning toss or not")
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            return Response(buf.getvalue(), mimetype='image/png')
        @app.route('/most_player_of_the_match',methods=['GET'])
        def most_player_of_the_match():
            # dt=df.dropna()
            plt.figure(figsize=(12, 10))
            sns.countplot(y='player_of_match',data=df)
            buf=io.BytesIO()
            plt.savefig(buf,format='png')
            buf.seek(0)
            return Response(buf.getvalue(),mimetype='image/png')
        @app.route('/won_1st_or_2nd_battings',methods=['GET'])
        def win_1st_or_2nd_battings():
            Data=df.dropna()

            d1=pd.DataFrame()
            d1['Whether Team Won by 1st Batting or 2nd']=np.where((Data['won_by'] == 'Runs'),'1st Batting','2nd Batting')


            col='Whether Team Won by 1st Batting or 2nd'
            count=d1.groupby(col).size()
            d2=pd.DataFrame(count)

            plot=d2.plot.pie(y=0, figsize=(10,10),autopct='%1.1f%%')
            plt.title("Pie Chart to show whether team won by 1st Batting or 2nd Batting")
            buf=io.BytesIO()
            plt.savefig(buf,format='png')
            buf.seek(0)
            return Response(buf.getvalue(),mimetype='image/png')
            # plt.show()
            # plt.savefig("D:\T20 World Cup\Plots/Fig.png")
        @app.route('/top_scorer', methods=['GET'])
        def top_scorer():
            plt.figure(figsize=(14, 14))
            # dt=df.dropna()
            sns.barplot(x='top_scorer',y='highest_score',data=df)
            plt.xticks(rotation = 'vertical')
            buf=io.BytesIO()
            plt.savefig(buf,format='png')
            buf.seek(0)
            return Response(buf.getvalue(),mimetype='image/png')
        @app.route('/total_score_in_each_venue',methods=['GET'])
        def total_score_in_each_venue():
            Data=df.dropna()
            
            plt.bar(Data["venue"], Data["first_inn_score"] + Data["second_inn_score"])
            plt.xlabel("Venue")
            plt.ylabel("Total Score")
            plt.title("Total Score in each Venue")
            plt.xticks(rotation=30)
            buf=io.BytesIO()    
            plt.savefig(buf,format="png")
            buf.seek(0)
            return Response(buf.getvalue(),mimetype='image/png')
        @app.route("/venue",methods=['GET'])
        def venue():
            sns.countplot(y='venue',data=df)
            buf=io.BytesIO()
            plt.savefig(buf,format='png')
            buf.seek(0)
            return Response(buf.getvalue(),mimetype='image/png')
    return app

#sns.barplot(x='top_scorer',y='highest_score',data=df)
# plt.xticks(rotation = 'vertical')
# plt.show()
# sns.countplot(y='venue',data=df)
# plt.show()
# Close the cursor and connection
cursor.close()
conn.close()
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)