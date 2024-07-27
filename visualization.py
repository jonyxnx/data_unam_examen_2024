import pandas as pd
import plotly.graph_objects as go


df = pd.read_json('data.json')
df['Scores'] = pd.to_numeric(df['Scores'])

grouped_df = df.groupby('Area')

fig = go.Figure()

for area, group in grouped_df:
    fig.add_trace(go.Histogram(
        x=group['Scores'],
        name=f'Area {area}',
        opacity=0.5,  
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
    
fig.update_layout(
    title='Histograma de Aciertos por Área',
    xaxis_title='Número de Aciertos',
    yaxis_title='Frecuencia',
    barmode='overlay',  
    legend_title='Área',
    template='plotly_white' 
)


fig.show()
