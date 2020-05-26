import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Establish a connection to the website, and download the html
my_url = "https://phish.net/setlists/phish-may-13-1989-the-orange-grove-syracuse-ny-usa.html"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#Hold the parsed-HTML in a BeautifulSoup data structure
page_soup = soup(page_html, "html.parser")


#gets the URL for the next show
contents = page_soup.findAll("div",{"class":"well clearfix"})
contents = contents[1]
nextATag = contents.find_all('a')[1]
nextURL = "https://phish.net" + nextATag["href"]


#Scrape the date from the site-header
contents = page_soup.find("div", {"class":"setlist-date-long"})
nextATag = contents.find_all('a')[1]
dateString = str(nextATag)
date = dateString[len(dateString) - 14: len(dateString) - 4]
year = date[len(date) - 4: len(date)]
month = date[0:2]
day = date[3:5]
date = year + "-" + month + "-" + day #Date is formatted for SQL, YYYY-MM-DD



#Get the Venue
contents = page_soup.find("div", {"class":"setlist-venue"})
nextATag = contents.find('a').contents[0]
venueCAPS = str(nextATag.contents[0])
venue = venueCAPS.title()



#Get the Location
contents = page_soup.find("div", {"class":"setlist-location"})
nextATag = contents.find_all('a')
loc = nextATag[0].contents[0] + ", " + nextATag[1].contents[0]



#Iterate through sets, and then songs per set
contents = page_soup.find("div", {"class":"setlist-body"})
#Outer-loop tracks the set number/encore
if(0 == 0):
    p = contents.find("p")
    for tag in p.find_all(["a","span"]):
        if(tag.name == "span"):
            print (tag.contents[0])
        else:
            song = tag.contents[0]
            print(song, end = "")
            sib = tag.next_sibling
            sibString = str(sib)
            while(sibString[0] == "<"):
                sib = sib.next_sibling
                sibString = str(sib)
            segue = False
            transition = False
            if("->" in sibString):
                #transition = True
                print("->")
            elif(">" in sibString):
                #segue = True
                print(">")
            else:
                print(",")
    
"""
    #Inner-loop gets the songs in each set
    for a in p.find_all("a"):
        song = a.contents[0]
        sib = a.next_sibling
        sibString = str(sib)
        while(sibString[0] == "<"):
            sib = sib.next_sibling
            sibString = str(sib)
        segue = False
        transition = False
        if("->" in sibString):
            transition = True
        elif(">" in sibString):
            segue = True

    print(p)
"""
