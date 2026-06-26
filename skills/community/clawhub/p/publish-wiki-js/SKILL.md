---
name: wiki-publisher
description: Publish markdown content to Wiki.js with proper formatting and metadata. Use when user wants to create or update wiki pages, convert notes/articles to wiki format, or publish content to a Wiki.js instance. Handles API authentication, content formatting (removing YAML frontmatter), automatic tagging, and path suggestions.
metadata: {"env": [{"name": "WIKI_KEY", "description": "Wiki.js API token (generate in Admin > API Access)", "required": true, "credential": true}, {"name": "WIKI_URL", "description": "Wiki.js GraphQL endpoint, e.g. https://your-wiki.example.com/graphql", "required": true}], "primaryCredential": "WIKI_KEY", "runtime": {"python": {"deps": ["requests"]}}}
---

# Wiki Publisher

Publish markdown content to Wiki.js with proper formatting and metadata handling.

## When to Use

Use this skill when:
- User wants to publish content to their Wiki.js instance
- Converting articles, notes, or analysis to wiki format
- Creating new wiki pages with proper structure
- Updating existing wiki pages
- Need to handle Wiki.js GraphQL API operations

## Prerequisites

- `WIKI_KEY` environment variable must be set (Wiki.js API key)
- Wiki.js instance URL must be accessible
- User must have write permissions to the target wiki

## Content Formatting Rules

### Remove YAML Frontmatter

**CRITICAL:** Wiki.js stores title/description in API parameters, NOT in content.

❌ **Don't include in content:**
```markdown
---
title: Page Title
description: Page description
---

# Page Title
```

✅ **Correct format:**
```markdown
# Page Title

Content starts here...
```

### Heading Structure

- Always start with H1 (`# Title`)
- Use proper hierarchy (H1 → H2 → H3)
- Don't skip levels

### Links

- Use markdown format: `[text](url)`
- Prefer relative links for internal wiki pages
- External links should use full URL

## API Usage

### ⚠️ CRITICAL: GraphQL String Handling

**The #1 cause of failures is incorrect string escaping.**

#### ❌ WRONG - Direct String Interpolation

```python
# DON'T DO THIS - will fail with complex content
query = f'''
mutation {{
  pages {{
    create(content: "{content}") {{  # Content with quotes/newlines will break
      page {{ id }}
    }}
  }}
}}
'''
```

**Why it fails:**
- Markdown contains `"` (quotes) that terminate the GraphQL string
- Newlines in content break the query syntax
- Backslashes in code blocks escape incorrectly
- JSON serialization double-escapes

#### ✅ CORRECT - Use GraphQL Variables (RECOMMENDED)

```python
import json
import requests

query = '''
mutation CreatePage($content: String!, $title: String!, $path: String!) {
  pages {
    create(
      content: $content
      title: $title
      path: $path
      editor: "markdown"
      isPublished: true
      isPrivate: false
      locale: "zh"
    ) {
      page {
        id
        path
        title
      }
      responseResult {
        succeeded
        errorCode
        message
      }
    }
  }
}
'''

variables = {
    "content": raw_content,  # Pass raw content, no preprocessing
    "title": "Page Title",
    "path": "category/page-name",
    "tags": []  # Required - can be empty list
}

# Let json.dumps handle all escaping automatically
payload = json.dumps({
    "query": query,
    "variables": variables
})

response = requests.post(
    WIKI_URL,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WIKI_KEY}"
    },
    data=payload
)
```

**Why this works:**
- `json.dumps()` properly escapes all special characters
- GraphQL Variables separate data from query structure
- Handles quotes, newlines, backslashes, Unicode automatically

#### ✅ ALTERNATIVE - Use Block String (Triple Quotes)

For simple updates when Variables cause issues:

```python
# Replace any """ in content first
safe_content = content.replace('"""', '\x00TRIPLE\x00')

mutation = f'''
mutation {{
  pages {{
    update(
      id: {page_id}
      content: """{safe_content}"""
      description: "Updated description"
      editor: "markdown"
      tags: []
    ) {{
      page {{ id path title }}
      responseResult {{ succeeded errorCode message }}
    }}
  }}
}}
'''
```

### Create Page

```graphql
mutation CreatePage($content: String!, $title: String!, $path: String!, $description: String!, $tags: [String]!) {
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
      responseResult {
        succeeded
        errorCode
        message
      }
    }
  }
}
```

**Variables:**
```json
{
  "content": "# Title\n\nContent...",
  "title": "Page Title",
  "path": "topic/category/page-name",
  "description": "Page description",
  "tags": ["tag1", "tag2"]
}
```

**Important:** `tags` must be provided even if empty (`[]`). Some Wiki.js versions require this field.

**Type Requirements:**
- `$content`: `String!` - Required, raw markdown
- `$title`: `String!` - Required
- `$path`: `String!` - Required, URL path
- `$description`: `String!` - **Required** (can be empty string)
- `$tags`: `[String]!` - **Required** array of strings (can be empty `[]`)

### Update Page

**Two-step process:**
1. Query page ID by path
2. Update page using ID

#### Step 1: Query Page ID

```graphql
query GetPage($path: String!) {
  pages {
    single(path: $path) {
      id
      title
      path
      description
      content
    }
  }
}
```

**Variables:**
```json
{"path": "tech/api/rpc"}
```

Or query all pages to find by path:

```graphql
query {
  pages {
    list {
      id
      path
      title
    }
  }
}
```

#### Step 2: Update Page

```graphql
mutation UpdatePage($id: Int!, $content: String!, $description: String!) {
  pages {
    update(
      id: $id
      content: $content
      description: $description
      editor: "markdown"
      tags: []
    ) {
      page {
        id
        path
        title
      }
      responseResult {
        succeeded
        errorCode
        message
      }
    }
  }
}
```

**⚠️ CRITICAL for Update:**
- `tags` is **REQUIRED** even if empty `[]`
- `description` is **REQUIRED** even if empty string `""`
- Missing either will cause: `Cannot read properties of undefined (reading 'map')`

**Variables:**
```json
{
  "id": 25,
  "content": "# Updated Content\n\n...",
  "description": "Updated description"
}
```

## GraphQL String Type Reference

### String Representation

GraphQL supports two string formats:

#### 1. Single-line Strings (Double Quote)
```graphql
description: "Single line text"
```

**Escape sequences required:**
| Character | Escape | Example |
|-----------|--------|---------|
| `"` | `\"` | `"Say \"hello\""` |
| `\` | `\\` | `"C:\\path"` |
| Newline | `\n` | `"Line1\nLine2"` |
| Tab | `\t` | `"Col1\tCol2"` |

#### 2. Block Strings (Triple Quote)
```graphql
content: """
Multi-line
content here
"""
```

**Notes:**
- Preserves newlines
- Must escape `"""` within content
- Leading whitespace is normalized based on first line

### Common Escape Pitfalls

#### Pitfall 1: Markdown Code Blocks

Markdown contains triple backticks that conflict:
```markdown
```python
def hello():
    pass
```
```

When inserted into GraphQL block string:
```graphql
content: """
```python  # ❌ Conflicts with GraphQL """
def hello()
```
"""
```

**Solution:** Use GraphQL Variables (recommended) or escape each `` ` `` as `\`.

#### Pitfall 2: JSON Double-Escaping

```python
# ❌ WRONG - manual escape then JSON serialize
content_escaped = content.replace('"', '\\"')
payload = json.dumps({"query": f'..."{content_escaped}"...'})
# Results in: \" (double escaped)

# ✅ CORRECT - pass raw content to variables
payload = json.dumps({
    "query": "mutation($c: String!) { create(content: $c) }",
    "variables": {"c": raw_content}
})
```

#### Pitfall 3: Unicode Characters

GraphQL Strings are UTF-8 encoded. Ensure:
- Source file is UTF-8
- HTTP request specifies `Content-Type: application/json; charset=utf-8`
- No BOM (Byte Order Mark) at file start

## Path Conventions

Suggest paths based on content type:

| Content Type | Suggested Path |
|--------------|----------------|
| Technical docs | `tech/{category}/{topic}` |
| Thinking models | `topic/thinking-models/{name}` |
| Financial concepts | `financial/{category}/{name}` |
| Personal notes | `notes/{category}/{name}` |
| Project docs | `projects/{name}/{doc}` |

## Workflow

### For New Pages:
1. **Extract content** - Get markdown from user or generate it
2. **Clean formatting** - Remove YAML frontmatter if present
3. **Suggest metadata** - Propose path, tags, description
4. **Confirm with user** - Show proposed wiki location
5. **Create** - Execute `pages.create` mutation with **all required fields**
6. **Return link** - Provide wiki page URL

### For Existing Pages:
1. **Query page ID** - Use `pages.single(path: "...")` or `pages.list`
2. **Get current content** (optional) - For comparison
3. **Update** - Execute `pages.update` mutation with **id + all required fields**
4. **Verify** - Check response for success
5. **Return link** - Provide wiki page URL

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ValidationError: Variable $content... invalid value` | String escaping issue | Use Variables + json.dumps |
| `Field "create" argument "tags" of type "[String]!" is required` | Missing required tags parameter | Always provide `tags: []` even if empty |
| `GraphQLError: Variable $tags of type [String]` | Tags type mismatch | Use `[String]!` in mutation signature |
| `Cannot read properties of undefined (reading 'map')` | Missing `tags` or `description` in update | Add `tags: []` and `description: "..."` |
| `Unauthorized` | Invalid API key | Check WIKI_KEY env var |
| `Page already exists` | Path conflict | Use update mutation or different path |

### Debugging Failed Requests

Always check both `errors` array and `responseResult`:

```python
result = response.json()

# Check GraphQL-level errors
if 'errors' in result:
    for err in result['errors']:
        print(f"GraphQL Error: {err.get('message')}")

# Check Wiki.js response result
resp_result = result.get('data', {}).get('pages', {}).get('create', {}).get('responseResult', {})
if not resp_result.get('succeeded'):
    print(f"Wiki.js Error {resp_result.get('errorCode')}: {resp_result.get('message')}")
```

## Example: Create Page (Complete)

```python
import os
import json
import urllib.request

WIKI_URL = os.environ.get("WIKI_URL")  # e.g. https://your-wiki.example.com/graphql
WIKI_KEY = os.environ.get("WIKI_KEY")

def create_wiki_page(content: str, title: str, path: str, 
                     description: str = "", tags: list = None) -> dict:
    """
    Create a Wiki.js page using GraphQL API.
    """
    query = '''
    mutation CreatePage($content: String!, $title: String!, 
                       $path: String!, $description: String!, 
                       $tags: [String]!) {
      pages {
        create(
          content: $content
          title: $title
          path: $path
          description: $description
          tags: $tags
          editor: "markdown"
          isPublished: true
          isPrivate: false
          locale: "zh"
        ) {
          page {
            id
            path
            title
          }
          responseResult {
            succeeded
            errorCode
            message
          }
        }
      }
    }
    '''
    
    variables = {
        "content": content,
        "title": title,
        "path": path,
        "description": description or title,
        "tags": tags if tags is not None else []
    }
    
    payload = json.dumps({
        "query": query,
        "variables": variables
    }).encode('utf-8')
    
    req = urllib.request.Request(
        WIKI_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WIKI_KEY}"
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

# Usage
with open('article.md', 'r', encoding='utf-8') as f:
    content = f.read()

result = create_wiki_page(
    content=content,
    title="软件反模式（Anti-Patterns）",
    path="tech/patterns/anti_patterns",
    description="软件工程中常见反模式的识别与规避指南",
    tags=["软件设计", "反模式", "最佳实践"]
)
```

## Example: Update Page (Complete)

```python
import os
import json
import urllib.request

WIKI_URL = os.environ.get("WIKI_URL")  # e.g. https://your-wiki.example.com/graphql
WIKI_KEY = os.environ.get("WIKI_KEY")

def update_wiki_page(page_id: int, content: str, description: str = "") -> dict:
    """
    Update a Wiki.js page using GraphQL API.
    
    ⚠️ IMPORTANT: tags and description are REQUIRED even if empty!
    """
    query = '''
    mutation UpdatePage($id: Int!, $content: String!, $description: String!) {
      pages {
        update(
          id: $id
          content: $content
          description: $description
          editor: "markdown"
          tags: []
        ) {
          page {
            id
            path
            title
          }
          responseResult {
            succeeded
            errorCode
            message
          }
        }
      }
    }
    '''
    
    variables = {
        "id": page_id,
        "content": content,
        "description": description
    }
    
    payload = json.dumps({
        "query": query,
        "variables": variables
    }).encode('utf-8')
    
    req = urllib.request.Request(
        WIKI_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WIKI_KEY}"
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_page_id_by_path(path: str) -> int:
    """Find page ID by path."""
    query = json.dumps({
        "query": "{ pages { list { id path title } } }"
    }).encode()
    
    req = urllib.request.Request(
        WIKI_URL,
        data=query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WIKI_KEY}"
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        pages = data.get('data', {}).get('pages', {}).get('list', [])
        for p in pages:
            if p.get('path') == path:
                return p.get('id')
    return None

# Usage: Update existing page
with open('wiki_rpc_article.md', 'r', encoding='utf-8') as f:
    content = f.read()

page_id = get_page_id_by_path("tech/api/rpc")
if page_id:
    result = update_wiki_page(
        page_id=page_id,
        content=content,
        description="RPC协议全面指南，涵盖架构、框架对比、协议设计、性能优化等"
    )
    print(f"Updated: https://<wiki-url>/tech/api/rpc")
```

## Reference

- [GraphQL Spec - String Type](https://spec.graphql.org/October2021/#sec-String)
- Wiki.js API Documentation: https://docs.requarks.io/dev/api

---

**Remember:** 
- **Create:** Use `pages.create` with all fields including `tags: []` and `description`
- **Update:** Use `pages.update` with `id`, `content`, `description`, and `tags: []`
- **Query:** Use `pages.single(path: "...")` to find page ID, or `pages.list` to list all
- Always use GraphQL Variables for content to avoid escaping issues
- Always check `responseResult` for detailed error messages
