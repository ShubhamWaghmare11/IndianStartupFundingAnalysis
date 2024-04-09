import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('\n')
    st.header('\n')
    st.header('\n')


    col1,col2=st.columns(2)
    with col1:
        st.header('MoM graph')
        selected_option1 = st.selectbox('Select Type', ['Total', 'Count'])
        if selected_option1 == 'Total':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x_axis'], temp_df['amount'])

        ax3.xaxis.set_major_locator(MaxNLocator())
        st.pyplot(fig3)

    with col2:

        st.header('Sector Analysis')
        choice=st.selectbox('Select Type',['Total - (Top Sectors based on amount invested)','Count- (Top Sectors based on number of companies)'],key='selectbox1')

        if choice == 'Total - (Top Sectors based on amount invested)':
            temp_df = df.groupby(['vertical'])['amount'].sum().sort_values(ascending=False).head(10)

        else:
            temp_df = df.groupby(['vertical'])['amount'].count().sort_values(ascending=False).head(10)


        fig1, ax1 = plt.subplots()
        ax1.pie(temp_df, labels=temp_df.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    st.header('\n')
    st.header('\n')
    st.header('\n')
    st.header('\n')

    st.header('Top 10 cities by Startup funding')

    city_funding= df.groupby('city')['amount'].sum().sort_values(ascending=False).head(20)
    fig1, ax1 = plt.subplots()
    ax1.bar(city_funding.index,city_funding)
    plt.xticks(rotation=90)
    st.pyplot(fig1)

    st.header('\n')
    st.header('\n')
    st.header('\n')
    st.header('\n')

    col1,col2=st.columns(2)
    with col1:

        st.subheader("Top Startups year wise")
        temp_df= df.groupby(['year','startup'])['amount'].sum().sort_values(ascending=False).reset_index().drop_duplicates(subset='year',keep='first').sort_values('year')
        st.dataframe(temp_df)

    with col2:
        st.subheader("Overall Top Starups")
        temp_df = df.groupby(['year','startup'])['amount'].sum().sort_values(ascending=False).head(5)
        st.dataframe(temp_df)

    st.header('\n')
    st.header('\n')

    st.subheader('Top Investors')
    temp_df = df.groupby(['investors','startup'])['amount'].sum().sort_values(ascending=False).head(10)
    st.dataframe(temp_df)
def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    print(df.info())

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment (Year-over-Year Investment)')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)


def load_startup_details(startup):
    st.title(startup)

    st.header('Industry')
    st.subheader(df[df['startup']==startup]['vertical'].values[0])
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup=st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)