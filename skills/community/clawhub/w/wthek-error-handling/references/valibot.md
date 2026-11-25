# Valibot Validation Integration with @wthek

Guide for `@wthek/valibot-transformer`.

---

## Installation

```bash
npm install @wthek/valibot-transformer http-error-kit http-response-status-code
```

**Peer dependencies:** `valibot >= 1.0.0`, `http-error-kit >= 1.2.0`

---

## Dual Conversion APIs

### 1. `fromValiError(error, options?)` — Non-Throwing

Converts a `ValiError` into a `KitHttpError` instance or returns `null` if the error is not a `ValiError`:

```typescript
import * as v from "valibot";
import { fromValiError } from "@wthek/valibot-transformer";

try {
    v.parse(schema, input);
} catch (err: unknown) {
    const kitError = fromValiError(err, {
        message: "Invalid form input",
        statusCode: 422,
    });

    if (kitError) {
        return c.json(kitError, kitError.statusCode ?? 400);
    }

    throw err;
}
```

### 2. `KitValibotTransformer(error, options?)` — Throwing

Transforms any `ValiError` into a `KitHttpError` and throws it. Non-ValiErrors are re-thrown unchanged. Return type is `never`.

```typescript
import * as v from "valibot";
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

try {
    v.parse(schema, input);
} catch (err) {
    KitValibotTransformer(err, {
        message: "Validation failed",
        statusCode: UNPROCESSABLE_ENTITY,
    });
}
```

---

## Options Reference

```typescript
interface IKitValibotTransformerOptions {
    message?: string;    // Default: "Valibot Validation Failed"
    statusCode?: number; // Default: 400
}
```

---

## Error Payload Structure

Valibot issues are preserved in `error.details.issues`:

```json
{
    "statusCode": 400,
    "message": "Valibot Validation Failed",
    "details": {
        "issues": [
            {
                "kind": "validation",
                "type": "min_value",
                "input": 14,
                "expected": ">=18",
                "received": "14",
                "message": "Invalid value: Expected >=18 but received 14",
                "path": [{ "type": "object", "origin": "value", "key": "age", "value": 14 }]
            }
        ]
    }
}
```

---

## Framework Integration Examples

### Express

```typescript
import express from "express";
import { KitExpressMiddleware } from "@wthek/express-middleware";
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import * as v from "valibot";

const app = express();
app.use(express.json());

app.post("/users", (req, res) => {
    try {
        const user = v.parse(UserSchema, req.body);
        res.status(201).json(user);
    } catch (err) {
        KitValibotTransformer(err);
    }
});

app.use(KitExpressMiddleware({ handleUnknownErrors: true }));
```

### Fastify

```typescript
import Fastify from "fastify";
import { KitFastifyMiddleware } from "@wthek/fastify-middleware";
import { KitValibotTransformer } from "@wthek/valibot-transformer";

const app = Fastify({ logger: true });
KitFastifyMiddleware(app, { log: true, handleUnknownErrors: true });

app.post("/users", async (request) => {
    try {
        return v.parse(UserSchema, request.body);
    } catch (err) {
        KitValibotTransformer(err);
    }
});
```

### Hono

```typescript
import { Hono } from "hono";
import { KitHonoMiddleware } from "@wthek/hono-middleware";
import { fromValiError } from "@wthek/valibot-transformer";

const app = new Hono();
KitHonoMiddleware(app, { handleUnknownErrors: true });

app.post("/users", async (c) => {
    const body = await c.req.json();
    try {
        const user = v.parse(UserSchema, body);
        return c.json(user, 201);
    } catch (err) {
        const kitError = fromValiError(err);
        if (kitError) throw kitError;
        throw err;
    }
});
```

### Koa

```typescript
import Koa from "koa";
import { KitKoaMiddleware } from "@wthek/koa-middleware";
import { KitValibotTransformer } from "@wthek/valibot-transformer";

const app = new Koa();
KitKoaMiddleware(app, { handleUnknownErrors: true });

app.use(async (ctx) => {
    try {
        const user = v.parse(UserSchema, ctx.request.body);
        ctx.status = 201;
        ctx.body = user;
    } catch (err) {
        KitValibotTransformer(err);
    }
});
```

---

## Valibot vs Zod vs TypeBox Transformer Comparison

| Feature | Zod | Valibot | TypeBox |
| :--- | :--- | :--- | :--- |
| **Package** | `@wthek/zod-transformer` | `@wthek/valibot-transformer` | `@wthek/typebox-transformer` |
| **Throwing fn** | `KitZodTransformer` | `KitValibotTransformer` | `KitTypeBoxTransformer` |
| **Non-throwing fn** | `fromZodError` | `fromValiError` | `fromTypeBoxError` |
| **Default message** | `"Zod Validation Failed"` | `"Valibot Validation Failed"` | `"TypeBox Validation Failed"` |
| **Issues location** | `details.issues` | `details.issues` | `details.issues` |
| **Detection** | `instanceof ZodError` | `isValiError()` | `instanceof TypeBoxError` + shape checks |
| **Express interceptor** | ✅ `@wthek/zod-express-interceptor` | ❌ Manual only | ❌ Manual only |
| **Input formats** | `ZodError` only | `ValiError` only | Multiple: `TypeBoxError`, `ValueError[]`, iterators, single `ValueError` |
