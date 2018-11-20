from bs4 import BeautifulSoup
import requests
import json
from requests_oauthlib import OAuth1
import secrets1
import sqlite3
import sys
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='hannahcooper716', api_key='khGMAoSUDKEVdzGreGww')

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(baseurl):
    unique_ident = get_unique_key(baseurl)

    if unique_ident in CACHE_DICTION:
      #print("Getting cached data...")
      return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
    # Make the request and cache the new data
        resp = requests.get(baseurl) #delete params but deal with header
        CACHE_DICTION[unique_ident] = resp.text #get rid of json
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME,"w")
        f.write(dumped_json_cache)
        f.close() # Close the open file
        return CACHE_DICTION[unique_ident]


try:
    nearby_cache = open('nearby_cache_file.json', 'r')
    contents = nearby_cache.read()
    diction = json.loads(contents)
    nearby_cache.close()

    # if there was no file, no worries. There will be soon!
except:
    diction = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

try:
    cache_twitter = open('twitter_cache.json', 'r')
    contents_twitter = cache_twitter.read()
    diction_twitter = json.loads(contents_twitter)
    cache_twitter.close()
except:
    diction_twitter = {}

def make_request_twitter_cache(baseurl, params, auth):
    indent_twitter = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if indent_twitter in diction_twitter:
        #print("fetching cache data...")
        return diction_twitter[indent_twitter]
    else:
        #print("making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params, auth=auth)
        r = json.loads(resp.text)
        #['statuses']
        diction_twitter[indent_twitter] = r
        dumped_json_cache = json.dumps(diction_twitter)
        fw = open('twitter_cache.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return diction_twitter[indent_twitter]

class ConcertInfo:
    def __init__ (self, genre = "No Genre", title = 'No Title', date = 'No Date', time = 'No Time', location = 'No Location', full_location_url = "No location description", ticket_price = "No Ticket Price"):
        self.genre = genre
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.full_location_url = full_location_url
        self.price = ticket_price
    def __str__(self):
        return '[{}] {} ({}): {}, {} ({}), {}'.format(self.genre, self.title, self.time, self.date, self.location, self.full_location_url, self.price)

class Tweet:
    def __init__(self, username = "no username", text = 'no text', creation_date = 'no date', num_retweets = 'no retweets', num_favorites = 'no favorites', id_ = 'no id', location = "No Location"):
        # super().__init__(location)
        self.username = username
        self.text = text
        self.creation_date = creation_date
        self.num_retweets = num_retweets
        self.num_favorites = num_favorites
        self.id = id_
        self.location = location

    def __str__(self):
        return "@{}: ({}) {} \n [retweeted {} times] \n [favorited {} times] \n [tweeted on {}] | [id: {}]".format(self.username, self.location, self.text, self.num_retweets, self.num_favorites, self.creation_date, self.id)

def concert_details_classical(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    # for x in searching_div:
    #     print(x.text)
    #print(searching_div)
    divs = searching_div.find_all('div', class_ = "event-box classical-music genre")
    #searching_div.find_all('div', class_ = "event-box classical-music genre")
    list_of_classical_concerts = []
    list_of_locations_classical = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            location_url = x.find('a')['href']
            #print(location_url)
            full_location_url = base + location_url
            #print(full_location_url)
            location = x.find('a').text.strip()
            #print(location.text.strip())
            #print('--------------------')
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            #print(all_details.__str__())
# concert_details()
            list_of_locations_classical.append(all_locations)
            list_of_classical_concerts.append(all_details)
            #print(list_of_classical_concerts)
    update_concertlocation(list_of_locations_classical, "classical")
    update_table(list_of_classical_concerts, "classical")
    return list_of_classical_concerts
    #return list_of_parks

def concert_details_opera(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    # for x in searching_div:
    #     print(x.text)
    #print(searching_div)
    divs = searching_div.find_all('div', class_ = "event-box opera genre")
    #searching_div.find_all('div', class_ = "event-box classical-music genre")
    list_of_opera = []
    list_of_opera_locations = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            location_url = x.find('a')['href']
            #print(location_url)
            full_location_url = base + location_url
            #print(full_location_url)
            location = x.find('a').text.strip()
            #print(location.text.strip())
            #print('--------------------')
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            #print(all_details.__str__())
# concert_details()
            list_of_opera_locations.append(all_locations)
            list_of_opera.append(all_details)
    update_concertlocation(list_of_opera_locations, "opera")
    update_table(list_of_opera, "opera")
    return list_of_opera

def concert_details_theater(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    divs = searching_div.find_all('div', class_ = "event-box theater genre")
    list_of_theater = []
    list_of_theater_location = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            try:
                location_url = x.find('a')['href']
            except:
                location_url = "Not given"
            #print(location_url)
            try:
                full_location_url = base + location_url
            except:
                full_location_url = "None"
            #print(full_location_url)
            try:
                location = x.find('a').text.strip()
            except:
                location = "None"
            #print(location.text.strip())
            #print('--------------------')
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            list_of_theater_location.append(all_locations)
            list_of_theater.append(all_details)
    update_concertlocation(list_of_theater_location, "theater")
    update_table(list_of_theater, "theater")
    return list_of_theater

def concert_details_pop(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    # for x in searching_div:
    #     print(x.text)
    #print(searching_div)
    divs = searching_div.find_all('div', class_ = "event-box popular-music genre")
    #searching_div.find_all('div', class_ = "event-box classical-music genre")
    list_of_pop = []
    list_of_pop_location = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            try:
                location_url = x.find('a')['href']
            except:
                location_url = "Not given"
            #print(location_url)
            try:
                full_location_url = base + location_url
            except:
                full_location_url = "None"
            #print(full_location_url)
            try:
                location = x.find('a').text.strip()
            except:
                location = "None"
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            #print(all_details.__str__())
# concert_details()
            list_of_pop_location.append(all_locations)
            list_of_pop.append(all_details)
    update_concertlocation(list_of_pop_location, "pop")
    update_table(list_of_pop, "pop")
    return list_of_pop

def concert_details_dance(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    # for x in searching_div:
    #     print(x.text)
    #print(searching_div)
    divs = searching_div.find_all('div', class_ = "event-box dance genre")
    #searching_div.find_all('div', class_ = "event-box classical-music genre")
    list_of_dance = []
    list_of_dance_location = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            location_url = x.find('a')['href']
            #print(location_url)
            full_location_url = base + location_url
            #print(full_location_url)
            location = x.find('a').text.strip()
            #print(location.text.strip())
            #print('--------------------')
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            #print(all_details.__str__())
# concert_details()
            list_of_dance_location.append(all_locations)
            list_of_dance.append(all_details)
    update_concertlocation(list_of_dance_location, "Dance")
    update_table(list_of_dance, "Dance")
    return list_of_dance

def concert_details_jazz(genre):
    html = make_request_using_cache('http://www.lincolncenter.org/calendar')
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    searching_div = soup.find('div', class_ = 'events-wrapper')
    base = 'http://www.lincolncenter.org'
    # for x in searching_div:
    #     print(x.text)
    #print(searching_div)
    divs = searching_div.find_all('div', class_ = "event-box jazz genre")
    #searching_div.find_all('div', class_ = "event-box classical-music genre")
    list_of_jazz = []
    list_of_jazz_location = []
    for x in divs:
        genre = genre
        title = x.find('h3').text.strip()
        #print(title.text.strip())
        date = x.find('span').text.strip()
        #print(date.text.strip())
        time = x.find_all('span')[1].text.strip()
        #print(time.text.strip())
        price =  x.find_all('span')[2].text.strip()
        #print(price.text.strip())
        url = x.find('a')['href']
        #print(url)
        full_url = base + url
        #print(full_url)

        html1 = make_request_using_cache(full_url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        #print(soup1.prettify())
        searching1 = soup1.find_all('div', class_ = 'ed-show-tell--data__item location')
        #print(searching1)
        for x in searching1:
            location_url = x.find('a')['href']
            #print(location_url)
            full_location_url = base + location_url
            #print(full_location_url)
            location = x.find('a').text.strip()
            #print(location.text.strip())
            #print('--------------------')
            all_details = ConcertInfo(genre = genre, title = title, date = date, time = time, location = location, full_location_url = full_location_url, ticket_price = price)
            all_locations = ConcertInfo(location = location)
            #print(all_details.__str__())
# concert_details()
            list_of_jazz_location.append(all_locations)
            list_of_jazz.append(all_details)
    update_concertlocation(list_of_jazz_location,'jazz')
    update_table(list_of_jazz, "jazz")
    return list_of_jazz

def get_tweets_for_site(concert_hall_object):
    consumer_key = secrets1.twitter_api_key
    consumer_secret = secrets1.twitter_api_secret
    access_token = secrets1.twitter_access_token
    access_secret = secrets1.twitter_access_token_secret
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
    requests.get(url, auth=auth)
    twitter_link = 'https://api.twitter.com/1.1/search/tweets.json?'
    l = concert_hall_object.location
    concert_hall_name = str(l)
    twitter_data = make_request_twitter_cache(twitter_link, {'q': concert_hall_name, 'count': 100}, auth)
    tweet = twitter_data['statuses']
    #print(tweet)
    t = []
    #number = 0
    for x in tweet:
        #print(x)
        # number = number + 1
        # if number > 10:
        #     break
        creation_date = x['user']['created_at']
        location = concert_hall_object.location
        #print(creation_date)
        text = x['text']
        #print(text)
        username = x['user']['screen_name']
        #print(username)
        num_retweets = x['retweet_count']
        #print(num_retweets)
        num_favorites = x['favorite_count']
        #print(num_favorites)
        id_ = x['id']
        #print(id_)
        #location = x['user']['location']
        #print(location)
        tweets = Tweet(username = username, location = location, text = text, creation_date = creation_date, num_retweets = num_retweets, num_favorites = num_favorites, id_ = id_)
        #print(tweets)
        t.append(tweets)
        #     #print(t)
    L = []
    eliminated_doubles = []
    for x in t:
        if x.__str__() not in L:
            L.append(x.__str__())
            eliminated_doubles.append(x)

    update_tweets(eliminated_doubles)
    return eliminated_doubles

DBNAME = 'concerts.db'

def init_db(DBNAME):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Concerts';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Tweets';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'ConcertLocations';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Concerts' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Title' TEXT NOT NULL,
                'Time' TEXT NOT NULL,
                'Date' TEXT NOT NULL,
                'Location' TEXT NOT NULL,
                'LocationId' TEXT NOT NULL,
                'Price' TEXT,
                'Genre' TEXT

        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Tweets' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Username' TEXT NOT NULL,
                'CreationDate' TEXT NOT NULL,
                'Text' TEXT,
                'Location' TEXT NOT NULL,
                'LocationId' TEXT NOT NULL,
                'RetweetCount' INTEGER,
                'FavoritesCount' INTEGER,
                'UserId' INTEGER
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'ConcertLocations' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Location' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit() #any time you are changing data or adding new tables you have to do this (not with queries)
    conn.close()

def update_table(list_theater_object,genre):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT Genre '
    statement += 'FROM Concerts '
    statement += 'WHERE Genre = "{}" '.format(genre)
    statement += "LIMIT 1"
    result = cur.execute(statement).fetchone()
    if result == None:
        for x in list_theater_object:
            Genre = genre
            # x0.append(Genre)
            Title = x.title
            Time = x.time
            Location = x.location
            Price = x.price
            Date = x.date
            LocationId = ''
            insert = (None,Title,Time,Date, Location,LocationId,Price,Genre)
            statement = '''
                INSERT INTO "Concerts"
                VALUES (?,?,?,?,?,?,?,?)
            '''
            # x0.append(Genre)
            cur.execute(statement,insert)
            conn.commit()
        conn.close()
            # trace0 =
    else:
        conn.close()

def update_tweets(List_objects):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for x in List_objects:
        statement = 'SELECT UserId '
        statement += 'FROM Tweets '
        statement += "WHERE UserId = \'{}\' ".format(x.id)
        statement += 'LIMIT 1'
        #print(statement)
        result = cur.execute(statement).fetchone()
        if result == None:
            username = x.username
            text = x.text
            creation_date = x.creation_date
            retweets = x.num_retweets
            favorites = x.num_favorites
            location = x.location
            UserId = x.id
            LocationId = ''
            insert = (None,username,creation_date,text,location,LocationId,retweets,favorites,UserId)
            statement = '''
                INSERT INTO "Tweets"
                VALUES (?,?,?,?,?,?,?,?,?)
            '''
            cur.execute(statement,insert)
            conn.commit()
    conn.close()

def update_concertlocation(Location_object, genre):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for x in Location_object:
        statement = 'SELECT Location '
        statement += 'FROM ConcertLocations '
        statement += "WHERE Location = \"{}\" ".format(x.location)
        statement += 'LIMIT 1'
        #print(statement)
        result = cur.execute(statement).fetchone()
        #print(result)
        if result == None:
            location = x.location
            insert = (None, location)
            statement = '''
                INSERT INTO "ConcertLocations"
                VALUES (?,?)
            '''
            cur.execute(statement,insert)
            conn.commit()
    conn.close()

def join_tables():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT ConcertLocations.Id, Concerts.Id
        FROM Concerts
        JOIN ConcertLocations
        ON Concerts.Location = ConcertLocations.Location
    '''
    y = cur.execute(statement).fetchall()
    #print(y)
    for x in y:
        ConcertsId = x[1]
        ConcertLocationsId = x[0]
        #print(ConcertsId)
        #print(ConcertLocationsId)
        insert = (ConcertLocationsId, ConcertsId)
        statement = 'UPDATE Concerts '
        statement += 'SET LocationId = ? '
        statement += 'WHERE Id=?'
        cur.execute(statement, insert)
        conn.commit()
    conn.close()

def join_tables_tweets():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT ConcertLocations.Id, Tweets.Id
        FROM Tweets
        JOIN ConcertLocations
        ON Tweets.Location = ConcertLocations.Location
    '''
    y = cur.execute(statement).fetchall()
    #print(y)
    for x in y:
        #print(x)
        TweetsId = x[1]
        #print(TweetsId)
        ConcertLocationsId = x[0]
        #print(TweetsId)
        #print(ConcertLocationsId)
        insert = (ConcertLocationsId, TweetsId)
        statement = 'UPDATE Tweets '
        statement += 'SET LocationId = ? '
        statement += 'WHERE Id=?'
        cur.execute(statement, insert)
        conn.commit()
    conn.close()

def plotly_graph(genre):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT [Time], Title '
    statement += 'FROM Concerts '
    statement += 'WHERE Genre = {} '.format(genre)
    y = cur.execute(statement).fetchall()
    #print(y)
    time = []
    location = []
    for x in y:
        time.append(x[0])
        location.append(x[1])
    #print(time)
    #print(location)
    data = [go.Bar(
            x= location,
            y= time
    )]
    py.plot(data, filename='bar')

def plotly_graph100(genre):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT [Time], Price '
    statement += 'FROM Concerts '
    statement += 'WHERE Genre = {} '.format(genre)
    y = cur.execute(statement).fetchall()
    #print(y)
    time = []
    price = []
    for x in y:
        time.append(x[0])
        price.append(x[1])
    #print(time)
    #print(location)
    data = [go.Bar(
            x= price,
            y= time
    )]
    py.plot(data, filename='bar-chart')

# def plotly_graph100(genre):
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()
#     statement = 'SELECT Title, Price '
#     statement += 'FROM Concerts '
#     statement += 'WHERE Genre = {} '.format(genre)
#     y = cur.execute(statement).fetchall()
#     #print(y)
#     time = []
#     price = []
#     for x in y:
#         time.append(x[0])
#         price.append(x[1])
#     trace = go.Pie(labels=time, values=price)
#
#     py.plot([trace], filename='basic_pie_chart')
    # trace = go.Scatter(
    #     x = time,
    #     y = price,
    #     mode = 'markers'
    # )
    #
    # data = [trace]
    #
    # # Plot and embed in ipython notebook!
    # py.plot(data, filename='basic-scatter')

def plotly_graph2(tweet):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT RetweetCount, CreationDate '
    statement += 'FROM Tweets'
    y = cur.execute(statement).fetchall()
    #print(y)
    RetweetCount = []
    CreationDate = []
    for x in y:
        RetweetCount.append(x[0])
        CreationDate.append(x[1])
    trace = go.Scatter(
        x = CreationDate,
        y = RetweetCount,
        mode = 'markers'
    )

    data = [trace]

    py.plot(data, filename='basic-line')

def plotly_graph3(genre):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT [Date], Title '
    statement += 'FROM Concerts '
    statement += 'WHERE Genre = {} '.format(genre)
    y = cur.execute(statement).fetchall()
    #print(y)
    Date = []
    Title = []
    for x in y:
        Date.append(x[0])
        Title.append(x[1])
    trace = go.Scatter(
        x = Title,
        y = Date,
        mode = 'markers'
    )

    data = [trace]

    # Plot and embed in ipython notebook!
    py.plot(data, filename='basic-scatter')






if __name__ == "__main__":
    join_tables_tweets()
    resp = input('Enter command: ')
    while resp != "exit":
        number = 0
        if "classical" in resp:
            list_ = {}
            print('Classical Concerts at Lincoln Center:')
            classical = concert_details_classical('classical')
            for x in classical:
                number = number + 1
                list_[x] = number
                # for x in list_.keys():
                #     print(x)
                #print(list_.keys())
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')

        elif "opera" in resp:
            list_ = {}
            print('Opera Performances at Lincoln Center:')
            opera = concert_details_opera('opera')
            for x in opera:
                number = number + 1
                list_[x] = number
                #print(x.__str__())
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')
        elif "theater" in resp:
            list_ = {}
            print('Theater Performances at Lincoln Center:')
            theater = concert_details_theater('theater')
            for x in theater:
                number = number + 1
                list_[x] = number
                # print(list_)
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')
        elif "jazz" in resp:
            list_ = {}
            print('Jazz Performances at Lincoln Center:')
            jazz = concert_details_jazz('jazz')
            for x in jazz:
                number = number + 1
                list_[x] = number
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')
        elif "dance" in resp:
            list_ = {}
            print('Dance Performances at Lincoln Center:')
            dance = concert_details_dance('dance')
            for x in dance:
                number = number + 1
                list_[x] = number
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')
        elif "pop" in resp:
            list_ = {}
            print('Pop Concerts at Lincoln Center:')
            pop = concert_details_pop('pop')
            for x in pop:
                number = number + 1
                list_[x] = number
                join_tables()
                print(str(number) + " " + x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph('genre')
                plotly_graph100('genre')
                plotly_graph3('genre')
        elif "tweets" in resp:
            split = resp.split()
            for x in list_:
                join_tables_tweets()
                if int(split[1]) == list_[x]:
                    #print(get_tweets_for_site(x))
                    join_tables_tweets()
                    top_tweets = get_tweets_for_site(x)
                    #print(top_tweets)
            if len(top_tweets) == 0:
                print('Unable to find tweets for this place.')
                resp = input("Please enter a new command: ")
                if 'exit' == resp:
                    print("Bye!")
                    exit()
                continue
            for x in top_tweets:
                print(x.__str__())
            r = input('Do you want to see graphs of this data?: ')
            if r == 'yes':
                plotly_graph2('tweet')
        else:
            resp = input("Not a valid Command. Please enter a new command: ")
            if 'exit' == resp:
                print("Bye!")
                break
            continue
        resp = input('Enter command: ')
        if 'exit' == resp:
            print('Bye!')
            break
