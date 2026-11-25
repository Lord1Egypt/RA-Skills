"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const zod_1 = require("zod");
const express_middleware_1 = require("@wthek/express-middleware");
const zod_express_interceptor_1 = require("@wthek/zod-express-interceptor");
const http_error_kit_1 = require("http-error-kit");
const http_response_status_code_1 = require("http-response-status-code");
// 1. Optional: Global response formatter
http_error_kit_1.KitHttpErrorConfig.configureFormatter((statusCode, message, details) => ({
    status: statusCode,
    error: message,
    details: details ?? null,
}));
const app = (0, express_1.default)();
app.use(express_1.default.json());
// 2. Application routes
app.post("/register", (req, res) => {
    const registerSchema = zod_1.z.object({
        username: zod_1.z.string().min(3),
        email: zod_1.z.string().email(),
    });
    const user = registerSchema.parse(req.body);
    res.status(201).json({ status: "created", user });
});
app.get("/items/:id", (req, res) => {
    if (req.params.id !== "42") {
        throw new http_error_kit_1.KitHttpError(http_response_status_code_1.NOT_FOUND, "Item not found", { id: req.params.id });
    }
    res.json({ id: 42, name: "Special Item" });
});
// 3. Interceptors (MUST be placed after routes)
app.use((0, zod_express_interceptor_1.KitZodExpressInterceptor)({
    message: "Validation failed on payload",
    statusCode: http_response_status_code_1.UNPROCESSABLE_ENTITY,
}));
// 4. Terminal error handler
app.use((0, express_middleware_1.KitExpressMiddleware)({
    log: true,
    handleUnknownErrors: true,
}));
app.listen(3000, () => {
    console.log("Server listening at http://localhost:3000");
});
