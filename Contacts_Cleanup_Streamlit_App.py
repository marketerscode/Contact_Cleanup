import pandas as pd
import phonenumbers
from fuzzywuzzy import process
import usaddress
import streamlit as st
import re


st.title('Contact Data Cleanup')

instructions = """
This tool allows you to upload a CSV file containing contact information and standardize the data. The standardization process includes:

- Capitalizing the first letter of the first and last names.
- Formatting phone numbers to the format (XXX) XXX-XXXX.
- Converting state abbreviations to full state names.
- Converting country abbreviations to full country names.
- Standardizing job titles based on a predefined list.
- Validating email addresses.

## Steps to Use the Tool:

1. **Upload a CSV File**: Click on the "Choose a CSV file" button to upload your CSV file containing the contact information.

2. **Wait for Processing**: Once the file is uploaded, the tool will process the data. This may take a few moments depending on the size of the file.

3. **Review the Processed Data**: After processing, the tool will display the original and processed data side by side. You can compare the changes made to each field.

4. **Download the Processed CSV**: If you're satisfied with the changes, you can download the processed CSV file by clicking on the "Download processed CSV" button.

## Notes:

- Ensure your CSV file contains columns for 'Address', 'Phone', 'State', 'Country', 'FirstName', 'LastName', 'Email', and 'Job Title'.
- The tool will attempt to standardize the data in these columns. If a column is missing or contains unexpected data, the tool may not be able to process it correctly.
- The tool uses fuzzy matching for job title standardization, which means it tries to match the closest standard title for each job title in your data.
"""

st.markdown(instructions, unsafe_allow_html=True)

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
        phone = phonenumbers.parse(phone, 'US')  # Specify 'US' as the country code
        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        return phone

# Define a function to return both full state names and abbreviations
def standardize_state(state):
    """Return the full name of the state and its abbreviation based on input, which could be either."""
    states = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
              'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 
              'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 
              'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 
              'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 
              'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
              'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 
              'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 
              'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 
              'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 
              'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
    rev_states = {v: k for k, v in states.items()}  # Reverse mapping for full name to abbreviation
    if state.upper() in states:
        abbreviation = state.upper()
        full_name = states[abbreviation]
    elif state.title() in rev_states:
        full_name = state.title()
        abbreviation = rev_states[full_name]
    else:
        abbreviation = full_name = state  # If no match is found, return the input as is
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
    """Capitalize the first letter of the first and last names."""
    return name.capitalize()

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
        df['Standardized State Abbreviation'], df['Standardized State'] = zip(*df['State'].apply(standardize_state))
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
            'Information Technology Director', 'System Analyst', 'Security Analyst', 'Application Developer',
            'Information Security Manager', 'Software Engineer', 'Systems Engineer', 'IT Project Manager',
            'Network Engineer', 'Database Administrator', 'Cloud Solutions Architect', 'DevOps Engineer',
            'Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'Data Center Manager',
            'IT Coordinator', 'Technical Support Specialist', 'Help Desk Technician', 'Cybersecurity Specialist',
            'Data Entry Clerk', 'IT Consultant', 'Software Quality Assurance Tester', 'User Interface Designer',
            'User Experience Designer', 'Mobile Developer', 'Webmaster', 'SEO Specialist', 'Digital Marketing Specialist',
            'E-commerce Manager', 'IT Systems Administrator', 'Network Operations Manager', 'Cloud Systems Engineer',
            'Penetration Tester', 'IT Asset Manager', 'IT Service Manager', 'Software Sales Specialist',
            'Customer Support Engineer', 'Technical Sales Engineer', 'Business Systems Analyst', 'CRM Technical Developer'
        ]  
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
