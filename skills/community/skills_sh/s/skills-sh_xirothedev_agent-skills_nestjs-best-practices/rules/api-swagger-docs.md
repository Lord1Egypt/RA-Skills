---
title: Generate Swagger/OpenAPI Documentation
impact: MEDIUM
section: 8
impactDescription: Enables automatic API documentation and client generation
tags: documentation, swagger, openapi, api
---

## Generate Swagger/OpenAPI Documentation

Undocumented APIs force clients to guess endpoints and payloads. NestJS Swagger module auto-generates interactive OpenAPI docs from controllers. **All public APIs must be self-documenting.**

**Incorrect (no documentation):**

```typescript
// users.controller.ts - Clients must guess schema 🚨
@Controller('users')
export class UsersController {
  @Post()
  create(@Body() data: any) {
    return this.usersService.create(data);
  }
}
```

**Correct (auto-generated docs):**

```typescript
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  const config = new DocumentBuilder()
    .setTitle('Users API')
    .setDescription('User management endpoints')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
    
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);  // ✅ Interactive docs
  
  await app.listen(3000);
}

// users.controller.ts
@ApiTags('users')
@ApiBearerAuth()
@Controller('users')
export class UsersController {
  @Post()
  @ApiOperation({ summary: 'Create new user' })
  @ApiResponse({ status: 201, description: 'User created', type: UserDto })
  @ApiResponse({ status: 400, description: 'Invalid input' })
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```