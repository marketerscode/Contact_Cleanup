import pandas as pd
import phonenumbers
from fuzzywuzzy import process
import usaddress
import streamlit as st

# Define a function to standardize addresses
def standardize_address(address):
    try:
        parsed_address, address_type = usaddress.tag(address)
        return ' '.join([component for component in parsed_address.values()])
    except:
        return address

# Define a function to standardize phone numbers
def standardize_phone(phone):
    try:
        phone = phonenumbers.parse(phone, None)
        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
    except:
        return phone

# Define a function to standardize states
def standardize_state(state):
    states = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}  # Add more states as needed
    return states.get(state, state)

# Define a function to standardize countries
def standardize_country(country):
    countries = {'USA': 'United States', 'UK': 'United Kingdom', 'CAN': 'Canada', 'AUS': 'Australia', 'DEU': 'Germany', 'FRA': 'France', 'ITA': 'Italy', 'JPN': 'Japan', 'CHN': 'China', 'RUS': 'Russia', 'IND': 'India', 'BRA': 'Brazil', 'ZAF': 'South Africa', 'MEX': 'Mexico'}  # Add more countries as needed
    return countries.get(country, country)

# Define a function to standardize job titles
def standardize_job_title(title, standard_titles):
    return process.extractOne(title, standard_titles)[0]

# Streamlit interface
st.title('Contact Data Standardization Tool')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Process and display the DataFrame
    try:
        # Identify correct header columns
        headers = ['Phone', 'State', 'Country', 'Job Title', 'Address']  # replace with your actual column headers
        df = df[headers]

        # Standardize the data values
        df['Address'] = df['Address'].apply(standardize_address)
        df['Phone'] = df['Phone'].apply(standardize_phone)
        df['State'] = df['State'].apply(standardize_state)
        df['Country'] = df['Country'].apply(standardize_country)

        # Standardize job titles
        standard_titles = ['Software Developer', 'Data Scientist', 'Product Manager']  # replace with your actual standard job titles
        df['Standardized Job Title'] = df['Job Title'].apply(lambda title: standardize_job_title(title, standard_titles))

        st.write(df)

 # Convert DataFrame to CSV and let user download it
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download processed CSV",
            data=csv,
            file_name='contacts_processed.csv',
            mime='text/csv',
        )
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info('Upload a CSV file to begin.')
