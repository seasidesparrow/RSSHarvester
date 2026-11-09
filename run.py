import os
from feedharvest.harvesters import FeedHarvester
from SciXPipelineUtils import setup_logging, load_config

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging('run.py', proj_home=proj_home,
                       level=config.get('LOGGING_LEVEL', 'INFO'),
                       attach_stdout=config.get('LOG_STDOUT', False))

DEFAULT_FEED = "https://joss.theoj.org/papers/published.atom"

def main():
    
    feed = config.get("FEED_URL", DEFAULT_FEED)

    harvester = FeedHarvester(sleep=config.get("SLEEP", False), 
                              sleep_sec=config.get("SLEEP_SECONDS", 5),
                              write_xml=config.get("WRITE_XML", False),
                              xml_out=config.get("OUTPUT_DIR", "./data/")
    )

    harvester.harvest(url=feed)
    xml_pages = harvester.xml_pages
    logger.info("Harvester loaded %s pages of XML from %s" % (len(xml_pages), feed))
    if config.get("WRITE_XML", False):
        logger.info("Writing XML to file(s) in %s" % config.get("OUTPUT_DIR", "./data/"))
        harvester.write()
    
    logger.info("Harvesting complete.")

if __name__ == "__main__":
    main()
