import express from "express";
import { z } from "zod";
import { KitExpressMiddleware } from "@wthek/express-middleware";
import { KitZodExpressInterceptor } from "@wthek/zod-express-interceptor";
import { KitHttpError, KitHttpErrorConfig } from "http-error-kit";
import { NOT_FOUND, UNPROCESSABLE_ENTITY } from "http-response-status-code";

// 1. Optional: Global response formatter
KitHttpErrorConfig.configureFormatter((statusCode, message, details) => ({
    status: statusCode,
    error: message,
    details: details ?? null,
}));

const app = express();
app.use(express.json());

// 2. Application routes
app.post("/register", (req, res) => {
    const registerSchema = z.object({
        username: z.string().min(3),
        email: z.string().email(),
    });

    const user = registerSchema.parse(req.body);
    res.status(201).json({ status: "created", user });
});

app.get("/items/:id", (req, res) => {
    if (req.params.id !== "42") {
        throw new KitHttpError(NOT_FOUND, "Item not found", { id: req.params.id });
    }
    res.json({ id: 42, name: "Special Item" });
});

// 3. Interceptors (MUST be placed after routes)
app.use(KitZodExpressInterceptor({
    message: "Validation failed on payload",
    statusCode: UNPROCESSABLE_ENTITY,
}));

// 4. Terminal error handler
app.use(KitExpressMiddleware({
    log: true,
    handleUnknownErrors: true,
}));

app.listen(3000, () => {
    console.log("Server listening at http://localhost:3000");
});

