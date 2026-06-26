# Java 后端编码规范

> 本规范适用于 Spring Boot 项目，AI 编码时必须遵守。如有与项目 `docs/architecture/coding-convention.md` 冲突之处，以项目文档为准。

## 一、项目结构

```
src/main/java/com/xxx/
├── controller/     ← 接口层：只做参数校验和路由，不写业务逻辑
├── service/        ← 业务层：接口+实现，业务逻辑写在这里
│   └── impl/
├── mapper/         ← 数据访问层：MyBatis-Plus Mapper 接口
├── entity/         ← 数据库实体（与表一一对应，不包含业务逻辑）
├── dto/            ← 数据传输对象：request/response，与前端交互
├── vo/             ← 视图对象：返回给前端的展示数据
├── config/         ← 配置类
├── common/         ← 公共类：统一返回体、异常定义、工具类
│   ├── Result.java       ← 统一返回体 {code, message, data}
│   ├── BizException.java ← 业务异常
│   └── ErrorCode.java    ← 错误码枚举
└── enums/          ← 枚举类
```

### 分层约束
| 层 | 允许调用 | 禁止 |
|----|---------|------|
| Controller | Service | 直接调 Mapper |
| Service | Mapper、其他 Service | 直接操作 HttpServletRequest |
| Mapper | Entity、数据库 | 调用 Service |

## 二、命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 类名 | UpperCamelCase | `UserService`, `OrderController` |
| 方法名 | lowerCamelCase | `getUserById`, `createOrder` |
| 变量名 | lowerCamelCase | `userName`, `orderList` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 包名 | 全小写，点分隔 | `com.xxx.user.controller` |
| 数据库表名 | snake_case，复数 | `t_user`, `t_order_item` |
| 数据库字段 | snake_case | `created_at`, `is_deleted` |
| URL 路径 | kebab-case | `/api/user-orders/{id}` |

### Controller 方法命名
- 查询列表：`list` / `page`
- 查询单个：`get` / `getById`
- 新增：`create` / `add`
- 修改：`update` / `modify`
- 删除：`delete` / `remove`
- 批量操作：`batchXxx`

## 三、API 设计（RESTful）

### 请求方式
| 操作 | 方法 | 路径示例 |
|------|------|---------|
| 分页查询 | GET | `/api/users?page=1&size=20` |
| 单个查询 | GET | `/api/users/{id}` |
| 新增 | POST | `/api/users` |
| 修改 | PUT | `/api/users/{id}` |
| 删除 | DELETE | `/api/users/{id}` |

### 必须遵守
- 所有 API 返回统一结构 `Result<T>`，不允许直接返回裸数据
- 分页查询使用 `PageResult<T>` 封装 `{total, page, size, records}`
- 所有时间字段使用 ISO 8601 格式（`yyyy-MM-dd HH:mm:ss`）
- PathVariable 和 RequestParam 必须有明确含义的命名

## 四、数据库访问

### MyBatis-Plus 规范
- 优先使用 LambdaQueryWrapper，禁止字符串拼接 SQL
- 逻辑删除使用 `@TableLogic` 注解，物理删除需评审
- 所有表必须包含字段：`id`、`created_at`、`updated_at`、`is_deleted`
- 禁止在循环中逐条查询数据库，使用 `selectBatchIds` 或 `in` 查询

### 事务管理
- Service 层方法使用 `@Transactional(rollbackFor = Exception.class)`
- 只读操作不加事务
- 事务方法内禁止 try-catch（除非显式 `throw`），否则不回滚

## 五、异常处理

```java
// 业务异常：统一抛出 BizException
throw new BizException(ErrorCode.USER_NOT_FOUND);

// 错误码定义：模块前缀 + 数字
public enum ErrorCode {
    USER_NOT_FOUND("USR001", "用户不存在"),
    INSUFFICIENT_BALANCE("ORD002", "余额不足");
}
```

- 禁止在 Controller 中 try-catch 后返回 null 或空对象
- 禁止吞异常（catch 后不处理也不抛出）
- 全局异常处理器统一拦截，不在各 Controller 重复处理

## 六、日志规范

```java
// 使用 Lombok @Slf4j
@Slf4j
public class UserService {
    public void process(User user) {
        log.info("处理用户, userId={}", user.getId());          // 业务关键节点
        log.warn("余额不足, userId={}, balance={}", id, balance); // 异常场景
        log.error("操作失败", e);                                // 错误（打印堆栈）
    }
}
```

- **禁止**在日志中打印密码、Token、身份证号等敏感信息
- **禁止**在循环中打印日志
- **禁止**使用 `System.out.println`
- info：关键业务节点；warn：可恢复的异常；error：需要人工介入

## 七、安全规范

- 所有请求参数必须校验（`@Valid` + 自定义校验注解）
- SQL 必须参数化，禁止拼接
- 敏感字段（密码等）数据库存储必须加密（BCrypt）
- 接口返回的 DTO 不得包含密码字段
- 用户输入在返回给前端时必须做 XSS 过滤
- 文件上传必须校验类型和大小

## 八、测试规范

- Service 层每个 public 方法必须覆盖：正常流程 + 边界条件 + 异常流程
- Controller 层使用 `@WebMvcTest` + MockMvc
- 测试类命名：`XxxTest`，放在 `src/test` 对应包路径下
- 禁止用修改断言来"通过"失败测试
