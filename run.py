import json
from feedharvest.harvesters import FeedHarvester

def main():
    #feed = "https://joss.theoj.org/papers/published.atom"
    feed = "http://www.astronomerstelegram.org/?adsbiblio"
    foo = FeedHarvester()
    foo.harvest(url=feed)
    xml_pages = foo.xml_pages
    print("I have harvested %s XML pages from the feed %s" % (len(xml_pages), feed))
    
#    # the xml pages are in FeedHarvester.xml_pages
#    # parsed records will be in .records
#    parser = ATOMFeedParser()
#    records = parser.parse_harvest(foo.xml_pages)
#    with open("mblahgbl.xml", "w") as fw:
#        for r in records:
#            fw.write("%s\n" % r)
#    print("I found %s records." % len(records))
        

if __name__ == "__main__":
    main()
