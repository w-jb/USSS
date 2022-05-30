import pandas as pd
import requests
import json
import csv
import urllib.request    
from bs4 import BeautifulSoup as bs
import urllib.parse


############### TEMP TO AVOID UNNECESSARY WEBSCRAPING ##############

##### WRITE SCRAPED PAGE TO TXT
# urllib.request.urlretrieve("https://en.wikipedia.org/wiki/United_States", "states.txt")

state_names = []

##### WRITE SCRAPED PAGES TO TXT
def state_files():
    for item in state_names:
        urllib.request.urlretrieve(f"https://en.wikipedia.org/wiki/{item}", f"{item}.txt")

##### READ SCRAPED PAGE FROM TXT
def txt_to_page(file_name):
    with open(f"{file_name}.txt", encoding="utf-8") as file:
        return bs(file.read(), "html.parser")

############### TEMP END


#save data in json file
def save_data_json(file_name, data):
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


#read data from json file
def load_data_json(file_name):
    with open(file_name, encoding="utf-8") as file:
        return json.loaad(file)


#save data to csv
def save_data_csv(filename, data, header_name):
    df = pd.DataFrame(data)
    df.to_csv(filename, header=header_name)


#read data from csv
def load_data_csv(filename):
    with open(filename) as file:
        data_lines = csv.reader(file, delimiter=',')
        for row in data_lines:
            data_list.append(row)


#webpage scraper
def scrape_page(url):
    r = requests.get(url)
    return bs(r.content, "html.parser")


#scrape list of the links to each state's page
states_list=[]
def scrape_list():
    url_base = "https://en.wikipedia.org//"

    #### TEMP
    ## scrap real page
    source = scrape_page("https://en.wikipedia.org/wiki/United_States")
    #### TEMP END

    for items in source.find(class_ = 'navbox-list navbox-odd plainlist'):
        for link in items.select('a'):
            url_part = link['href']

            #### TEMP
            ## make a list of states
            state_names.append(url_part.split('/',2)[2])
            #### TEMP END

            states_list.append(url_base + url_part)


#non-breakline spaces remove
def nbsp_remove(item):
    item = item.encode("ascii","replace")
    item = item.decode('utf-8')
    item = item.split("?")[0]
    item = item.replace("sqmi","").replace("mi","").replace("$","").replace("US","").replace("ft","").replace("/sqmi","").replace("/sq","").replace(",","")
    space_separator = item.find(" ")
    if space_separator != -1:
        if item.split(' ')[0].isnumeric():
            item = item.split(" ")[0]
        else:
            item = item.split(" ")[1]
    return item


# scrap area
def area_scrape(state):
    try:
        area_item = state.find(text="Area")
        area = area_item.parent.findNext('td').contents[0]

        if area.name == "a":
            area = area.text

        area = nbsp_remove(area)
        area = area.replace("sqmi","")
        area = area.replace(",","")

    except Exception:
        print("Area not available")
        area = "N/A"
    return area


#scrap length
def lenght_scrape(state):
    try:
        dims_item = state.find(text="Dimensions")
        length = dims_item.parent.findNext('td').contents[0]

        if length.name == "a":
            length = length.text

        length = nbsp_remove(length)

    except Exception:
        print("Length not available")
        length ="N/A"
    return length


#scrap width
def width_scrape(state):
    try:
        dims_item = state.find(text="Dimensions")
        width = dims_item.parent.findNext('td').findNext('td').contents[0]

        if width.name == "a":
            width = width.text

        width = nbsp_remove(width)

    except Exception:
        print("Width not available")
        width ="N/A"
    return width


#scrap avarage elevation
def avg_elev_scrape(state):
    try:
        elevation = state.find(text="Elevation")
        avg_elev = elevation.parent.findNext('td').contents[0]

        if avg_elev.name == "a":
            avg_elev = avg_elev.text

        avg_elev = nbsp_remove(avg_elev)

    except Exception:
        print("Avarage elevation not available")
        avg_elev = "N/A"
    return avg_elev


#scrap highest elevation
def hi_elev_scrape(state):
    try:
        elevation = state.find(text="Elevation")
        highest_elev = elevation.parent.findNext('td').findNext('td').contents[0]

        if highest_elev == "a":
            highest_elev = highest_elev.text

        highest_elev = nbsp_remove(highest_elev)

    except Exception:
        print("Highest elevation not available")
        highest_elev = "N/A"
    return highest_elev


#scrap lowest elevation
def low_elev_scrape(state):
    try:
        elevation = state.find(text="Elevation")
        lowest_elev = elevation.parent.findNext('td').findNext('td').findNext('td').contents[0]

        if lowest_elev.name == "a":
            lowest_elev = lowest_elev.text

        lowest_elev = nbsp_remove(lowest_elev)

    except Exception:
        print("Lowest elevation not available")
        lowest_elev = "N/A"
    return lowest_elev


#scrap population
def population_scrape(state):
    try:
        population = state.find(text="Population")
        total_pop = population.findNext('td').contents[0]

        if total_pop.name == "a":
            total_pop = total_pop.text

        total_pop = nbsp_remove(total_pop)

    except Exception:
        print("Population not available")
        total_pop = "N/A"
    return total_pop


#scrap density
def density_scrape(state):
    try:
        population = state.find(text="Population")
        density = population.findNext('td').findNext('td').findNext('td').contents[0]

        if density.name == "a":
            density = density.text

        density = nbsp_remove(density)

    except Exception:
        print("Density not available")
        density = "N/A"
    return density


#scrap populatio, density and medium houshold income
def income_scrape(state):
    try:
        population = state.find(text="Population")
        med_household_income = population.findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').contents[0]

        if med_household_income.name == "a":
            med_household_income = med_household_income.text

        med_household_income = nbsp_remove(med_household_income)

    except Exception:
        print("Household income not available")
        med_household_income = "N/A"
    return med_household_income


#scrape arae, dimensions(length/width), elevation(avarage, highest, lowest), population(total/density), median houshold income
data_list = []
def data_scrape(state_webpage):

    #### TEMP
    ## to scrap the page
    state = scrape_page(state_webpage)
    
    ## to use saved file instead real scrapping
    #state = txt_to_page(f"{state_webpage}")
    #### TEMP END

    area = area_scrape(state)
    length = lenght_scrape(state)
    width = width_scrape(state)
    avg_elev = avg_elev_scrape(state)
    highest_elev = hi_elev_scrape(state)
    lowest_elev = low_elev_scrape(state)
    total_pop = population_scrape(state)
    density = density_scrape(state)
    med_household_income = income_scrape(state)

    state_name = state_webpage.split('/',6)[6]
    sub_data = [state_name.replace(",",""), area, length, width, avg_elev, highest_elev, lowest_elev, total_pop, density, med_household_income]
    data_list.append(sub_data)


#for each state scrape arae, dimensions, population, median houshold income
def data_aquisition():
    for state in states_list:
        ## to work with files under state name
        #data_scrape(state.split('/',5)[5])
        ## for webscrapping
        data_scrape(state)

#### DEFS END

#### MAIN LOOP BEGINS

# #### TEMP
## real scrapping
scrape_list()
data_aquisition()

## using saved file
#source = txt_to_page("states")

## saving sub sites
#state_files()
## one in case of using saved files
#scrape_list()
save_data_csv("states_list.csv", states_list, "states")

## one in case of using saved files
#data_aquisition()

#### TEMP END

data_header = [ 'state', 'area' , 'length', 'width', 'avg_elev', 'highest_elev', 'lowest_elev', 'total_pop', 'density', 'med_household_income']
save_data_csv("data.csv", data_list, data_header)
