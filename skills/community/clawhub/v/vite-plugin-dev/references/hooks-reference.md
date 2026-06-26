# Vite Plugin Hooks Reference

## Full Hook Execution Order

### Dev Server (serve)
1. config
2. configResolved
3. options (rollup)
4. buildStart
5. configureServer ← add middleware here
6. Per request: resolveId → load → transform
7. handleHotUpdate (on file change)
8. configurePreviewServer (vite preview)

### Build
1. config
2. configResolved
3. options (rollup)
4. buildStart
5. Per module: resolveId → load → transform
6. moduleParsed
7. buildEnd
8. generateBundle
9. writeBundle
10. closeBundle

## Hook Signatures

```ts
interface Plugin {
  name: string
  enforce?: 'pre' | 'post'
  apply?: 'build' | 'serve' | ((config: UserConfig, env: ConfigEnv) => boolean)

  // Config
  config?: (config: UserConfig, env: ConfigEnv) =>
    UserConfig | null | void | Promise<UserConfig | null | void>
  configResolved?: (config: ResolvedConfig) => void | Promise<void>

  // Server
  configureServer?: (server: ViteDevServer) => (() => void) | void | Promise<...>
  handleHotUpdate?: (ctx: HmrContext) => Array<ModuleNode> | void | Promise<...>

  // Build
  buildStart?: (options: InputOptions) => void | Promise<void>
  buildEnd?: (error?: Error) => void | Promise<void>
  closeBundle?: () => void | Promise<void>

  // Module
  resolveId?: (
    source: string,
    importer: string | undefined,
    options: { ssr?: boolean }
  ) => ResolveIdResult | Promise<ResolveIdResult>

  load?: (
    id: string,
    options?: { ssr?: boolean }
  ) => LoadResult | Promise<LoadResult>

  transform?: (
    code: string,
    id: string,
    options?: { ssr?: boolean }
  ) => TransformResult | Promise<TransformResult>

  // Bundle
  generateBundle?: (
    options: OutputOptions,
    bundle: OutputBundle,
    isWrite: boolean
  ) => void | Promise<void>
}
```

## enforce Order
Plugins execute in this order:
1. Plugins with `enforce: 'pre'`
2. Vite core plugins
3. Plugins without `enforce`
4. Vite build plugins
5. Plugins with `enforce: 'post'`

## apply Examples
```ts
// Only run during build
apply: 'build'

// Only run during dev
apply: 'serve'

// Conditional
apply(config, { command }) {
  return command === 'build' && !config.build?.ssr
}
```
