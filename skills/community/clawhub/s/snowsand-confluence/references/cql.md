# Confluence Query Language (CQL) Reference

CQL is a SQL-like query language for searching Confluence content.

## Basic Syntax

```
field operator value [AND|OR field operator value]
```

## Fields

### Content Fields

| Field | Description | Example |
|-------|-------------|---------|
| `type` | Content type | `type=page` |
| `space` | Space key | `space=PROJ` |
| `title` | Page title | `title="Meeting Notes"` |
| `text` | Full-text content | `text ~ "api"` |
| `id` | Content ID | `id=12345678` |

### User Fields

| Field | Description | Example |
|-------|-------------|---------|
| `creator` | Created by user | `creator=currentUser()` |
| `contributor` | Edited by user | `contributor="john.doe"` |
| `mention` | Mentions user | `mention=currentUser()` |
| `watcher` | Watched by user | `watcher=currentUser()` |
| `favourite` | Favorited by user | `favourite=currentUser()` |

### Date Fields

| Field | Description | Example |
|-------|-------------|---------|
| `created` | Creation date | `created > "2024-01-01"` |
| `lastModified` | Last modified | `lastModified > now('-7d')` |

### Label Fields

| Field | Description | Example |
|-------|-------------|---------|
| `label` | Has label | `label=documentation` |

### Parent/Ancestor Fields

| Field | Description | Example |
|-------|-------------|---------|
| `parent` | Direct parent | `parent=12345678` |
| `ancestor` | Any ancestor | `ancestor=12345678` |

## Operators

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `type=page` |
| `!=` | Not equals | `type!=blogpost` |
| `>` | Greater than | `created > "2024-01-01"` |
| `>=` | Greater or equal | `lastModified >= "2024-01-01"` |
| `<` | Less than | `created < now()` |
| `<=` | Less or equal | `lastModified <= now()` |

### Text Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `~` | Contains (fuzzy) | `text ~ "keyword"` |
| `!~` | Does not contain | `text !~ "draft"` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `AND` | Both conditions | `type=page AND space=PROJ` |
| `OR` | Either condition | `label=api OR label=documentation` |
| `NOT` | Negation | `NOT label=archived` |

### List Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `IN` | In list | `space IN (PROJ, DOCS)` |
| `NOT IN` | Not in list | `label NOT IN (draft, wip)` |

## Content Types

| Type | Description |
|------|-------------|
| `page` | Wiki pages |
| `blogpost` | Blog posts |
| `attachment` | File attachments |
| `comment` | Comments |
| `space` | Spaces |

## Functions

### User Functions

| Function | Description |
|----------|-------------|
| `currentUser()` | Currently logged in user |

### Date Functions

| Function | Description | Example |
|----------|-------------|---------|
| `now()` | Current time | `lastModified > now()` |
| `now('offset')` | Time with offset | `now('-7d')` for 7 days ago |
| `startOfDay()` | Start of today | `created >= startOfDay()` |
| `startOfWeek()` | Start of this week | `created >= startOfWeek()` |
| `startOfMonth()` | Start of this month | `created >= startOfMonth()` |
| `startOfYear()` | Start of this year | `created >= startOfYear()` |
| `endOfDay()` | End of today | `created <= endOfDay()` |
| `endOfWeek()` | End of this week | |
| `endOfMonth()` | End of this month | |
| `endOfYear()` | End of this year | |

### Date Offset Format

```
now('±Nd') - Days
now('±Nw') - Weeks
now('±NM') - Months
now('±Ny') - Years
now('±Nh') - Hours
now('±Nm') - Minutes
```

Examples:
- `now('-7d')` - 7 days ago
- `now('-2w')` - 2 weeks ago
- `now('-1M')` - 1 month ago
- `now('+1d')` - 1 day in future

## Example Queries

### By Type

```cql
# All pages
type=page

# All blog posts
type=blogpost

# All attachments
type=attachment
```

### By Space

```cql
# Pages in specific space
type=page AND space=PROJ

# Pages in multiple spaces
type=page AND space IN (PROJ, DOCS, WIKI)

# Exclude space
type=page AND space != ARCHIVE
```

### Full-Text Search

```cql
# Search in content
text ~ "api documentation"

# Search in title
title ~ "meeting"

# Combined
title ~ "release" AND text ~ "features"
```

### By User

```cql
# My pages
type=page AND creator=currentUser()

# Pages I've edited
type=page AND contributor=currentUser()

# Pages mentioning me
type=page AND mention=currentUser()

# My favorites
type=page AND favourite=currentUser()
```

### By Date

```cql
# Created today
type=page AND created >= startOfDay()

# Modified this week
type=page AND lastModified >= startOfWeek()

# Modified in last 7 days
type=page AND lastModified > now('-7d')

# Created in 2024
type=page AND created >= "2024-01-01" AND created < "2025-01-01"

# Modified in last hour
type=page AND lastModified > now('-1h')
```

### By Label

```cql
# Has specific label
type=page AND label=documentation

# Has any of multiple labels
type=page AND (label=api OR label=sdk)

# Multiple labels (AND)
type=page AND label=api AND label=v2

# Exclude label
type=page AND NOT label=draft
```

### By Hierarchy

```cql
# Direct children of page
type=page AND parent=12345678

# All descendants of page
type=page AND ancestor=12345678
```

### Complex Queries

```cql
# Recent API documentation
type=page AND 
space=DOCS AND 
label=api AND 
lastModified > now('-30d')

# Meeting notes from this month
type=page AND 
title ~ "meeting" AND 
created >= startOfMonth() AND
space=TEAM

# Draft pages I created
type=page AND 
creator=currentUser() AND 
label=draft

# Active projects in multiple spaces
type=page AND 
space IN (PROJ1, PROJ2, PROJ3) AND 
label=active AND 
NOT label=archived AND
lastModified > now('-7d')
```

## Sorting

Note: Sorting is not directly supported in CQL. Results are sorted by relevance by default. Use the API's sort parameter instead:

```bash
# Via API parameter
confluence.py search "type=page" --sort "-modified"
```

## Tips

1. **Use quotes for values with spaces**: `title="My Page Title"`
2. **Use `~` for fuzzy/partial matching**: `text ~ "partial"`
3. **Combine conditions efficiently**: Put most restrictive first
4. **Test queries incrementally**: Start simple, add conditions
5. **Use IN for multiple values**: Cleaner than multiple OR
6. **Remember field names are case-sensitive**

## Common Patterns

### Find outdated content
```cql
type=page AND lastModified < now('-90d') AND NOT label=archived
```

### Find my recent work
```cql
type=page AND contributor=currentUser() AND lastModified > now('-7d')
```

### Find all documentation
```cql
type=page AND label IN (documentation, docs, guide, tutorial)
```

### Find empty/stub pages
```cql
type=page AND label=stub OR label=todo OR label=wip
```
