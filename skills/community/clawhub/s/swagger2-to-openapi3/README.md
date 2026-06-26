# Swagger 2 to OpenAPI 3.0 Migration Skill

这是一个用于帮助 Java Spring Boot 项目从 Swagger 2 (Springfox) 迁移到 OpenAPI 3.0 (SpringDoc) 的 OpenCode Skill。

## 功能特性

- ✅ **注解自动替换**：Api→Tag, ApiOperation→Operation 等
- ✅ **包名自动迁移**：swagger.annotations → swagger.v3.oas.annotations
- ✅ **Jakarta 迁移**：javax.* → jakarta.*
- ✅ **预览模式**：先预览变更，确认后再执行
- ✅ **详细统计**：输出迁移统计报告

## 快速开始

### 1. 安装 Skill

将 `swagger2-to-openapi3` 目录复制到你的 OpenCode skills 目录：

```bash
# Linux/Mac
cp -r swagger2-to-openapi3 ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse swagger2-to-openapi3 "$env:USERPROFILE\.config\opencode\skills"
```

### 2. 使用 OpenCode 调用

在 OpenCode 中直接描述你的迁移需求：

```
帮我把 /path/to/project 从 Swagger 2 迁移到 OpenAPI 3.0
```

或

```
迁移这个 Spring Boot 项目的 API 文档到 OpenAPI 3.0，项目路径是 /path/to/project
```

### 3. 直接使用 Python 脚本

```bash
# 先预览变更（推荐）
python scripts/migrate_swagger_to_openapi.py \
  --project-path /path/to/your/project \
  --dry-run

# 确认无误后执行实际迁移
python scripts/migrate_swagger_to_openapi.py \
  --project-path /path/to/your/project
```

## 迁移对照表

### 注解替换

| Swagger 2 | OpenAPI 3.0 |
|-----------|-------------|
| `@Api` | `@Tag` |
| `@ApiOperation` | `@Operation` |
| `@ApiParam` | `@Parameter` |
| `@ApiModel` | `@Schema` |
| `@ApiModelProperty` | `@Schema` |
| `@ApiImplicitParam` | `@Parameter` |
| `@ApiImplicitParams` | `@Parameters` |

### 包名替换

| Swagger 2 | OpenAPI 3.0 |
|-----------|-------------|
| `io.swagger.annotations` | `io.swagger.v3.oas.annotations` |
| `io.swagger.annotations.Api` | `io.swagger.v3.oas.annotations.tags.Tag` |
| `io.swagger.annotations.ApiOperation` | `io.swagger.v3.oas.annotations.Operation` |

### Jakarta EE 迁移

| Java EE | Jakarta EE |
|---------|------------|
| `javax.annotation` | `jakarta.annotation` |
| `javax.persistence` | `jakarta.persistence` |
| `javax.validation` | `jakarta.validation` |
| `javax.servlet` | `jakarta.servlet` |

## 实际迁移示例

### 示例 1: Controller 类

**Before:**
```java
@RestController
@Api(tags = "用户管理")
public class UserController {
    
    @GetMapping("/users/{id}")
    @ApiOperation(value = "获取用户信息", notes = "根据ID获取用户详情")
    public User getUser(
        @ApiParam(value = "用户ID", required = true) @PathVariable Long id
    ) {
        // ...
    }
}
```

**After:**
```java
@RestController
@Tag(name = "用户管理")
public class UserController {
    
    @GetMapping("/users/{id}")
    @Operation(summary = "获取用户信息", description = "根据ID获取用户详情")
    public User getUser(
        @Parameter(description = "用户ID", required = true) @PathVariable Long id
    ) {
        // ...
    }
}
```

### 示例 2: DTO 类

**Before:**
```java
@ApiModel(value = "用户对象", description = "用户信息")
public class UserDTO {
    
    @ApiModelProperty(value = "用户名", required = true, example = "张三")
    private String username;
    
    @ApiModelProperty(value = "年龄", example = "25")
    private Integer age;
}
```

**After:**
```java
@Schema(description = "用户对象")
public class UserDTO {
    
    @Schema(description = "用户名", requiredMode = Schema.RequiredMode.REQUIRED, example = "张三")
    private String username;
    
    @Schema(description = "年龄", example = "25")
    private Integer age;
}
```

## 注意事项

### 1. 备份项目
迁移前务必备份项目或确保代码已提交到版本控制

### 2. 复杂场景需手动处理
以下场景可能需要手动调整：
- 包含 `response` 属性的 `@ApiOperation`
- 使用 `@ApiImplicitParam` 的复杂场景
- 自定义扩展注解

### 3. 依赖更新
迁移后需要更新 pom.xml 或 build.gradle：

**Maven:**
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

**Gradle:**
```groovy
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
```

### 4. Swagger UI 路径变更
- Swagger 2: `http://localhost:8080/swagger-ui.html`
- OpenAPI 3.0: `http://localhost:8080/swagger-ui/index.html`

## Troubleshooting

### 问题 1: 迁移后注解没有变化
**解决:** 确保文件编码为 UTF-8，且文件有写入权限

### 问题 2: 包名替换后编译错误
**解决:** 检查是否所有 javax 包都已替换为 jakarta，特别是间接依赖

### 问题 3: OpenAPI 注解不生效
**解决:** 确认已添加 springdoc-openapi-starter-webmvc-ui 依赖，且版本与 Spring Boot 版本兼容

## 贡献

欢迎提交 Issue 和 PR 来改进这个迁移工具。

## 许可证

MIT License
