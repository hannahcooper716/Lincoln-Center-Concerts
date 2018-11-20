**************Do not delete the cache that is submitted in order for the tests to run correctly for the database***********

Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
1. In this project, I have scraped the lincoln center calendar of events coming up (http://www.lincolncenter.org/calendar) in order to get information on the different concerts
a. these concerts are separated by genre
b. The information from these concerts are put into a database called concerts.db all separated by the information you get from running the program
2. Since these concert halls are very famous, and many people would like to know more about them, there is a feature to ask for tweets about a certain concert hall.
a. for this, you will have to get the twitter api information, which you will then put into a file called secrets.py so that when you connect your files to the internet, no one can get access to your secrets file (which gives them access to the information on your twitter account).
(https://apps.twitter.com/) This is the link to loading your twitter api information in order to connect to twitter

Any other information needed to run the program (e.g., pointer to getting started info for plotly)
1. Here, I have used plotly as a visualization tool to show graphs of my data. Here is the getting started info for plotly so you can do it too (https://plot.ly/python/getting-started/)

Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
1. For each genre, I had to scrape the webpage differently, so there are different functions for each one of them. A list of them are:
a. concert_details_pop
b. concert_details_opera
c. concert_details_jazz
d. concert_details_dance
e. concert_details_theater
f. concert_details_classical
2. There is also a main function for getting tweets
a. get_tweets_for_site
3. There are also many function to creating tables, adding the data to the tables, and then each of the graphs that were made to show a visualization of my data

Brief user guide, including how to run the program and how to choose presentation options.
1. First, in the secrets1.py file, go to the twitter API website that is linked above and get those four keys in order for your program to connect to facebook. Add them into the file
2. Next, when you load the program it will ask you to enter a command.
Depending on what genre you want to know more about, type that in
The options are:
1. classical
2. pop
3. jazz
4. theater
5. dance
(all of these must be typed with lowercase letters)
3. Next, after it loads a numbered list of the concerts for that genre, it will ask if you want to see a graph of the data
a. if you say yes, they will load in your browser
b. if you say no, it will ask you for a command
4. When it asks you for a command again, either type in tweets and the number of the concert hall in the above list (genre list of concerts) that you want to see tweets about (in the format "tweets" and then the number you want to see more about), type in another genre, or type in exit.
a. Example: you type in classical and it gives you a list of the classical concerts coming up. It asks if you want to see the visualization and you say no. The next command I want to see the tweets about David Geffen Hall, and number 4 in the list of concerts is at David Geffen Hall, so I will type in "Tweets 4" and get a list of those tweets
5. If you type in tweets, it will ask you if you want to see visualization of that data. Say yes if you want to and it will appear in your browser. If not, say no, then proceed to another command.
