import logging.config
import os
import time
from datetime import date
from emailer import SeatAlertEmailer
from scraper import Scraper
from urllib.error import URLError
from settings import logging_config, scraper_settings

class SeatSecurer(object):
    def __init__(self):
        if not os.path.exists("logs/"):
            os.makedirs("logs/")

        logging.config.dictConfig(logging_config)

        self.logger = logging.getLogger(__name__)
        
        FORMAT_ERROR = "scraper_settings format is invalid, please refers to project doc"

        try:
            self.interval = float(scraper_settings["scraping_interval"])
            self.do_email_alert = scraper_settings["do_email_alert"]

            start_date_parts = scraper_settings["start_date"].split('-')
            end_date_parts = scraper_settings["end_date"].split('-')

            self.scraper = Scraper(
                                    date(int(start_date_parts[0]), int(start_date_parts[1]), int(start_date_parts[2])), 
                                    date(int(end_date_parts[0]), int(end_date_parts[1]), int(end_date_parts[2])), 
                                    scraper_settings["do_email_alert"], scraper_settings["city"]
                                )

        except:
            raise ValueError(FORMAT_ERROR)

        self.alert = SeatAlertEmailer()

    def start(self):
        i = 0
        errorFree = True
        while errorFree:
            i += 1
            self.logger.info("####### START SCRAPING {0} #######".format(i))
            try:
                scrape_result = self.scraper.scrape()
                # with open("log","a+") as fw:
                #     fw.write(str(scrape_result[0]))
                if scrape_result[1] and self.do_email_alert:
                    self.alert.send(scrape_result[0])

                self.logger.info(
                    "####### SCRAPING {0} FINISHED, STARTING AGAIN IN {1} MIN #######\n".format(i, self.interval))
                time.sleep(self.interval * 60)

            except (ConnectionRefusedError, URLError):
                self.logger.error(
                    "******* CONNECTION ERROR, STARTING AGAIN IN {0} MIN *******".format(self.interval * 3))
                time.sleep(self.interval * 3 * 60)
            except KeyboardInterrupt:
                self.logger.info("####### EXIT PROGRAM #######")
                errorFree = False
            except:
                self.logger.exception("******* EXCEPTION RAISED WHEN SCRAPING, EXIT PROGRAM *******")
                errorFree = False
