#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
"""My implementation of the Swiss-system tournament"""

import psycopg2

def connect():
    """Connect to the PostgreSQL database.
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""


def deletePlayers():
    """Remove all the player records from the database."""
    myconn = connect()
    mycursor = myconn.cursor()
    mycursor.execute('DELETE from players;')
    rows = mycursor.rowcount
    myconn.commit()
    myconn.close()
    return rows

def countPlayers():
    """Returns the number of players currently registered."""
    myconn = connect()
    mycursor = myconn.cursor()
    mycursor.execute('SELECT * from players;')
    rows = mycursor.rowcount
    rows = 0 if rows is None else rows
    myconn.commit()
    myconn.close()
    return rows

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    myconn = connect()
    mycursor = myconn.cursor()
    query = mycursor.mogrify(
            "INSERT INTO players (fullname,wins,matches)" \
            " VALUES (%s, %s, %s)", (name, 0, 0))
    mycursor.execute(query)
    myconn.commit()
    myconn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
       A list of tuples, each of which contains (id, name, wins, matches):
         id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    myconn = connect()
    mycursor = myconn.cursor()
    mycursor.execute("SELECT * FROM players;")
    rows = mycursor.fetchall()
    myconn.commit()
    myconn.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
     """

    myconn = connect()
    mycursor = myconn.cursor()
    winnerq = mycursor.mogrify("UPDATE players " \
           "SET (wins, matches) = (wins+1, matches+1) " \
           "WHERE playerid = %s", [winner])
    mycursor.execute(winnerq)
    loserq = "UPDATE players " \
            "SET (matches) = (matches+1) " \
            "WHERE playerid = %s"
    mycursor.execute(loserq, [loser])
    myconn.commit()
    myconn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered,
    each player appears exactly once in the pairings.  Each player
    is paired with another player with an equal or nearly-equal
    win record, that is, a player adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    myconn = connect()
    mycursor = myconn.cursor()
    mycursor.execute(
            "SELECT playerid, fullname FROM players ORDER BY wins DESC;")
    results = mycursor.fetchall()
    newresults = []
    for i in range(0, len(results), 2):
        newresults.append(list(results[i] + results[i+1]))
    myconn.commit()
    myconn.close()
    return newresults
