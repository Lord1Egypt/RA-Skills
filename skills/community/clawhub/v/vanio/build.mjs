import { build } from 'esbuild'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

await build({
  entryPoints: [resolve(__dirname, 'src/index.ts')],
  bundle: true,
  platform: 'node',
  target: 'node20',
  format: 'cjs',
  outfile: resolve(__dirname, 'dist/index.cjs'),
  external: [],
  resolveExtensions: ['.ts', '.js', '.json'],
  banner: { js: '#!/usr/bin/env node' },
  sourcemap: false,
  minify: true,
  logLevel: 'warning',
})

console.log('Built dist/index.cjs')
