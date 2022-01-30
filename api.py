import requests
import json
from Tokens import yahooKey


def Call(stocks = []):
    q = listFix(stocks)

    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols":"{}".format(q)}
    headers = {'x-api-key': yahooKey}

    res = requests.request("GET", url, headers=headers, params=querystring)
    print(res.json())
    return resFix(str(res.json()))

def resFix(s):
    s = s.replace("'", '"')
    s = s.replace("True", '"True"')
    s = s.replace("False", '"False"')
    s = s.replace("None", '"None"')
    s = json.loads(s)
    return s



def listFix(li = []):
    q = ""
    for i in li:
        q += "{},".format(i)
    
    return "{}".format(q[:-1])

