logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': 'logs/ST.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 7
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO'
    }
}

scraper_settings = {
    'start_date': '2017-10-10',
    'end_date': '2017-11-30',
    'city': 'melbourne',
    'scraping_interval': 1,
    'do_email_alert': False,
    'do_check_time': True,
}

email_settings = {
    'domain': 'sandboxec965127a863426a8cfec6bd9f7de862.mailgun.org',
    'api_key': 'key-130feb495a9412b0ec6e08f1c3103d5f',
}

emails = ['xinbaDeveloper@gmail.com']