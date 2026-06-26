#!/usr/bin/env python3
"""
Wiki Publisher Script - Publish markdown content to Wiki.js via GraphQL API.

Usage:
  python3 publish_to_wiki.py publish <file.md> --path <wiki/path> [--title <title>] [--description <desc>] [--tags tag1,tag2]
  python3 publish_to_wiki.py list
"""

import argparse
import json
import os
import re
import sys

import requests


def get_wiki_config():
    """Get wiki configuration from environment variables."""
    wiki_key = os.environ.get("WIKI_KEY")
    wiki_url = os.environ.get("WIKI_URL")

    if not wiki_key:
        print("Error: WIKI_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    if not wiki_url:
        print("Error: WIKI_URL environment variable not set (e.g. https://your-wiki.example.com/graphql)", file=sys.stderr)
        sys.exit(1)

    return wiki_url, wiki_key


def clean_content(content: str) -> str:
    """Remove YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n.*?\n---\s*\n'
    return re.sub(pattern, '', content, flags=re.DOTALL).strip()


def extract_title(content: str, fallback: str) -> str:
    """Extract title from first H1 heading, or use fallback."""
    for line in content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return fallback


def _post(wiki_url: str, wiki_key: str, payload: str) -> dict:
    response = requests.post(
        wiki_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {wiki_key}"
        },
        data=payload
    )
    return response.json()


def create_page(wiki_url: str, wiki_key: str, content: str, title: str,
                path: str, description: str = "", tags: list = None) -> dict:
    """Create a new Wiki.js page using GraphQL Variables."""
    query = '''
    mutation CreatePage($content: String!, $title: String!,
                        $path: String!, $description: String!,
                        $tags: [String]!) {
      pages {
        create(
          content: $content
          title: $title
          path: $path
          description: $description
          tags: $tags
          editor: "markdown"
          isPublished: true
          isPrivate: false
          locale: "zh"
        ) {
          page {
            id
            path
            title
          }
        }
      }
    }
    '''
    variables = {
        "content": content,
        "title": title,
        "path": path,
        "description": description or title,
        "tags": tags or []
    }
    return _post(wiki_url, wiki_key, json.dumps({"query": query, "variables": variables}))


def update_page(wiki_url: str, wiki_key: str, page_id: int, content: str,
                title: str, description: str = "") -> dict:
    """Update an existing Wiki.js page using GraphQL Variables."""
    query = '''
    mutation UpdatePage($id: Int!, $content: String!, $title: String!, $description: String!) {
      pages {
        update(
          id: $id
          content: $content
          title: $title
          description: $description
          editor: "markdown"
        ) {
          page {
            id
            path
            title
          }
        }
      }
    }
    '''
    variables = {
        "id": page_id,
        "content": content,
        "title": title,
        "description": description
    }
    return _post(wiki_url, wiki_key, json.dumps({"query": query, "variables": variables}))


def get_page_by_path(wiki_url: str, wiki_key: str, path: str) -> dict:
    """Check if a page exists by path. Returns page dict or None."""
    query = '''
    query GetPage($path: String!) {
      pages {
        singleByPath(path: $path, locale: "zh") {
          id
          path
          title
        }
      }
    }
    '''
    result = _post(wiki_url, wiki_key, json.dumps({"query": query, "variables": {"path": path}}))
    try:
        return result["data"]["pages"]["singleByPath"]
    except (KeyError, TypeError):
        return None


def list_pages(wiki_url: str, wiki_key: str) -> dict:
    """List all wiki pages."""
    query = '''
    query {
      pages {
        list {
          id
          path
          title
          description
        }
      }
    }
    '''
    return _post(wiki_url, wiki_key, json.dumps({"query": query}))


def cmd_publish(args, wiki_url, wiki_key):
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    content = clean_content(raw_content)
    title = args.title or extract_title(content, os.path.basename(args.file))
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []

    existing_page = get_page_by_path(wiki_url, wiki_key, args.path)

    if existing_page:
        print(f"Page exists (ID: {existing_page['id']}), updating...")
        result = update_page(wiki_url, wiki_key, existing_page['id'], content, title, args.description or "")
        page = result.get("data", {}).get("pages", {}).get("update", {}).get("page")
        if page:
            print(f"✅ Updated: {wiki_url.replace('/graphql', '')}/{page['path']}")
        else:
            print(f"❌ Update failed: {result}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Creating new page at path: {args.path}")
        result = create_page(wiki_url, wiki_key, content, title, args.path, args.description or "", tags)
        page = result.get("data", {}).get("pages", {}).get("create", {}).get("page")
        if page:
            print(f"✅ Created: {wiki_url.replace('/graphql', '')}/{page['path']}")
        else:
            print(f"❌ Create failed: {result}", file=sys.stderr)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Publish markdown content to Wiki.js')
    subparsers = parser.add_subparsers(dest='action', required=True)

    pub = subparsers.add_parser('publish', help='Create or update a wiki page')
    pub.add_argument('file', help='Markdown file to publish')
    pub.add_argument('--path', '-p', required=True, help='Wiki page path (e.g. tech/security/guide)')
    pub.add_argument('--title', '-t', help='Page title (auto-extracted from H1 if not set)')
    pub.add_argument('--description', '-d', help='Page description')
    pub.add_argument('--tags', help='Comma-separated tags (e.g. "k8s,security")')

    subparsers.add_parser('list', help='List all wiki pages')

    args = parser.parse_args()
    wiki_url, wiki_key = get_wiki_config()

    if args.action == 'publish':
        cmd_publish(args, wiki_url, wiki_key)
    elif args.action == 'list':
        result = list_pages(wiki_url, wiki_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()