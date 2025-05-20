import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("train.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

# Initialize app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            options=[{'label': r, 'value': r} for r in df['Region'].unique()],
            value=df['Region'].unique().tolist(),
            multi=True,
            id='region-filter'
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='sales-over-time'),
    dcc.Graph(id='top-products'),
    dcc.Graph(id='category-sales')
])

# Callback for interactivity
@app.callback(
    [Output('sales-over-time', 'figure'),
     Output('top-products', 'figure'),
     Output('category-sales', 'figure')],
    [Input('region-filter', 'value')]
)
def update_dashboard(selected_regions):
    filtered = df[df['Region'].isin(selected_regions)]

    fig_time = px.line(
        filtered.groupby('Month')['Sales'].sum().reset_index(),
        x='Month', y='Sales', title='Monthly Sales Trend'
    )

    top_products = filtered.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    fig_top = px.bar(top_products, x='Sales', y='Product Name', orientation='h', title='Top 10 Products')

    cat_sales = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig_cat = px.pie(cat_sales, names='Category', values='Sales', title='Sales by Category')

    return fig_time, fig_top, fig_cat

# Run the app
app.run(debug=True)
