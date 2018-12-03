from datetime import datetime
from array import array

import warnings
warnings.simplefilter('ignore')


import plotly
import plotly.graph_objs as go


init_notebook_mode(connected=True)

import matplotlib.pyplot as plt
import matplotlib as mpl 

from pylab import rcParams
rcParams['figure.figsize'] = 8, 5
import pandas as pd


import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html



import re



def get_url(url):
    """
    Get page from url and decodes it via .decode('utf8').
    """
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content




def get_provinces_data(what, when, TYPE=["VHI_Parea", "Mean"]):

    # https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=11&year1=1981&year2=2018&type=Mean

    files = []

    for count in range(0, 2):

        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1={}&year2={}&type={}".format(what, when[0], when[1], TYPE[count])

        resp = get_url(url)

        filename = str(what) + "_" + TYPE[count] + "_" + str(when[0]) + "-" + str(when[1]) + "(" + datetime.strftime(datetime.now(), "%Y.%m.%d_%H-%M-%S") + ")" + '.txt'
        open(filename, 'wb').write(resp)
        print(filename, " created.")
        files.append(filename)


    return files







def choose_province():

    when = []
    for i in range(2):
       when.append('f')
    what = input("Choice province: ")
    when[0] = input("Choice year: ")
    when[1] = input("Choice year: ") 
    return(get_provinces_data(what, when))


def mean_file(file):
        raw = open(file,'r+')
        headers = raw.readline().rstrip()
        headers = headers.split(',')[:2] + headers.split(',')[4:]
        data = raw.readlines()

        result = []

        # deleting stuff to get it in df
        for every in data:
            result.append(str(re.sub(r',\s\s|\s\s|\s|,\s',',',every)[:-1]).split(','))


        df = pd.DataFrame(result,columns=headers)   

        return df

def vhi_file(file):
    raw = open(file,'r+')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()

    result = []

    # deleting stuff to get it in df
    for every in data:
        result.append(str(re.sub(r'\s\s\s|,\s\s|\s\s|,\s|\s',',',every)[:-1]).split(','))

    df = pd.DataFrame(result,columns=headers)

    return df


def get_data_from_txt_to_df(filenames):
    for file in filenames: 
        if "Mean" in file:
            mean_file(file)
        if "VHI" in file:
            vhi_file(file)


def get_file_to_normal_stage(filenames):
    for file in filenames:
        data = open(file,'r').read()
        data = data[data.find('<pre>')+5:data.find("</pre></tt>")]

        write_to = open(file,'w').write(data)



def main():
    filenames = choose_province()
    get_file_to_normal_stage(filenames)
    get_data_from_txt_to_df(filenames)

#main()

if __name__ == "__main__":
        

    
    df = mean_file("1_Mean_2017-2018(2018.12.02_14-21-04).txt")      
    df1 = vhi_file("1_VHI_Parea_2017-2018(2018.12.02_14-21-03).txt")
    df = df.rename(columns={' SMN': 'SMN'})
    df.rename(columns={' SMN': 'SMN'}, inplace=True)

    print(df.head(20))

    print(df.VHI.min())
    print(df.VHI.max())

    print(df1.head(20))

    print(df.info())
    df['year'] = df.year.astype('int64')
    df['week'] = df.week.astype('int64')
    df['SMN'] = df.SMN.astype('float64')
    df['SMT'] = df.SMT.astype('float64')
    df['VCI'] = df.VCI.astype('float64')
    df['TCI'] = df.TCI.astype('float64')
    df['VHI'] = df.VHI.astype('float64')
    print(df.info())
    

    
   

    dfx = ['SMN','SMT','VCI']
    dfy = ['year','week']
    sales_df = df[dfx + dfy]
    sales_df.groupby(dfy).sum().plot()
    plt.savefig('to1.png')

    vis_df = df
    
    
    trace0 = go.Scatter(
        x=vis_df.index + 1,
        y=vis_df.SMN,
        name='SMN'
    )

    
    trace1 = go.Scatter(
        x=vis_df.index + 1,
        y=vis_df.SMT,
        name='SMT'
    )

    trace2 = go.Scatter(
        x=vis_df.index + 1,
        y=vis_df.VCI,
        name='VCI'
    )

    trace3 = go.Scatter(
        x=vis_df.index + 1,
        y=vis_df.TCI,
        name='TCI'
    )

    trace4 = go.Scatter(
        x=vis_df.index + 1,
        y=vis_df.VHI,
        name='VHI'
    )

 

    
    
    data = [trace0, trace1, trace2, trace3, trace4]
    layout = {'title': 'Statistics '}

    
    fig = go.Figure(data=data, layout=layout)
    iplot(fig, show_link=False)
    plotly.offline.plot(fig, filename='years_stats.html', show_link=False)
    
    plt.show()

    


    
