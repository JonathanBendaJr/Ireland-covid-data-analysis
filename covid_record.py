#URL = "https://opendatageohive.hub.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
import pandas as pd


def get_covid_records():
    df = pd.read_csv("covid_data.csv")
    df = df.drop(['X', 'Y','Date', 'CovidCasesConfirmed','TotalConfirmedCovidCases', 'DeathsCumulative_DOD','CommunityTransmission', 'CloseContact',
       'SevenDayAvg_Cases','ConfirmedCovidDeaths', 'TotalCovidDeaths','ClustersNotified','TravelAbroad', 'FID', 'Median_Age',], axis=1)
    
    new_data = df.copy()
    
    new_data['StatisticsProfileDate'] = pd.to_datetime(new_data['StatisticsProfileDate']).dt.date
    new_data['StatisticsProfileDate'] = pd.to_datetime(new_data['StatisticsProfileDate'])
    
    melt_gender = pd.melt(new_data, 
                           ['StatisticsProfileDate', 'ConfirmedCovidCases',
       'HospitalisedCovidCases', 'RequiringICUCovidCases',
       'HealthcareWorkersCovidCases', 'HospitalisedAged5',
       'HospitalisedAged5to14', 'HospitalisedAged15to24',
       'HospitalisedAged25to34', 'HospitalisedAged35to44',
       'HospitalisedAged45to54', 'HospitalisedAged55to64','Aged1to4', 'Aged5to14', 'Aged15to24', 'Aged25to34',
       'Aged35to44', 'Aged45to54', 'Aged55to64', 'HospitalisedAged65to74',
       'HospitalisedAged75to84', 'HospitalisedAged85up', 'Aged65to74',
       'Aged75to84', 'Aged85up', 'DeathsToday_DOD'],
                           var_name="gender",
                           value_name="no_infected_gender")
    melt_gender = melt_gender.sort_values(ascending=True,by=["StatisticsProfileDate"])
    
    melt_hospitalised = pd.melt(melt_gender, 
                           ['StatisticsProfileDate', 'ConfirmedCovidCases',
       'HospitalisedCovidCases', 'RequiringICUCovidCases',
       'HealthcareWorkersCovidCases','Aged1to4',
       'Aged5to14', 'Aged15to24', 'Aged25to34', 'Aged35to44', 'Aged45to54',
       'Aged55to64', 'Aged65to74', 'Aged75to84', 'Aged85up',
       'DeathsToday_DOD', 'gender', 'no_infected_gender'],
                           var_name="Hospitalised",
                           value_name="no_hospitalised")
    melt_hospitalised = melt_hospitalised.sort_values(ascending=True,by=["StatisticsProfileDate"])
    
    melt_infected = pd.melt(melt_hospitalised, 
                           ['StatisticsProfileDate', 'ConfirmedCovidCases',
       'HospitalisedCovidCases', 'RequiringICUCovidCases',
       'HealthcareWorkersCovidCases', 'DeathsToday_DOD', 'gender',
       'no_infected_gender', 'Hospitalised', 'no_hospitalised'],
                           var_name="Infected",
                           value_name="no_infected")
    melt_infected = melt_infected.sort_values(ascending=True,by=["StatisticsProfileDate"])
    
    melted_data = melt_infected.copy()
    
    melted_data = melted_data.drop(['Hospitalised'], axis=1)
    melted_data.rename(columns={'StatisticsProfileDate':'Date','ConfirmedCovidCases':'ConfirmedCases','HospitalisedCovidCases':'HospitalisedCases',
                            'RequiringICUCovidCases':'CasesRequiedICU','HealthcareWorkersCovidCases':'HealthWorkerCases','DeathsToday_DOD':'DeathsToday', 
                            'gender':'Gender','no_infected_gender':'NumberByGender','no_hospitalised':'NumberHospitalised',
                            'Infected':'AgeRange','no_infected':'NumberInfected'}, inplace=True)
    melted_data = melted_data.dropna()
    
    melted_data["AgeRange"] = melted_data["AgeRange"].str.replace('to', ' - ')
    melted_data["AgeRange"] = melted_data["AgeRange"].str.replace('Aged', 'Age ')
    melted_data["AgeRange"] = melted_data["AgeRange"].str.replace('up', ' +')

    melted_data['ConfirmedCases'] = pd.to_numeric(melted_data['ConfirmedCases'])
    melted_data['HospitalisedCases'] = pd.to_numeric(melted_data['HospitalisedCases'])
    melted_data['CasesRequiedICU'] = pd.to_numeric(melted_data['CasesRequiedICU'])
    melted_data['HealthWorkerCases'] = pd.to_numeric(melted_data['HealthWorkerCases'])
    melted_data['DeathsToday'] = pd.to_numeric(melted_data['DeathsToday'])
    melted_data['NumberByGender'] = pd.to_numeric(melted_data['NumberByGender'])
    melted_data['NumberHospitalised'] = pd.to_numeric(melted_data['NumberHospitalised'])
    melted_data['NumberInfected'] = pd.to_numeric(melted_data['NumberInfected'])
    
    melted_data = melted_data[['Date', 'ConfirmedCases', 'HospitalisedCases', 'CasesRequiedICU', 'HealthWorkerCases',
                           'DeathsToday','NumberInfected', 'AgeRange', 'Gender', 'NumberHospitalised', 'NumberByGender']]

    melted_data=melted_data.reset_index(drop=True)

    melted_data = melted_data.sort_values(ascending=True,by=["Date"])
    
    tidy_data = melted_data.copy()
    
    
    return tidy_data