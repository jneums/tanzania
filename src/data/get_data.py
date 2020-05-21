#!/usr/bin/env python
'''Download data sets for the project'''

import logging
import argparse
import requests

def set_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    return logger

def main():
    s = requests.Session()
    data_path = '../../data/raw/'

    base_url = 'https://s3.amazonaws.com/drivendata-prod/data/7/public/'

    urls = { 'X_test_url': '702ddfc5-68cd-4d1d-a0de-f5f566f76d91.csv',
             'X_train_url': '4910797b-ee55-40a7-8668-10efd5c1b960.csv',
             'Y_train_url': '0bf8bc6e-30d0-4c50-956a-603fc693d966.csv' }

    
    for name, url in urls.items():
        file = s.get(base_url + url)
        if file.status_code == 200:
            with open(data_path + name[:-4] +'.csv', 'wb') as f_out:
                f_out.write(file.content)

if __name__ == "__main__":    
    logger = set_logging()

    main()