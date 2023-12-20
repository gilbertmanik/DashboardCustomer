import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

#----READ DATA-----
customer_merge = pd.read_pickle('data/customer_merge.pkl')
coord = pd.read_csv('data/coordinate.csv')

#----ROW 1-----
st.write('# Customer Demography Dashboard')
st.write("""Customer Demography Dashboard provides a comprehensive overview of key demographic characteristics of your customer base, 
         offering valuable insights into their profiles. 
         The dashboard leverages visualizations to make complex data easily understandable. """)

#----ROW 2-----
col1, col2 = st.columns(2)

df_profession = customer_merge['Profession'].value_counts().reset_index().sort_values(by='count', ascending=True)

plot_profession = px.bar(df_profession, x='count', y='Profession', 
                   labels = {'count' : 'Customer Count'})


col1.write('### Customer Profession Landscape')
col1.plotly_chart(plot_profession, use_container_width=True)

# data: map
prov_gender = pd.crosstab(index=customer_merge['province'],
                        columns=customer_merge['gender'], colnames=[None])
prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']
df_map = prov_gender.merge(coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False})

col2.write('### Customer Count across Indonesia')
col2.plotly_chart(plot_map, use_container_width=True)

#----ROW 3-----
st.divider()
col3, col4 = st.columns(2)

#----INPUT SELECT
input_select = col3.selectbox(
    label='Select Profession',
    options=customer_merge['Profession'].unique().sort_values()
    )

#----INPUT SLIDER
input_slider = col4.slider(
    label='Select age range',
    min_value=customer_merge['age'].min(),
    max_value=customer_merge['age'].max(),
    value=[20,50]
)
min_slider=input_slider[0]
max_slider=input_slider[1]

#----ROW 4-----
col5, col6 = st.columns(2)

#---- bar plot---
# data: barplot
customer_profession = customer_merge[customer_merge['Profession'] == input_select]
df_gen = pd.crosstab(index=customer_profession['generation'], columns='num_people', colnames=[None])
df_gen = df_gen.reset_index()

# plot: barplot
plot_gen = px.bar(df_gen, x='generation', y='num_people', 
                   labels = {'generation' : 'Generation',
                             'num_people' : 'Customer Count'})

col5.write(f'Customer Demographics: Generation-wise Distribution of Profession {input_select}')#f-string
col5.plotly_chart(plot_gen, use_container_width=True)

#----multi variate---

# data: multivariate
customer_age = customer_merge[customer_merge['age'].between(left=min_slider, right=max_slider)]
prof_gender = pd.crosstab(index=customer_age['Profession'],
                          columns=customer_age['gender'],
                          colnames=[None])
prof_gender_melt = prof_gender.melt(ignore_index=False, var_name='gender', value_name='num_people')
prof_gender_melt = prof_gender_melt.reset_index()
 
# plot: multivariate
plot_dept = px.bar(prof_gender_melt.sort_values(by='num_people'), 
                   x="num_people", y="Profession", 
                   color="gender", 
                   barmode='group',
                   labels = {'num_people' : 'Customer Count',
                             'Profession' : 'Profession',
                             'gender': 'Gender'}
                             )
 

col6.write(f'Multivariate: Gender per Profession, Age {min_slider} to {max_slider}')#f-string
col6.plotly_chart(plot_dept, use_container_width=True)


 
