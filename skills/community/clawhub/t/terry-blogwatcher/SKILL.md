---
name: blogwatcher
description: Monitor blogs and RSS feeds
version: 1.0.0
author: ClawdBot
tags: [rss, blogs]
requires_bins: []
requires_env: []
requires_config: []
feishu_acl:
  sensitivity: internal
  access:
    owner: full_access
    team_editors: edit
    team_viewers: view
    external: none
  review_cadence: 90d
---

# Blog Watcher

Monitor blogs and RSS feeds

## Available Tools

This skill uses ClawdBot's standard tools:
- **bash** - Execute commands
- **read_file** - Read files
- **write_file** - Write files  
- **web_fetch** - Fetch web content
- **web_search** - Search the web

## Usage Examples

User: "Help me with blog watcher"
1. Assess what the user needs
2. Use appropriate tools
3. Provide helpful response

## Configuration

Check documentation for specific setup requirements.

## Notes

This skill requires integration with Blog Watcher service/application.
