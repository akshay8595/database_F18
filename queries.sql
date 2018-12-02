
SELECT FIRSTNAME, LASTNAME, YEAR, AWARD
FROM BIO JOIN PLAYERAWARDS
ON BIOID = PLAYERID
WHERE AWARD = 'Most Valuable Player' AND YEAR = '1972';

# get input from the user on year

# top 5 colleges with maximum mvps

SELECT college, count(college) FROM BASKETBALL_MASTER
JOIN PLAYERAWARDS ON BIOID = PLAYERID
WHERE AWARD = 'Most Valuable Player' GROUP BY college
ORDER BY count(college) DESC
LIMIT 5;

# player who won a maximum particular awards

SELECT bioid, firstname, count(bioid)
FROM basketball_master JOIN playerawards
ON bioid = playerid AND AWARD = 'Most Valuable Player'
GROUP BY bioid, firstname
ORDER BY COUNT(bioid) DESC
LIMIT 1;

# pos at which players win maximum mvps

SELECT basketball_master.POS, COUNT(basketball_master.POS)
FROM PLAYERAWARDS JOIN basketball_master on bioid = playerid
WHERE AWARD = 'Most Valuable Player'
GROUP BY basketball_master.pos
ORDER BY COUNT DESC;

# maximum count players from a college
SELECT college, count(college) FROM basketball_master GROUP by college ORDER BY count DESC;

# maximum players by state
SELECT birthstate, count(birthstate) FROM origin GROUP by birthstate ORDER BY count DESC;

# college with maximum hof inductees
SELECT college, COUNT(college)
FROM basketball_master JOIN hof on bioid = hofid
GROUP BY COLLEGE
ORDER BY count DESC;
