---
title: Never Hardcode Secrets - Use Environment Variables
impact: CRITICAL
impactDescription: Prevents credential leaks in source control
section: 9
tags: security, config, environment, secrets
---

## Never Hardcode Secrets - Use Environment Variables

Hardcoded credentials in source code get committed to git and exposed publicly. The `@nestjs/config` package provides a secure way to manage configuration through environment variables. **Secrets belong in environment only.**

### Installation

```bash
bun add @nestjs/config
```

**Incorrect:**

```typescript
// database.module.ts
TypeOrmModule.forRoot({
  url: 'postgres://user:password@localhost/db',  // 🚨 Exposed!
  ssl: {
    cert: process.env.DB_CERT,  // Still vulnerable if cert is committed
  },
})

// auth.service.ts
@Injectable()
export class AuthService {
  private readonly jwtSecret = 'my-super-secret-key-12345';  // 🚨 Exposed!
  private readonly apiKey = 'sk_test_abc123xyz';  // 🚨 Exposed!
}

// payment.controller.ts
const stripe = require('stripe')('sk_test_51ABC...');  // 🚨 Exposed!
```

**Correct:**

```typescript
// app.module.ts
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: `.env.${process.env.NODE_ENV || 'development'}`,
      cache: true,
    }),
  ],
})
export class AppModule {}

// database.module.ts
import { ConfigService } from '@nestjs/config';

TypeOrmModule.forRootAsync({
  imports: [ConfigModule],
  inject: [ConfigService],
  useFactory: (configService: ConfigService) => ({
    url: configService.getOrThrow('DATABASE_URL'),  // ✅ Secure
    ssl: configService.get('DB_SSL') === 'true' ? {
      cert: configService.get('DB_CERT'),
    } : false,
  }),
})

// auth.service.ts
@Injectable()
export class AuthService {
  constructor(private configService: ConfigService) {}

  private get jwtSecret(): string {
    return this.configService.getOrThrow('JWT_SECRET');  // ✅ Secure
  }
}

// payment.module.ts
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
  imports: [
    StripeModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        apiKey: configService.getOrThrow('STRIPE_SECRET_KEY'),  // ✅ Secure
        webhookSecret: configService.get('STRIPE_WEBHOOK_SECRET'),
      }),
    }),
  ],
})
export class PaymentModule {}
```

## Type-Safe Configuration with Validation

Use Joi or Zod to validate environment variables at startup:

```typescript
// app.module.ts
import * as Joi from 'joi';

ConfigModule.forRoot({
  isGlobal: true,
  validationSchema: Joi.object({
    // Database
    DATABASE_URL: Joi.string().required(),
    DB_HOST: Joi.string().required(),
    DB_PORT: Joi.number().default(5432),
    DB_USERNAME: Joi.string().required(),
    DB_PASSWORD: Joi.string().required(),

    // JWT
    JWT_SECRET: Joi.string().min(32).required(),
    JWT_EXPIRES_IN: Joi.string().default('1d'),

    // API Keys
    STRIPE_SECRET_KEY: Joi.string().when('NODE_ENV', {
      is: 'production',
      then: Joi.required(),
      otherwise: Joi.optional(),
    }),
  }),
  validationOptions: {
    abortEarly: false,  // Show all errors
    allowUnknown: true,
  },
})
```

## Custom Configuration with Namespaces

Use `registerAs` for type-safe, grouped configuration:

```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT, 10) || 5432,
  username: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
}));

// config/jwt.config.ts
export default registerAs('jwt', () => ({
  secret: process.env.JWT_SECRET,
  expiresIn: process.env.JWT_EXPIRES_IN || '1d',
  refreshSecret: process.env.JWT_REFRESH_SECRET,
  refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d',
}));

// config/index.ts
import databaseConfig from './database.config';
import jwtConfig from './jwt.config';

export default [databaseConfig, jwtConfig];

// app.module.ts
ConfigModule.forRoot({
  isGlobal: true,
  load: [config],
})

// Using in services
@Injectable()
export class MyService {
  constructor(private configService: ConfigService) {}

  getDbHost(): string {
    return this.configService.get<string>('database.host');
  }

  getJwtSecret(): string {
    return this.configService.getOrThrow('jwt.secret');
  }
}
```

## Environment-Specific Configuration

```bash
# .env.development
NODE_ENV=development
DATABASE_URL=postgres://localhost:5432/dev_db
JWT_SECRET=dev-secret-key

# .env.production
NODE_ENV=production
DATABASE_URL=postgres://prod-server:5432/prod_db
JWT_SECRET=${PROD_JWT_SECRET}

# .env.test
NODE_ENV=test
DATABASE_URL=postgres://localhost:5432/test_db
JWT_SECRET=test-secret-key
```

## .env.example Template

Always provide a `.env.example` file to document required variables:

```bash
# Application
NODE_ENV=development|production|test
PORT=3000

# Database (Required)
DATABASE_URL=
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=
DB_PASSWORD=
DB_DATABASE=

# JWT (Required - min 32 characters)
JWT_SECRET=
JWT_EXPIRES_IN=1d
JWT_REFRESH_SECRET=
JWT_REFRESH_EXPIRES_IN=7d

# API Keys (Optional)
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
SENDGRID_API_KEY=
```

## Production Considerations

```typescript
// For production, ignore .env files and use process.env only
ConfigModule.forRoot({
  isGlobal: true,
  ignoreEnvFile: process.env.NODE_ENV === 'production',
  validationSchema: productionValidationSchema,
})
```

**Sources:**
- [Configuration | NestJS - Official Documentation](https://docs.nestjs.com/techniques/configuration)
- [Managing Environment Variables in NestJS with ConfigModule | Medium](https://medium.com/@hashirmughal1000/managing-environment-variables-in-nestjs-with-configmodule-5b0742efb69c)
- [Managing Configuration and Environment Variables in NestJS | dev.to](https://dev.to/vishnucprasad/managing-configuration-and-environment-variables-in-nestjs-28ni)
- [NestJS Environment Configuration Using Zod | Medium](https://medium.com/@rotemdoar17/nestjs-environment-configuration-using-zod-92e3decca5ca)
