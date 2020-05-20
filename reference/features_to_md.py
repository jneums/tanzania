#!/usr/bin/env python
'''Read in features from txt file and write formatted MD'''

import logging
import argparse

def get_options():
    description = ''
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('fname',
                        help='File Name')

    return parser.parse_args()


def set_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    return logger

def main(options):
    md = '# Feature Definitions:\n'
    with open(options.fname + '.txt', 'r') as f_in:
        lines = f_in.readlines()
        for line in lines:
            line = '- **{}**: {}\n'.format(line.split('-')[0].strip(), line.split('-')[1])
            md += line
        with open(options.fname + '.md', 'w') as f_out:
            f_out.write(md)

if __name__ == "__main__":
    options = get_options()
    
    logger = set_logging()

    main(options)