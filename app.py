import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Function to load CSV data
def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load CSV file
filename = "data.csv"  # Change "data.csv" to the path of your CSV file
df = load_data(filename)

# Function to get exchange rate from DataFrame
def get_exchange_rate(date, df):
    # Check if the date is present in the DataFrame
    if date.strftime('%Y-%m-%d') in df['Date'].values:
        # Retrieve the forecast for the given date from the DataFrame
        forecast = df.loc[df['Date'] == date.strftime('%Y-%m-%d'), 'Forecast'].values[0]
        return forecast
    else:
        return None  # Return None if the date is not found in the DataFrame

# Function to get date corresponding to the lowest exchange rate within the next 7 days
def get_lowest_rate_date(data_next_7_days):
    lowest_rate_index = data_next_7_days['Forecast'].idxmin()
    lowest_rate_date = data_next_7_days.loc[lowest_rate_index, 'Date']
    return lowest_rate_date

# Set page background color to white
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation buttons
navigation = st.sidebar.radio("Go to", ["Check Exchange Rate", "Find Best Exchange Rate"])

# Page 1: Check Exchange Rate
if navigation == "Check Exchange Rate":
    st.markdown("<h1 style='text-align: center; color: black;'>Check EUR/JOD Exchange Rate</h1>", unsafe_allow_html=True)
    # Set label for date picker
    st.write("")
    st.markdown("<h3 style='text-align: center; color: grey;'>Choose date:</h3>", unsafe_allow_html=True)
    # Get today's date
    today = datetime.date.today()
    # Calculate the end date by adding 30 days to the current date
    end_date = today + datetime.timedelta(days=30)
    # Limit the date picker to 30 days from the current date
    selected_date = st.date_input("", value=today, min_value=today, max_value=end_date)
    # Button to trigger exchange rate check
    if st.button("Check"):
        exchange_rate = get_exchange_rate(selected_date, df)  # Pass the DataFrame as an argument
        if exchange_rate is not None:
            st.write(f"The exchange rate for {selected_date.strftime('%Y-%m-%d')} is: {exchange_rate}")
            
            # Get the week start and end dates for the selected date
            week_start = selected_date - datetime.timedelta(days=selected_date.weekday())
            week_end = week_start + datetime.timedelta(days=6)
            
            # Filter the DataFrame for the selected week
            data_selected_week = df[(df['Date'] >= week_start.strftime('%Y-%m-%d')) & (df['Date'] <= week_end.strftime('%Y-%m-%d'))]
            if not data_selected_week.empty:
                lowest_rate_index = data_selected_week['Forecast'].idxmin()
                lowest_rate_date = data_selected_week.loc[lowest_rate_index, 'Date']
                lowest_rate = data_selected_week.loc[lowest_rate_index, 'Forecast']
                st.write(f"The best exchange rate within the week ({week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}) is: {lowest_rate} on {lowest_rate_date}")
                st.write("It would be a good idea to exchange on that day!")
            else:
                st.write("No data available for the selected week.")
        else:
            st.write("No forecast available for the selected date.")



# Page 2: Find Best Exchange Rate
elif navigation == "Find Best Exchange Rate":
    st.markdown("<h1 style='text-align: center; color: black;'>Find Best EUR/JOD Exchange Rate</h1>", unsafe_allow_html=True)
    
    # Calculate the start and end dates for the next 7 days
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=7)
    
    # Get the data for the next 7 days
    data_next_7_days = df[(df['Date'] >= today.strftime('%Y-%m-%d')) & (df['Date'] <= end_date.strftime('%Y-%m-%d'))]
    
    # Button to find the lowest forecast rate within the next 7 days
    if st.button("Search"):
        if not data_next_7_days.empty:
            lowest_forecast = data_next_7_days['Forecast'].min()
            lowest_rate_date = get_lowest_rate_date(data_next_7_days)
            st.write(f"The best exchange rate within the next 7 days is: {lowest_forecast} on {lowest_rate_date}")
            
            # Create a line chart for the next 7 days
            fig, ax = plt.subplots()
            data_next_7_days.plot(x='Date', y='Forecast', ax=ax)
            ax.set_yticks([0.8826 + i * 0.0001 for i in range(4)])
            ax.set_xticks(range(len(data_next_7_days)))
            ax.set_xticklabels([(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(len(data_next_7_days))], rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.write("No data available for the next 7 days.")
