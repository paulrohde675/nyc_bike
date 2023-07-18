import random
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_toggle as tog
from matplotlib.figure import Figure
from dashboard_sidebar import side_bar

@st.cache_data
def load_dataset(fraction: float = 0.0) -> pd.DataFrame:
    
    filename = 'data/raw/2018-citibike-tripdata_02.csv'
    
    # Set the number of rows
    #n_rows = 17548339
    n_rows = 3509668

    # Use skiprows to randomly sample the lines
    skip_idx = random.sample(range(1, n_rows), int((1-fraction)*n_rows))

    # Read the data
    df = pd.read_csv(filename, skiprows=skip_idx)

    return df

@st.cache_data
def create_dis_figure(df: pd.DataFrame, col: str, log: bool, bins: int) -> Figure:
    fig, ax = plt.subplots(figsize=(8,5))

    if log:
        df[col].hist(bins=bins)
        ax.set_xlabel(col)
        ax.set_ylabel("log counts")
        ax.set_yscale('log')

    else:
        df[col].hist(bins=bins)
        ax.set_xlabel(col)
        ax.set_ylabel("counts")
    
    
    fig.tight_layout()
    return fig

def page_data_exploration():
    st.title("Data Exploration")
    
    # render side_bar
    side_bar()
    
    st.write("""The first step in any data science project is getting to know the data. 
             In this case, the NYC Bike dataset from 2018, which is a 
             rich source of information about bike usage in New York City. It includes 
             details like trip duration, start and end locations, birth year of the 
             rider, and user type (Customer or Subscriber). By exploring this data, 
             one can gain insights about the feature and their distribution, missing values and 
             outliers.""")
    
    st.subheader('Load Data')
    
    fraction = st.slider('Fraction of dataset to explore', min_value=0.05, max_value=1.0, value=0.05, step=0.05)
    df = load_dataset(fraction)
    st.write('Total number of rwos = 17548339')
    st.write(f'Number of rwos loaded = {len(df.index)}')
    st.markdown('#')

    # Show the first few rows of the dataset
    st.subheader('Inspect Head')
    st.dataframe(df.head())
    
    st.markdown("- **usertype** is the target variable")
    st.markdown("- **start/stop time** include dates and times")
    st.markdown("- **start/stop time** is in seconds")
    st.markdown("- **station names** can be dropped")
    st.markdown("- **bikeid** can be dropped")
    st.markdown('#')
    
    # Inspect the datatypes of the columns
    st.subheader('Inspect Columns')
    types_df = df.dtypes
    types_df = pd.DataFrame(types_df, columns=types_df.name).T
    st.dataframe(types_df)    
    
    st.markdown("- **usertype** is a string an needs to be converted")
    st.markdown("- **start/stop times** are strings and need to be converted")
    st.markdown("- **start/stop station id** are strings and need to be converted")
    st.markdown('#')
    
    # Check for missing values
    st.subheader('Missing values')
    missing_values_df = df.isnull().sum()
    missing_values_df = pd.DataFrame(missing_values_df, columns=missing_values_df.name).T
    st.dataframe(missing_values_df)    
    st.markdown("- there are missing values that need to be removed")
    st.markdown('#')    
    
    # Get summary statistics
    st.subheader('Inspect Statistics')
    st.dataframe(df.describe())    

    # Split the page into two columns
    col1, col2 = st.columns(2)

    # distribution of usertype
    with col1:
        st.subheader('Gender counts')
        gender_df = df.groupby(['gender']).size().reset_index(name='counts')
        st.dataframe(gender_df)    
        st.markdown("- 0 : unknown")
        st.markdown("- 1 : female")
        st.markdown("- 2 : male")
        st.markdown("- there are much more female than male user")
        st.markdown("- there is a decent fraction of 'unknown' users")

    # distribution of gender
    with col2:
        st.subheader('Usertype counts')
        usertype_df = df.groupby(['usertype']).size().reset_index(name='counts')
        st.dataframe(usertype_df)   
        st.markdown("- the dataset is highly **imbalanced**")
        st.markdown("- this issue needs to be adressed")    

    st.markdown('#')

    st.subheader('Plot usertype vs gender counts')

    # Perform the groupby operation and reset the index
    gender_usertype_df = df.groupby(['usertype', 'gender']).size().reset_index(name='counts')

    # Pivot the data to create a matrix format suitable for a heatmap
    pivot_df = gender_usertype_df.pivot(index='usertype', columns='gender', values='counts')

    # Create a confusion matrix / heatmap
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.heatmap(pivot_df, annot=True, fmt="d", cmap="YlGnBu")
    
    ax.set_title('Counts of Different Genders for Each User Type')
    ax.set_xlabel('Gender')
    ax.set_ylabel('User Type')
    st.pyplot(fig)
    plt.cla()

    st.markdown("- most of the **Customers** are unkown")
    st.markdown("- **Subscribers** have only few unkwon observations") 
    st.markdown('#')
    
    st.subheader('Plot distributions')
    numeric_columns = df.select_dtypes(include=['int64', 'float64', 'int32']).columns
    col = st.selectbox("Select column", numeric_columns)
    bins = st.slider('Number of bins', min_value=5, max_value=100, value=30, step=5)
    log = tog.st_toggle_switch(label="Logarithmic scale")
    
    fig = create_dis_figure(df, col, log, bins)
    st.pyplot(fig)
    
    st.markdown("- **tripduration** longer than a day")
    st.markdown("- **tripduration** shorter than a minute") 
    st.markdown("- **longitude** and latitude that are very distant") 
    st.markdown("- people older than 100 years") 
    st.markdown('#')    
    
if __name__ == '__main__':
    page_data_exploration()