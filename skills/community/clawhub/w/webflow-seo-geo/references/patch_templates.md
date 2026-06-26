# Patch templates (JSON)

## Create item
{
  "fieldData": {
    "name": "...",
    "slug": "...",
    "contenu-de-l-article": "<p>...</p>",
    "seo---meta-description": "...",
    "image-de-couverture": {"fileId":"...","url":"...","alt":"..."},
    "image---alt-text": "...",
    "date-de-redaction": "2026-03-09T00:00:00.000Z",
    "categorie": "..."
  }
}

## Patch item
{
  "fieldData": {
    "name": "...",
    "seo---meta-description": "...",
    "image-de-couverture": {"fileId":"...","url":"...","alt":"..."},
    "image---alt-text": "..."
  }
}

## Publish
{"itemIds": ["..."]}
