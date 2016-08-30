import ConfigParser
import codecs
from tinydb import TinyDB, Query


parser = ConfigParser.SafeConfigParser()
parser.read("./config.ini")
dbfname = parser.get("output","BASE_DIR") + parser.get("output","DB_FNAME")
ofname = parser.get("output","BASE_DIR") + parser.get("output","TWEET_FNAME")

db = TinyDB(dbfname)

if __name__ == '__main__':
    print "DB 2 FILE Start"
    with codecs.open(ofname,mode = "w",encoding="utf-8") as out:
        i = 0
        for tweet in db.all():
            out.write(tweet["text"] + "\n")
            i += 1
    print "file writing complete." + str(i) + "tweets.\n\n"