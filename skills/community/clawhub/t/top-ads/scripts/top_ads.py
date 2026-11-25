#!/usr/bin/env python3
"""Read Denote Top Ads using the key from the agent host's secret environment."""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGINS = {'production': 'https://denote.net', 'development': 'https://dev.denote.net'}
API_PATH = '/api/open/v1/skills/top-ads/'
KEY_ENV = 'DENOTE_API_KEY'


class NoRedirect(HTTPRedirectHandler):
    """Keep the credential on the explicitly selected Denote HTTPS origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def media_destination(value):
    """Keep API URLs intact, including signed queries, in Markdown destinations."""
    if not isinstance(value, str) or any(c.isspace() or c in '<>\\' or not c.isprintable() for c in value):
        return None
    try:
        url = urlsplit(value)
        if url.scheme in ('http', 'https') and url.hostname and url.username is None:
            return '<' + value + '>'
    except ValueError:
        pass
    return None


def creative_media(preview_url, video_url=None):
    preview = media_destination(preview_url)
    video = media_destination(video_url)
    if preview:
        return f'[![]({preview})]({video or preview})'
    return video


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--environment', choices=ORIGINS, default='production')
    commands = parser.add_subparsers(dest='command', required=True)
    rankings = commands.add_parser('rankings', help='Read the latest complete weekly charts')
    detail = commands.add_parser('detail', help='Read detail for one ranked creative')
    for command in (rankings, detail):
        command.add_argument('--app-type', choices=('game', 'app'), default='game')
        command.add_argument('--with-media', action='store_true',
                             help='Include embeddable creative media for the report')
    detail.add_argument('--chart', choices=('trending', 'rising', 'new'), required=True)
    detail.add_argument('--creative-key', required=True)
    detail.add_argument('--week-start', required=True)
    args = parser.parse_args(argv)

    key = os.environ.get(KEY_ENV, '').strip()
    if not key:
        print(f'Configure {KEY_ENV} in your agent host’s secret settings.', file=sys.stderr)
        return 1

    query = {'app_type': args.app_type}
    if args.command == 'detail':
        query.update(chart=args.chart, creative_key=args.creative_key, week_start=args.week_start)
    url = ORIGINS[args.environment] + API_PATH + args.command + '?' + urlencode(query)
    request = Request(url, headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json'})
    try:
        with build_opener(NoRedirect()).open(request, timeout=90) as response:
            data = json.load(response)
    except HTTPError as exc:
        # Decode user-facing structured errors from the service. Avoid printing a proxy error page.
        with exc:
            try:
                data = json.load(exc)
            except (ValueError, OSError):
                data = {'error': {'reason_code': 'HTTP_ERROR', 'http_status': exc.code}}
        print(json.dumps(data, ensure_ascii=False), file=sys.stderr)
        return 1
    except (URLError, OSError, ValueError):
        print('Could not read the Denote Top Ads API.', file=sys.stderr)
        return 1
    if args.with_media:
        result = data['data']
        if args.command == 'rankings':
            for chart in result['charts'].values():
                for item in chart['items']:
                    item['media_markdown'] = creative_media(item.get('preview_image_url'))
        else:
            creative = result.get('basic', {}).get('creative', {})
            result['media_markdown'] = creative_media(creative.get('preview_img_url'),
                                                     creative.get('video_url'))
    print(json.dumps(data, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
