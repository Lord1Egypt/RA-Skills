# Express.js Error Handling with @wthek

Guide for implementing `@wthek/express-middleware` and `@wthek/zod-express-interceptor`.

---

## Installation

```bash
npm install @wthek/express-middleware @wthek/zod-express-interceptor http-error-kit http-response-status-code
```

## Production Recipe

```typescript
import express from "express";
import { z } from "zod";
import { KitExpressMiddleware } from "@wthek/express-middleware";
import { KitZodExpressInterceptor } from "@wthek/zod-express-interceptor";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, UNPROCESSABLE_ENTITY } from "http-response-status-code";

const app = express();
app.use(express.json());

// Routes
app.post("/users", (req, res) => {
    const userSchema = z.object({
        email: z.string().email(),
        age: z.number().min(18),
    });

    const validated = userSchema.parse(req.body);
    res.status(201).json({ success: true, data: validated });
});

app.get("/users/:id", (req, res) => {
    // Manually throwing a KitHttpError
    throw new KitHttpError(NOT_FOUND, "User not found", { userId: req.params.id });
});

// 1. Intercept Zod validation errors (MUST be after routes)
app.use(KitZodExpressInterceptor({
    message: "Invalid request payload",
    statusCode: UNPROCESSABLE_ENTITY, // 422
}));

// 2. Final Error Handler (MUST be the last middleware)
app.use(KitExpressMiddleware({
    log: (err, req) => console.error(`[Error on ${req.method} ${req.url}]:`, err),
    handleUnknownErrors: true, // Safely turns uncaught exceptions into 500 JSON
}));

app.listen(3000, () => console.log("Server listening on port 3000"));
```

## Options Reference

```typescript
app.use(KitExpressMiddleware({
    // Enable simple console.error logging:
    log: true,
    
    // OR custom logger callback (e.g. Pino/Winston):
    log: (error: unknown, req: express.Request) => {
        logger.error({ err: error, path: req.path }, "API error occurred");
    },

    // Catch non-Kit errors (Error, TypeError, etc.) and return structured 500:
    handleUnknownErrors: true,
}));
```

