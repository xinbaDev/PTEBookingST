import logging
from abc import ABCMeta, abstractmethod

import requests
from settings import email_settings, emails


class Emailer(metaclass=ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        FORMAT_ERROR = "emailer_settings format is invalid, please refers to project doc"

        try:
            self.domain = email_settings["domain"]
            self.api_key = email_settings["api_key"]

        except:
            raise ValueError(FORMAT_ERROR)

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def email_list(self):
        pass

    @abstractmethod
    def format_data(self, data):
        return ''

    def send(self, data):
        text_string = self.format_data(data)
        self.logger.warning("Request Body:\n" + text_string)

        self.logger.warning("####### SENDING EMAIL ALERT #######")
        response = requests.post(
            "https://api.mailgun.net/v3/{0}/messages".format(self.domain),
            auth=("api", self.api_key),
            data={"from": "PTEBookingST <mailgun@{0}>".format(self.domain),
                  "to": self.email_list,
                  "subject": self.title + text_string,
                  "text": text_string})
        self.logger.warning(response.text)


class SeatAlertEmailer(Emailer):
    @property
    def title(self):
        return "New Seat Alert: "

    @property
    def email_list(self):
        return emails

    def format_data(self, centre_datetimes_dict):
        text_string = ""
        for centre in centre_datetimes_dict:
            date_times_dict = centre_datetimes_dict[centre]
            centre_string = "{0}:\n".format(centre)
            for date in date_times_dict:
                centre_string += "{0}:  ".format(date)
                for time in date_times_dict[date]:
                    centre_string += (str(time) + ', ')
                centre_string = centre_string[:-2] + '\n'
            text_string += centre_string + "\n"

        return text_string