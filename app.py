import pandas as pd
import numpy as np
import dash_core_components
import dash
import dash_core_components as dcc
import dash_html_components as html

# df = pd.read_excel(
#     "G:\My Drive\99other_project_work\covid marketing support\wkCountyFCWk_pivot.xlsx" #to-do:change this line to where you saved wkCountyFCWk_pivot.xlsx
# )

url = 'https://raw.githubusercontent.com/haley-zhao/worktask/master/app_source.csv'
df = pd.read_csv(url, error_bad_lines=False)

geo = df["county names"].unique()

app = dash.Dash()

app.layout = html.Div([
    html.H2("Congestion Changes during COVID-19"),
    html.Div(
        [
            dcc.Dropdown(
                id="County",
                options=[{
                    'label': i,
                    'value': i
                } for i in geo],
                value='Alameda'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('County', 'value')])
def update_graph(County):

    df_plot = df[df['county names'] == County]

    pv = pd.pivot_table(
        df_plot,
        index=['weeknum_Friday'], #weeknum_Friday week_number
        columns=['Road'],
        values=['congestion_pct_xy_pct','weighted_avg_tti_xy_pct'],
        aggfunc=np.mean,
        fill_value=0).reset_index()
    #congestion percentage color
    PuBuGn = plotly.colors.sequential.PuBuGn
    OrRd = plotly.colors.sequential.OrRd


    trace3 = go.Scatter(x=pv.index, y=pv[('congestion_pct_xy_pct','Freeway')], mode='lines+markers',line_color=PuBuGn[4], name='Freeway congestion_pct')
    trace4 = go.Scatter(x=pv.index, y=pv[('congestion_pct_xy_pct', 'Arterial')], mode='lines+markers',line=dict(color=PuBuGn[3],dash='dash'), name='Arterial congestion_pct')
    trace5 = go.Scatter(x=pv.index, y=pv[('weighted_avg_tti_xy_pct', 'Freeway')], mode='lines+markers',line_color=OrRd[4], name='Freeway,weighted_avg_tti_xy_pct')
    trace6 = go.Scatter(x=pv.index, y=pv[('weighted_avg_tti_xy_pct', 'Arterial')], mode='lines+markers', line=dict(color=OrRd[3],dash='dash'), name='Arterial,weighted_avg_tti_xy_pct')
    trace1 = go.Scatter(x=pv.index, y=(pv[('weighted_avg_tti_xy_pct', 'Freeway')] + pv[('congestion_pct_xy_pct','Freeway')])/2, mode='lines+markers',line=dict(color=PuBuGn[3]), name='Freeway') #https://plotly.com/python/builtin-colorscales/
    trace2 = go.Scatter(x=pv.index, y=(pv[('congestion_pct_xy_pct', 'Arterial')] + pv[('weighted_avg_tti_xy_pct', 'Arterial')])/2, mode='lines+markers',line=dict(color=OrRd[3], dash='dash'), name='Arterial')

    return {
        'data': [trace1,trace2],
        # 'data': [trace3, trace4, trace5, trace6],
        'layout':
        dict(
            title='Congestion Percentage & Travel Time Index Changes, {}'.format(County),
            showlegend = True,
            # margin={'l': 0, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 0},
            xaxis={'title': 'Week Number (since 3/1/2020)'},  #,'tickformat': '%Y-%m-%d','tickangle': '45','tickmode':'array',
            yaxis={'title': 'Avg Changes','range':[0,1.2]},
            plot_bgcolor=plotly.colors.sequential.Blues[1]

            )

    }

# plotly.offline.plot(app, filename=r"G:\My Drive\99other_project_work\covid marketing support\test.html")
if __name__ == '__main__':
    app.run_server()
