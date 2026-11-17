# Hermes Desktop Architecture Reference

Do NOT rediscover this the hard way. Learned through 3 consecutive crashes.

## File Layout (Windows, v0.17+)

```
apps/desktop/
├── electron/              ← TypeScript SOURCE (modify HERE)
│   ├── main.ts            ← Electron main process
│   ├── preload.ts         ← Context bridge
│   └── *.ts               ← Supporting modules
├── scripts/
│   └── bundle-electron-main.mjs  ← Official ESBuild bundler
├── dist/                  ← Build OUTPUT (NEVER hand-edit)
│   ├── electron-main.mjs
│   └── electron-preload.js
└── release/win-unpacked/
    ├── Hermes.exe
    └── resources/
        ├── app.asar              ← Static assets (icons, fonts). DO NOT REBUILD.
        └── app.asar.unpacked/
            └── dist/             ← Deployment target for compiled output
                ├── electron-main.mjs
                └── electron-preload.js
```

## Critical Path Rules

1. **electron-main.mjs**: Built from `main.ts` → deployed to `app.asar.unpacked/dist/`. NOT in asar.
2. **electron-preload.js**: Built from `preload.ts` → MUST be at `dist/electron-preload.js` INSIDE app.asar. `PRELOAD_PATH` resolves to `dist/electron-preload.js` — if it's at root, you get "Desktop IPC bridge unavailable".
3. **app.asar**: ~40MB static assets. Contains fonts, KaTeX, icons. Never rebuild unless you know EXACTLY what you're doing.
4. **Build**: `node scripts/bundle-electron-main.mjs` (ESBuild). Never skip this.
5. **Deploy**: Copy from `dist/` to `app.asar.unpacked/dist/`.
6. **Asar load order**: Electron loads from asar FIRST, filesystem second. If same file exists in both, asar version wins.

## Build Chain

```
electron/main.ts  ──┐
electron/preload.ts ─┤
electron/*.ts      ──┤
                     ├──→ bundle-electron-main.mjs (ESBuild)
                     │
                     ▼
               dist/electron-main.mjs    →  app.asar.unpacked/dist/
               dist/electron-preload.js  →  app.asar (in dist/ subdir)
```

## Incident Log

| # | Wrong Action | Symptom | Rule Violated |
|---|-------------|---------|---------------|
| 1 | Patched compiled `electron-main.mjs` directly | Worked briefly, lost on update | "Modify source, not compiled output" |
| 2 | Repacked asar with dist/ inside → 38MB | Electron loaded old version from asar, ignored patched file | "Never touch asar" |
| 3 | Re-extracted corrupted asar, deleted dist/ → 0.0MB asar | Complete crash (only package.json left) | "Start from clean state" |
| 4 | All 8 patches at once, tested last | Unknown which change broke it | "One change → verify" |
| 5 | preload at root in asar, not dist/ | "Desktop IPC bridge unavailable" | "Directory structure must match" |
| Kimi | Clean asar + same TS patches + correct preload path | ✅ Works | All rules followed |

## Debugging the asar

```javascript
// Check if file exists in asar
const a = require('@electron/asar');
try { a.extractFile(path, 'dist/electron-preload.js'); console.log('found'); }
catch { console.log('not in asar'); }

// List files (use backslash on Windows!)
const files = a.listPackage(path);
// Windows paths use backslash: 'dist\\electron-preload.js'
// NOT 'dist/electron-preload.js'
```
