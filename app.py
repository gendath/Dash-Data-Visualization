from dash import Dash,dcc,html
import pandas as pd
import yfinance as yf
import dash_bootstrap_components as dbc
data=pd.read_csv("avocado.csv", parse_dates=True)
data=data.query("type=='conventional' and region == 'Albany'")
data.sort_values("Date",inplace=True)

app = Dash(__name__)

app.layout = html.Div(children=[
  html.H1(children="Avocado Analytics"),
  html.P(children="Analyze the behavior of avocado prices and the number of avocados sold in the US between 2015 and 2018"),
  dcc.Graph(
    figure={
      "data":[
        {
          "x":data["Date"],
          "y":data["AveragePrice"],
          "type":"lines",
          },

      ],
      "layout":{
        "title":"Average Price of Avocados"
      },
    }
  ),
  dcc.Graph(
    figure={
      "data":[
        {
          "x":data["Date"],
          "y":data["Total Volume"],
          "type":"lines"

        }
      ],
      "layout":{
        "title":"Avocados Sold"

      }
    }
  )
])

if __name__=="__main__":
  app.run_server(debug=True)