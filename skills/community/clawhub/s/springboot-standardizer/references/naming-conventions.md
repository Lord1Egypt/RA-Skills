# Java SpringBoot 项目命名规范

## 包结构规范

### 根包命名
```
com.{公司}.{项目}
```

示例：
- `com.alibaba.ecommerce`
- `com.tencent.wechat`

### 子包划分

| 包名 | 用途 | 说明 |
|------|------|------|
| `controller` | 控制器层 | REST API 入口，处理 HTTP 请求/响应 |
| `service` | 业务接口 | 定义业务逻辑接口 |
| `service.impl` | 业务实现 | 业务逻辑具体实现 |
| `dao` | 数据访问 | Mapper/DAO 接口，数据库操作 |
| `entity` | 实体类 | 对应数据库表的 POJO |
| `dto` | 传输对象 | API 入参，用于接收前端数据 |
| `vo` | 视图对象 | API 出参，返回给前端的数据 |
| `bo` | 业务对象 | 业务逻辑内部使用的对象 |
| `config` | 配置类 | Spring 配置、第三方组件配置 |
| `util` | 工具类 | 通用工具方法 |
| `common` | 公共类 | 通用常量、枚举、结果封装 |
| `exception` | 异常处理 | 自定义异常、全局异常处理器 |
| `interceptor` | 拦截器 | 请求拦截、权限检查 |
| `aspect` | 切面 | AOP 日志、性能监控 |
| `enums` | 枚举 | 状态枚举、类型枚举 |

## 类命名规范

### 按层命名

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| Controller | `XxxController` | `UserController`, `OrderController` |
| Service 接口 | `XxxService` | `UserService`, `OrderService` |
| Service 实现 | `XxxServiceImpl` | `UserServiceImpl`, `OrderServiceImpl` |
| Mapper/DAO | `XxxMapper` 或 `XxxDao` | `UserMapper`, `OrderDao` |
| Entity | `Xxx`（对应表名） | `User`, `Order`, `OrderItem` |
| DTO | `XxxDTO` 或 `XxxCreateDTO` | `UserDTO`, `UserCreateDTO` |
| VO | `XxxVO` | `UserVO`, `OrderListVO` |
| BO | `XxxBO` | `OrderBO` |
| Config | `XxxConfig` | `RedisConfig`, `MybatisConfig` |
| Util | `XxxUtil` 或 `XxxUtils` | `JsonUtil`, `DateUtils` |
| Exception | `XxxException` | `BusinessException` |
| Handler | `XxxHandler` | `GlobalExceptionHandler` |
| Interceptor | `XxxInterceptor` | `AuthInterceptor` |
| Aspect | `XxxAspect` | `LogAspect` |

### 常见后缀对照

| 后缀 | 含义 | 使用场景 |
|------|------|----------|
| `Controller` | 控制器 | REST API 类 |
| `Service` | 服务 | 业务逻辑接口 |
| `ServiceImpl` | 服务实现 | 业务逻辑实现类 |
| `Mapper` | 映射器 | MyBatis 数据访问 |
| `Repository` | 仓库 | JPA 数据访问 |
| `DAO` | 数据访问对象 | 通用数据访问 |
| `DTO` | 数据传输对象 | API 入参 |
| `VO` | 视图对象 | API 出参 |
| `BO` | 业务对象 | 业务层内部对象 |
| `PO` | 持久化对象 | 同 Entity |
| `DO` | 领域对象 | 同 Entity |
| `Config` | 配置 | Spring 配置类 |
| `Util/Utils` | 工具 | 工具类 |
| `Helper` | 辅助 | 辅助类 |
| `Interceptor` | 拦截器 | 请求拦截 |
| `Filter` | 过滤器 | Servlet 过滤器 |
| `Listener` | 监听器 | 事件监听 |
| `Handler` | 处理器 | 异常/消息处理 |
| `Aspect` | 切面 | AOP 切面 |
| `Template` | 模板 | 模板类 |
| `Converter` | 转换器 | 类型转换 |
| `Resolver` | 解析器 | 参数/异常解析 |

## 方法命名规范

### Controller 层

使用 HTTP 方法语义：

| 操作 | 方法名 | 示例 |
|------|--------|------|
| 查询单个 | `getXxx` | `getUser`, `getOrder` |
| 查询列表 | `listXxx` | `listUsers`, `listOrders` |
| 分页查询 | `pageXxx` | `pageUsers` |
| 创建 | `createXxx` | `createUser` |
| 更新 | `updateXxx` | `updateUser` |
| 删除 | `deleteXxx` | `deleteUser` |
| 批量删除 | `batchDeleteXxx` | `batchDeleteUsers` |

### Service 层

使用业务语义：

| 操作 | 方法名 | 示例 |
|------|--------|------|
| 查询单个 | `findXxx`, `getXxx` | `findById`, `getUser` |
| 查询列表 | `findXxxList`, `listXxx` | `findUserList` |
| 查询条件 | `findXxxByYyy` | `findUsersByStatus` |
| 保存 | `saveXxx` | `saveUser` |
| 新增 | `insertXxx`, `addXxx` | `insertUser` |
| 更新 | `updateXxx` | `updateUser` |
| 删除 | `deleteXxx`, `removeXxx` | `deleteUser` |
| 校验 | `validateXxx`, `checkXxx` | `validateUser` |
| 处理 | `processXxx`, `handleXxx` | `processOrder` |
| 发送 | `sendXxx` | `sendMessage` |
| 同步 | `syncXxx` | `syncData` |
| 导入 | `importXxx` | `importUsers` |
| 导出 | `exportXxx` | `exportUsers` |

### DAO/Mapper 层

使用数据库操作语义：

| 操作 | 方法名 | 示例 |
|------|--------|------|
| 根据ID查询 | `selectById` | `selectById` |
| 根据条件查询 | `selectByXxx` | `selectByName` |
| 查询列表 | `selectList` | `selectList` |
| 查询单个 | `selectOne` | `selectOne` |
| 查询数量 | `countXxx` | `countByStatus` |
| 插入 | `insert` | `insert` |
| 批量插入 | `insertBatch` | `insertBatch` |
| 更新 | `update` | `update` |
| 选择性更新 | `updateSelective` | `updateSelective` |
| 删除 | `deleteById` | `deleteById` |
| 条件删除 | `deleteByXxx` | `deleteByStatus` |

## 变量命名规范

### 通用规则

- 使用小驼峰命名（camelCase）
- 避免单字母变量（循环除外）
- 布尔变量使用 `is`, `has`, `can`, `should` 前缀

### 常见命名

| 类型 | 命名 | 示例 |
|------|------|------|
| ID | `xxxId` | `userId`, `orderId` |
| 列表 | `xxxList` | `userList`, `orderList` |
| 数量 | `xxxCount`, `xxxNum` | `userCount`, `pageNum` |
| 标识 | `isXxx`, `hasXxx` | `isDeleted`, `hasPermission` |
| 时间 | `xxxTime` | `createTime`, `updateTime` |
| 日期 | `xxxDate` | `startDate`, `endDate` |
| 状态 | `xxxStatus` | `orderStatus`, `userStatus` |
| 类型 | `xxxType` | `userType`, `orderType` |
| 名称 | `xxxName` | `userName`, `productName` |
| 编码 | `xxxCode` | `productCode`, `errorCode` |

## 常量命名规范

使用全大写，下划线分隔：

```java
public static final int MAX_RETRY_TIMES = 3;
public static final String DEFAULT_CHARSET = "UTF-8";
public static final long CACHE_EXPIRE_SECONDS = 3600;
```

## 数据库相关命名

### 表名
- 小写，下划线分隔
- 单数或复数统一（推荐复数）
- 示例：`user`, `order`, `order_item`

### 字段名
- 小写，下划线分隔
- 主键：`id`
- 外键：`xxx_id`
- 时间：`create_time`, `update_time`
- 状态：`status`, `is_deleted`

### 索引名
- 主键：`pk_表名`
- 唯一：`uk_字段名`
- 普通：`idx_字段名`
