# Public Commons Media Search Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `public-commons-media-search`

x402 availability: not enabled for this product.

## `get_file`

Action slug: `get-file`

Price: `5` credits

Retrieve detailed file metadata and URLs (original, preferred, thumbnail) for a specific media file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_title` | `string` | yes | Full file title including the 'File:' prefix (e.g., 'File:Example.jpg'). |
| `language` | `string` | no | Language code (e.g., 'en'). Required when project is not 'commons'. |
| `project` | `string` | no | Wikimedia project. Set to 'commons' when the file is hosted on Wikimedia Commons. |

Sample parameters:

```json
{
  "file_title": "example file title",
  "language": "en",
  "project": "wikipedia"
}
```

Generated JSON parameter schema:

```json
{
  "file_title": {
    "description": "Full file title including the 'File:' prefix (e.g., 'File:Example.jpg').",
    "required": true,
    "type": "string"
  },
  "language": {
    "default": "en",
    "description": "Language code (e.g., 'en'). Required when project is not 'commons'.",
    "required": false,
    "type": "string"
  },
  "project": {
    "default": "wikipedia",
    "description": "Wikimedia project. Set to 'commons' when the file is hosted on Wikimedia Commons.",
    "required": false,
    "type": "string"
  }
}
```

## `list_page_media`

Action slug: `list-page-media`

Price: `5` credits

List all media files (images, audio, video) embedded on a specific Wikipedia page.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | `string` | no | Language code (e.g., 'en', 'fr', 'de'). |
| `project` | `string` | no | Wikimedia project (e.g., 'wikipedia'). Must not be 'commons' for this action. |
| `title` | `string` | yes | Canonical page title (e.g., 'Solar_eclipse', 'Golden_Gate_Bridge'). |

Sample parameters:

```json
{
  "language": "en",
  "project": "wikipedia",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "language": {
    "default": "en",
    "description": "Language code (e.g., 'en', 'fr', 'de').",
    "required": false,
    "type": "string"
  },
  "project": {
    "default": "wikipedia",
    "description": "Wikimedia project (e.g., 'wikipedia'). Must not be 'commons' for this action.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Canonical page title (e.g., 'Solar_eclipse', 'Golden_Gate_Bridge').",
    "required": true,
    "type": "string"
  }
}
```

## `search_commons_media`

Action slug: `search-commons-media`

Price: `5` credits

Search Wikimedia Commons directly for media files (images, audio, video, SVGs). Supports pagination for browsing large result sets.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum number of results to return. |
| `offset` | `integer` | no | Pagination offset. Use the next_offset value from a previous response to get the next page. |
| `q` | `string` | yes | Search query string. |

Sample parameters:

```json
{
  "limit": 50,
  "offset": 0,
  "q": "example q"
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 50,
    "description": "Maximum number of results to return.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "default": 0,
    "description": "Pagination offset. Use the next_offset value from a previous response to get the next page.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "q": {
    "description": "Search query string.",
    "required": true,
    "type": "string"
  }
}
```

## `search_titles`

Action slug: `search-titles`

Price: `5` credits

Search Wikipedia for article titles matching a query. Returns matching pages with title, description, and excerpt.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | `string` | no | Language code (e.g., 'en', 'fr', 'de'). |
| `limit` | `integer` | no | Maximum number of results to return. |
| `project` | `string` | no | Wikimedia project (e.g., 'wikipedia'). Must not be 'commons' for this action. |
| `q` | `string` | yes | Search query string. |

Sample parameters:

```json
{
  "language": "en",
  "limit": 50,
  "project": "wikipedia",
  "q": "example q"
}
```

Generated JSON parameter schema:

```json
{
  "language": {
    "default": "en",
    "description": "Language code (e.g., 'en', 'fr', 'de').",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 50,
    "description": "Maximum number of results to return.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "project": {
    "default": "wikipedia",
    "description": "Wikimedia project (e.g., 'wikipedia'). Must not be 'commons' for this action.",
    "required": false,
    "type": "string"
  },
  "q": {
    "description": "Search query string.",
    "required": true,
    "type": "string"
  }
}
```
