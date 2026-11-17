---
name: telegram-group-finder
description: Find Telegram groups/channels by topic using web search and fetch. Use when you need to locate Telegram communities for specific subjects (e.g., payment channels, niche interests).
---

# Telegram Group Finder

## Overview

This skill enables you to discover Telegram groups and channels related to a given topic by performing web searches, extracting relevant links, and presenting deduplicated results. It is useful for market research, community outreach, or finding niche discussion groups.

## Quick Start

1. Define your search topic (e.g., "支付通道 资源合群").
2. Use the web_search tool with a query in Chinese or English as appropriate.
3. For each promising result, use web_fetch to extract the page content.
4. Parse the content for Telegram usernames or t.me links.
5. Deduplicate and list the groups with brief descriptions.

## Search Groups

- Use web_search with query like "<topic> telegram 群" or "<topic> Telegram group".
- Limit results to 10 per search to avoid overload.
- Exclude irrelevant domains (e.g., known non-Telegram sites) if needed.

## Fetch Details

- For each search result URL, call web_fetch with extractMode="markdown" to get readable text.
- Look for patterns: @username, t.me/username, or phrases like "Telegram群", "Telegram group".
- Extract the username and a short description from surrounding text.

## Deduplicate Results

- Keep a set of seen usernames.
- If a username appears multiple times, merge descriptions or keep the most informative one.
- Output a numbered list: `@username – description`.

## Example Workflow

User: "帮我找关于支付通道相关的telegram群，要以中文为语言媒介的，找20个，不要重复的！"
Assistant: Perform web_search for "支付通道 telegram 群 中文", fetch results, extract usernames, deduplicate, and return list.

## Resources (optional)

### scripts/
You may add a helper script (e.g., deduplicate_groups.py) to automate deduplication and formatting.

### references/
Not required for this skill; but you could add a reference file with common Telegram-related patterns if desired.

### assets/
Not required.

---
**Not every skill requires all three types of resources.**