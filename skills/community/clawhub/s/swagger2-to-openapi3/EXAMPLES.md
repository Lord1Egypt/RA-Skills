# 使用示例

本文档提供 `swagger2-to-openapi3` skill 的使用示例。

## 示例 1: 使用 OpenCode 直接迁移

最简单的方式是在 OpenCode 中描述你的需求：

```
帮我把 /path/to/my-project 从 Swagger 2 迁移到 OpenAPI 3.0
```

OpenCode 会自动：
1. 加载 swagger2-to-openapi3 skill
2. 分析项目结构
3. 生成迁移脚本
4. 执行迁移（或提供详细的迁移指南）

## 示例 2: 使用 Python 脚本直接迁移

### 步骤 1: 进入 skill 目录

```bash
cd skills/swagger2-to-openapi3
```

### 步骤 2: 预览迁移（推荐）

在正式迁移前，先预览将要做的修改：

```bash
python scripts/migrate_swagger_to_openapi.py \
  --project-path /path/to/your/project \
  --dry-run
```

输出示例：
```
============================================================
Swagger 2 → OpenAPI 3.0 迁移工具
项目路径: /path/to/your/project
模式: 预览 (dry-run)
============================================================

找到 150 个 Java 文件

[Dry Run] 将修改: src/main/java/com/example/controller/UserController.java (8 处替换)
  [Api-tags]: 1 处替换
  [ApiOperation-value]: 3 处替换
  [ApiParam-value]: 4 处替换
[Dry Run] 将修改: src/main/java/com/example/dto/UserDTO.java (5 处替换)
  [ApiModel-description]: 1 处替换
  [ApiModelProperty-value]: 4 处替换

============================================================
迁移统计:
============================================================
处理文件数: 150
修改文件数: 45
注解替换数: 386
Import 替换数: 124

这是预览模式，实际未修改文件。
如需执行实际迁移，请去掉 --dry-run 参数
```

### 步骤 3: 执行实际迁移

确认预览结果无误后，执行实际迁移：

```bash
python scripts/migrate_swagger_to_openapi.py \
  --project-path /path/to/your/project
```

输出示例：
```
============================================================
Swagger 2 → OpenAPI 3.0 迁移工具
项目路径: /path/to/your/project
模式: 实际执行
============================================================

找到 150 个 Java 文件

✓ 已修改: src/main/java/com/example/controller/UserController.java (8 处替换)
✓ 已修改: src/main/java/com/example/dto/UserDTO.java (5 处替换)
✓ 已修改: src/main/java/com/example/controller/OrderController.java (12 处替换)
...

============================================================
迁移统计:
============================================================
处理文件数: 150
修改文件数: 45
注解替换数: 386
Import 替换数: 124
```

## 示例 3: 单独迁移注解或 Import

如果你只想迁移特定部分，可以使用专用脚本：

### 仅迁移注解（不处理 import）

```bash
python scripts/migrate_annotations.py \
  --project-path /path/to/your/project \
  --dry-run  # 预览模式
```

### 仅迁移 Import 语句

```bash
python scripts/migrate_imports.py \
  --project-path /path/to/your/project \
  --dry-run  # 预览模式
```

## 示例 4: 典型的迁移工作流

### 场景：将 Spring Boot 2.x 项目升级到 3.x

**步骤 1: 备份项目**
```bash
cd /path/to/project
git checkout -b swagger-to-openapi-migration
```

**步骤 2: 更新 pom.xml 依赖**

将 Springfox 依赖替换为 SpringDoc：

```xml
<!-- 删除旧的 Swagger 2 依赖 -->
<!-- <dependency> -->
<!--     <groupId>io.springfox</groupId> -->
<!--     <artifactId>springfox-swagger2</artifactId> -->
<!-- </dependency> -->
<!-- <dependency> -->
<!--     <groupId>io.springfox</groupId> -->
<!--     <artifactId>springfox-swagger-ui</artifactId> -->
<!-- </dependency> -->

<!-- 添加新的 OpenAPI 3.0 依赖 -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

**步骤 3: 执行自动迁移**

```bash
# 进入项目目录
cd /path/to/project

# 执行迁移（先预览）
python /path/to/skills/swagger2-to-openapi3/scripts/migrate_swagger_to_openapi.py \
  --project-path . \
  --dry-run

# 确认无误后，执行实际迁移
python /path/to/skills/swagger2-to-openapi3/scripts/migrate_swagger_to_openapi.py \
  --project-path .
```

**步骤 4: 手动检查复杂场景**

自动迁移完成后，需要手动检查以下场景：

1. **包含 `response` 属性的 `@ApiOperation`**
   ```java
   // 需要手动将：
   @ApiOperation(value = "查询", response = User.class)
   // 替换为：
   @Operation(summary = "查询", responses = {
       @ApiResponse(responseCode = "200", 
           content = @Content(schema = @Schema(implementation = User.class)))
   })
   ```

2. **使用 `@ApiImplicitParam` 的复杂场景**

3. **自定义扩展注解**

**步骤 5: 编译并测试**

```bash
# 清理并编译
mvn clean compile

# 运行测试
mvn test

# 启动应用并验证 Swagger UI
mvn spring-boot:run
```

访问新的 Swagger UI 地址：
- 旧地址：`http://localhost:8080/swagger-ui.html`
- 新地址：`http://localhost:8080/swagger-ui/index.html`

**步骤 6: 提交变更**

```bash
git add .
git commit -m "refactor: 迁移 Swagger 2 到 OpenAPI 3.0

- 替换所有 Swagger 2 注解为 OpenAPI 3.0 注解
- 更新 import 语句
- 迁移 javax 包到 jakarta 包
- 更新 pom.xml 依赖"
```

## 迁移前后对比

### Controller 类对比

**迁移前 (Swagger 2):**
```java
@RestController
@RequestMapping("/api/users")
@Api(tags = "用户管理")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    @ApiOperation(value = "获取用户信息", notes = "根据用户ID获取用户详细信息")
    public Result<UserDTO> getUser(
            @ApiParam(value = "用户ID", required = true) @PathVariable Long id) {
        return Result.success(userService.getById(id));
    }
    
    @PostMapping
    @ApiOperation(value = "创建用户", notes = "创建新用户")
    public Result<Long> createUser(
            @ApiParam(value = "用户信息", required = true) @RequestBody UserCreateDTO dto) {
        return Result.success(userService.create(dto));
    }
}
```

**迁移后 (OpenAPI 3.0):**
```java
@RestController
@RequestMapping("/api/users")
@Tag(name = "用户管理")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    @Operation(summary = "获取用户信息", description = "根据用户ID获取用户详细信息")
    public Result<UserDTO> getUser(
            @Parameter(description = "用户ID", required = true) @PathVariable Long id) {
        return Result.success(userService.getById(id));
    }
    
    @PostMapping
    @Operation(summary = "创建用户", description = "创建新用户")
    public Result<Long> createUser(
            @Parameter(description = "用户信息", required = true) @RequestBody UserCreateDTO dto) {
        return Result.success(userService.create(dto));
    }
}
```

### DTO 类对比

**迁移前 (Swagger 2):**
```java
@ApiModel(value = "用户信息", description = "用户详细信息")
public class UserDTO {
    
    @ApiModelProperty(value = "用户ID", required = true, example = "10001")
    private Long id;
    
    @ApiModelProperty(value = "用户名", required = true, example = "张三")
    private String username;
    
    @ApiModelProperty(value = "邮箱", example = "zhangsan@example.com")
    private String email;
    
    @ApiModelProperty(value = "创建时间", example = "2024-01-15 10:30:00")
    private LocalDateTime createTime;
    
    // getters and setters
}
```

**迁移后 (OpenAPI 3.0):**
```java
@Schema(description = "用户信息")
public class UserDTO {
    
    @Schema(description = "用户ID", requiredMode = Schema.RequiredMode.REQUIRED, example = "10001")
    private Long id;
    
    @Schema(description = "用户名", requiredMode = Schema.RequiredMode.REQUIRED, example = "张三")
    private String username;
    
    @Schema(description = "邮箱", example = "zhangsan@example.com")
    private String email;
    
    @Schema(description = "创建时间", example = "2024-01-15 10:30:00")
    private LocalDateTime createTime;
    
    // getters and setters
}
```

## 最佳实践

### 1. 始终先使用预览模式
在实际执行迁移前，务必先使用 `--dry-run` 参数预览将要做的修改，确保理解迁移工具会做什么。

### 2. 在版本控制下工作
确保项目已纳入版本控制（如 Git），这样可以在迁移出现问题时轻松回滚。

### 3. 分步骤验证
对于大型项目，建议分模块进行迁移，每个模块验证通过后再进行下一个。

### 4. 处理特殊情况
迁移工具无法自动处理所有场景，特别是：
- 包含 `response` 属性的 `@ApiOperation`
- 复杂的 `@ApiImplicitParam` 配置
- 自定义扩展注解

这些需要手动检查和调整。

### 5. 更新文档
迁移完成后，记得更新相关文档，包括：
- API 文档说明
- 开发环境配置指南
- Swagger UI 访问地址

## 故障排除

### 问题 1: 迁移后编译失败
**可能原因:**
- 某些 import 语句未正确替换
- 新旧注解混用导致冲突

**解决方案:**
1. 检查编译错误信息，定位问题文件
2. 手动修复未正确替换的 import 或注解
3. 确保所有 Swagger 2 依赖已从 pom.xml 中移除

### 问题 2: Swagger UI 无法访问
**可能原因:**
- SpringDoc 依赖未正确添加
- 配置文件缺少必要配置

**解决方案:**
1. 确认 pom.xml 中包含 springdoc-openapi-starter-webmvc-ui 依赖
2. 在 application.yml 中添加配置：
   ```yaml
   springdoc:
     api-docs:
       enabled: true
     swagger-ui:
       enabled: true
   ```
3. 确认访问地址正确：`http://localhost:8080/swagger-ui/index.html`

### 问题 3: javax 包找不到
**可能原因:**
- Spring Boot 3.x 已迁移到 Jakarta EE
- 某些依赖仍使用 javax 包

**解决方案:**
1. 使用本 skill 的 import 迁移功能：
   ```bash
   python scripts/migrate_imports.py --project-path /path/to/project
   ```
2. 检查并更新所有依赖到支持 Jakarta EE 的版本
3. 清理并重新构建项目：
   ```bash
   mvn clean install
   ```

## 获取更多帮助

如遇到问题，可以：
1. 查看 SKILL.md 中的详细说明
2. 检查示例代码和最佳实践
3. 在 OpenCode 中寻求帮助
