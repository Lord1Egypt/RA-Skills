# Publishing a Vite Plugin to npm

## Project Structure
```
vite-plugin-my/
├── src/
│   └── index.ts          # Plugin entry
├── dist/                  # Build output (generated)
├── package.json
├── tsconfig.json
├── README.md
└── CHANGELOG.md
```

## package.json Template
```json
{
  "name": "vite-plugin-my",
  "version": "1.0.0",
  "description": "A Vite plugin that does X",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist", "README.md", "CHANGELOG.md"],
  "keywords": ["vite", "vite-plugin"],
  "peerDependencies": {
    "vite": "^5.0.0 || ^6.0.0"
  },
  "peerDependenciesMeta": {
    "vite": { "optional": true }
  },
  "devDependencies": {
    "vite": "^6.0.0",
    "typescript": "^5.0.0",
    "tsup": "^8.0.0",
    "vitest": "^2.0.0"
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "test": "vitest run",
    "prepublishOnly": "npm run build && npm test"
  }
}
```

## tsup Build Config (tsup.config.ts)
```ts
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  clean: true,
  external: ['vite'],
})
```

## TypeScript Config
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "declaration": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

## README Template
```markdown
# vite-plugin-my

> One-line description of what the plugin does.

## Install
npm i -D vite-plugin-my

## Usage
// vite.config.ts
import myPlugin from 'vite-plugin-my'

export default defineConfig({
  plugins: [myPlugin({ option: 'value' })]
})

## Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| include | string/RegExp | '**/*' | Files to include |

## License
MIT
```

## Publishing Checklist
- [ ] `npm run build` succeeds, dist/ has .js, .cjs, .d.ts
- [ ] `npm pack --dry-run` shows expected files only
- [ ] Tested with both Vite 5 and Vite 6
- [ ] CHANGELOG.md updated
- [ ] Git tag created: `git tag v1.0.0`
- [ ] `npm publish --access public`
- [ ] Announce on Twitter/X, Vite Discord #plugins channel
