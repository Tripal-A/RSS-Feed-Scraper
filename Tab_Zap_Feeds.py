import feedparser
import pandas as pd
from sqlalchemy import create_engine
import datetime #Imported this in because the Rss feed has date as str, need to convert it to date object done on line 26
import codecs #Library that decodes or encodes to binary this library was needed for the pythonanywhere environment and not pycharm



if __name__ == '__main__':
    rss = {
        'Tableau' : 'https://www.upwork.com/ab/feed/jobs/rss?q=tableau&sort=recency&paging=0%3B10&api_params=1&securityToken' \
            '=41b814cd0cdc3f5757dc7bea625ce904b0942d87b91356f02e0ac37c031e4b57477fe06f3fdc69c05fbb2641984b2b713c90e520e21a9' \
            'a39ae7f686aff2cfb2d&userUid=1199087053722742784&orgUid=1266513265949421569',
        'Zapier' : 'https://www.upwork.com/ab/feed/jobs/rss?q=zapier&sort=recency&paging=0%3B10&api' \
                '_params=1&securityToken=41b814cd0cdc3f5757dc7bea625ce904b0942d87b91356f02e0ac37c031' \
                'e4b57477fe06f3fdc69c05fbb2641984b2b713c90e520e21a9a39ae7f686aff2cfb2d&userUid=1199087' \
                '053722742784&orgUid=1266513265949421569'
    }

    rssFeeds=[] #Creating empty list to store posts from all feeds

    posts = [] # list of posts [(title1, link1, summary1,published), (title2, link2, summary2,published) ... ]
    for source in rss: #This is what creates the loop that runs through the RSS feed and grabs entry elements , this will execute as many times as there are Rss feeds
        rssFeed = feedparser.parse(rss.get(source))
        for post in rssFeed.entries:
            pub_date=datetime.datetime.strptime(codecs.decode(post.published.encode("ascii"),'utf-8'),'%a, %d %b %Y %H:%M:%S +0000')
            posts.append((post.title, post.summary, post.link, pub_date, source))#Adds new information to already ran loops

    df = pd.DataFrame(posts, columns=['Title', 'Summary', 'Link','Published_Date','Keyword']) # pass data to init



    hostname = "danmergeyourdata.mysql.pythonanywhere-services.com"
    dbname = "danmergeyourdata$Upwork-RSS"
    uname = "danmergeyourdata"
    pwd = "nad5645!"


    engine = create_engine(
        "mysql://{user}:{pw}@{host}/{db}"
        .format(host=hostname, db=dbname, user=uname, pw=pwd),pool_recycle=280)

    df.to_sql('Rss_Feed',  con = engine,  index=False,if_exists='append')

    engine.dispose()

#writer = pd.ExcelWriter('RSS.xlsx', engine='xlsxwriter')
#df.to_excel(writer, sheet_name='Sheet1')
#df_2.to_excel(writer, sheet_name='Sheet1')
#writer.save()


