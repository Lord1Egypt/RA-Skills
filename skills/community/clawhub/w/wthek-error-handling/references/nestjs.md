# NestJS Error Handling with @wthek

Guide for implementing `@wthek/nestjs-middleware`.

---

## Installation

```bash
npm install @wthek/nestjs-middleware http-error-kit http-response-status-code
```

Also ensure the underlying platform adapter package is installed:
- For Express (default): `@wthek/express-middleware`
- For Fastify: `@wthek/fastify-middleware`

---

## 1. Global Filter Registration (in `main.ts`)

NestJS applications can apply `KitExceptionFilter` globally. The filter automatically detects whether your application is running on the **Express** or **Fastify** adapter:

```typescript
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { KitExceptionFilter } from "@wthek/nestjs-middleware";

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    // Apply the Kit exception filter globally with options
    app.useGlobalFilters(
        new KitExceptionFilter({
            log: true,
            handleUnknownErrors: true,
        })
    );

    await app.listen(3000);
}
bootstrap();
```

---

## 2. Module Provider Registration (in `app.module.ts`)

Alternatively, register the filter as an `APP_FILTER` provider to allow dependency injection (such as custom NestJS loggers):

```typescript
import { Module } from "@nestjs/common";
import { APP_FILTER } from "@nestjs/core";
import { KitExceptionFilter } from "@wthek/nestjs-middleware";

@Module({
    providers: [
        {
            provide: APP_FILTER,
            useValue: new KitExceptionFilter({
                log: (error, req) => {
                    console.error("NestJS Error caught:", error);
                },
                handleUnknownErrors: true,
            }),
        },
    ],
})
export class AppModule {}
```

---

## Options Reference

```typescript
interface IKitNestJsMiddlewareOptions {
    // Optional logger flag or custom callback:
    log?: boolean | ((error: unknown, req: unknown) => void);

    // When true, wraps unexpected runtime errors in a structured 500 JSON response:
    handleUnknownErrors?: boolean;
}
```

