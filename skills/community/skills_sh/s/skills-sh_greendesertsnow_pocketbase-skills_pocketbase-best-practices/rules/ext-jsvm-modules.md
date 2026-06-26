---
title: Load Shared Code with CommonJS require() in pb_hooks
impact: MEDIUM
impactDescription: Correct module usage prevents require() failures, race conditions, and ESM import errors
tags: jsvm, pb_hooks, modules, require, commonjs, esm, filesystem
---

## Load Shared Code with CommonJS require() in pb_hooks

The embedded JSVM (goja) supports **only CommonJS** (`require()`). ES module `import` syntax is not supported without pre-bundling. Modules use a shared registry — they are evaluated once and cached, so avoid mutable module-level state to prevent race conditions across concurrent requests.

**Incorrect (ESM imports, mutable shared state, Node.js APIs):**

```javascript
// ❌ ESM import syntax — not supported by goja
import { sendEmail } from "./utils.js";

// ❌ Node.js APIs don't exist in the JSVM sandbox
const fs = require("fs");
fs.writeFileSync("output.txt", "hello"); // ReferenceError

// ❌ Mutable module-level state is shared across concurrent requests
// pb_hooks/counter.js
let requestCount = 0;
module.exports = { increment: () => ++requestCount }; // race condition
```

**Correct (CommonJS require, stateless helpers, JSVM bindings for OS/file ops):**

```javascript
// pb_hooks/utils.js  — stateless helper module
module.exports = {
    formatDate: (d) => new Date(d).toISOString().slice(0, 10),
    validateEmail: (addr) => /^[^@]+@[^@]+\.[^@]+$/.test(addr),
};

// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

onRecordAfterCreateSuccess((e) => {
    const utils = require(`${__hooks}/utils.js`);
    const date = utils.formatDate(e.record.get("created"));
    console.log("Record created on:", date);
    e.next();
}, "posts");

// Use $os.* for file system operations (not Node.js fs)
routerAdd("GET", "/api/myapp/read-config", (e) => {
    const raw = $os.readFile(`${__hooks}/config.json`);
    const cfg = JSON.parse(raw);
    return e.json(200, { name: cfg.appName });
});

// Use $filesystem.s3(...) or $filesystem.local(...) for storage (v0.36.4+)
routerAdd("POST", "/api/myapp/upload", (e) => {
    const bucket = $filesystem.s3({
        endpoint: "s3.amazonaws.com",
        bucket:   "my-bucket",
        region:   "us-east-1",
        accessKey: $app.settings().s3.accessKey,
        secret:    $app.settings().s3.secret,
    });
    // ... use bucket to store/retrieve files
    return e.json(200, { ok: true });
}, $apis.requireAuth());
```

**Using third-party CJS packages:**

```javascript
// node_modules/ is searched automatically alongside __hooks.
// Install packages with npm next to the pb_hooks directory, then require by name.
onBootstrap((e) => {
    e.next();
    // Only CJS-compatible packages work without bundling
    const slugify = require("slugify");
    console.log(slugify("Hello World")); // "Hello-World"
});
```

**Using ESM-only packages (bundle to CJS first):**

```bash
# Bundle an ESM package to CJS with rollup before committing it to pb_hooks
npx rollup node_modules/some-esm-pkg/index.js \
  --file pb_hooks/vendor/some-esm-pkg.js \
  --format cjs
```

```javascript
onBootstrap((e) => {
    e.next();
    const pkg = require(`${__hooks}/vendor/some-esm-pkg.js`);
});
```

**JSVM engine limitations:**
- No `setTimeout` / `setInterval` — no async scheduling inside handlers.
- No Node.js APIs (`fs`, `Buffer`, `process`, etc.) — use `$os.*` and `$filesystem.*` JSVM bindings instead.
- No browser APIs (`fetch`, `window`, `localStorage`) — use `$app.newHttpClient()` for outbound HTTP requests.
- ES6 is mostly supported but not fully spec-compliant (goja engine).
- The prebuilt PocketBase executable starts a **pool of 15 JS runtimes** by default; adjust with `--hooksPool=N` for high-concurrency workloads (more runtimes = more memory, better throughput).
- `nullString()`, `nullInt()`, `nullFloat()`, `nullBool()`, `nullArray()`, `nullObject()` helpers are available (v0.35.0+) for scanning nullable DB columns safely.

Reference: [Extend with JavaScript - Loading modules](https://pocketbase.io/docs/js-overview/#loading-modules)
