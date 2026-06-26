# Wiki.js GraphQL API Reference

## Authentication

All API requests require an Authorization header:

```
Authorization: Bearer <WIKI_KEY>
```

## Common Operations

### List Pages

```graphql
query {
  pages {
    list {
      id
      path
      title
      description
    }
  }
}
```

### Get Single Page

```graphql
query {
  pages {
    single(id: PAGE_ID) {
      id
      path
      title
      description
      content
      tags
    }
  }
}
```

### Create Page

```graphql
mutation {
  pages {
    create(
      content: "# Title\n\nContent..."
      description: "Description"
      editor: "markdown"
      isPublished: true
      isPrivate: false
      locale: "zh"
      path: "category/subcategory/page-name"
      tags: ["tag1", "tag2"]
      title: "Page Title"
    ) {
      page {
        id
        path
        title
      }
    }
  }
}
```

### Update Page

```graphql
mutation {
  pages {
    update(
      id: PAGE_ID
      content: "# Updated Title\n\nUpdated content..."
      description: "Updated description"
      editor: "markdown"
    ) {
      page {
        id
        path
        title
      }
    }
  }
}
```

### Delete Page

```graphql
mutation {
  pages {
    delete(id: PAGE_ID) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

## Python Example

Always use GraphQL Variables — never interpolate content strings directly into queries.

```python
import json
import os
import requests

WIKI_URL = os.environ["WIKI_URL"]   # e.g. https://your-wiki.example.com/graphql
WIKI_KEY = os.environ["WIKI_KEY"]

def create_page(title, content, path, description="", tags=None):
    query = '''
    mutation CreatePage($content: String!, $title: String!,
                        $path: String!, $description: String!,
                        $tags: [String]!) {
      pages {
        create(
          content: $content
          description: $description
          editor: "markdown"
          isPublished: true
          isPrivate: false
          locale: "zh"
          path: $path
          tags: $tags
          title: $title
        ) {
          page {
            id
            path
            title
          }
        }
      }
    }
    '''
    variables = {
        "content": content,
        "title": title,
        "path": path,
        "description": description,
        "tags": tags or []
    }
    response = requests.post(
        WIKI_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WIKI_KEY}"
        },
        data=json.dumps({"query": query, "variables": variables})
    )
    return response.json()
```

## Error Codes

| Error | Meaning |
|-------|---------|
| `Unauthorized` | Invalid or missing API key |
| `Forbidden` | Insufficient permissions |
| `ValidationError` | Invalid input data |
| `PageNotFound` | Page ID doesn't exist |

## Best Practices

1. Always check for existing pages before creating
2. Use consistent path naming (kebab-case)
3. Set appropriate tags for discoverability
4. Keep content under 100KB for performance
