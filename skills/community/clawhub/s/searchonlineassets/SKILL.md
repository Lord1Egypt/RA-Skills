---
name: searchOnlineAssets
version: 1.0.9
description: 'Online asset search tool: queries public stock libraries (Pixabay) for high-quality photos, illustrations, vectors and videos, returning result metadata and URLs for use in the current workflow.'
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.0.9',
        'installAlternative': 'npx @dlazy/cli@1.0.9',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': 'When invoking this skill, call the searchOnlineAssets tool to query public asset libraries (Pixabay).' },
  }
---

# searchOnlineAssets

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Online asset search tool: queries public stock libraries (Pixabay) for high-quality photos, illustrations, vectors and videos, and returns result metadata + URLs for use in the current workflow.

## Trigger Keywords

- searchOnlineAssets
- pixabay
- online asset search

## Authentication

All requests require a dLazy API key, configured through the CLI:

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

## About & Provenance

- **CLI source code**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.0.8` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.0.9 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.0.9`). Review the GitHub source before installing.

## How It Works

This skill is a thin wrapper around the public Pixabay search API, exposed through the dLazy tool runtime. When you invoke it:

- The query and filter parameters you provide are forwarded to the Pixabay API.
- Pixabay returns a list of hits; the tool projects each entry to a stable shape (id, tags, preview / web-format / large URLs, dimensions).
- The skill itself does not access network or filesystem resources beyond the Pixabay HTTP request handled inside the dLazy tool runtime.

This is the standard SaaS pattern; the asset URLs returned are hosted by Pixabay (`pixabay.com`), not by dLazy. See [dlazy.com](https://dlazy.com) for the full service terms.

## Usage

**CRITICAL INSTRUCTION FOR AGENT**:
Invoke the `searchOnlineAssets` tool with a structured input object. This is an internal AI tool, not a CLI command — it runs inside the model's tool-call channel.

Input schema:

```ts
{
  query: string;                                            // required search keyword(s); prefer English for better recall
  imageType?: "all" | "photo" | "illustration" | "vector";  // default: "all"
  orientation?: "all" | "horizontal" | "vertical";          // default: "all"
  page?: number;                                            // default: 1
  perPage?: number;                                         // default: 10 (max 200 per Pixabay)
  lang?: string;                                            // default: "zh"; pass "en" for English-tagged matches
}
```

Behaviour notes:

- `safesearch` is forced to `true` server-side; explicit content is filtered out.
- Pixabay performs best with English keywords. Translate user-provided Chinese terms (e.g., "咖啡 → coffee") before issuing the request when accuracy matters.
- Pick the most relevant `largeImageURL` (or matching video preview URL) and surface the URL plus `tags` to the user; do not dump the entire `hits` array.
- If `total === 0`, tell the user no matching asset was found and suggest a broader keyword.

## Output Format

```json
{
  "total": 1234,
  "hits": [
    {
      "id": 5179107,
      "tags": "coffee, cup, latte art",
      "previewURL": "https://cdn.pixabay.com/.../preview.jpg",
      "webformatURL": "https://pixabay.com/.../webformat.jpg",
      "largeImageURL": "https://pixabay.com/.../large.jpg",
      "imageWidth": 6000,
      "imageHeight": 4000
    }
  ]
}
```

## Examples

```ts
// Find horizontal photos of cityscapes
searchOnlineAssets({
  query: 'cityscape skyline',
  imageType: 'photo',
  orientation: 'horizontal',
  perPage: 6,
})
```

```ts
// Find vector icons for nature
searchOnlineAssets({
  query: 'leaf nature icon',
  imageType: 'vector',
  perPage: 12,
})
```

## Error Handling

| Code | Error Type                | Example Message                        |
| ---- | ------------------------- | -------------------------------------- |
| 401  | Unauthorized (No API Key) | `Pixabay API key is not configured`    |
| 502  | Upstream API failed       | `Pixabay API error: <statusText>`      |
| 503  | Network / fetch failed    | `Failed to search images from Pixabay` |

> **AGENT CRITICAL INSTRUCTION**:
>
> 1. If the tool throws `Pixabay API key is not configured`, the workspace is missing its Pixabay credentials — inform the user and stop; do not retry.
> 2. If `Pixabay API error` is returned, retry once with a simpler / shorter query before falling back to telling the user no result was found.

## Tips

Visit https://dlazy.com for more information.
