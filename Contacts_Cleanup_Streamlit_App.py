import pandas as pd
import phonenumbers
from fuzzywuzzy import process
import usaddress
import streamlit as st
import re

# Define a function to standardize addresses
def standardize_address(address):
    """Standardize addresses using the usaddress library, replacing 'Address' with 'Street'."""
    try:
        parsed_address, address_type = usaddress.tag(address)
        return ' '.join([component for component in parsed_address.values()]).replace('Address', 'Street')
    except:
        return address

# Define a function to standardize phone numbers with specific format
def standardize_phone(phone):
    """Standardize phone numbers to the format (XXX) XXX-XXXX."""
    try:
        phone = phonenumbers.parse(phone, 'US') # Specify 'US' as the country code
        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        return phone

# Define a function to return both full state names and abbreviations
def standardize_state(state):
    """Return both full state name and abbreviation based on input, which could be either."""
    states = {v: k for k, v in {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
              'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 
              'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 
              'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 
              'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 
              'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
              'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 
              'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 
              'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 
              'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 
              'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}.items()}
    full_name = state.title()  # Assume it might be full name initially
    abbreviation = states.get(full_name, state)  # Get abbreviation from full name, or keep original if not found
    return abbreviation, full_name

# Define a function to standardize countries
def standardize_country(country):
    """Convert country abbreviations to full country names."""
    countries = {'USA': 'United States', 'UK': 'United Kingdom', 'CAN': 'Canada', 'AUS': 'Australia', 
                 'DEU': 'Germany', 'FRA': 'France', 'ITA': 'Italy', 'JPN': 'Japan', 'CHN': 'China', 
                 'RUS': 'Russia', 'IND': 'India', 'BRA': 'Brazil', 'ZAF': 'South Africa', 'MEX': 'Mexico'}
    return countries.get(country, country)

# Define a function to standardize job titles
def standardize_job_title(title, standard_titles):
    """Match job titles to a predefined list of standard titles using fuzzy matching."""
    return process.extractOne(title, standard_titles)[0]

# Standardize names by capitalizing them
def standardize_name(name):
    """Capitalize the first and last names."""
    return name.upper()

# Validate email addresses
def validate_email(email):
    """Validate email using regex pattern matching."""
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(pattern, email.lower()) is not None

# Streamlit interface
st.title('Contact Data Standardization Tool')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Process and display the DataFrame
    try:
        original_df = df.copy()  # Keep a copy of the original DataFrame

        # Standardize the data values
        df['Standardized Address'] = df['Address'].apply(standardize_address)
        df['Standardized Phone'] = df['Phone'].apply(standardize_phone)
        df[['Standardized State Abbreviation', 'Standardized State']] = df['State'].apply(lambda x: pd.Series(standardize_state(x)))
        df['Standardized Country'] = df['Country'].apply(standardize_country)
        df['FirstName'] = df['FirstName'].apply(standardize_name)
        df['LastName'] = df['LastName'].apply(standardize_name)
        df['Email Validation'] = df['Email'].apply(lambda email: validate_email(str(email)))

        # Standardize job titles
        standard_titles = [
            'Software Developer', 'Data Scientist', 'Product Manager', 'Project Manager', 'Account Manager',
            'Sales Representative', 'Customer Service Representative', 'Marketing Manager', 'Graphic Designer',
            'Operations Manager', 'Human Resources Manager', 'Administrative Assistant', 'Quality Assurance Analyst',
            'Business Analyst', 'Financial Analyst', 'Accountant', 'Nurse Practitioner', 'Physician Assistant',
            'Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer', 'Web Developer', 'UX/UI Designer',
            'Compliance Officer', 'Supply Chain Manager', 'Procurement Specialist', 'IT Support Specialist',
            'Network Administrator', 'Systems Administrator', 'Chief Executive Officer', 'Chief Operating Officer',
            'Chief Financial Officer', 'Chief Technology Officer', 'Chief Marketing Officer', 'Chief Human Resources Officer',
            'Legal Counsel', 'Paralegal', 'Pharmacist', 'Physical Therapist', 'Occupational Therapist', 'Dentist',
            'Educational Administrator', 'Academic Advisor', 'Research Scientist', 'Laboratory Technician',
            'Environmental Scientist', 'Social Media Manager', 'Content Strategist', 'Event Planner', 'Logistics Coordinator',
            'Director of Engineering', 'Chief Information Officer', 'Business Development Manager', 'Software Engineer',
            'System Engineer', 'Product Designer', 'Data Analyst', 'Clinical Research Coordinator', 'Biomedical Engineer',
            'Public Relations Manager', 'Media Planner', 'IT Manager', 'Marketing Director', 'Creative Director',
            'Brand Manager', 'SEO Specialist', 'Recruiter', 'Copywriter', 'Technical Writer', 'Health and Safety Engineer',
            'Community Manager', 'Customer Success Manager', 'User Experience Researcher', 'Database Administrator',
            'Machine Learning Engineer', 'Network Security Engineer', 'Solutions Architect', 'Technical Support Specialist',
            'Sales Engineer', 'Corporate Lawyer', 'Management Consultant', 'Risk Manager', 'Audit Manager', 'Portfolio Manager'
        ]  # Expanded list to 100 standard job titles
        df['Standardized Job Title'] = df['Job Title'].apply(lambda title: standardize_job_title(title, standard_titles))

        # Display the original and the new DataFrame
        st.write('Original Data:', original_df)
        st.write('Processed Data:', df)

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
