#!/usr/bin/env python3
import json
import argparse
import sys
import logging
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from trafilatura import fetch_url, extract

logging.getLogger("trafilatura").setLevel(logging.ERROR)


class DDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_result = False
        self.in_title = False
        self.current_title = ""
        self.current_url = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "result__url" in attrs_dict.get("class", ""):
            self.current_url = attrs_dict.get("href", "")
        if tag == "h2" and "result__title" in attrs_dict.get("class", ""):
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "h2" and self.in_title:
            self.in_title = False
            if self.current_url and self.current_title:
                # DDG prefixes urls with //duckduckgo.com/l/?uddg=
                url = self.current_url
                if "uddg=" in url:
                    url = urllib.parse.unquote(url.split("uddg=")[1].split("&")[0])

                if "duckduckgo.com/y.js" not in url and "/y.js" not in url:
                    self.results.append(
                        {"title": self.current_title.strip(), "href": url}
                    )

                self.current_title = ""
                self.current_url = ""

    def handle_data(self, data):
        if self.in_title:
            self.current_title += data


def search_ddg(query, max_results=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            parser = DDGParser()
            parser.feed(html)
            return parser.results[:max_results]
    except Exception as e:
        return []


def clean_extract(url):
    try:
        downloaded = fetch_url(url)
        if downloaded is None:
            return None
        result = extract(
            downloaded,
            include_links=True,
            include_images=False,
            output_format="markdown",
        )
        return result
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Pure Search: Zero-config search tool returning clean Markdown"
    )
    parser.add_argument("query", help="Search query string")
    parser.add_argument(
        "--max-results", type=int, default=3, help="Maximum number of results to fetch"
    )
    args = parser.parse_args()

    output = {"query": args.query, "results": [], "errors": []}

    try:
        results = search_ddg(args.query, max_results=args.max_results)
        if not results:
            output["errors"].append(
                "Failed to retrieve search results or no results found."
            )

        for result in results:
            url = result.get("href")
            title = result.get("title")

            if url:
                md_content = clean_extract(url)
                if md_content:
                    output["results"].append(
                        {"title": title, "url": url, "markdown_content": md_content}
                    )
                else:
                    output["errors"].append(f"Could not extract content from: {url}")
    except Exception as e:
        output["errors"].append(str(e))

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
