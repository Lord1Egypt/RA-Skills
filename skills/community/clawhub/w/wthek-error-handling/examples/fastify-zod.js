"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fastify_1 = require("fastify");
const zod_1 = require("zod");
const fastify_middleware_1 = require("@wthek/fastify-middleware");
const zod_transformer_1 = require("@wthek/zod-transformer");
const http_error_kit_1 = require("http-error-kit");
const http_response_status_code_1 = require("http-response-status-code");
const app = (0, fastify_1.default)({ logger: true });
// Schema definition
const loginSchema = zod_1.z.object({
    email: zod_1.z.string().email(),
    password: zod_1.z.string().min(8),
});
app.post("/login", async (req) => {
    const parseResult = loginSchema.safeParse(req.body);
    if (!parseResult.success) {
        // Transform ZodError into KitHttpError
        const error = (0, zod_transformer_1.fromZodError)(parseResult.error, {
            message: "Invalid login credentials format",
            statusCode: http_response_status_code_1.UNPROCESSABLE_ENTITY,
        });
        throw error;
    }
    return { token: "sample-jwt-token" };
});
app.get("/profile", async () => {
    throw new http_error_kit_1.KitHttpError(http_response_status_code_1.NOT_FOUND, "Profile not found");
});
// Attach global WTHek Fastify error handler
(0, fastify_middleware_1.KitFastifyMiddleware)(app, {
    log: true,
    handleUnknownErrors: true,
});
app.listen({ port: 3000 }, (err) => {
    if (err) {
        app.log.error(err);
        process.exit(1);
    }
});
