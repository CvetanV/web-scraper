# Install frameworks
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

################################################################################################
########################################### BODY OF THE CODE ###################################

##### 1. Read and store the whole HTML code of the website #####################################
# Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
# Store the result in 'res' variable
res = requests.get(
    "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/"
)
# res = requests.get('https://tocka.com.mk/')
txt = res.text
status = res.status_code

# print(txt, status)

##### 2. Select the various elements of the website that you want to scrape #####################
# Invoke the beautifulsoup framework that will take the content of the request and parse it from HTML
soup = BeautifulSoup(res.content, "html.parser")

# Extract title of page
page_title = soup.title.text
# print(page_title)


# Extract head of page
page_head = soup.head
# print(page_head)


# Extract body of page
page_body = soup.body
# print(page_body)


# Extract first <h1>(...)</h1> text
first_h1 = soup.select("h1")[0].text
# print(first_h1)

# Extract the seventh_p_text and set it to 7th p element text of the page
seventh_p_text = soup.select("p")[6].text
# print(seventh_p_text)


##### 3. Extract all H1s ############################################################
# Count the number of h1 tags(sections)
h1_sections = soup.select("h1")
# print(h1_sections)

# Create an empty list all_h1_tags
all_h1_tags = []

# Set all_h1_tags to all h1 tags of the soup
for element in soup.select("h1"):
    all_h1_tags.append(element.text)
# print(all_h1_tags)


##### 4. Select top items #########################################################
# Create top_items as empty list
top_items = []

# Extract and store in the list top_items the title and the reviews for each item
products = soup.select("div.thumbnail")
# print(products)
for elem in products:
    title = elem.select("h4 > a.title")[0].text
    # description = elem.select('p.description')[0].text
    review_label = elem.select("div.ratings")[0].text
    # price = elem.select('h4.price')[0].text
    info = {
        "title": title.strip(),
        #    "description": description.strip(),
        "review": review_label.strip(),
        #    "price": price.strip()
    }
    top_items.append(info)

# print(top_items)


##### 5. Extract image information ###############################################
image_data = []

# Extract and store in image_data the links for the items
images = soup.select("img")
# print(images)
for image in images:
    src = image.get("src")
    alt = image.get("alt")
    img_info = {"src": src, "alt": alt}
    image_data.append(img_info)

# print(image_data)


##### 6. Extract href and links #################################################
all_links = []

links = soup.select("a")
# print(links)
for ahref in links:
    link_text = ahref.text
    link_text = link_text.strip() if link_text is not None else ""

    link_href = ahref.get("href")
    link_href = link_href.strip() if link_href is not None else ""

    link_info = {"href": link_href, "text": link_text}

    all_links.append(link_info)

# print(all_links)


##### 7. Store scraped data into a CSV file ###########################################
# Create all_products as empty list
all_products = []

# Extract and store in all_products all the scraped data
products = soup.select("div.thumbnail")
# print(products)
for product in products:
    name = product.select("h4 > a")[0].text.strip()
    description = product.select("p.description")[0].text.strip()
    price = product.select("h4.price")[0].text.strip()
    reviews = product.select("div.ratings")[0].text.strip()
    image = product.select("img")[0].get("src")

    product_info = {
        "name": name,
        "description": description,
        "price": price,
        "reviews": reviews,
        "image": image,
    }

    all_products.append(product_info)

# print(all_products)

column_names = all_products[0].keys()
# print(column_names)

with open("scraped_products.csv", "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, column_names)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)


##### 8. Store scraped data into a dataframe #######################################
# Create all_products as empty list
all_products = []

# Extract and store in all_products all the scraped data
products = soup.select("div.thumbnail")
# print(products)
for product in products:
    name = product.select("h4 > a")[0].text.strip()
    description = product.select("p.description")[0].text.strip()
    price = product.select("h4.price")[0].text.strip()
    reviews = product.select("div.ratings")[0].text.strip()
    image = product.select("img")[0].get("src")

    product_info = {
        "name": name,
        "description": description,
        "price": price,
        "reviews": reviews,
        "image": image,
    }

    all_products.append(product_info)
# print(all_products)

# Extract the keys of the dictionary as column names
column_names = all_products[0].keys()
column_names_list = list(column_names)
# print(column_names_list)

# Extract the values of the dictionary for each product
product_values = []
for product in all_products:
    product_values.append(product.values())

# Transform the dictionary of values into a list
product_values_list = list(product_values)
# print(product_values_list)

# Transofrm the list of values into a dataframe
df = pd.DataFrame(product_values_list)

# Add the names of the columns to the dataframe
df.columns = column_names
# print(df)
print("Web Scraper finished with scraping the website!")
