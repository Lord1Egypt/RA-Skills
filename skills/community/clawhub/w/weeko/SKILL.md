---
name: weeko
description: Weeko CLI commands for bookmark management. Search, add, update, delete bookmarks. Create and organize groups. Batch operations.
metadata:
  author: occupy5
  homepage: https://weeko.blog
  version: "1.4.0"
---

# Weeko CLI Assistant

Expert guidance for interacting with the Weeko CLI - a Bun-powered, AI-native CLI for managing your Weeko bookmarks and groups.

## Overview

The Weeko CLI provides command-line access to your Weeko bookmark manager with AI-friendly output formats. All commands support:
- **Output formats**: `json` (default) or `toon` (AI-optimized via `--format toon`) or `pretty` (formatted tables)
- **Dry-run mode**: Test commands safely with `--dry-run`
- **Schema validation**: All API responses validated with Zod schemas

## Requirements & Installation

### Prerequisites
- **Bun runtime** (v1.0 or later) - [Install Bun](https://bun.sh)
- **Weeko account** - [Sign up](https://weeko.blog)

### Installation

**Install from npm** (recommended)
```bash
bun install -g weeko-cli
```

**Verify installation:**
```bash
weeko --version
```

## Quick Start

```bash
# Authentication
weeko login [api-key]         # Login with API key
weeko whoami                  # Show current user
weeko logout                  # Remove credentials

# Get context about the account
weeko status                  # Account overview (alias: context)
weeko tree                    # Show all groups (alias: structure)

# Search and manage bookmarks
weeko search "query"          # Search bookmarks
weeko add <url>               # Add new bookmark
weeko get <id>                # Get bookmark details
weeko update <id>             # Update bookmark
weeko delete <id>             # Delete bookmark
weeko list                    # List all bookmarks

# Manage groups
weeko group list              # List groups
weeko group create "Name"     # Create group
weeko group update <id>       # Update group
weeko group delete <id>       # Delete group

# Batch operations
weeko batch move --ids "1,2,3" --group <id>    # Move bookmarks
weeko batch delete --ids "1,2,3"               # Delete bookmarks
```

## Authentication & Setup

### Login
```bash
weeko login                   # Interactive prompt
weeko login "wk_xxx"          # Provide key directly
```

**Getting an API key:**
1. Visit https://weeko.blog/zh/dashboard
2. Generate a new API key
3. Copy the key (starts with `wk_`)

### Check Current User
```bash
weeko whoami                  # Returns user ID, name, email
```

### Account Overview
```bash
weeko status                  # High-level overview:
                              # - User details
                              # - Bookmark stats (total, links, colors, text, public)
                              # - Group count
                              # - Recent groups

weeko tree                    # All groups with IDs, names, and bookmark counts
```

## Working with Bookmarks

### List Bookmarks
```bash
weeko list                    # List all bookmarks
weeko list -g <groupId>       # Filter by group ID
weeko list --pretty           # Formatted table output
```

### Search Bookmarks
```bash
weeko search "query"          # Search by title, URL, or description
weeko search "javascript" --pretty    # Formatted results
```

Search is performed client-side across bookmark title, URL, and description fields.

### Get Bookmark Details
```bash
weeko get <id>                # Full bookmark details:
                              # - id, title, url, description
                              # - image, favicon, siteName
                              # - type (link/color/text)
                              # - color, isPublic, groupId
                              # - group info (id, name, color)
                              # - createdAt, updatedAt
```

### Add Bookmarks
```bash
weeko add "https://example.com"
weeko add "https://example.com" -t "My Title"
weeko add "https://example.com" -g <groupId>
weeko add "https://example.com" -t "Title" -g <groupId> -d "Description"
```

If no group is specified with `-g`, you'll be prompted to select one interactively.

**Options:**
- `-t, --title <title>`: Bookmark title (prompts if not provided)
- `-g, --group <id>`: Target group ID
- `-d, --description <desc>`: Description

### Update Bookmarks
```bash
weeko update <id> -t "New Title"
weeko update <id> -u "https://new-url.com"
weeko update <id> -g <newGroupId>
weeko update <id> -d "New description"
weeko update <id> -t "Title" -g <groupId> -d "Desc"
```

**Options:**
- `-t, --title <title>`: New title
- `-u, --url <url>`: New URL
- `-g, --group <id>`: Move to different group
- `-d, --description <desc>`: New description

All options are optional. Only provided fields will be updated.

### Delete Bookmarks
```bash
weeko delete <id>             # Deletes after confirmation
```

## Working with Groups

### List Groups
```bash
weeko group list              # All groups with IDs and counts
weeko group list --pretty     # Formatted table
```

### Get Group Details
```bash
weeko group get <id>          # Full group details:
                              # - id, name, color
                              # - isPublic, bookmarkCount
                              # - createdAt, updatedAt
```

### Create Groups
```bash
weeko group create "My Group"
weeko group create "Work" -c "#ef4444"
```

**Options:**
- `-c, --color <hex>`: Group color in hex format (default: `#3b82f6`)

### Update Groups
```bash
weeko group update <id> -n "New Name"
weeko group update <id> -c "#ec4899"
weeko group update <id> -n "Name" -c "#10b981"
```

**Options:**
- `-n, --name <name>`: New group name
- `-c, --color <hex>`: New hex color

### Delete Groups
```bash
weeko group delete <id>       # Deletes group AND all its bookmarks
```

**Warning:** Deleting a group permanently deletes all bookmarks within it.

## Batch Operations

### Batch Move
```bash
weeko batch move --ids "id1,id2,id3" --group <targetGroupId>
```

Move multiple bookmarks to a different group.

### Batch Delete
```bash
weeko batch delete --ids "id1,id2,id3"
```

Delete multiple bookmarks at once.

## Output Formats

### JSON (Default)
Standard JSON output:
```json
{
  "id": "clx...",
  "title": "Example",
  "url": "https://example.com"
}
```

### TOON (AI-Optimized)
Token-optimized format for AI agents via `--format toon`:
```
id\tclx...
title\tExample
url\thttps://example.com
```

### Pretty (Formatted Tables)
Human-readable formatted tables via `--pretty`:
```
┌────────────┬──────────────────────┬─────────────────────────────┐
│ ID         │ Title                │ URL                         │
├────────────┼──────────────────────┼─────────────────────────────┤
│ clx...     │ Example              │ https://example.com         │
└────────────┴──────────────────────┴─────────────────────────────┘
(1 bookmarks)
```

## Global Options

All commands support:

```bash
--dry-run                        # Log actions without making API calls
--format toon                    # Output as TOON instead of JSON
-v, --version                    # Show version
```

## Best Practices

1. **Start with context**: Run `weeko status` or `weeko tree` to understand the account structure
2. **Search before adding**: Use `weeko search` to avoid duplicates
3. **Use dry-run**: Test destructive operations with `--dry-run` first
4. **Use TOON format**: Use `--format toon` for AI-optimized token-efficient output
5. **Batch when possible**: Use `batch move` and `batch delete` for bulk operations

## Error Handling

The CLI provides helpful error messages with hints:

- **401 Unauthorized**: Run `weeko login` to authenticate
- **404 Not Found**: Verify the ID is correct
- **429 Rate Limited**: Wait a few minutes before retrying
- **500 Server Error**: The Weeko server is experiencing issues

All errors include:
- Error message
- HTTP status code
- Hint for resolution (when available)

## Examples

### Daily Workflow
```bash
# Check account status
weeko status

# See group structure
weeko tree

# Add a new bookmark
weeko add "https://example.com/article" -g <groupId> -t "Great Article"

# Search for existing bookmarks
weeko search "javascript" --pretty

# Move bookmarks between groups
weeko batch move --ids "id1,id2" --group <newGroupId>
```

### Clean Up Workflow
```bash
# Review all bookmarks
weeko list --pretty

# Search for specific items
weeko search "example.com"

# Delete unwanted bookmarks
weeko delete <id>

# Check group sizes before cleanup
weeko group list --pretty
```

### Content Curation
```bash
# Create a new group
weeko group create "AI Resources" -c "#8b5cf6"

# Add bookmarks to the new group
weeko add "https://arxiv.org" -g <newGroupId> -t "arXiv"
weeko add "https://paperswithcode.com" -g <newGroupId> -t "Papers With Code"

# List group contents
weeko list -g <newGroupId> --pretty
```

## Resources

See `references/commands.md` for detailed command reference, architecture info, and output format specifications.
