# Raindrop.io Search Query Syntax

The `search` query parameter on the `/raindrops/{collectionId}` endpoint accepts the same search syntax used in the Raindrop.io app. You can test searches in the app first, then copy the query string for API use.

Full help: https://help.raindrop.io/using-search

## Basic Search

| Syntax | Description | Example |
|--------|-------------|---------|
| `word1 word2` | Items containing these words (in title, description, domain, or page content) | `apple iphone` |
| `"exact phrase"` | Items containing the exact phrase | `"superman vs. batman"` |
| `-term` | Exclude results containing term | `-superman` |

## Tag Operators

| Syntax | Description | Example |
|--------|-------------|---------|
| `#tag` | Items with a specific tag | `#coffee` |
| `#"multi word"` | Items with a multi-word tag | `#"coffee beans"` |
| `-#tag` | Items without a specific tag | `-#coffee` |

## Boolean Logic

| Syntax | Description | Example |
|--------|-------------|---------|
| `word1 word2` | AND (default) - items containing all terms | `apple iphone` |
| `word1 word2 match:OR` | OR - items containing either term | `superman batman match:OR` |

## Field-Specific Search

| Syntax | Description | Example |
|--------|-------------|---------|
| `title:term` | Search in title only | `title:css` |
| `title:"phrase"` | Search exact phrase in title | `title:"css grid"` |
| `excerpt:term` | Search in description/excerpt | `excerpt:css` |
| `excerpt:"phrase"` | Exact phrase in description | `excerpt:"css grid"` |
| `note:term` | Search in notes | `note:css` |
| `note:"phrase"` | Exact phrase in notes | `note:"css grid"` |
| `link:term` | Search in URL | `link:drop` |
| `link:"phrase"` | Exact phrase in URL | `link:"crunch base"` |

## Date Filters

| Syntax | Description | Example |
|--------|-------------|---------|
| `created:YYYY-MM-DD` | Created on specific date | `created:2024-06-15` |
| `created:YYYY-MM` | Created in specific month | `created:2024-06` |
| `created:YYYY` | Created in specific year | `created:2024` |
| `created:>YYYY-MM-DD` | Created after date | `created:>2024-01-01` |
| `created:<YYYY-MM-DD` | Created before date | `created:<2024-07-01` |
| `lastUpdate:YYYY-MM-DD` | Last updated on date | `lastUpdate:2024-06-15` |

## Type Filters

| Syntax | Description |
|--------|-------------|
| `type:link` | Regular links |
| `type:article` | Articles |
| `type:image` | Images |
| `type:video` | Videos |
| `type:document` | Documents |
| `type:audio` | Audio files |

## Special Filters

| Syntax | Description |
|--------|-------------|
| `❤️` | Favourites (important items) |
| `file:true` | Items with file attachments |
| `notag:true` | Untagged items |
| `cache.status:ready` | Items with permanent copy saved |
| `-cache.status:ready` | Items without permanent copy |
| `reminder:true` | Items with reminders |
| `info:` | Prefix to disable full-text search |

## URL Encoding for curl

When using search queries with curl, URL-encode special characters:

```bash
# Search by tag
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=%23tagname"

# Search by exact phrase
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=%22exact%20phrase%22"

# Search by type
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=type%3Aarticle"

# Favourites
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=%E2%9D%A4%EF%B8%8F"

# Untagged items
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=notag%3Atrue"

# Created after a date
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=created%3A%3E2024-01-01"
```

## Common Encoding Reference

| Character | Encoded |
|-----------|---------|
| space | `%20` |
| `#` | `%23` |
| `"` | `%22` |
| `:` | `%3A` |
| `<` | `%3C` |
| `>` | `%3E` |
| `❤️` | `%E2%9D%A4%EF%B8%8F` |

## Combined Search Examples

### Articles tagged "design" created this year

```bash
search="type%3Aarticle%20%23design%20created%3A2024"
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=$search"
```

### Untagged items in a specific collection

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/COLLECTION_ID?search=notag%3Atrue"
```

### Bookmarks matching either term

```bash
search="react%20vue%20match%3AOR"
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=$search"
```
