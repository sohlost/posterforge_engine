from bs4 import BeautifulSoup
import lxml
import requests
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_rendered_html(url, chromedriver_path):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-video")
    chrome_options.add_argument("--disable-audio")
    
    # Block loading of specific resource types
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.default_content_setting_values.animations": 2,
    })

    # Set up the WebDriver with the provided ChromeDriver path
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for JavaScript to render (you might need to adjust the wait time)
        driver.implicitly_wait(5)

        # Get the rendered HTML
        rendered_html = driver.page_source

        return rendered_html

    finally:
        # Make sure to close the browser
        driver.quit()

def download_image(url, save_path):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the file name from the URL
        file_name = os.path.basename(url)
        
        # Combine the save path and file name
        full_path = os.path.join(save_path, file_name)
        
        # Write the content to a file
        with open(full_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Image downloaded successfully: {full_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")        


# Example usage
url = "https://genius.com/Joji-die-for-you-lyrics"  # Replace with the desired URL
chromedriver_path = '/home/sohlost/Projects/beatprints_engine/scrapper/chromedriver-linux64/chromedriver'  # Replace with your ChromeDriver path
html_content = get_rendered_html(url, chromedriver_path)


html_text = requests.get('https://genius.com/Joji-die-for-you-lyrics').text

soup = BeautifulSoup(html_content,'lxml')
trackname = soup.find('span', class_='SongHeaderdesktop__HiddenMask-sc-1effuo1-11 iMpFIj').text
artistname = soup.find('a', class_='StyledLink-sc-3ea0mt-0 iegxRM').text
trackno = soup.find('div', class_='HeaderArtistAndTracklistdesktop__Tracklist-sc-4vdeb8-2 glZsJC').text
releasedate = soup.find('span', class_='LabelWithIcon__Label-hjli77-1 hgsvkF').text
image = soup.find('img')
image_url = image['src']

save_directory = "/home/sohlost/Projects/beatprints_engine/scrapper/pictures"  # Change this to your desired directory

download_image(image_url, save_directory)


print(trackname)
print (artistname)
print(trackno)
print(releasedate)


#with open('home.html', 'r') as html_file:
#   content = html_file.read()
#    soup = BeautifulSoup(content, 'lxml')
#    tags = soup.find('h1')
#    print(tags.text)

   