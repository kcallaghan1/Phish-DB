
#Checks the Song table to see if a song exists before entering it
#Returns True if song exists
def checkSong(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Songs WHERE songName LIKE (?) ", (name,))

    if(len(cur.fetchall()) == 0):
        return False

    else:
        return True



#Returns True if Venue exists
def checkVenue(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Venues WHERE venueName LIKE (?)", (name,))

    if(len(cur.fetchall()) == 0):
        return False

    else:
        return True
