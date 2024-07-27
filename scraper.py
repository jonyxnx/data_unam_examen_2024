from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import pandas as pd

def get_info_from_results_url(url, df, career, faculty_name, area):
    """
    Extracts information from a results page and appends it to the provided DataFrame list.

    Args:
    - url (str): The URL of the results page to scrape.
    - df (list): A list to which the scraped data will be appended as dictionaries.
    - career (str): The name of the career related to the results.
    - faculty_name (str): The name of the faculty offering the career.
    - area (str): The area of study.

    Returns:
    - None: The function modifies the df list in place by appending dictionaries with the extracted data.
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    container = page_soup.findAll("tr")

    for element in container:
        values = element.find_all("td")
        if len(values) > 2: 
            df.append({
                'Area': area,
                'Career': career,
                'Faculty': faculty_name,
                'Scores': values[1].text.strip(),
                'Accepted': values[2].text.strip() == 'S'
            })

# Function to get the information for all the careers
def get_info_from_area_url(url, df):
    """
    Extracts career and faculty information from an area page and retrieves detailed results for each career.

    Args:
    - url (str): The URL of the area page to scrape.
    - df (list): A list to which the scraped data from results pages will be appended.

    Returns:
    - None: The function modifies the df list in place by appending dictionaries with the extracted data from results pages.
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    area = url[53]
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    containers = page_soup.findAll("div", "post-preview")

    for container in containers:
        career = container.find("h3").text.strip()
        faculties = container.find("p", class_="post-meta")
        links = faculties.find_all("a")

        for link in links:
            faculty_name = link.text.strip()
            href = link["href"]

            full_link = 'https://www.dgae.unam.mx/Licenciatura2024/resultados/' + href
            get_info_from_results_url(full_link, df, career, faculty_name, area)


# Initialize an empty list for storing the data
df = []

# Collect data from each Area
get_info_from_area_url('https://www.dgae.unam.mx/Licenciatura2024/resultados/15.html', df)
get_info_from_area_url('https://www.dgae.unam.mx/Licenciatura2024/resultados/25.html', df)
get_info_from_area_url('https://www.dgae.unam.mx/Licenciatura2024/resultados/35.html', df)
get_info_from_area_url('https://www.dgae.unam.mx/Licenciatura2024/resultados/45.html', df)

# Convert the list to a DataFrame and save as JSON Lines
df = pd.DataFrame(df, columns=['Area', 'Career', 'Faculty', 'Scores', 'Accepted'])
df.to_json('data.json', orient='records')

