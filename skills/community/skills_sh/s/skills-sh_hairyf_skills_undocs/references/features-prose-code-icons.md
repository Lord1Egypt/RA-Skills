---
name: undocs-prose-code-icons
description: File type icons in code blocks and prose in undocs
---

# Prose Code Icons

Undocs configures file type icons for code blocks in documentation. Icons appear next to code block filenames.

## Built-in Mappings

Undocs provides mappings for common file types:

| File/Filename | Icon |
|---------------|------|
| package.json | vscode-icons:file-type-node |
| tsconfig.json | vscode-icons:file-type-tsconfig |
| .config | vscode-icons:file-type-config |
| .gitignore | vscode-icons:file-type-git |
| .env | vscode-icons:file-type-dotenv |
| nuxt.config.ts | vscode-icons:file-type-nuxt |
| nitro.config.ts | i-undocs-nitro |
| vite.config.* | i-logos-vitejs |
| tailwind.config.* | vscode-icons:file-type-tailwind |
| ts, tsx | vscode-icons:file-type-typescript |
| js, jsx, mjs, cjs | vscode-icons:file-type-js |
| md | vscode-icons:file-type-markdown |
| py | vscode-icons:file-type-python |
| yml | vscode-icons:file-type-yaml |
| terminal | i-heroicons-command-line |
| npm, pnpm, yarn, bun, deno | vscode-icons:file-type-* |

## Usage in Markdown

Code blocks with filename show the icon automatically:

````markdown
```json [package.json]
{ "scripts": { "dev": "undocs dev" } }
```

```ts [nuxt.config.ts]
export default defineNuxtConfig({})
```

```sh [Terminal]
pnpm dev
```
````

## Customization

Icons are configured via Nuxt UI prose `codeIcon`. To customize, extend app config in your docs layer. The undocs app.config.ts defines the default mappings.

## Icon Sources

- **vscode-icons**: File type icons from vscode-icons
- **i-undocs-***: Undocs built-in icons (nitro, h3, etc.)
- **i-logos-***: Technology logos
- **i-heroicons-***: Heroicons

## Key Points

- Icons appear next to code block filename/title
- Matching is by filename or extension
- Uses Nuxt UI Prose codeIcon configuration
- Custom mappings can be added via app config override

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/app.config.ts
- https://ui.nuxt.com/docs/typography
-->
