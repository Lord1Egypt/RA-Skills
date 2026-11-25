# http-response-status-code Usage Guide

Comprehensive reference for `http-response-status-code` — the companion status code package for the @wthek ecosystem.

---

## Installation

```bash
npm install http-response-status-code
```

---

## Import Patterns

```typescript
// ESM — named imports (tree-shaking friendly)
import { OK, NOT_FOUND, CREATED, UNPROCESSABLE_ENTITY } from "http-response-status-code";

// CJS
const { OK, NOT_FOUND } = require("http-response-status-code");

// CODES enum (alternative — all codes via single import)
import { CODES } from "http-response-status-code";
CODES.HTTP_CODE_404; // 404
CODES.HTTP_CODE_200; // 200

// Utility functions
import { getStatusName, getStatusDescription, toResponseInit, isClientError } from "http-response-status-code";
```

---

## Usage with http-error-kit

### Throwing Errors

```typescript
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, BAD_REQUEST, CONFLICT } from "http-response-status-code";

throw new KitHttpError(NOT_FOUND, "User not found");
throw new KitHttpError(BAD_REQUEST, "Missing required field", { field: "email" });
throw new KitHttpError(CONFLICT, "Email already registered");
```

### With Validation Transformers

```typescript
import { KitZodTransformer } from "@wthek/zod-transformer";
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import { KitTypeBoxTransformer } from "@wthek/typebox-transformer";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

// All transformers accept statusCode option
KitZodTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
KitValibotTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
KitTypeBoxTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
```

### Success Responses

```typescript
import { CREATED, NO_CONTENT, OK } from "http-response-status-code";

res.status(CREATED).json({ user });       // 201
res.status(NO_CONTENT).send();            // 204
return c.json({ data }, OK);              // 200
```

---

## Utility Functions

### `getStatusDescription(code)` — Human-Readable Names

```typescript
import { getStatusDescription } from "http-response-status-code";

getStatusDescription(200); // "OK"
getStatusDescription(404); // "Not Found"
getStatusDescription(500); // "Internal Server Error"
getStatusDescription(422); // "Unprocessable Entity"
```

### `getStatusName(code)` — Constant Name Lookup

```typescript
import { getStatusName } from "http-response-status-code";

getStatusName(404); // "NOT_FOUND"
getStatusName(418); // "IM_A_TEAPOT"
```

### `getStatusCode(name)` — Reverse Lookup

```typescript
import { getStatusCode } from "http-response-status-code";

getStatusCode("NOT_FOUND");    // 404
getStatusCode("IM_A_TEAPOT");  // 418
```

### `toResponseInit(code, init?)` — Fetch API Helper

Creates a `{ status, statusText, ...init }` object compatible with the Fetch `Response` constructor:

```typescript
import { toResponseInit, OK, NOT_FOUND } from "http-response-status-code";

// Basic
new Response("Hello", toResponseInit(OK));
// → Response with status: 200, statusText: "OK"

// With headers
new Response(body, toResponseInit(NOT_FOUND, {
    headers: { "Content-Type": "application/json" },
}));

// Response.json() shorthand (Hono, Next.js App Router, Deno, Bun)
return Response.json({ data }, toResponseInit(OK));
return Response.json({ error: "not found" }, toResponseInit(NOT_FOUND));

// Accepts string name too
toResponseInit("OK"); // { status: 200, statusText: "OK" }
```

### Category Validators

```typescript
import {
    isInformational, isSuccess, isRedirectional,
    isClientError, isServerError, isValidStatusCode,
} from "http-response-status-code";

isClientError(404);        // true
isServerError(500);        // true
isSuccess(200);            // true
isValidStatusCode(999);    // false (safe — doesn't throw)
isClientError(999);        // ⚠️ THROWS — use isValidStatusCode() first!
```

> **Warning:** All `is*` validators except `isValidStatusCode` **throw** for unrecognized codes.

### Category Listers

```typescript
import { getClientErrorCodes, getServerErrorCodes } from "http-response-status-code";

getClientErrorCodes(); // [400, 401, 402, ..., 451]
getServerErrorCodes(); // [500, 501, 502, ..., 511]
```

---

## Common Patterns

### Dynamic Error Messages

```typescript
import { getStatusDescription } from "http-response-status-code";

function createError(statusCode: number, detail?: string) {
    const message = detail ?? getStatusDescription(statusCode);
    return new KitHttpError(statusCode, message);
}
```

### Conditional Response Handling

```typescript
import { isClientError, isServerError } from "http-response-status-code";

if (isClientError(error.statusCode)) {
    logger.warn("Client error", error);
} else if (isServerError(error.statusCode)) {
    logger.error("Server error", error);
    alertOps(error);
}
```
