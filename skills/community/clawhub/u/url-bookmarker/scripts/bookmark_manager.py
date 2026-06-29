#!/usr/bin/env python3
"""Bookmark manager - add, list, search, tag, remove, export bookmarks."""

import json
import sys
import os
import re
from pathlib import Path

BOOKMARKS_FILE = Path(__file__).parent.parent / "assets" / "bookmarks.json"

def load():
    if BOOKMARKS_FILE.exists():
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"urls": [], "tags": [], "folders": []}

def save(data):
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cmd_add(url, title=None, tags=None, folder=None):
    data = load()
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    # Default title from hostname
    if not title:
        title = re.sub(r"https?://(www\.)?", "", url.split("/")[2] if "//" in url else url.split("/")[0])
    tags = tags or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    # Check duplicate
    for b in data["urls"]:
        if b["url"] == url:
            b["title"] = title
            if tags:
                b["tags"] = tags
            if folder:
                b["folder"] = folder
            save(data)
            print(f"Updated: {url}")
            return
    bookmark = {"url": url, "title": title, "tags": tags, "folder": folder, "added": "2026-05-15"}
    data["urls"].append(bookmark)
    for tag in tags:
        if tag not in data["tags"]:
            data["tags"].append(tag)
    if folder and folder not in data["folders"]:
        data["folders"].append(folder)
    save(data)
    print(f"Added: {title} ({url})")

def cmd_list(filter=None):
    data = load()
    urls = data["urls"]
    if filter:
        if filter.startswith("-t "):
            tag = filter[3:].strip()
            urls = [b for b in urls if tag in b.get("tags", [])]
        elif filter.startswith("-f "):
            folder = filter[3:].strip()
            urls = [b for b in urls if b.get("folder") == folder]
        elif filter == "-a":
            print(f"Tags: {', '.join(data['tags'])}")
            print(f"Folders: {', '.join(data['folders'])}")
            return
    if not urls:
        print("No bookmarks found.")
        return
    for i, b in enumerate(urls, 1):
        tags_str = f" [#{', #'.join(b['tags'])}]" if b["tags"] else ""
        folder_str = f" /{b['folder']}" if b.get("folder") else ""
        print(f"{i}. {b['title']} - {b['url']}{tags_str}{folder_str}")

def cmd_search(query):
    data = load()
    query = query.lower()
    results = [b for b in data["urls"]
               if query in b["url"].lower() or query in b["title"].lower()
               or any(query in t.lower() for t in b.get("tags", []))]
    if not results:
        print("No bookmarks match your search.")
        return
    for b in results:
        tags_str = f" [#{', #'.join(b['tags'])}]" if b["tags"] else ""
        print(f"- {b['title']} ({b['url']}){tags_str}")

def cmd_tag(url, tags):
    data = load()
    tags = [t.strip() for t in tags.split(",") if t.strip()]
    for b in data["urls"]:
        if b["url"] == url:
            b["tags"] = tags
            for tag in tags:
                if tag not in data["tags"]:
                    data["tags"].append(tag)
            save(data)
            print(f"Tagged {url}: {', '.join(tags)}")
            return
    print(f"Bookmark not found: {url}")

def cmd_remove(url):
    data = load()
    original = len(data["urls"])
    data["urls"] = [b for b in data["urls"] if b["url"] != url]
    if len(data["urls"]) < original:
        save(data)
        print(f"Removed: {url}")
    else:
        print(f"Bookmark not found: {url}")

def cmd_export(fmt="json"):
    data = load()
    if fmt == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif fmt == "html":
        lines = ["<html><body><ul>"]
        for b in data["urls"]:
            lines.append(f'<li><a href="{b["url"]}">{b["title"]}</a></li>')
        lines.append("</ul></body></html>")
        print("\n".join(lines))
    elif fmt == "csv":
        print("title,url,tags,folder,added")
        for b in data["urls"]:
            print(f'"{b["title"]}","{b["url"]}","{",".join(b["tags"])}","{b.get("folder","")}","{b["added"]}"')
    else:
        print(f"Unknown format: {fmt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: bookmark_manager.py <command> [args]")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "add":
        url = args[0] if args else ""
        title = None
        tags = None
        folder = None
        i = 1
        while i < len(args):
            if args[i] == "-t" and i+1 < len(args):
                tags = args[i+1]
                i += 2
            elif args[i] == "-f" and i+1 < len(args):
                folder = args[i+1]
                i += 2
            elif not title and not url.startswith("-"):
                title = args[i]
                i += 1
            else:
                i += 1
        cmd_add(url, title, tags, folder)
    elif cmd == "list":
        cmd_list(args[0] if args else None)
    elif cmd == "search":
        cmd_search(args[0] if args else "")
    elif cmd == "tag":
        cmd_tag(args[0] if args else "", args[1] if len(args) > 1 else "")
    elif cmd == "remove":
        cmd_remove(args[0] if args else "")
    elif cmd == "export":
        cmd_export(args[0] if args else "json")
    else:
        print(f"Unknown command: {cmd}")