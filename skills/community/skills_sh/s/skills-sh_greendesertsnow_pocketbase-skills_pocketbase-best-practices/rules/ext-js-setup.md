---
title: Set Up JSVM (pb_hooks) for Server-Side JavaScript
impact: HIGH
impactDescription: Correct setup unlocks hot-reload, type-completion, and the full JSVM API
tags: jsvm, pb_hooks, extending, setup, typescript
---

## Set Up JSVM (pb_hooks) for Server-Side JavaScript

The prebuilt PocketBase executable embeds an ES5 JavaScript engine (goja). Drop `*.pb.js` files into a `pb_hooks` directory next to the executable and they load automatically at startup. Files are loaded in **filename sort order**, and on UNIX platforms the process auto-reloads when any `pb_hooks` file changes.

**Incorrect (TypeScript without transpile, wrong filename, missing types reference):**

```typescript
// pb_hooks/main.ts  ❌ PocketBase loads ONLY *.pb.js - a .ts file is ignored
import { something } from "./lib"; // ❌ ES modules not supported in goja

routerAdd("GET", "/hello", (e) => e.json(200, { ok: true }));
```

```javascript
// pb_hooks/hooks.js  ❌ wrong extension - must be *.pb.js
// No /// reference -> editor shows every call as "any"
onRecordAfterUpdateSuccess((e) => {
    console.log(e.record.get("email"));
    // Missing e.next() - stops the execution chain silently
}, "users");
```

**Correct (valid filename, types reference, `e.next()` called):**

```javascript
// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

// Hooks defined earlier in the filename sort order run first.
// Use prefixes like "01_", "10_", "99_" if order matters.

routerAdd("GET", "/api/myapp/hello/{name}", (e) => {
    const name = e.request.pathValue("name");
    return e.json(200, { message: "Hello " + name });
});

onRecordAfterUpdateSuccess((e) => {
    console.log("user updated:", e.record.get("email"));
    e.next(); // REQUIRED - otherwise the execution chain is broken
}, "users");
```

**Key details:**
- JS method names are **camelCase** versions of their Go equivalents (`FindRecordById` → `$app.findRecordById`).
- Errors are thrown as regular JS exceptions, not returned as values.
- Global objects: `$app` (the app), `$apis` (routing helpers/middlewares), `$os` (OS primitives), `$security` (JWT, random strings, AES), `$filesystem` (file factories), `$dbx` (query builder), `$mails` (email helpers), `__hooks` (absolute path to `pb_hooks`).
- `pb_data/types.d.ts` is regenerated automatically - commit the triple-slash reference but not the file itself if you prefer.
- Auto-reload on file change works on UNIX only. On Windows, restart the process manually.

Reference: [Extend with JavaScript - Overview](https://pocketbase.io/docs/js-overview/)
