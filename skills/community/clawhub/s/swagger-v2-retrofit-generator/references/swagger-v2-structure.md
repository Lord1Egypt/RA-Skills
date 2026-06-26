# Swagger v2 结构参考

Swagger v2 (OpenAPI 2.0) 规范的核心结构。

## 根对象

```json
{
  "swagger": "2.0",
  "info": { ... },
  "host": "api.example.com",
  "basePath": "/v1",
  "schemes": ["https"],
  "consumes": ["application/json"],
  "produces": ["application/json"],
  "paths": { ... },
  "definitions": { ... },
  "securityDefinitions": { ... }
}
```

## Paths 结构

```json
{
  "paths": {
    "/users/{id}": {
      "get": {
        "operationId": "getUserById",
        "summary": "Get user by ID",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "type": "string"
          },
          {
            "name": "includeDeleted",
            "in": "query",
            "required": false,
            "type": "boolean"
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "schema": {
              "$ref": "#/definitions/User"
            }
          }
        }
      }
    }
  }
}
```

### 参数位置 (in)

| 值 | 说明 | Retrofit 注解 |
|---|------|--------------|
| path | URL 路径参数 | @Path |
| query | URL 查询参数 | @Query |
| header | HTTP 头 | @Header |
| body | 请求体 (POST/PUT) | @Body |
| formData | 表单数据 | @Field |

## Definitions 结构

```json
{
  "definitions": {
    "User": {
      "type": "object",
      "properties": {
        "id": { "type": "integer", "format": "int64" },
        "username": { "type": "string" },
        "email": { "type": "string" },
        "roles": {
          "type": "array",
          "items": { "$ref": "#/definitions/Role" }
        }
      },
      "required": ["id", "username"]
    }
  }
}
```

### 类型映射

| Swagger 类型 | Kotlin 类型 |
|-------------|-------------|
| string | String |
| integer (int32) | Int |
| integer (int64) | Long |
| number (float) | Float |
| number (double) | Double |
| boolean | Boolean |
| array | List<T> |
| object (inline) | Any |
| $ref | 引用类型名 |

## 认证方式

### Basic Auth

```json
{
  "securityDefinitions": {
    "basicAuth": {
      "type": "basic"
    }
  }
}
```

### Bearer Token (JWT)

```json
{
  "securityDefinitions": {
    "bearerAuth": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header"
    }
  }
}
```

### API Key

```json
{
  "securityDefinitions": {
    "apiKey": {
      "type": "apiKey",
      "name": "X-API-Key",
      "in": "header"
    }
  }
}
```
