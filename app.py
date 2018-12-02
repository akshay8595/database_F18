import psycopg2
import getpass

'''
def __init__(self, connection_string):
    self.conn = psycopg2.connect(connection_string)


def check_connectivity(self):
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM recipe LIMIT 1")
    records = cursor.fetchall()
    return len(records) == 1
'''

def mvpList(cursor, year):
    if(year==''):
        cursor.execute("SELECT FIRSTNAME, LASTNAME, YEAR, AWARD\
                            FROM BIO JOIN PLAYERAWARDS\
                            ON BIOID = PLAYERID\
                            WHERE AWARD = 'Most Valuable Player'\
                            ;")
    else:
        cursor.execute("SELECT FIRSTNAME, LASTNAME, YEAR, AWARD\
                            FROM BIO JOIN PLAYERAWARDS\
                            ON BIOID = PLAYERID\
                            WHERE AWARD = 'Most Valuable Player'\
                            AND YEAR = %s;", (year))
    return cursor.fetchall()

def maxCollegeMVP(cursor, limitNum):
    cursor.execute("SELECT college, count(college) FROM BASKETBALL_MASTER\
                    JOIN PLAYERAWARDS ON BIOID = PLAYERID\
                    WHERE AWARD = 'Most Valuable Player' GROUP BY college\
                    ORDER BY count(college) DESC\
                    LIMIT %s;",[limitNum])
    return cursor.fetchall()

def maxAward(cursor, awardName, playerCount):
    cursor.execute("SELECT basketball_master.firstname, lastname, count(basketball_master.bioid)\
                    FROM basketball_master JOIN playerawards\
                    ON basketball_master.bioid = playerid AND AWARD = %s\
                    JOIN bio ON basketball_master.bioid = bio.bioid\
                    GROUP BY basketball_master.bioid, basketball_master.firstname, bio.lastname\
                    ORDER BY COUNT(basketball_master.bioid) DESC\
                    LIMIT %s;",(awardName,playerCount))
    return cursor.fetchall()

def maxMVP(cursor):
    cursor.execute("SELECT basketball_master.POS, COUNT(basketball_master.POS)\
                    FROM PLAYERAWARDS JOIN basketball_master on bioid = playerid\
                    WHERE AWARD = 'Most Valuable Player'\
                    GROUP BY basketball_master.pos\
                    ORDER BY COUNT DESC\
                    LIMIT 3;")
    return cursor.fetchall()

def maxHOF(cursor, numLim):
    cursor.execute("SELECT college, COUNT(college)\
                    FROM basketball_master JOIN hof on bioid = hofid\
                    GROUP BY COLLEGE\
                    ORDER BY count DESC\
                    LIMIT %s;",[numLim])
    return cursor.fetchall()

def maxCollege(cursor):
    cursor.execute("SELECT college, count(college)\
                    FROM basketball_master\
                    GROUP by college\
                    ORDER BY count DESC\
                    LIMIT 3;")
    return cursor.fetchall()

def maxState(cursor):
    cursor.execute("SELECT birthstate, count(birthstate)\
                    FROM origin\
                    GROUP by birthstate\
                    ORDER BY count DESC\
                    LIMIT 3;")
    return cursor.fetchall()

user = input("Enter User Name")
password = getpass.getpass('Password:')

connection_string = "host = 'localhost' dbname = 'project'"+\
                    " user = " + user + " password = "+ password
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()


while(True):
    print("******   Menu    ******\n",
          "1. Find MVP of an year",
          "2. Colleges with Most MVPs",
          "3. Players with Maximum Individual Awards",
          "4. Position of Player with Maximum MVPs",
          "5. Top 3 Colleges with Most Players",
          "6. Top 3 States with Most Players",
          "7. Colleges with Maximum Hall of Fame Inductees\n", sep = '\n',end='\n')

    print("******   ****    ******\n")
    choice = int(input('Enter your choice  '))

    if(choice==1):
        print("Do you want list of MVPs or yearly ",
              "1. List ",
              "2. Year ",sep='\n', end='\n')
        ch = int(input('Enter your choice '))
        if(ch==1):
            year = ''
        else:
            year = int(input('Enter the year '))

        fetchList = mvpList(cursor, year)
        for i in fetchList:
            print("MVP for year {} is {} {}".format(i[2],i[0],i[1]),end='\n')
        print()

    elif(choice==2):
        limitNum = int(input("How many colleges do you want "))
        fetchList = maxCollegeMVP(cursor, limitNum)
        for i in fetchList:
            print("{} {}".format(i[1], i[0]), end='\n')
        print()
    elif(choice==3):
        print("Which Award do you want",
              "1. Most Valuable Player",
              "2. Finals MVP",
              "3. Defensive Player of the Year",
              "4. Sixth Man of the Year",
              "5. Most Improved Player",
              "6. Rookie of the Year\n", sep='\n',end='\n'
              )
        awardEntry = {1: 'Most Valuable Player', 2: 'Finals MVP', 3: 'Defensive Player of the Year',\
                      4: 'Sixth Man of the Year', 5: 'Most Improved Player',\
                      6: 'Rookie of the Year'}

        ch = int(input('Enter choice'))
        playerCount = int(input('Enter the number of players'))
        fetchList = maxAward(cursor, awardEntry[ch], playerCount)
        for i in fetchList:
            print("{} {} {}".format(i[2], i[0], i[1]), end='\n')
        print()
    elif(choice==4):
        fetchList = maxMVP(cursor)
        print("Positions Most Likely to Win MVP are ")
        for i in fetchList:
            print(i[0])
        print()
    elif(choice==5):
        fetchList = maxCollege(cursor)
        for i in fetchList:
            print(i[1], i[0])
        print()
    elif (choice == 6):
        fetchList = maxState(cursor)
        for i in fetchList:
            print(i[1], i[0])
        print()
    elif(choice==7):
        numLim = int(input('How many top colleges do you want? '))
        fetchList = maxHOF(cursor, numLim)
        for i in fetchList:
            print(i[0])
        print()
