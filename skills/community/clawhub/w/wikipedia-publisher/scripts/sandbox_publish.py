#!/usr/bin/env python3
from __future__ import annotations
import argparse
import os
from pathlib import Path
import requests

API_DEFAULT = 'https://en.wikipedia.org/w/api.php'
UA = 'wikipedia-publisher/0.1 sandbox utility'


def read_text(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')


def get_login_token(session: requests.Session, api: str) -> str:
    r = session.get(api, params={'action':'query','meta':'tokens','type':'login','format':'json'}, timeout=30)
    r.raise_for_status()
    return r.json()['query']['tokens']['logintoken']


def login(session: requests.Session, api: str, username: str, password: str) -> dict:
    token = get_login_token(session, api)
    r = session.post(api, data={'action':'login','lgname':username,'lgpassword':password,'lgtoken':token,'format':'json'}, timeout=30)
    r.raise_for_status()
    return r.json()


def get_csrf(session: requests.Session, api: str) -> str:
    r = session.get(api, params={'action':'query','meta':'tokens','format':'json'}, timeout=30)
    r.raise_for_status()
    return r.json()['query']['tokens']['csrftoken']


def main():
    ap = argparse.ArgumentParser(description='Publish a local wiki draft to a user sandbox or Draft: page')
    ap.add_argument('--file', required=True, help='Path to local .wiki draft')
    ap.add_argument('--title', required=True, help='Target wiki page title')
    ap.add_argument('--summary', default='Save sourced draft for review', help='Edit summary')
    ap.add_argument('--api', default=API_DEFAULT, help='MediaWiki API endpoint')
    ap.add_argument('--username', default=os.getenv('WIKI_USERNAME'))
    ap.add_argument('--password', default=os.getenv('WIKI_PASSWORD'))
    ap.add_argument('--dry-run', action='store_true', help='Print target info without editing')
    args = ap.parse_args()

    text = read_text(args.file)
    if args.dry_run:
        print(f'title: {args.title}')
        print(f'summary: {args.summary}')
        print(f'chars: {len(text)}')
        print('mode: dry-run')
        return
    if not args.username or not args.password:
        raise SystemExit('Missing credentials. Use --username/--password or WIKI_USERNAME/WIKI_PASSWORD')

    s = requests.Session()
    s.headers.update({'User-Agent': UA})
    login_result = login(s, args.api, args.username, args.password)
    print(f'login_result: {login_result.get("login", {}).get("result")}')
    csrf = get_csrf(s, args.api)
    r = s.post(args.api, data={
        'action':'edit',
        'title':args.title,
        'text':text,
        'summary':args.summary,
        'format':'json',
        'token':csrf,
    }, timeout=30)
    r.raise_for_status()
    print(r.text)


if __name__ == '__main__':
    main()
