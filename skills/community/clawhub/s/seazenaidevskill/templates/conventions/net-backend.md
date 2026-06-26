# .NET 后端编码规范

> 本规范适用于 .NET（ASP.NET Core/C#）项目，AI 编码时必须遵守。如有与项目 `docs/architecture/coding-convention.md` 冲突之处，以项目文档为准。

## 一、项目结构

```
ProjectName/
├── Controllers/        ← 接口层：只做路由和参数绑定
├── Services/           ← 业务层：接口+实现
│   └── Impl/
├── Repositories/       ← 数据访问层
├── Domain/             ← 领域实体（Entity 与数据库一一对应）
├── Dtos/               ← 数据传输对象：Request/Response
├── Infrastructure/     ← 基础设施：DbContext、缓存、邮件等
├── Common/             ← 公共类：统一返回体、异常、工具类
│   ├── ApiResult.cs         ← 统一返回体 {Code, Message, Data}
│   ├── BusinessException.cs ← 业务异常
│   └── ErrorCode.cs         ← 错误码
├── Configurations/     ← 配置类（Config/Settings）
├── Middlewares/        ← 自定义中间件
├── Filters/            ← Action Filter / Exception Filter
├── Enums/              ← 枚举定义
└── appsettings.json
```

### 分层约束
| 层 | 允许调用 | 禁止 |
|----|---------|------|
| Controller | Service | 直接调 Repository |
| Service | Repository、其他 Service | 操作 HttpContext |
| Repository | DbContext、Entity | 调用 Service |

## 二、命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `UserService`, `OrderController` |
| 接口 | `I` 前缀 + PascalCase | `IUserService` |
| 方法名 | PascalCase | `GetUserById`, `CreateOrder` |
| 变量名 | camelCase | `userName`, `orderList` |
| 私有字段 | `_camelCase` | `_dbContext`, `_logger` |
| 常量 | PascalCase | `MaxRetryCount` |
| 命名空间 | PascalCase，点分隔 | `Company.Project.User.Controllers` |
| 异步方法 | `Async` 后缀 | `GetUserByIdAsync` |
| 数据库表名 | snake_case | `t_user`, `t_order_item` |
| API 路由 | kebab-case | `/api/user-orders/{id}` |

### Controller 方法命名
- 查询列表：`GetList` / `GetPage`
- 查询单个：`Get` / `GetById`
- 新增：`Create` / `Add`
- 修改：`Update` / `Modify`
- 删除：`Delete` / `Remove`

## 三、API 设计（RESTful）

### 请求方式
| 操作 | 方法 | 路由示例 |
|------|------|---------|
| 分页查询 | `[HttpGet]` | `/api/users?page=1&size=20` |
| 单个查询 | `[HttpGet("{id}")]` | `/api/users/{id}` |
| 新增 | `[HttpPost]` | `/api/users` |
| 修改 | `[HttpPut("{id}")]` | `/api/users/{id}` |
| 删除 | `[HttpDelete("{id}")]` | `/api/users/{id}` |

### 必须遵守
- 所有 API 返回统一的 `ApiResult<T>`，不允许直接返回裸数据
- Controller 必须标注 `[ApiController]` 和 `[Route("api/[controller]")]`
- 请求参数必须使用 `[FromBody]`、`[FromQuery]`、`[FromRoute]` 明确标注
- 所有方法默认 `async Task<ActionResult<T>>`，除非确认为同步

## 四、Controller 规范

```csharp
[ApiController]
[Route("api/users")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet]
    public async Task<ActionResult<ApiResult<List<UserDto>>>> GetList(
        [FromQuery] UserQueryDto query)
    {
        var result = await _userService.GetListAsync(query);
        return Ok(ApiResult<List<UserDto>>.Success(result));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ApiResult<UserDto>>> Get(string id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound(ApiResult<UserDto>.Fail("用户不存在"));
        return Ok(ApiResult<UserDto>.Success(user));
    }
}
```

- Controller 只做参数绑定和返回，**零业务逻辑**
- 所有输入参数必须做 Model Validation（`[Required]`、`[Range]` 等）

## 五、Entity Framework Core 规范

### 实体定义
```csharp
public class User : BaseEntity
{
    public string UserName { get; set; }
    public string Email { get; set; }
    // 导航属性
    public virtual ICollection<Order> Orders { get; set; }
}

public abstract class BaseEntity
{
    [Key]
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; }
    public bool IsDeleted { get; set; }  // 软删除
}
```

### 必须遵守
- 禁止直接拼接 SQL，必须使用 LINQ 或参数化
- 禁止在循环中调用 `SaveChanges`，批量操作后统一保存
- 查询投影使用 `Select` 到 DTO，不直接在 Controller 返回 Entity
- 逻辑删除使用 `IsDeleted` 字段 + 全局查询过滤器
- 所有表必须包含：`Id`、`CreatedAt`、`UpdatedAt`、`IsDeleted`

## 六、异常处理

```csharp
// 全局异常过滤器 + 业务异常
public class BusinessException : Exception
{
    public string ErrorCode { get; }
    public BusinessException(string errorCode, string message) : base(message)
    {
        ErrorCode = errorCode;
    }
}

// 使用
throw new BusinessException("USR001", "用户不存在");
```

- 禁止在 Controller 中 `try-catch` 后返回 null
- 禁止吞异常（catch 后不处理也不 rethrow）
- 全局 ExceptionFilter 统一处理异常并返回标准格式

## 七、日志规范

```csharp
public class UserService : IUserService
{
    private readonly ILogger<UserService> _logger;

    public async Task<UserDto> GetByIdAsync(string id)
    {
        _logger.LogInformation("查询用户, userId={UserId}", id);
        // ...
    }
}
```

- 使用 `ILogger<T>` 依赖注入，禁止 `Console.WriteLine`
- **禁止**在日志中打印密码、Token、身份证号
- LogInformation：关键业务节点；LogWarning：可恢复异常；LogError：带异常对象的错误

## 八、安全规范

- 所有公开 API 必须经过认证（`[Authorize]`）
- SQL 查询必须 EF Core LINQ，禁止拼接
- 敏感字段（密码）使用 BCrypt 或 ASP.NET Core Identity 内置哈希
- 返回 DTO 不得包含密码字段
- 文件上传必须校验扩展名、ContentType 和大小
- 配置中的连接字符串、密钥必须使用 User Secrets / Azure KeyVault，不硬编码

## 九、测试规范

- Service 层使用 xUnit + Moq 单元测试
- Controller 层使用 `WebApplicationFactory` 集成测试
- 测试类命名：`XxxTests`，测试方法命名：`Method_Scenario_Expected`
- 必须覆盖：正常流程 + 边界条件 + 异常流程
