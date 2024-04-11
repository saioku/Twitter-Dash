import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("ProcessedTweets.csv")

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in df['Month'].unique()],
            value=df['Month'].unique()[0],
            multi=False,
            placeholder="Select a month"
        ),
        dcc.RangeSlider(
            id='sentiment-slider',
            min=-1,
            max=1,
            step=0.1,
            marks={i: str(i) for i in range(-1, 2)},
            value=[-1, 1],
            tooltip={'placement': 'bottom'}
        ),
        dcc.RangeSlider(
            id='subjectivity-slider',
            min=0,
            max=1,
            step=0.1,
            marks={i/10: str(i/10) for i in range(11)},
            value=[0, 1],
            tooltip={'placement': 'bottom'}
        )
    ]),
    dcc.Graph(id='scatter-plot'),
    html.Div(id='table-container')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = df[(df['Month'] == selected_month) &
                     (df['Sentiment'] >= sentiment_range[0]) &
                     (df['Sentiment'] <= sentiment_range[1]) &
                     (df['Subjectivity'] >= subjectivity_range[0]) &
                     (df['Subjectivity'] <= subjectivity_range[1])]
    
    fig = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', color='Sentiment', color_continuous_scale='gray', hover_data=[])
    fig.update_traces(marker=dict(size=8, opacity=0.5))
    fig.update_layout(xaxis=dict(title=None), yaxis=dict(title=None))
    return fig

@app.callback(
    Output('table-container', 'children'),
    [Input('scatter-plot', 'selectedData')]
)
def update_table(selectedData):
    if selectedData is not None:
        selected_points = selectedData['points']
        tweet_texts = [df.iloc[point['pointIndex']]['RawTweet'] for point in selected_points]
        return html.Table([
            html.Tr([html.Td(text)]) for text in tweet_texts
        ])
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)
