import { Hono } from "hono";
import { KitHonoMiddleware } from "@wthek/hono-middleware";
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, UNPROCESSABLE_ENTITY, CREATED } from "http-response-status-code";
import * as v from "valibot";

const app = new Hono();

// 1. Attach global error handler
KitHonoMiddleware(app, {
    log: true,
    handleUnknownErrors: true,
});

// 2. Schema definition
const UserSchema = v.object({
    username: v.pipe(v.string(), v.minLength(3, "Username must be at least 3 characters")),
    email: v.pipe(v.string(), v.email("Invalid email address")),
});

// 3. Routes
app.post("/users", async (c) => {
    const body = await c.req.json();
    try {
        const user = v.parse(UserSchema, body);
        return c.json({ status: "success", data: user }, CREATED);
    } catch (err) {
        KitValibotTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
    }
});

app.get("/users/:id", (c) => {
    const id = c.req.param("id");
    if (id !== "42") {
        throw new KitHttpError(NOT_FOUND, "User not found", { userId: id });
    }
    return c.json({ id: "42", username: "alex" });
});

export default app;

