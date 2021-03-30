from flask import Flask,request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    if name:
        output =  data_parse(name)
        
    else:
        output = ""
    return (
        """<form action="" method="get">
                Company Ticker Name: <input type="text" name="name">
                <input type="submit" value="Submit">
            </form>"""
        
        + output
    )


def data_parse(stack_ticker_name):

    URL = "https://in.finance.yahoo.com/quote/"+stack_ticker_name+"/financials?p="+stack_ticker_name
    r=requests.get(URL)
    soup=BeautifulSoup(r.text, 'html.parser')
    features=soup.find_all('div', class_='D(tbr)')
    headers=[]
    temp_list=[]
    final=[]
    index=0
    companyName=""
    features1=soup.find_all('div', class_='D(ib)')
    
    for item in features1[9].find_all('h1', class_='D(ib)'):
        companyName=item.text
    
    finalStr="<h1>"+companyName+"</h1><br><table border='1px'>"
 
    for item in features[0].find_all('div', class_='D(ib)'):
        headers.append(item.text)

    while index <= len(features)-1:  #filter for each line of the statement
        temp = features[index].find_all('div', class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list = []
        index+=1
    df = pd.DataFrame(final[1:])
    df.columns = headers
    finalStr+=listHeaderToString(headers)
    for list in df.values.tolist():
        finalStr+=listToString(list)

    finalStr+="</table>"
    return finalStr

def listToString(s):
    str="<tr>"
    for a in s:
        str+="<td>"+a+"</td>"
    str+="</tr>"
    return str

def listHeaderToString(s): 
    str="<tr>"
    for a in s:
        str+="<th>"+a+"</th>"
    str+="</tr>"
    return str

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
