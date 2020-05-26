

def insert_song(conn, song):
    """ insert an entry into the Songs table
    :param conn:
    :param song:
    :return:
    """

    sql = """ INSERT INTO Songs(songID,songName)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, song)



def insert_venue(conn, venue):
    """ insert an entry into the Venues table
    :param conn:
    :param venue:
    :return:
    """

    sql = """ INSERT INTO Venues(venueID,venueName,venueCity,venueState)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql,venue)



def insert_show(conn, show):
    """ insert an entry into the Shows table
    :param conn:
    :param show:
    :return:
    """

    sql = """ INSERT INTO Shows(showID,showDate,venueID)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, show)


def insert_setlist(conn, setlist):
    """ insert an entry into the Setlists table
    :param conn:
    :param setlist:
    :return:
    """

    sql = """ INSERT INTO Setlists(setlistEntry,showID,setNumber,setInfo,SongNumber,SongID,Segue,Transition)
              VALUES(?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, setlist)
