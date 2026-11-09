import requests
from rss_parser import parse, detect_feed_type, FeedType
from time import sleep


class FetchXMLException(Exception):
    pass


class MissingURLException(Exception):
    pass


class FeedHarvestException(Exception):
    pass


class FeedHarvester(object):

    def __init__(self):
        self.xml_data = None
        self.xml_pages = []
        self.next_url = ""
        self.last_url = ""
        self.feed = None
        self.type = None
        self.parsed = None
        self.entries = []
        self.sleep = 1
        self.nice = True
        pass

    def _fetch_xml(self, url):
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "SciX@Harvard testbed; adshelp@cfa.harvard.edu"}
            )
            response.raise_for_status()
            self.xml_data = response.text
            self.xml_pages.append(self.xml_data)
            self.type = detect_feed_type(self.xml_data)
            self.parsed = parse(self.xml_data)
            print("haha self.type is %s" % self.type)
        except Exception as err:
            raise FetchXMLException("Failed to get feed data: %s" % err)

    def _get_next_page(self):

        # only ATOM feeds have pagination that we want
        self.next_url = ""
        if self.type == FeedType.ATOM:
            feed = self.parsed.feed
            links = feed.links
            if not links:
                raise Exception("This ATOM feed has no links section.")
            next_url = ""
            last_url = ""
    
            for l in links:
                if l.attributes["rel"] == "next":
                    next_url = l.attributes["href"]
                elif l.attributes["rel"] == "last":
                    last_url = l.attributes["href"]
            if not next_url or next_url == self.next_url:
                self.next_url = ""
            else:
                self.next_url = next_url
            if not self.last_url:
                self.last_url = last_url

    def harvest(self, url=None):
        try:
            if url:
                self.next_url = url
                while self.next_url:
                     self._fetch_xml(self.next_url)
                     self._get_next_page()
                     if self.type == FeedType.ATOM and self.nice:
                         sleep(self.sleep)
            else:
                raise MissingURLException("You must provide harvest with a feed URL")
        except Exception as err:
            raise FeedHarvestException("Feed harvest failed: %s" % err)
