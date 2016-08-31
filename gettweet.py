# -*- coding: utf-8 -*-
import tweepy
import json
import sys
import ConfigParser
import re,string
from tinydb import TinyDB, Query
import os



#region - Import Config
parser = ConfigParser.SafeConfigParser()
parser.read("./account.ini")

consumer_key = parser.get("apikey","CONSUMER_KEY")
consumer_secret = parser.get("apikey","CONSUMER_SECRET")
access_token =  parser.get("accesstoken","ACCESS_TOKEN")
access_secret = parser.get("accesstoken","ACCESS_SECRET")
userid = parser.get("user","OWNER_ID")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
#endregion

#region - DataBase Setting
parser.read("./config.ini")
if not os.path.exists(parser.get("output","BASE_DIR")):
    os.mkdir(parser.get("output","BASE_DIR"))
dbfname = parser.get("output","BASE_DIR") + parser.get("output","DB_FNAME")
db = TinyDB(dbfname)
#endregion

#region Tweepy
api = tweepy.API(auth)
COUNT = int(parser.get("app","TWEET_COUNT"))

class StdOutListener(tweepy.StreamListener):

    def __init__(self,count,exithook=None):
        tweepy.StreamListener.__init__(self)
        self.count = count
        self.counthook = exithook
    hash_tags = re.compile(ur"[#＃][Ａ-Ｚａ-ｚA-Za-z一-鿆0-9０-９ぁ-ヶｦ-ﾟー]+",re.UNICODE)

    @staticmethod
    def strip_links(text):
        link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links         = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')    
        return text

    @staticmethod
    def strip_all_entities(text):
        entity_prefixes = ['@','#',u'＃',u'＠']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)

    def on_error(self, status):
        print status
    def on_status(self,status):
        if status.user.lang == u"ja" and self.countDown():
            tags = status.entities["hashtags"]
            text = StdOutListener.strip_all_entities(StdOutListener.strip_links(status.text))
            print text

            dic = {}
            dic["text"] = text
            dic["tags"] = tags
            db.insert(dic)

    def countDown(self):
        if self.count <= 0:
            if self.counthook != None : self.counthook()
            return False
        else:
            self.count -= 1
            return True
def exit():
    sys.exit()            

if __name__ == '__main__':
    searchword = None
    if len(sys.argv) > 1: searchword = sys.argv[1].decode("utf-8")
    l = StdOutListener(COUNT,exit)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = tweepy.Stream(auth, l)

    if searchword:
        stream.filter(track=[searchword])
    else:
        stream.sample()
    #endregion
