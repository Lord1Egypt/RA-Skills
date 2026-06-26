# Vite Plugin Patterns & Examples

## Pattern 1: File Type Transformer
Transform `.yaml` files into JS objects:

```ts
import { parse } from 'yaml'
import type { Plugin } from 'vite'

export default function yamlPlugin(): Plugin {
  return {
    name: 'vite-plugin-yaml',
    transform(code, id) {
      if (!id.endsWith('.yaml') && !id.endsWith('.yml')) return null
      try {
        const data = parse(code)
        return {
          code: `export default ${JSON.stringify(data)}`,
          map: { mappings: '' },
        }
      } catch (e) {
        this.error(`Failed to parse YAML: ${e.message}`)
      }
    },
  }
}
```

## Pattern 2: Virtual Module with Runtime Data
Inject build-time data accessible as a module:

```ts
export default function buildInfoPlugin(): Plugin {
  const VIRTUAL = 'virtual:build-info'
  const RESOLVED = '\0virtual:build-info'

  return {
    name: 'vite-plugin-build-info',
    resolveId(id) {
      if (id === VIRTUAL) return RESOLVED
    },
    load(id) {
      if (id !== RESOLVED) return
      return `
        export const buildTime = ${Date.now()}
        export const version = ${JSON.stringify(process.env.npm_package_version)}
        export const mode = ${JSON.stringify(process.env.NODE_ENV)}
      `
    },
  }
}

// Usage in app:
// import { buildTime, version } from 'virtual:build-info'
```

## Pattern 3: Dev Server Middleware
Add custom API routes in dev mode:

```ts
export default function mockApiPlugin(): Plugin {
  return {
    name: 'vite-plugin-mock-api',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use('/api/hello', (req, res) => {
        res.setHeader('Content-Type', 'application/json')
        res.end(JSON.stringify({ message: 'Hello from mock API' }))
      })
    },
  }
}
```

## Pattern 4: Asset Processing
Process and emit custom assets:

```ts
export default function svgSpritePlugin(): Plugin {
  const sprites: string[] = []

  return {
    name: 'vite-plugin-svg-sprite',
    transform(code, id) {
      if (!id.endsWith('.svg')) return null
      sprites.push(code)
      return { code: `export default ""`, map: null }
    },
    generateBundle() {
      this.emitFile({
        type: 'asset',
        fileName: 'sprite.svg',
        source: `<svg>${sprites.join('')}</svg>`,
      })
    },
  }
}
```

## Pattern 5: Config Injection
Expose env/config to client code:

```ts
export default function configPlugin(userConfig: Record<string, unknown>): Plugin {
  return {
    name: 'vite-plugin-config',
    config() {
      return {
        define: {
          __APP_CONFIG__: JSON.stringify(userConfig),
        },
      }
    },
  }
}
```

## Testing Setup
```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import myPlugin from './src/index'

export default defineConfig({
  plugins: [myPlugin()],
  test: { environment: 'node' },
})

// plugin.test.ts
import { build } from 'vite'
import { test, expect } from 'vitest'

test('transforms .myext files', async () => {
  const result = await build({
    plugins: [myPlugin()],
    build: { write: false },
  })
  expect(result).toBeDefined()
})
```
