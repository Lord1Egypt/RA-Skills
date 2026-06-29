# WeChat Channels Content Search / wechat-channels-search

---

## Overview

Enter a keyword to search for trending content on WeChat Channels (视频号), presented in a structured table with likes, author, duration, and publish time—helping you quickly understand how different content categories are performing on the platform.

**Core Value**

- **Instant search**: Enter any content keyword and immediately receive a list of popular works.
- **Comprehensive data**: Each result shows the title, likes, author, duration, and publish time at a glance.
- **Continuous tracking**: Subscribe to keywords of interest and receive daily push notifications at 9:00 AM with the latest data—never miss an update.

**Intended Users**

- 📝 **Content creators** — Track trending content in your niche for data-driven topic and creative inspiration.
- 🏢 **MCN / brand operators** — Quickly gauge the popularity and top-performing content for a specific category on WeChat Channels.
- 📊 **Marketing teams** — Gain keyword-based content trend insights to inform strategy and campaign decisions.

---

## Features

### Core Capabilities

- **Keyword Search**: Search trending WeChat Channels content by keyword—precisely discover quality content.
- **Sort Options**: Default sort by popularity; optionally sort by latest publish time to suit different needs.
- **Pagination**: Browse results page by page—never miss a work when exploring broader results.
- **Subscription Push**: Subscribe to keywords for daily automated updates at 9:00 AM with the latest works.

### Highlights

- **One-click subscription**: No extra steps—search, subscribe, and receive daily push notifications to stay on top of trends.
- **Clean data output**: Search results displayed directly as a table—title, likes, author, duration, and publish time all at a glance.

> 🔔 Due to WeChat Channels platform restrictions, direct work links are unavailable. Copy the work title to search within WeChat Channels.

---

## API Key Acquisition & Security

- This skill requires the environment variable: `REDFOX_API_KEY`.
- `REDFOX_API_KEY` is issued by [RedFoxHub](https://redfox.hk/settings/api-keys?source=clawhub) (`https://redfox.hk`).
- Register at [RedFoxHub](https://redfox.hk?source=github) to obtain `REDFOX_API_KEY`.
- Configure `REDFOX_API_KEY` on your device before using this skill.
- Before providing your key, confirm its source, scope, validity period, and whether it can be reset or revoked.
- Do not hard-code or expose keys in plain text in code, prompts, logs, or output files.

---

## Usage Guide

Simply describe the content category you want to explore in natural language—no fixed commands to memorize.

### Quick Reference

| Intent | Example | Result |
| ------ | ------- | ------ |
| Search by keyword | "Search Luckin Coffee" | Search results sorted by popularity |
| Sort by latest | "Show me the latest 占豪" | Results sorted by publish time |
| Browse pages | "Next page" | View more search results |
| Subscribe to daily updates | Reply "Confirm subscription" after a search | Daily push at 9:00 AM with the latest works for that keyword |

### Output Example

After a search, you'll see a table like this:

> 📊 Keyword "**Luckin Coffee**" search results:

| # | Title | Likes | Author | Duration | Publish Time |
|---|-------|-------|--------|----------|--------------|
| 1 | Luckin Coffee new launch: Flamenco popping iced tea... | 1189 | 新之助1- | 00:46 | 06-15 16:18 |
| 2 | Ronaldo fans choose Luckin, Messi fans pick Cotti!... | 20 | 大象财富 | 04:21 | 06-24 21:00 |

> 🔔 Due to WeChat Channels platform restrictions, direct work links are unavailable. Copy the work title to search within WeChat Channels.

> 📄 More results available. Reply "Next page" to continue.

---

## Use Cases

| Scenario | Role | Example | Benefit |
| -------- | ---- | ------- | ------- |
| Topic research | Content creator | "What food content is trending lately?" | Quickly pinpoint high-engagement directions |
| Brand monitoring | Brand operator | "Check how Luckin Coffee is performing on WeChat Channels" | Understand brand-related content heat and user feedback |
| Trend tracking | Marketing team | "How is beauty content performing on WeChat Channels?" | Judge niche heat by data, adjust strategy in time |
| Daily monitoring | Individual user | "Send me daily updates on 占豪's latest works" | Subscribe once—receive automatic updates every 9:00 AM |
