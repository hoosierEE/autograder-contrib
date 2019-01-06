#! /usr/bin/env python3

import argparse
import os
import requests
from urllib.parse import urljoin

import utils


def main():
    args = parse_args()

    api_token = None
    try:
        api_token = utils.get_api_token(args.token_file)
    except utils.TokenFileNotFound as e:
        print(e)
        exit(1)

    response = requests.post(
        urljoin(args.base_url, f'/api/courses/{args.course_pk}/copy/'),
        data={
            'new_name': args.new_course_name,
            'new_semester': args.new_course_semester,
            'new_year': args.new_course_year
        },
        headers={'Authorization': f'Token {api_token}'}
    )

    print(response.json())
    response.raise_for_status()
    print('New course created successfully')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('course_pk', type=int)
    parser.add_argument('new_course_name')
    parser.add_argument('new_course_semester',
                        choices=['Winter', 'Spring', 'Summer', 'Fall'])
    parser.add_argument('new_course_year', type=int)

    parser.add_argument('--base_url', '-u', type=str,
                        default='https://autograder.io/')
    parser.add_argument(
        '--token_file', '-t', type=str, default='.agtoken',
        help="A filename or a path describing where to find the API token. "
             "If a filename, searches the current directory and each "
             "directory up to and including the current user's home "
             "directory until the file is found.")

    return parser.parse_args()


if __name__ == '__main__':
    main()