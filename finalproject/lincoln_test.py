import unittest
import lincoln
import sqlite3

DBNAME = 'concerts.db'
lincoln.init_db(DBNAME)
lincoln.concert_details_classical('classical')
lincoln.join_tables()
o=lincoln.concert_details_opera('opera')
lincoln.join_tables()
lincoln.concert_details_theater('theater')
lincoln.join_tables()
lincoln.concert_details_jazz('jazz')
lincoln.join_tables()
lincoln.concert_details_dance('dance')
lincoln.join_tables()
lincoln.concert_details_pop('pop')
lincoln.join_tables()
lincoln.get_tweets_for_site(o[0])


class TestConcertInfo(unittest.TestCase):
    def testConstructor(self):
        m1 = lincoln.ConcertInfo()
        m2 = lincoln.ConcertInfo("classical", 'Concert', 'April 11', '2 pm', 'David Geffen Hall', 'None', '$30')

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.time, "No Time")
        self.assertEqual(m2.date, "April 11")
        self.assertEqual(m2.location, "David Geffen Hall")
        self.assertEqual(m2.genre, "classical")

    def testConstructor1(self):
        m1 = lincoln.ConcertInfo('Yes')
        m2 = lincoln.ConcertInfo("jazz", 'Concert', 'Tomorrow', '6', 'Alice Tully', 'None', 'Free')

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.genre, "Yes")
        self.assertEqual(m2.date, "Tomorrow")
        self.assertEqual(m1.location, 'No Location')
        self.assertEqual(m2.genre, "jazz")

class TestTweet(unittest.TestCase):
    def testConstructor2(self):
        m1 = lincoln.Tweet()
        m2 = lincoln.Tweet('Hannah', 'I am so happy to be here', 'Today at 3', '3', '222', 'None', 'Class')

        self.assertEqual(m1.text, "no text")
        self.assertEqual(m1.location, 'No Location')
        self.assertEqual(m2.location, "Class")
        self.assertEqual(m2.username, 'Hannah')
        self.assertEqual(m2.text, "I am so happy to be here")

class TestDatabase(unittest.TestCase):

    def test_concert_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()


        sql = 'SELECT Location FROM Concerts WHERE genre = "classical"'
        results = cur.execute(sql)
        result_list = results.fetchall()
        print(result_list)
        self.assertIn(('David Geffen Hall',), result_list)
        #self.assertEqual(len(result_list), 15)

        sql = '''
            SELECT Location
            FROM Concerts
            WHERE genre = "opera"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        #self.assertEqual(len(result_list), 8)
        #self.assertEqual(result_list[0][3], 4.0)
        self.assertIn(('Metropolitan Opera House',), result_list)

        conn.close()

    def test_tweets_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Location
            FROM Tweets
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        # print(result_list)
        self.assertIn(('Metropolitan Opera House',), result_list)

        conn.close()





unittest.main()
