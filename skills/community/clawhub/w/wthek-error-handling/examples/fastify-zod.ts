import Fastify from "fastify";
import { z } from "zod";
import { KitFastifyMiddleware } from "@wthek/fastify-middleware";
import { fromZodError } from "@wthek/zod-transformer";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, UNPROCESSABLE_ENTITY } from "http-response-status-code";

const app = Fastify({ logger: true });

// Schema definition
const loginSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
});

app.post("/login", async (req) => {
    const parseResult = loginSchema.safeParse(req.body);
    if (!parseResult.success) {
        // Transform ZodError into KitHttpError
        const error = fromZodError(parseResult.error, {
            message: "Invalid login credentials format",
            statusCode: UNPROCESSABLE_ENTITY,
        });
        throw error;
    }
    return { token: "sample-jwt-token" };
});

app.get("/profile", async () => {
    throw new KitHttpError(NOT_FOUND, "Profile not found");
});

// Attach global WTHek Fastify error handler
KitFastifyMiddleware(app, {
    log: true,
    handleUnknownErrors: true,
});

app.listen({ port: 3000 }, (err) => {
    if (err) {
        app.log.error(err);
        process.exit(1);
    }
});

