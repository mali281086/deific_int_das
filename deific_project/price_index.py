from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Master Data.csv")
df_sbp = pd.read_excel("sbp_pkr_exchange.xls")

df.Date = pd.to_datetime(df.Date)
# df_sbp.Date = pd.to_datetime(df_sbp.Date)

app = Dash()

city_dropdown = dcc.Dropdown(options=df['City'].unique(),
                             value=['Average','Karachi'],
                             multi=True,
                             id='city_dropdown_id')

product_dropdown = dcc.Dropdown(options=df['Description'].unique(),
                                value=['Wheat','Wheat Flour Bag'],
                                multi=True,
                                id='product_dropdown_id')

year_slider = dcc.RangeSlider(df['Year'].min(),
                              df['Year'].max(),
                              step=None,
                              value=[df['Year'].min(),
                                     df['Year'].max()],
                              tooltip={"placement": "bottom", "always_visible": True},
                              id='year_slider_id',
                              marks={str(year): str(year) for year in df['Year'].unique()})

app.layout = html.Div(children=[
    html.H1(children='Commodity Price Index'),
    city_dropdown,
    product_dropdown,
    dcc.Graph(id='commodity_price_index',
              config={'displayModeBar': False #This config command is to hide the plotly toolbar.
                     }
             ),
    year_slider,
    dcc.Graph(id='currency_index',
            config={'displayModeBar': False #This config command is to hide the plotly toolbar.
                    }
            ),
])

@app.callback(
    Output(component_id='commodity_price_index',component_property='figure'),
    Output(component_id='currency_index',component_property='figure'),
    Input(component_id='city_dropdown_id',component_property='value'),
    Input(component_id='product_dropdown_id',component_property='value'),
    Input(component_id='year_slider_id',component_property='value')
)

def update_graph(city_param,product_param,year_param):
    dff = df[(df['Year'].between(min(year_param),max(year_param))) & (df['City'].isin(city_param)) & (df['Description'].isin(product_param))]
    commodity_fig = px.line(dff,
                       x='Date',
                       y='Price',
                       color='City',
                       line_dash='Description',
                       title=f'Government Issued Price Index for {product_param} in {city_param}')
    
    commodity_fig.update_xaxes(title='Year')
    
    commodity_fig.update_yaxes(title='Price')
    
    dff2 = df_sbp[(df_sbp['Year'].between(min(year_param),max(year_param)))]
    currency_fig = px.line(dff2,
                       x='Date',
                       y='PKR',
                       color='Currency')
    
    currency_fig.update_xaxes(title='Year')
    
    currency_fig.update_yaxes(title='PKR')
    
    return commodity_fig, currency_fig
# Following lines can be added if we want to create a input page separately and view the chart.
#     line_fig.show(config=dict(displayModeBar=False)
#     )
  
if __name__ == '__main__':
    app.run_server(debug=True)