---
name: serving-web-content
description: How to serve static files and integrated Vite/React applications in Harper.
metadata:
  mode: synthesized
---

# Serving Web Content

Instructions for the agent to follow when serving web content from Harper.

## When to Use

Use this skill when you need to serve a frontend (HTML, CSS, JS, or a React/Vue app) directly from your Harper instance — either plain static files or an integrated Vite app with hot module replacement (HMR) in development and a real production build when deployed.

## How It Works

There are two building blocks. Harper's built-in `static` plugin **serves** files; the `@harperfast/vite` plugin **builds** (and, for SSR, **renders**) a Vite app. For a Vite app they work **together** — the plugin builds into a directory and `static` serves that same directory.

### Option A: Static plugin only (simple, pre-built assets)

For a plain static site or already-built assets, use `static` on its own:

```yaml
static:
  files: 'web/*'
```

- Place files in a `web/` folder in the project root; they are served from the root URL (e.g. `http://localhost:9926/index.html`).
- Static files are matched first; if none matches, Harper falls through to your resource and table APIs.

### Option B: Vite plugin + static plugin (integrated Vite app)

> **Renamed in v1:** the plugin was previously `@harperfast/vite-plugin`. From `1.0.0` on it is **`@harperfast/vite`** (same key and `package`). It now pairs with the `static` plugin instead of building into `web/` itself.

`@harperfast/vite` **builds** your app — in `harper dev` it runs Vite in middleware mode with HMR; in `harper run` it runs `vite build` and rebuilds when watched files change (and renders HTML for SSR). The `static` plugin **serves** the built output. Point both at the same directory (`output`, default `dist`) — that shared directory is the only contract between them.

**SPA `config.yaml`** — list the plugin first so its dev server wins in `harper dev`; `notFound` + `fallthrough: false` makes client-side routing work:

```yaml
'@harperfast/vite':
  package: '@harperfast/vite'
  files: 'src/**/*'
  output: 'dist'

static:
  files: 'dist/**'
  notFound:
    file: 'index.html'
    statusCode: 200
  fallthrough: false
```

**SSR `config.yaml`** — add an `ssr` entry so the plugin renders `index.html`, and set `index: false` on `static` so it serves assets only:

```yaml
'@harperfast/vite':
  package: '@harperfast/vite'
  files: 'src/**/*'
  output: 'dist'
  ssr: 'src/entry-server.tsx'

static:
  files: 'dist/**'
  index: false
```

- Install dependencies: `npm install --save-dev vite @harperfast/vite @vitejs/plugin-react` (swap in your framework's Vite plugin, e.g. `@vitejs/plugin-vue`).
- Then `harper dev .` runs the app with HMR and `harper run .` runs the production build. Vite does _not_ need to be executed separately.

## Reading Harper Data During SSR

The render entry (`src/entry-server.tsx`) runs **inside Harper**, so it can read straight from the database and render the data into the HTML — no client-side fetch/XHR. `tables` is the same live, process-wide registry available everywhere (see [Programmatic Table Requests](programmatic-table-requests.md)); import it and query a table in an async `render`:

```tsx
import { tables } from 'harper';

export async function render(url: string): Promise<string> {
	const product = await tables.Product.get(idFromUrl(url));
	return renderToString(
		<StrictMode>
			<App product={product} />
		</StrictMode>,
	);
}
```

Keep `harper` external in `vite.config.ts` so this import resolves to Harper's running runtime instead of being bundled. `node_modules/harper` is symlinked to the running install, and symlinked deps aren't reliably auto-externalized for SSR:

```typescript
export default defineConfig({
	ssr: { external: ['harper'] },
	// ...plugins, resolve, build
});
```

To hydrate on the client without re-fetching, embed the rendered data in the HTML (e.g. an inline `<script type="application/json">`) and read it back before hydration — so the page needs no XHR at all.

## Deploying to Production

Because `@harperfast/vite` builds on the node and `static` serves the output, deploy the component as-is — no manual build-and-move step is needed:

```json
{
	"scripts": {
		"dev": "harper dev .",
		"start": "harper run .",
		"deploy": "harper deploy_component . restart=true replicated=true"
	}
}
```

On deploy the plugin runs `vite build` at startup (and rebuilds when `files` change) while `static` serves the result. If you prefer to build in CI, commit the build output, point `static` at it, and omit `files` so the plugin stays idle while `static` serves the prebuilt assets. Either way, `npm create harper@latest` scaffolds a working setup for you.
