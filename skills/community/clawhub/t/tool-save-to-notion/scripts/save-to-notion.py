#!/usr/bin/env python3
"""
Save tool information to Notion Toolbox database.
Usage: python save-to-notion.py --url "https://example.com" --name "Tool Name" --type "网站" --tags "AI,效率" --description "Tool description"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser

NOTION_API_KEY = os.environ.get('NOTION_API_KEY', '')
DATABASE_ID = '6f7bb9cc-ac01-41c5-9856-fb1568d197ae'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

# Valid types (exactly 5 options)
VALID_TYPES = {'软件', '网站', '浏览器插件', 'Prompt', '工具包'}
NOTION_VERSION = '2025-09-03'


class MetaParser(HTMLParser):
    """Parse meta tags from HTML to extract og:image and twitter:image."""

    def __init__(self):
        super().__init__()
        self.og_image = None
        self.twitter_image = None
        self.title = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'meta':
            # Open Graph Image
            if attrs_dict.get('property') == 'og:image':
                self.og_image = attrs_dict.get('content', '')
            # Twitter Card Image
            if attrs_dict.get('name') == 'twitter:image':
                self.twitter_image = attrs_dict.get('content', '')
        elif tag == 'title':
            pass  # Title content comes in handle_data

    def handle_data(self, data):
        if self.lasttag == 'title' and not self.title:
            self.title = data.strip()


def extract_cover_image(url):
    """Extract cover image URL from web page.

    Priority:
    1. og:image (Open Graph)
    2. twitter:image (Twitter Card)
    3. GitHub special handling (opengraph.githubassets.com)
    4. Common favicon/apple-touch-icon as fallback

    Returns None if no suitable image found.
    """

    try:
        # Fetch page HTML
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; NotionTool/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

        # Parse meta tags
        parser = MetaParser()
        parser.feed(html)

        # Priority 1 & 2: og:image or twitter:image
        cover_url = parser.og_image or parser.twitter_image

        if cover_url:
            # Convert relative URL to absolute
            if cover_url.startswith('/'):
                from urllib.parse import urlparse
                parsed = urlparse(url)
                cover_url = f'{parsed.scheme}://{parsed.netloc}{cover_url}'
            elif cover_url.startswith('//'):
                cover_url = f'https:{cover_url}'

            return cover_url

        # Priority 3: GitHub special handling
        if 'github.com' in url:
            match = re.search(r'github\.com/([^/]+/[^/]+)', url)
            if match:
                repo_path = match.group(1)
                # Use GitHub's default Open Graph image
                return f'https://opengraph.githubassets.com/1/{repo_path}'

    except Exception as e:
        # Silently fail, cover is optional
        pass

    return None


def save_to_notion(name, tool_type, tags, url, description, starred=False, cover_image_url=None):
    """Save tool info to Notion database."""

    if not NOTION_API_KEY:
        return {'success': False, 'error': 'NOTION_API_KEY environment variable not set'}

    # Validate type
    if tool_type not in VALID_TYPES:
        return {'success': False, 'error': f'Invalid type. Must be one of: {", ".join(VALID_TYPES)}'}

    # Build properties
    properties = {
        'Name': {
            'title': [{'text': {'content': name}}]
        },
        'URL': {
            'url': url
        }
    }

    # Add type (类型) - single select
    properties['类型'] = {
        'multi_select': [{'name': tool_type}]
    }

    # Add tags (标签)
    if tags:
        properties['标签'] = {
            'multi_select': [{'name': t.strip()} for t in tags]
        }

    # Add description (简介)
    if description:
        properties['简介'] = {
            'rich_text': [{'text': {'content': description}}]
        }

    # Add starred (⭐ 置顶)
    properties['⭐ 置顶'] = {'checkbox': starred}

    # Build request
    data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': properties
    }

    # Add cover image and children blocks if available
    if cover_image_url:
        data['cover'] = {
            'type': 'external',
            'external': {
                'url': cover_image_url
            }
        }
        # Add image block to page content (children only works at creation time)
        data['children'] = [
            {
                'object': 'block',
                'type': 'image',
                'image': {
                    'type': 'external',
                    'external': {'url': cover_image_url}
                }
            }
        ]

    try:
        req = urllib.request.Request(
            NOTION_API_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {NOTION_API_KEY}',
                'Notion-Version': NOTION_VERSION,
                'Content-Type': 'application/json'
            },
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                'success': True,
                'id': result.get('id'),
                'url': result.get('url'),
                'properties': result.get('properties')
            }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {'success': False, 'error': f'HTTP {e.code}: {error_body}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Save tool to Notion Toolbox')
    parser.add_argument('--url', required=True, help='Tool URL')
    parser.add_argument('--name', required=True, help='Tool name')
    parser.add_argument('--type', required=True, choices=list(VALID_TYPES), help='Tool type (single select)')
    parser.add_argument('--tags', nargs='+', default=[], help='Tags')
    parser.add_argument('--description', default='', help='Description')
    parser.add_argument('--starred', action='store_true', help='Starred')
    parser.add_argument('--cover', default=None, help='Cover image URL (optional, will auto-extract if not provided)')

    args = parser.parse_args()

    # Auto-extract cover image if not provided
    cover_image_url = args.cover
    if not cover_image_url:
        cover_image_url = extract_cover_image(args.url)

    result = save_to_notion(
        name=args.name,
        tool_type=args.type,
        tags=args.tags,
        url=args.url,
        description=args.description,
        starred=args.starred,
        cover_image_url=cover_image_url
    )

    if result['success']:
        output = {
            'success': True,
            'url': result['url'],
            'id': result['id'],
            'has_cover': cover_image_url is not None,
            'has_cover_in_content': cover_image_url is not None  # Cover is added to content via children parameter
        }
        print(json.dumps(output))
        sys.exit(0)
    else:
        print(json.dumps({'success': False, 'error': result['error']}))
        sys.exit(1)


if __name__ == '__main__':
    main()
