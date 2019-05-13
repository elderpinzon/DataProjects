import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import StockUtils

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# tickers = open("tickers.txt","r")
# ticks = tickers.readlines()
# print(ticks)

app = dash.Dash(__name__)#, external_stylesheets = external_stylesheets)

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

colors = {
    # 'background': '#111111',
    # 'text': '#7FDBFF'
    'background': '#ffffff',
    'text': '#111111'

}


app.layout = html.Div(style={'backgroundColor':colors['background']},children=[

    html.H1(children='Simple Stock Analyzer',
            style={'textAlign': 'center',
                   'color': colors['text']
            }
    ),
    
    #html.Div(children='Choose your stock.'),
    
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label':'TSLA','value':'TSLA'},
            {'label':'AAPL','value':'AAPL'},
            {'label':'MSFT','value':'MSFT'},
            {'label':'COKE','value':'COKE'}
        ],
        value='AAPL'
        #placeholder='Select a stock'
    ),

    dcc.Graph(id='my-graph'),  

    html.Div(id='my-div',
             style={'textAlign': 'center',
                    'color': colors['text']
             }),
    
    html.H2('Add a new stock'),
    
    dcc.Input(
        placeholder='Enter stock ticker...',
        type='text',
        value=''
    ),
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x':[1999,2000,2001], 'y':[4,1,2], 'type':'bar', 'name': 'Vancouver'},
    #             {'x':[1999,2000,2001], 'y':[2,4,5], 'type':'bar', 'name': 'Toronto'},
    #             {'x':[1999,2000,2001], 'y':[8,3,4], 'type':'bar', 'name': 'Bogota'}
    #         ],
    #         'layout': {'title':'Deaths by Year'}
    #     }
    # )
])

@app.callback(Output(component_id='my-div', component_property='children'),
              [Input('my-dropdown','value')])

def update_output_div(this_stock):

    df = StockUtils.get_yahoo_single_stock(this_stock)
    min_price, min_date = StockUtils.GetMinimumPriceAndDate(df)

    df_twelve_months = StockUtils.GetLastTwelveMonths(df)
    min_price_12, min_date_12 = StockUtils.GetMinimumPriceAndDate(df_twelve_months)

    df_before_min, df_after_min = StockUtils.GetBeforeAfterMin(df)
    
    trend_overall, fit_overall = StockUtils.FitTrendLine(df)
    trend_before_min, fit_before_min =  StockUtils.FitTrendLine(df_before_min)
    trend_after_min, fit_after_min =  StockUtils.FitTrendLine(df_after_min)
    
    relative_trend_before_min = fit_before_min[0] / fit_overall[0]
    relative_trend_after_min = fit_after_min[0] / fit_overall[0]

    
    return html.Div([
        html.P("Overall minimum: $%.2f on %s" % (min_price, min_date.strftime("%Y-%m-%d"))),
        html.P("Last 12 months minimum: $%.2f on %s" % (min_price_12, min_date_12.strftime("%Y-%m-%d"))),
        html.P("Relative trend before min: %.2f" % relative_trend_before_min),
        html.P("Relative trend after min: %.2f" % relative_trend_after_min),
    ])

@app.callback(Output('my-graph','figure'),
              [Input('my-dropdown','value')])

def update_graph(this_stock):

    #dff = df[df['Stock'] == this_stock]
    df = StockUtils.get_yahoo_single_stock(this_stock)

    df_before_min, df_after_min = StockUtils.GetBeforeAfterMin(df)
    
    trend_overall, fit_overall = StockUtils.FitTrendLine(df)
    trend_before_min, fit_before_min =  StockUtils.FitTrendLine(df_before_min)
    trend_after_min, fit_after_min =  StockUtils.FitTrendLine(df_after_min)
    
    relative_trend_before_min = fit_before_min[0] / fit_overall[0]
    relative_trend_after_min = fit_after_min[0] / fit_overall[0]
    
    return {
        'data':[
            {'x':df.Date, 'y':df.Close,
             'line': {'width':3,'shape':'spline'}, 'name':'Stock Price'},
            {'x':df.Date, 'y':trend_overall,
             'line':{'width':1}, 'name':'Overall trend'},
            {'x':df_before_min.Date, 'y':trend_before_min,
             'line':{'width':1}, 'name':'Before min trend: %.3f' % relative_trend_before_min},
            {'x':df_after_min.Date, 'y':trend_after_min,
             'line':{'width':1}, 'name':'After min trend: %.3f' % relative_trend_after_min}
        ],
        'layout': {'title':this_stock,
                   'yaxis': {'title':'Closing price ($)'},
                   'plot_bgcolor': colors['background'],
                   'paper_bgcolor': colors['background'],
                   'font': {'color': colors['text']}
        }
    }

if __name__ == '__main__':

    app.run_server(debug=True)
