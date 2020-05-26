import SQLInsert
import valueCheck
import bs4
import sqlite3
from sqlite3 import Error
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



def main():
    database = r"C:\Users\Kenny\Documents\webscrape\Phish.db"

    #create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()

        #These are the variables responsible for tracking ID in each respective table.
        songCount = 1
        venueCount = 1
        showCount = 1
        setCount = 0
        setlistEntryCount = 1

        

        #Set-up with the first URL
        url = "https://phish.net/setlists/phish-december-02-1983-harris-millis-cafeteria-university-of-vermont-burlington-vt-usa.html"
        while (url != "https://phish.net/setlist/jump/next?showdate=2020-02-23"):
            uClient = uReq(url)
            page_html = uClient.read()
            uClient.close()


            #Hold the parsed-HTML in a BeautifulSoup data structure
            page_soup = soup(page_html, "html.parser")


            #gets the URL for the next show
            urlDivContainer = page_soup.findAll("div",{"class":"well clearfix"})
            urlDiv = urlDivContainer[1]
            aTag = urlDiv.find_all('a')[1]
            url = "https://phish.net" + aTag["href"]


            #Get the date from the site-header
            dateDiv = page_soup.find("div",{"class":"setlist-date-long"})
            aTag = dateDiv.find_all('a')[1]
            dateString = str(aTag)
            date = dateString[len(dateString) - 14: len(dateString) - 4] #Formatted in "MM/DD/YYYY"
            #Reorganizes date-format to "YYYY-MM-DD"
            year = date[len(date) - 4: len(date)]
            month = date[0:2]
            day = date[3:5]
            date = year + "-" + month + "-" + day
            

            #Get the Venue
            venueDiv = page_soup.find("div", {"class":"setlist-venue"})
            aTag = venueDiv.find('a').contents[0]
            venue = str(aTag.contents[0]).title()


            #Get the Location
            locDiv = page_soup.find("div", {"class":"setlist-location"})
            aTag = locDiv.find_all("a")
            city = aTag[0].contents[0]
            state = aTag[1].contents[0]


            #Iterate through sets
            setlistBody = page_soup.find("div", {"class":"setlist-body"})


            p = setlistBody.find("p")
            
            #Works through and gets the set or song information
            setlistSongCount = 1
            setInfo = ""
            for tag in p.find_all(["a", "span"]):
                #If next tag is span tag, it will hold the setInfo instead of a song
                if(tag.name == "span"):
                    setInfo = tag.contents[0]
                    setlistSongCount = 1
                    setCount += 1

                else: #Otherwise, the next tag will be an <a>, which holds a song.

                    song = tag.contents[0]

                    songID = 1
                    #Check whether or not to add song to Song table
                    val = valueCheck.checkSong(conn,song)
                    if(val == False):
                        songToInsert = (songCount, song)
                        SQLInsert.insert_song(conn, songToInsert)
                        songID = songCount
                        songCount += 1
                    else:
                        cur.execute("SELECT songID FROM Songs WHERE songName LIKE (?)", (song,))
                        songID = cur.fetchall()[0][0]

                    #Handles whether songs are separated by ",", ">", or "->"
                    sib = tag.next_sibling
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


                    setlistEntryToInsert = (setlistEntryCount, showCount, setCount, setInfo, setlistSongCount, songID, segue, transition)
                    SQLInsert.insert_setlist(conn, setlistEntryToInsert)
                    setlistSongCount += 1
                    setlistEntryCount += 1


            #Check the Venues table if this Venue already exists
            val = valueCheck.checkVenue(conn, venue)
            if(val == False):
                venueToInsert = (venueCount, venue, city, state)
                SQLInsert.insert_venue(conn, venueToInsert)
                venueID = venueCount
                venueCount += 1
            #Otherwise, get the venueID from the Venues table
            else:
                cur.execute("SELECT venueID FROM Venues WHERE venueName LIKE (?)", (venue,))
                venueID = cur.fetchall()[0][0]


            #Add the Show to the Shows table
            showToInsert = (showCount, date, venueID)
            SQLInsert.insert_show(conn, showToInsert)

            showCount += 1
            



if __name__ == "__main__":
    main()
