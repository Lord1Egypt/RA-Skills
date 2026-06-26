---
title: Avoid Capturing Variables Outside JSVM Handler Scope
impact: HIGH
impactDescription: Variables defined outside a handler are undefined at runtime due to handler serialization
tags: jsvm, pb_hooks, scope, isolation, variables
---

## Avoid Capturing Variables Outside JSVM Handler Scope

Each JSVM handler (hook, route, middleware) is **serialized and executed as an isolated program**. Variables or functions declared at the module/file scope are NOT accessible inside handler bodies. This is the most common source of `undefined` errors in `pb_hooks` code.

**Incorrect (accessing outer-scope variable inside handler):**

```javascript
// pb_hooks/main.pb.js
const APP_NAME = "myapp"; // ❌ will be undefined inside handlers

onBootstrap((e) => {
    e.next();
    console.log(APP_NAME); // ❌ undefined — APP_NAME is not in handler scope
});

// ❌ Even $app references captured here may not work as expected
const helper = (id) => $app.findRecordById("posts", id);

onRecordAfterCreateSuccess((e) => {
    helper(e.record.id); // ❌ helper is undefined inside the handler
}, "posts");
```

**Correct (move shared state into a required module, or use `$app`/`e.app` directly):**

```javascript
// pb_hooks/config.js  — stateless CommonJS module
module.exports = {
    APP_NAME: "myapp",
    MAX_RETRIES: 3,
};

// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

onBootstrap((e) => {
    e.next();
    // Load the shared module INSIDE the handler
    const config = require(`${__hooks}/config.js`);
    console.log(config.APP_NAME); // ✅ "myapp"
});

routerAdd("GET", "/api/myapp/status", (e) => {
    const config = require(`${__hooks}/config.js`);
    return e.json(200, { app: config.APP_NAME });
});

onRecordAfterCreateSuccess((e) => {
    // Access the app directly via e.app inside the handler
    const post = e.app.findRecordById("posts", e.record.id);
    e.next();
}, "posts");
```

**Key rules:**
- Every handler body is serialized to a string and executed in its own isolated goja runtime context. There is no shared global state between handlers at runtime.
- `require()` loads modules from a **shared registry** — modules are evaluated once and cached. Keep module-level code stateless; avoid mutable module exports to prevent data races under concurrent requests.
- `__hooks` is always available inside handlers and resolves to the absolute path of the `pb_hooks` directory.
- Error stack trace line numbers may not be accurate because of the handler serialization — log meaningful context manually when debugging.
- Workaround for simple constants: move them to a `config.js` module and `require()` it inside each handler that needs it.

Reference: [Extend with JavaScript - Handlers scope](https://pocketbase.io/docs/js-overview/#handlers-scope)
