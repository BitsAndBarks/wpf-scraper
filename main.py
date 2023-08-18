import requests
from bs4 import BeautifulSoup
import json

# Step 1: Fetch the webpage
url = 'https://www.iwi.h-ka.de/iwii/info/compulsoryoptionalsubjects/INFB'
response = requests.get(url)
response.raise_for_status()

# Step 2: Parse the page with Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Locate all divs containing tables
table_wrappers = soup.find_all('div', class_='ui-datatable-tablewrapper')

json_data = []

for wrapper in table_wrappers:
    # Locate the preceding h2 for the current table
    heading = wrapper.find_previous('h2')

    if heading:
        title = heading.text.strip()
    else:
        title = "Unknown"

    # Extract table data
    table = wrapper.find('table')
    desired_columns = [0, 4]
    data = []

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        selected_data = [columns[i].text.strip() for i in desired_columns if i < len(columns)]

        # Check if selected data isn't empty
        if selected_data and all(selected_data):
            row_data = {
                "Defaultmodul": title,
                "Fach": selected_data[0],
                "ECTS": selected_data[1]
            }
            json_data.append(row_data)

# Step 4: Save the data to a JSON file
with open('WPF_Liste.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("Data saved to WPF_Liste.json!")