import pandas as pd
import plotly.graph_objects as go
import numpy as np

df = pd.read_json('data.json')
df['Scores'] = pd.to_numeric(df['Scores'])

grouped_df = df.groupby('Area')

fig = go.Figure()

all_scores = pd.concat([group['Scores'] for _, group in grouped_df])
overall_mean = all_scores.mean()

grouped_df_sorted = sorted(grouped_df, key=lambda x: len(x[1]), reverse=True)

for area, group in grouped_df_sorted:
    fig.add_trace(go.Histogram(
        x=group['Scores'],
        name=f'Area {area}',
        opacity=0.7,
        marker=dict(
            line=dict(
                color='black',
                width=1
            )
        ),
        xbins=dict(
            start=min(group['Scores'].min(), 0),
            end=group['Scores'].max() + 10,
            size=5
        )
    ))

fig.add_trace(go.Scatter(
    x=[overall_mean, overall_mean],
    y=[0, 8000],
    mode='lines',
    line=dict(color='red', dash='dash'),
    name='Media de aciertos'
))

fig.update_layout(
    title='Distribución de Aciertos por Área',
    xaxis_title='Número de Aciertos',
    yaxis_title='Frecuencia',
    barmode='overlay',
    legend_title='Área',
    template='plotly_white'
)

fig.show()
