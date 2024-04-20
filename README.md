
# Project Name: ***Contacts Cleanup***

### Description of Business Problem:
Businesses often face challenges with inconsistent contact data formats which hinder effective data analysis and communication strategies. This solution automates the cleansing and standardization of contact details such as phone numbers, addresses, state and country names, and job titles, which are often error-prone and inconsistently formatted.

    Major Use Cases
    1. **CRM Systems Integration**: Standardizing data before it enters CRM systems to ensure uniformity.
    2. **Data Migration Projects**: Cleansing data during migrations between systems or databases.
    3. **Marketing Campaigns**: Preparing contact lists to ensure accuracy in targeting and communications.

### Solution Design (high-level):
The solution is designed as a series of Python functions that apply transformations and standardization rules to specific data fields in a contact dataset. These functions leverage various Python libraries to parse and format data, ensuring consistency and reliability across records. The solution currently offers a minimum viable product (MVP) version 1.0 with core functionalities such as data validation, standardization, and a basic user interface via Streamlit. Future versions (v2, v3, etc.) will introduce enhanced GUI features, support for additional data formats, and more robust integration capabilities with enterprise systems.

### Solution Code Description (low-level design):
The codebase is structured around multiple Python functions, each dedicated to standardizing a different aspect of contact data. Key libraries used include pandas for data manipulation, phonenumbers for phone format standardization, usaddress for address parsing, and streamlit for the interactive web application interface. The code is hosted on GitHub, allowing easy access and collaboration.

### Solution Code Description: 
    • The code consists of multiple functions, each handling a specific type of data standardization.
    • Github: https://github.com/marketerscode/Contact_Cleanup

The product code consists of several Python functions integrated into a Streamlit application, providing a user-friendly interface for uploading CSV files, viewing processed data, and downloading the standardized outputs.

Certainly! Here’s a detailed description of the key functions used in the Contact Harmonizer Pro script. These functions are essential for the data standardization process, each serving a specific purpose to ensure the integrity and uniformity of contact data:

### Key Functions:

        1. standardize_address(address)
           - Purpose: This function standardizes addresses using the `usaddress` library. It aims to parse and format addresses 
           into a more consistent format, specifically replacing generic terms like 'Address' with 'Street' for clarity.
        
        2. standardize_phone(phone)
           - Purpose: Formats phone numbers into a consistent format. It uses the `phonenumbers` library to parse and format 
           phone numbers according to the national standard (e.g. (XXX) XXX-XXXX for US numbers).
        
        3. standardize_state(state)
           - Purpose: Converts state abbreviations to full state names and vice versa, depending on the input. It helps in 
           maintaining consistency whether the input is an abbreviation or a full name.
        
        4. standardize_country(country)
           - Purpose: Maps country abbreviations to their full names using a predefined dictionary. This function is crucial 
           for datasets that may contain various forms of country identifiers.
        
        5. standardize_job_title(title, standard_titles)
           - Purpose: Standardizes job titles based on a list of predefined standard titles using fuzzy matching provided by 
           the `fuzzywuzzy` library. This function aims to match and replace job titles with the closest standard title from the list.
        
        6. standardize_name(name)
           - Purpose: Capitalizes the first letter of first and last names to ensure name data is formatted uniformly across the dataset.
        
        7. validate_email(email)
           - Purpose: Validates email addresses using a regular expression to ensure they adhere to a standard email format.

## Installation:

### Instructions to get the solution working:

**Installation:**
1. **Clone the Repository:**
   - `git clone URL_to_GitHub_repository`
2. **Install Required Libraries:**
   - Run pip install pandas phonenumbers fuzzywuzzy python-usaddress streamlit
3. **Run the Script:**
   - Navigate to the script directory and execute streamlit run contact_standardization.py to start the web application

**Configuration, Input, and Output:**
- Ensure the input CSV file is placed in the specified directory and conforms to the expected format (columns for 'Address', 'Phone', 'State', etc.).
- The output is processed data saved in the same directory or can be directly downloaded through the Streamlit interface.

### Additional Important Guidelines:
    • The toolkit handles common data formats. If you encounter unique formats, you may need to adjust the parsing functions.
    • Data Backup: Always ensure that a backup of original data is available before applying standardization processes.
    • Regular Updates: Regularly update the standardization dictionaries and libraries to accommodate changes in data standards 
    and formats.
    • Customization: Users may need to customize parsing functions to accommodate unique data formats encountered in specific 
    use cases.
