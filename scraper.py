from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def remove_label(html, string_label):
    label = html.find("strong", string=string_label)
    value = label.next_sibling
    return value

def get_listed_items(content):
    items = []
    for span in content:
        item = span.text.strip()
        items.append(item)
    return items

def scrape(URL):
    session = HTMLSession()
    r = session.get(URL)
    r.html.render(timeout=24)
    html_doc = r.html.search('seconds{}Territorial Acknowledgement')[0]
    soup = BeautifulSoup(html_doc, "html.parser")
    program_info = soup.find_all("div", class_="coveo-list-layout CoveoResult")
    
    # crete general dict here 
    program_dict = {}
    for program in program_info:
        header = program.find("a", class_="CoveoResultLink")
        link = header.get('href')
        title = header.text.strip()
        campus = program.find(class_=re.compile("campus-label")).text.strip()
        
        body = program.find("div", class_="col-12")
        program_details = body.find_all("p")[0]
        degree = program_details.find_all("strong")[0].text.strip()
        faculty = program_details.find_all("strong")[1].text.strip()
        
        ## TODO ask openai to complete statement and basically get keywords and important context 
        why_study = program.find("div", class_="CoveoExcerpt body-copy-4 my-2").text.strip()
        
        program_type = remove_label(body, "Program Type: ")  # space is critical
        
        # some programs dont have themes or interests
        if (body.find("strong", string="Themes: ")):
            theme_content = body.find("strong", string="Themes: ").find_next_siblings()
            themes = get_listed_items(theme_content)
        else:
            themes = ""
        if (body.find("strong", string="Interests: ")):
            interest_content = body.find("strong", string="Interests: ").find_next_siblings()
            interests = get_listed_items(interest_content)
        else:
            interests = ""

        program_id = remove_label(body, "Program ID: ")

        info = {
            "link": link,
            "campus": campus,
            "degree": degree,
            "faculty": faculty,
            "study_reason": why_study,
            "program_type": program_type,
            "themes": themes,
            "interests": interests,
            "program_id": program_id,
        }
        program_dict.update({title: info})
    return program_dict

def main(): 
    page = 0 
    # page should end at 312
    while page <= 12: 
        URL = "https://www.ualberta.ca/undergraduate-programs/index.html#first=" + str(page) + "&sort=%40ua__program%20ascending"
        print(URL)
        # TODO: see if u can implement async and await
        dictionary = scrape(URL)
        keys = dictionary.keys()
        links = [] # delete
        # print(dictionary)
        for title in keys:
            links.append(dictionary[title]["link"]) # delete
            # print(dictionary[title]["link"])
            # what you should send to sql: print(title, link, campus, degree, faculty, why_study, program_type, themes, interests, program_id)
            # pass
        print(links) # delete
        page += 24

if __name__ == "__main__":
    main()

## TODO: save data in SQL database
# - maybe do a coniditionn to make sure that the last thing scraped by the program is indeed the last program
## TODO: updating the information
