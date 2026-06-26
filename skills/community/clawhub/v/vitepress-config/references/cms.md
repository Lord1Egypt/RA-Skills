# Connecting to CMS

> Source: https://vitepress.dev/guide/cms

## General Workflow

1. Load environment variables for API tokens:

```javascript
import { loadEnv } from 'vitepress'

const env = loadEnv('', process.cwd())
```

2. Fetch CMS data and format into paths:

```javascript
export default {
  async paths() {
    const data = await fetch('https://my-cms-api', {
      headers: { /* token */ }
    }).then(r => r.json())

    return data.map(entry => ({
      params: { id: entry.id },
      content: entry.content
    }))
  }
}
```

3. Render content in page:

```md
# {{ $params.title }}

- by {{ $params.author }}

<!-- @content -->
```

## Key Points

- Uses [Dynamic Routes](routing.md) feature
- Each CMS integration is different - adapt workflow
- Content can be raw Markdown or HTML via `<!-- @content -->`

## Integration Guides

VitePress documentation accepts community-contributed CMS integration guides. Consider submitting your integration!
