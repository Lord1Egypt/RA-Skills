import Koa from "koa";
import bodyParser from "koa-bodyparser";
import { KitKoaMiddleware } from "@wthek/koa-middleware";
import { KitTypeBoxTransformer } from "@wthek/typebox-transformer";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, UNPROCESSABLE_ENTITY, CREATED } from "http-response-status-code";
import { Type, Static } from "@sinclair/typebox";
import { Value } from "@sinclair/typebox/value";

const app = new Koa();

// 1. Error middleware MUST be mounted at the top of the Koa stack
app.use(
    KitKoaMiddleware({
        log: true,
        handleUnknownErrors: true,
        emitAppError: true,
    })
);

app.use(bodyParser());

// 2. Schema definition
const CreateItemSchema = Type.Object({
    title: Type.String({ minLength: 3 }),
    price: Type.Number({ minimum: 0 }),
});

type CreateItemDto = Static<typeof CreateItemSchema>;

// 3. Application routes
app.use(async (ctx) => {
    if (ctx.method === "POST" && ctx.path === "/items") {
        try {
            Value.Assert(CreateItemSchema, ctx.request.body);
            const data = ctx.request.body as CreateItemDto;
            ctx.status = CREATED;
            ctx.body = { status: "created", item: data };
        } catch (err: unknown) {
            KitTypeBoxTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
        }
        return;
    }

    if (ctx.method === "GET" && ctx.path === "/items/1") {
        ctx.body = { id: 1, title: "Standard Item", price: 29.99 };
        return;
    }

    throw new KitHttpError(NOT_FOUND, "Route not found", { path: ctx.path });
});

export default app;

