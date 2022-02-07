from dash import Dash,dcc,html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

data=pd.read_csv("avocado.csv", parse_dates=True)
data.sort_values("Date",inplace=True)

external_stylesheets = [
  {
    "href":"https://fonts.googleapis.com/css2?"
    "family = Lato:wght@400;700&display=swap",
    "rel": "styesheet"
  },
  {
    "href":"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    "rel":"stylesheet"
  }
]

external_scripts=[
  {
    "src":"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
  }
]
app = Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=external_scripts)
app.title="Avocado Analytics: Analysing Avocado Prices from 2015 - 2018"
server =app.server
@app.callback(
  [
    Output("price-chart","figure"),
    Output("volume-chart","figure")
    ],
    [
      Input("region-filter","value"),
      Input("type-filter","value"),
      Input("date-range","start_date"),
      Input("date-range","end_date"),
      ]
      )
def update_graphs(region,avocadoType,start_date,end_date):
  mask=((data.region == region) & (data.type==avocadoType)&(data.Date>start_date) & (data.Date < end_date))
  filtered_data = data.loc[mask,:]

  price_chart_figure = {
    "data":[{
      "x":filtered_data["Date"],
      "y":filtered_data["AveragePrice"],
      "type":"lines",
      "hovertemplate":"$%{y:.2f}<extra></extra>"
    },
    ],
    "layout":{
      "title":{
        "text":"Average Price of Avocados",
        "x":.05,
        "xanchor":"left",
        },
        "xaxis":{"fixedrange":True},
        "yaxis":{
          "tickprefix":"$",
          "fixedrange":True},
          "colorway":["#17b897"],

    },
  }

  volume_chart_figure = {
    "data":[{
      "x":filtered_data["Date"],
      "y":filtered_data["Total Volume"],
      "type":"lines",
    },
    ],
    "layout":{
      "title":{
        "text":"Avocados Sold",
        "x":.05,
        "xanchor":"left",
        },
        "xaxis":{"fixedrange":True},
        "yaxis":{"fixedrange":True},
        "colorway":["red"],

    },}

  return price_chart_figure,volume_chart_figure


avePriceGraph = dcc.Graph(
            id="price-chart",
            config={"displayModeBar":False},
          ),

soldGraph = dcc.Graph(
            id="volume-chart",
            config={"displayModeBar":False},
          ),

regionDropdown=html.Div(children=[
      html.Div(
        children="Region",className="menu-title"
      ),
      dcc.Dropdown(
        id="region-filter",
        options=[
          {"label":region,"value":region}
          for region in np.sort(data.region.unique())
        ],
        value="Albany",
        clearable=False,
        className="dropdown"
      )
    ],)

avocadoTypeDropdown=html.Div(children=[
      html.Div(
        children="Avocado Type",className="menu-title"
      ),
      dcc.Dropdown(
        id="type-filter",
        options=[
          {"label":avocado_type,"value":avocado_type}
          for avocado_type in data.type.unique()
        ],
        value="organic",
        clearable=False,
        searchable=False,
        className="dropdown"
      )
    ],)

datePicker =html.Div(children=[
      html.Div(
        children="Date Range",className="menu-title"
      ),
      dcc.DatePickerRange(
        id="date-range",
        min_date_allowed = pd.to_datetime(data.Date.min()),
        max_date_allowed = pd.to_datetime(data.Date.max()),
        start_date = pd.to_datetime(data.Date.min()),
        end_date = pd.to_datetime(data.Date.max()),
      ),
    ],
    )


controls = html.Div(className="container",children=[
  html.Div(className="row menu",children=[
    html.Div(className="col",children=[
      regionDropdown,

    ]),
    html.Div(className="col",children=[
      avocadoTypeDropdown,

    ]),
    html.Div(className="col",children=[
      datePicker,

    ]),
  ])
])
app.layout = html.Div(children=[
    html.Div(children=[
    html.H1(children="Avocado Analytics", className="header-title"),
    html.P(children="Analyze the behavior of avocado prices and the number of avocados sold in the US between 2015 and 2018", className="header-description")],
    className="header"),
    controls,
    html.Div(
      children=[
        html.Div(
          children=
          avePriceGraph,
          className="card"
        ),
      ],
      className="wrapper row"
    ),
        html.Div(
      children=[
        html.Div(
          children=
          soldGraph,
          className="card"
        ),
      ],
      className="wrapper row"
    )
])

if __name__=="__main__":
  app.run_server(debug=True)