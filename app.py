from flask import Flask, render_template, request
from werkzeug.utils import secure_filename  #

import pandas as pd
import plotly.express as px

from covid_record import get_covid_records


import datetime as dt

app = Flask(__name__)

date= dt.datetime.now()
current_year = date.year

formatted_date = date.strftime("%B %d, %Y")

@app.route('/')
def home():
    return render_template('home.html', year=current_year)

@app.route('/analysis')
def analysis():
    options = [
        {'value': 'head', 'label':'Select a Criteria to Display'}, 
        {'value': 'deaths', 'label':'Death Trends'}, 
        {'value': 'age', 'label':'Infection by Age Range'}, 
        {'value': 'hospitalised', 'label':'Confirmed Cases VS Hospitalised Cases'}, 
        {'value':'gender', 'label':'Infection Percentage by Gender'}, 
        {'value':'icu', 'label':'Patients Requied ICU'},
    ]    
    
    
    return render_template('analysis.html', options=options,  year=current_year)


@app.route('/about')
def about():
    return render_template('about.html', year=current_year)   


@app.route('/displayvisual', methods=['GET', 'POST'])
def display_visualization():
    if request.method == 'POST':
        selected_plot = request.form.get('plot')

        if selected_plot == 'deaths':
            df = get_covid_records()
            death_df= df[['Date','DeathsToday']].copy()
            
            fig = px.line(death_df, x = 'Date', y = 'DeathsToday', 
               labels={
                     "Date": "Date of Occurence",
                     "DeathsToday": "Number of Deaths Occured Per Day",
                     "variable": "Situation"
                 }
               )
            fig.update_layout(
                showlegend=False,
                title= f"Death Trends Per Day (From March 3, 2020 - {formatted_date})"
            )
            filename = f"{selected_plot}.html"
            the_div = fig.to_html(full_html=False)
            return the_div
                        
                        
        elif selected_plot == 'age':
            df = get_covid_records()
            age_data=df.copy()
            byAge = age_data.groupby('AgeRange')['NumberInfected'].max()
            age_df=pd.DataFrame({'AgeRange':byAge.index, 'high_value':byAge.values})
            fig = px.bar(age_df, x = 'AgeRange', y = 'high_value', 
             labels={
                     "AgeRange": "Patient Age Range",
                     "high_value": "Total Covid Case",
                     "variable": "Situation"
                 },
             title=f"Total Covid Infection Case By Age Range from (March 3, 2022 - {formatted_date}).", 
             color='AgeRange')
            filename = f"{selected_plot}.html"
            the_div = fig.to_html(full_html=False)
            return the_div 
        
     
        elif selected_plot == 'hospitalised':
            df = get_covid_records()
            date_vis= df.copy()
            date_vis['YearMonth'] = pd.to_datetime(date_vis['Date']).apply(lambda x: '{year}-{month}'.format(year=x.year, month=x.month))
            date_vis['MonthYear'] = pd.to_datetime(date_vis['Date']).apply(lambda x: '{year}{month}'.format(year=x.year, month=x.month))
            date_vis['MonthYear'] = pd.to_numeric(date_vis['MonthYear'])
            date_res = date_vis.groupby('MonthYear')['YearMonth','ConfirmedCases','NumberHospitalised'].max()
            date_res_df=pd.DataFrame({'sorter':date_res.index, 'Date':date_res.YearMonth,'CasesConfirmed':date_res.ConfirmedCases, 'hospitalCase':date_res.NumberHospitalised})
            date_res_df = date_res_df.reset_index()
            date_res_df.sort_values(by=['sorter'], ascending=False)
            date_res_df.rename(columns={'CasesConfirmed':'Confirmed Covid Cases','hospitalCase':'Hospitalized Cases'}, inplace=True)
            
            fig = px.bar(date_res_df, x = 'Date', y = ['Confirmed Covid Cases','Hospitalized Cases'], 
             labels={
                     "Date": "Month Recorded",
                     "value": "Patient Count",
                     "variable": "Situation"
                 },
             title=f"Confirmed Covid Cases Compared to Hospitalised Cases from March 2, 2020 - {formatted_date}.")
            fig.update_layout(barmode='group')
            filename = f"{selected_plot}.html"
            the_div = fig.to_html(full_html=False)
            return the_div 
        
        
        elif selected_plot == 'gender':
            df = get_covid_records()
            by_gender = df[['NumberInfected','Gender','ConfirmedCases','NumberByGender']].copy()
            gender_df = by_gender.groupby(['Gender'], as_index=False)['NumberByGender'].max()
            
            fig = px.pie(gender_df, values='NumberByGender', names='Gender', 
             title=f"Percentage Total Of Infection Based On The Gender as of  {formatted_date}", color='Gender')
            filename = f"{selected_plot}.html"
            the_div = fig.to_html(full_html=False)
            return the_div 
        
        
        elif selected_plot == 'icu':
            df = get_covid_records()
            cases = df[['Date','NumberHospitalised','CasesRequiedICU']].copy()
            by_cases=cases.groupby(['Date'], as_index=False)['NumberHospitalised','CasesRequiedICU'].max()
            by_cases.rename(columns={'Date':'Date of Occurence','NumberHospitalised':'Hospitalised Patient','CasesRequiedICU':'Patient Requiring ICU'}, inplace=True)
            
            fig = px.scatter(by_cases, x='Date of Occurence', y=['Hospitalised Patient','Patient Requiring ICU'], 
                 labels={
                     "Date": "Date of Occurence",
                     "value": "Patient Count",
                     "variable": "Situation"
                 },
                 title=f"The Trends Of Patients Who Are Hospitalised As Compared To Those Also Required Intensive Care /(ICU) as of  {formatted_date}")
            filename = f"{selected_plot}.html"
            the_div = fig.to_html(full_html=False)
            return the_div 

            
        else:
            pass
   
   
   
   
   
   
   


if __name__ == '__main__':
    app.run(debug=True)
