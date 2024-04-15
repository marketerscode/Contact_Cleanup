
# Project Name: ***Contacts Cleanup***

## Project & Work Product Description: 
### Project Goals 
    • Learn to reuse Python libraries for data manipulation
    • Learn to automate data cleaning tasks
    • Get the toolkit working efficiently
    • Support multiple data formats
    • Ensure robust error handling and data validation

### Description of Business Problem:
Businesses often face challenges with inconsistent contact data formats which hinder effective data analysis and communication strategies. This project aims to develop a toolkit that standardizes contact data such as phone numbers, addresses, states, countries, and job titles to improve data reliability and usability.

### Solution Design (high-level):
The solution is designed as a series of Python functions that apply transformations and standardization rules to specific data fields in a contact dataset. These functions leverage various Python libraries to parse and format data, ensuring consistency and reliability across records.

### Solution Code Description: 
    • The code consists of multiple functions, each handling a specific type of data standardization.
    • [Link to complete code on GitHub](URL_to_GitHub_repository)

## Lessons Learned:
Learning how to integrate multiple external libraries and handle various data inconsistencies were key outcomes of this project. Handling edge cases and unexpected data formats were crucial for ensuring the robustness of the toolkit.

## Application Use: 
### Major Use Cases
1. **CRM Systems Integration**: Standardizing data before it enters CRM systems to ensure uniformity.
2. **Data Migration Projects**: Cleansing data during migrations between systems or databases.
3. **Marketing Campaigns**: Preparing contact lists to ensure accuracy in targeting and communications.

## Description of Solution:
    • The toolkit provides functions to standardize phone numbers, addresses, states, countries, and job titles.
    • Future versions will include a GUI for easier interaction and support for additional data types.
    • **MVP 1.0** delivered, focusing on core functionalities. Future versions (v2, v3) will expand capabilities and user interface.

### Application Use - ***Tips & Tricks***:
    • Always backup your data before applying standardization processes.
    • Review the standardization dictionaries regularly to ensure they remain up-to-date with changes in data formats or standards.

## Installation:

### Instructions to get the solution working:

**Installation:**
1. **Clone the Repository:**
   - `git clone URL_to_GitHub_repository`
2. **Install Required Libraries:**
   - `pip install pandas phonenumbers fuzzywuzzy usaddress`
3. **Run the Script:**
   - Navigate to the script directory and run `python contact_standardization.py`

**Configuration, Input, and Output:**
- Place your input CSV in the specified directory, ensure it matches the expected format.
- Outputs will be saved in the same directory as processed CSV files.

### Additional Important Guidelines:
    • The toolkit handles common data formats. If you encounter unique formats, you may need to adjust the parsing functions.
    • Consider contributing improvements or additional functions back to the project via GitHub to help it grow and support more use cases.
