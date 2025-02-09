import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide')
df = pd.read_csv('startup_funding.csv')
df1 = pd.read_csv('startup_cleened.csv')
df1['date'].fillna('2017-07-01',inplace=True)
df1['investors'].fillna('ABCD',inplace=True)
# df1[df1['investors'].apply(lambda x: str(x).isdigit())]
df1['year'] = df1['date'].fillna('').str.split('-').str.get(0)
df1['month'] = df1['date'].fillna('').str.split('-').str.get(1)

def overallAnalysis():
    st.title('Overall analysis')
    total = round(df1['amount'].sum())
    max = df1.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    max_name = df1.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).index[0]
    avg = round(df1.groupby('startup')['amount'].sum().mean())
    number = df1['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total Funding ',str(total)+' Cr','+22.22%')
    with col2 :
        st.metric('Maximun Funding ',str(max)+' Cr','+37.13%')
    with col3:
        st.metric('Average Funding ',str(avg)+' Cr','-15.67%')
    with col4:
        st.metric('Total startup',number,'33.33%')

    st.header('Month-On-Month Graph')
    temp_df = df1.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year']
    fig2, ax2 = plt.subplots(figsize=(4,1))
    ax2.plot(temp_df['x_axis'], temp_df['amount'])
    ax2.set_xlabel('Month-year',fontsize=6)
    ax2.set_ylabel('Amount(in cr)',fontsize=6)
    ax2.tick_params(axis='y', labelsize=4)
    ax2.tick_params(axis='x', labelsize=0.01)
    st.pyplot(fig2)

    yearWise = df1.groupby('year')['amount'].sum()
    monthWise = df1.groupby('month')['amount'].sum()
    col5,col6,col7 = st.columns(3)
    with col5:
     btn1 = st.button('See year wise deatils')
    with col6:
      btn2 = st.button('See month wise details')
    with col7:
        btn3 = st.button('clear screen')
    # in overall year wise graph
    if btn1:
        fig3, ax3 = plt.subplots(figsize=(4,1.56))
        ax3.bar(yearWise.index, yearWise.values)
        ax3.set_xlabel("--Year--",fontsize=6)
        ax3.set_ylabel("Amount(in cr)",fontsize=6)
        ax3.set_title("Year-wise Data(-@anoop-)",fontsize=6)
        ax3.tick_params(axis='y', labelsize=4)
        ax3.tick_params(axis='x', labelsize=5)
        st.pyplot(fig3)
    #in overall monthwise graph
    if btn2:
        fig4, ax4 = plt.subplots(figsize=(4,1.56))
        ax4.bar(monthWise.index, monthWise.values)
        ax4.set_xlabel("Month",fontsize=6)
        ax4.set_ylabel("Amount(in cr)",fontsize=6)
        ax4.set_title("Month-wise Data(-@anoop-)",fontsize=6)
        ax4.tick_params(axis='y', labelsize=4)
        ax4.tick_params(axis='x', labelsize=5)
        st.pyplot(fig4)
    if btn3:
        st.write(" ")

def load_startup_details(company):

    st.subheader('funding in startup '+str(company))
    startup = df1[df1['startup'].str.contains(company)].sort_index().head()[
        ['startup','vertical','subvertical','city','round','amount']]

    st.dataframe(startup)

def load_investors_details(investor):
    st.title(investor)
    #load last 5 recent investement
    last5_df = df1[df1['investors'].str.contains(investor)].sort_index().head()[['date','startup','vertical','city','round','amount']]
    big_series = df1[df1['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    low_series = df1[df1['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).tail()
    year_series = df1[df1['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('Most recent Investement')
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Inestement')
        st.dataframe(big_series)
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        st.subheader('Lowest Inestement')
        st.dataframe(low_series)
        fig, ax = plt.subplots()
        ax.bar(low_series.index, low_series.values)
        ax.tick_params(axis='x', labelsize=8)
        st.pyplot(fig)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Year wise Investement')
        st.dataframe(year_series)
        fig1, ax1 = plt.subplots()
        ax1.plot(year_series.index, year_series.values)
        ax1.set_xlabel('Year Of investement')
        ax1.set_ylabel('Amount in crore')
        st.pyplot(fig1)
    with col4:
        st.subheader('Sample of  Inestement')
        st.dataframe(year_series)
        fig, ax = plt.subplots()
        ax.bar(year_series.index, year_series.values)
        ax.tick_params(axis='x', labelsize=8)
        st.pyplot(fig)

df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')
st.sidebar.title('Startup funding analysis with anoop')
option = st.sidebar.selectbox('Selsect one :', ['Overall analysis', 'StartUp', 'Investor'])
if option == 'Overall analysis':
        overallAnalysis()
elif option == 'StartUp':
    company = st.sidebar.selectbox('selset startup', sorted(df['Startup Name'].unique().tolist()))
    st.title('Startup Analysis')
    btn1 = st.sidebar.button('Find startup Details')
    if btn1:
        load_startup_details(company)

else:
    selected_investor = st.sidebar.selectbox('select startup', sorted(set(df1['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investors_details(selected_investor)


