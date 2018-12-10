import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd 
import pandas_datareader.data as web
import datetime

app = dash.Dash()
"""
Import the Excel with the portfolio and assing to data frame"""
df_xl_file = pd.read_excel("shares.xlsx")

app.layout = html.Div(children=[
    html.Div(children="Dynamic Stocks"),
    dash_table.DataTable(
        id='table',
    columns=[{"name": i, "id": i} for i in df_xl_file.columns],
    data=df_xl_file.to_dict("rows"),
    ),
    dcc.RadioItems(
        id='input',
        options=[
            {'label': 'AAPL', 'value': 'AAPL'},
            {'label': 'JNJ', 'value': 'JNJ'},
            {'label': 'MCD', 'value': 'MCD'},
            {'label': 'MTCH', 'value': 'MTCH'},
            {'label': 'NFLX', 'value': 'NFLX'},
            {'label': 'WMT', 'value': 'WMT'},
            {'label': 'FB', 'value': 'FB'},
            {'label': 'TWTR', 'value': 'TWTR'}
        ],
        value = "AAPL"
    ),
    html.Div(id = "output_graph")
])
@app.callback(
    Output(component_id = "output_graph", component_property = "children"),
    [Input(component_id = "input", component_property = "value")]
)
def update(input_data):
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2018,9,3)
    df = web.DataReader(input_data, "yahoo", start, end)
    return dcc.Graph(id=f"{input_data} Stock",
        figure={
            "data":[
                {"x":df.index, "y":df.Close, "type":"line", "name": input_data},
                ],
            "layout":{
                "title":f"Historical shares of {input_data}"
            }

        })

if __name__ == "__main__":
    app.run_server(debug = True, port = 8080)   