from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import base64

my_data ={}

url = "https://pryka.in/product/one-flower-print-maxi-dress/"
# url1= "https://pryka.in/product/trellis-hand-embroidered-sharara-set/"
# url2 = 'https://pryka.in/product/off-white-bloom-print-3-piece-set-skirt-bandeau-cape/'

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"} 

soup = requests.get(url, headers)

doc= BeautifulSoup(soup.text, "html.parser")

# #Collecting Name
name = doc.find("h1").text.strip()
my_data["Product Name"]= name

#Collecting Price
tags = doc.find_all("p")
spans = (tags[0]).find_all("span")
startprice = (spans[0].find("bdi")).text
my_data["Startprice"]= startprice
try:
    endprice = (spans[2].find("bdi")).text
except: 
    endprice="-"
    if endprice=="-":
        my_data["Endprice"]= startprice

#Collecting Details
tags = doc.find_all("div", class_= "nm-tabs-panel-inner entry-content")
details = tags[0].contents
details = (details[1].text).split("\n")

for detail_type in details[:-1]:
    x= detail_type.index(":")
    
    my_data[detail_type[:x]]= detail_type[x+2:]

#Collecting other details
more_details = doc.find('div', id="nm-product-meta").div.div.text.split("\n")[1:-1]

for detail_type in more_details:
    x= detail_type.index(":")
    my_data[detail_type[:x]]= detail_type[x+2:]

print(more_details, end="\n\n")

img= doc.find("img", class_= 'wp-post-image')['src']
print(img)
img_name = f"Product Images/Pryka-{name}.jpg" 
urllib.request.urlretrieve(img, img_name)

#saving image in the dictionary
with open(f'{img_name}', 'rb') as f:
     image = f.read()
my_data['image'] = base64.encodebytes(image).decode('utf-8')


with open(f"{name}.json", "w") as outfile: 
    json.dump(my_data, outfile)
    


print(my_data)