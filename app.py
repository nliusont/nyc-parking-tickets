import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt

st.set_page_config(layout="wide")

# title and description
st.title('NYC Alternate Side Parking Violations')

st.write('Most NYC streets receive street cleaning one to two days a week, forcing car owners to vacate their street parking if they want to avoid a ticket. This is known as _alternate side parking_.\
         Which streets are you most likely to receive a ticket on? What times of day or year have the most tickets? I\'ve compiled the data below from NYC\'s Open Data portal to answer these questions. \
         This data is based on NYC FY24 data.')

# ---- cached funcs ----

# create a plotly map
def create_map(df_heatmap):
    use_log = True
    if use_log:
        metric = 'log_violations'
    else:
        metric = 'violations'

    fig = px.scatter_mapbox(
        df_heatmap, 
        lat='lat', 
        lon='long', 
        color=metric, 
        center=dict(lat=40.7128, lon=-74.0000),
        zoom=10, 
        mapbox_style="carto-positron",
        hover_data={      
            'street': True,            
            'violations': True,      
            'lat': False,            
            'long': False,            
            'log_violations': True
        },
        color_continuous_scale='RdYlGn_r',
        title="NYC Alternate Side Parking Violations Scatter Map",
        range_color=(df_heatmap[metric].min(), df_heatmap[metric].max())  
    )

    ticks = [1, 10, 25, 50, 100, 200, 400, 600, 800]
    
    fig.update_traces(marker=dict(size=16, opacity=0.8))
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        height=800,
        coloraxis_colorbar=dict(
            title="Violations",  
            tickvals=[np.log(x) for x in ticks],  
            ticktext=[str(x) for x in ticks],
            orientation="v",  
            yanchor="top",  
            y=1,  
            xanchor="left",  
            x=-0.1  
        )
    )

    return fig

col1, col2 = st.columns(2)

# ---- heatmap ----
with col1:
    if 'nyc_map' not in st.session_state:
        # load heatmap data and compute log_violations
        df_heatmap = pd.read_pickle('data/heatmap_df.pkl')
        df_heatmap['log_violations'] = np.log1p(df_heatmap['violations'])

        st.session_state['nyc_map'] = create_map(df_heatmap)

    # display the Plotly map
    st.plotly_chart(st.session_state['nyc_map'], use_container_width=True)

with col2:
    # load and display monthly violations chart
    violations_by_month = pd.read_pickle('data/by_month.pkl')
    violations_by_month['month_year'] = pd.to_datetime(violations_by_month['Month-Year'].astype(str), format='%Y-%m')

    month_chart = alt.Chart(violations_by_month).mark_line().encode(
        x=alt.X('month_year:T', title='Year-Month', axis=alt.Axis(format='%Y-%m', tickCount='month')),  
        y=alt.Y('Violations:Q', title='Number of Violations'),
        tooltip=[alt.Tooltip('month_year:T', title='Year-Month', format='%Y-%m'),
             alt.Tooltip('violations:Q', title='Violations')]  
    ).properties(
        title='Violations by Month',
        height=300  
    )

    st.altair_chart(month_chart, use_container_width=True)

    # load and display hourly violations chart
    violations_by_hour = pd.read_pickle('data/by_hour.pkl')
    hour_chart = alt.Chart(violations_by_hour).mark_line().encode(
        x=alt.X('hour:O', title='Hour of the Day'),  
        y=alt.Y('Violations:Q', title='Number of Violations'),
        tooltip=['hour', 'Violations']  
    ).properties(
        title='Violations by hour of day',
        height=300  
    )

    st.altair_chart(hour_chart, use_container_width=True)

# ---- footer ----
st.markdown("<h4 style='text-align: left;'>Background & sources</h4>", unsafe_allow_html=True)
li = 'https://www.nls.website/'
st.write('This streamlit app and underlying model were developed \
        by [Nick Liu-Sontag](%s), a data scientist :nerd_face: in Brooklyn, NY' % li)

od = 'https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data'
gh = 'https://github.com/nliusont/nyc-parking-tickets'
noa = 'https://data.cityofnewyork.us/City-Government/LION/2v4z-66xt/data?no_mobile=true'
st.write('[GitHub](%s)' % gh)
st.write('Sources: ')
st.write('[NYC Open Data - Parking Violations](%s)' % od)
st.write('[NYC LION GeoDatabase](%s)' % noa)
