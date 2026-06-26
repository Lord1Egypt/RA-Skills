# CLI Reference

> Source: https://vitepress.dev/reference/cli

## vitepress dev

Start dev server.

```sh
vitepress [root]
vitepress dev [root]
```

| Option | Type | Description |
|--------|------|-------------|
| `--open` | `boolean \| string` | Open browser on startup |
| `--port` | `number` | Specify port |
| `--base` | `string` | Public base path (default: `/`) |
| `--cors` | - | Enable CORS |
| `--strictPort` | `boolean` | Exit if port is in use |
| `--force` | `boolean` | Force re-bundle ignoring cache |

**Example:**

```sh
vitepress dev docs --port 3000 --open
```

## vitepress build

Build for production.

```sh
vitepress build [root]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--mpa` | `boolean` | - | Build in MPA mode |
| `--base` | `string` | `/` | Public base path |
| `--target` | `string` | `modules` | Transpile target |
| `--outDir` | `string` | `<root>/.vitepress/dist` | Output directory |
| `--assetsInlineLimit` | `number` | `4096` | Inline threshold (bytes) |

**Example:**

```sh
vitepress build docs --outDir ../dist
```

## vitepress preview

Preview production build locally.

```sh
vitepress preview [root]
```

| Option | Type | Description |
|--------|------|-------------|
| `--base` | `string` | Public base path |
| `--port` | `number` | Specify port |

**Example:**

```sh
vitepress preview docs --port 8080
```

## vitepress init

Start setup wizard.

```sh
vitepress init
```

Questions asked:
- Config location
- Markdown files location
- Site title / description
- Theme selection
- TypeScript usage
- npm scripts addition
