---
name: swagger2-to-openapi3
description: Use when migrating Java Spring Boot projects from Swagger 2 (Springfox) to OpenAPI 3.0 (SpringDoc), including annotation replacements, import updates, and javax-to-jakarta migration. Triggers on mentions of Swagger upgrade, OpenAPI migration, springfox to springdoc, or API documentation migration.
---

# Swagger 2 到 OpenAPI 3.0 迁移指南

## Overview

本 Skill 提供从 Swagger 2 (Springfox) 迁移到 OpenAPI 3.0 (SpringDoc) 的完整指南，包括：
- 注解替换对照表
- 自动替换脚本
- 包名迁移（javax → jakarta）
- 常见问题和解决方案

## When to Use

- 升级 Spring Boot 2.x → 3.x
- 迁移 Swagger 2 → OpenAPI 3.0
- 更换 springfox → springdoc
- javax 包升级到 jakarta

## 注解替换速查表

| Swagger 2 | OpenAPI 3.0 | 说明 |
|-----------|-------------|------|
| `@Api` | `@Tag` | 类/接口标注 |
| `@ApiOperation` | `@Operation` | 方法标注 |
| `@ApiParam` | `@Parameter` | 参数标注 |
| `@ApiModel` | `@Schema` | 模型类标注 |
| `@ApiModelProperty` | `@Schema` | 模型属性标注 |
| `@ApiResponse` | `@ApiResponse` | 响应标注（保留） |
| `@ApiResponses` | `@ApiResponses` | 多响应标注（保留） |
| `@ApiImplicitParam` | `@Parameter` | 隐式参数 |
| `@ApiImplicitParams` | `@Parameters` | 多隐式参数 |

## 核心替换规则

### 1. 类级别注解

**@Api → @Tag**
```java
// Before (Swagger 2)
@Api(tags = "用户管理")
public class UserController {}

// After (OpenAPI 3.0)
@Tag(name = "用户管理")
public class UserController {}
```

### 2. 方法级别注解

**@ApiOperation → @Operation**
```java
// Before
@ApiOperation(value = "获取用户信息", notes = "根据ID获取用户详情")
public User getUser(@ApiParam("用户ID") Long id) {}

// After
@Operation(summary = "获取用户信息", description = "根据ID获取用户详情")
public User getUser(@Parameter(description = "用户ID") Long id) {}
```

**Response 处理（复杂替换）**
```java
// Before
@ApiOperation(value = "查询用户", response = User.class)
public ResponseEntity<User> query() {}

// After
@Operation(
    summary = "查询用户",
    responses = {
        @ApiResponse(
            responseCode = "200",
            content = @Content(schema = @Schema(implementation = User.class))
        )
    }
)
public ResponseEntity<User> query() {}
```

### 3. 模型类注解

**@ApiModel → @Schema**
```java
// Before
@ApiModel(value = "用户对象", description = "用户信息")
public class UserDTO {}

// After
@Schema(description = "用户对象")
public class UserDTO {}
```

**@ApiModelProperty → @Schema**
```java
// Before
@ApiModelProperty(value = "用户名", required = true, example = "张三")
private String username;

// After
@Schema(description = "用户名", requiredMode = Schema.RequiredMode.REQUIRED, example = "张三")
private String username;
```

## 包名替换

### Swagger 包替换
```java
// 旧包 (Swagger 2)
import io.swagger.annotations.*;

// 新包 (OpenAPI 3.0)
import io.swagger.v3.oas.annotations.*;
import io.swagger.v3.oas.annotations.media.*;
import io.swagger.v3.oas.annotations.responses.*;
import io.swagger.v3.oas.annotations.parameters.*;
```

### 详细替换对照表

| 旧包 (Swagger 2) | 新包 (OpenAPI 3.0) |
|-----------------|-------------------|
| `io.swagger.annotations.Api` | `io.swagger.v3.oas.annotations.tags.Tag` |
| `io.swagger.annotations.ApiOperation` | `io.swagger.v3.oas.annotations.Operation` |
| `io.swagger.annotations.ApiParam` | `io.swagger.v3.oas.annotations.Parameter` |
| `io.swagger.annotations.ApiModel` | `io.swagger.v3.oas.annotations.media.Schema` |
| `io.swagger.annotations.ApiModelProperty` | `io.swagger.v3.oas.annotations.media.Schema` |
| `io.swagger.annotations.ApiResponse` | `io.swagger.v3.oas.annotations.responses.ApiResponse` |
| `io.swagger.annotations.ApiResponses` | `io.swagger.v3.oas.annotations.responses.ApiResponses` |

### javax → jakarta 包替换

| 旧包 (javax) | 新包 (jakarta) |
|-------------|---------------|
| `javax.annotation.Resource` | `jakarta.annotation.Resource` |
| `javax.annotation.PostConstruct` | `jakarta.annotation.PostConstruct` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.servlet.*` | `jakarta.servlet.*` |

## 自动迁移脚本

### 使用说明

本 skill 提供自动化脚本帮助快速完成迁移：

```bash
# 1. 执行完整迁移（注解 + 包名）
python scripts/migrate_swagger_to_openapi.py --project-path /path/to/your/project

# 2. 仅迁移注解
python scripts/migrate_annotations.py --project-path /path/to/your/project

# 3. 仅迁移包名
python scripts/migrate_imports.py --project-path /path/to/your/project
```

### 手动迁移建议

对于复杂的迁移场景，建议分步进行：

1. **先备份项目**
2. **全局替换包名**（使用 IDE 的全局替换功能）
3. **逐个文件检查注解替换**
4. **特别注意 Response 相关的复杂替换**

## 常见问题

### Q1: @Api 的 tags 属性如何转换？
**A:** `tags` → `name`，多标签使用多个 @Tag 注解
```java
// Before
@Api(tags = {"用户管理", "账号管理"})

// After
@Tag(name = "用户管理")
@Tag(name = "账号管理")
```

### Q2: @ApiOperation 的 value 和 notes 如何对应？
**A:** `value` → `summary`，`notes` → `description`
```java
// Before
@ApiOperation(value = "获取用户", notes = "详细说明...")

// After
@Operation(summary = "获取用户", description = "详细说明...")
```

### Q3: response 属性最复杂，如何处理？
**A:** 需要使用 @ApiResponse + @Content + @Schema 组合
```java
// Before
@ApiOperation(value = "查询", response = User.class)

// After
@Operation(
    summary = "查询",
    responses = {
        @ApiResponse(
            responseCode = "200",
            content = @Content(schema = @Schema(implementation = User.class))
        )
    }
)
```

### Q4: 升级后 Swagger UI 无法访问？
**A:** 检查以下配置：
1. 添加 springdoc-openapi-starter-webmvc-ui 依赖
2. 配置 springdoc.api-docs.enabled=true
3. 访问地址从 /swagger-ui.html 变为 /swagger-ui/index.html

### Q5: javax 包找不到？
**A:** Spring Boot 3.x 已迁移到 Jakarta EE，需要：
1. 将所有 `javax.*` 替换为 `jakarta.*`
2. 更新 pom.xml 中的依赖版本
3. 清理并重新构建项目

## 总结

迁移要点：
1. **注解层面**：@Api→@Tag, @ApiOperation→@Operation, @ApiModel→@Schema
2. **包层面**：swagger.annotations → swagger.v3.oas.annotations
3. **JDK层面**：javax.* → jakarta.*
4. **最复杂的是 Response 处理**，需要组合多个注解

建议按文件逐个检查，特别注意复杂的 @ApiResponse 场景。
