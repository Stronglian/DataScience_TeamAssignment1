# DataScience_TeamAssignment1
*. Goal 
The goal of this assignment is to build a simple text analytics system. This system will crawl the news from Yahoo news every 3 hours and compute the top-5 most similar news for each news. 

*. Architecture of this system 
See attachment.

*. Requirements
1. Crawler
get the latest news from politics (https://tw.news.yahoo.com/politics) and entertainment (https://tw.news.yahoo.com/entertainment) categories in Yahoo. Then put these latest news to the message queue.
2. Message Queue
Make two queues for the news in different two categories.
3. Text Analytics 
For each category, do the following actions: 
1) get the latest news from queue
2) generate a list which follows the format shown in attachment
3) store this list in a local folder

*. Presentation of the result

1. a PPT (no more than 10 pages)

1) the idea of your implementation

2) the repository of your source code (you may upload your code in github)

3) the ppt file should upload to iclass before the class.

2. In-Class Demo
3. Each group will have 15 minutes (including 1 and 2).
