# EARS 格式指南

EARS（Easy Approach to Requirements Syntax）提供了一种结构化格式，用于编写清晰、可测试的需求。

## 目录
- 需求结构与关键字
- 场景格式（Given/When/Then）
- 需求类型与模式
- 示例与反模式

## 需求结构

### 基本格式

```markdown
### Requirement: {描述性名称}
{TRIGGER 子句},
系统 SHALL {动作与结果}。
```

### 触发类型

**WHEN**（事件驱动）：
```markdown
### Requirement: 保存用户资料
WHEN 用户点击“保存”按钮,
系统 SHALL 将资料变更持久化到数据库。
```

**IF**（状态驱动）：
```markdown
### Requirement: 免运费
IF 购物车总额超过 $50,
系统 SHALL 免除运费。
```

**WHERE**（特定范围）：
```markdown
### Requirement: 管理员访问
WHERE 用户具有管理员权限,
系统 SHALL 显示管理面板。
```

**WHILE**（持续进行）：
```markdown
### Requirement: 实时同步
WHILE 文档处于打开状态,
系统 SHALL 每 5 秒同步一次更改。
```

## SHALL / SHOULD / MAY

- **SHALL**：具约束性的需求（必须实现）
- **SHOULD**：推荐但非强制
- **MAY**：可选能力

**生产环境需求优先使用 SHALL**。谨慎使用 SHOULD/MAY。

## 场景格式

每条需求必须包含展示预期行为的场景。

### 结构

```markdown
#### Scenario: {描述性名称}
GIVEN {前置条件}
AND {附加前置条件}
WHEN {动作或触发}
THEN {期望结果}
AND {附加结果}
```

### 示例：完整的需求与场景

```markdown
### Requirement: 用户登录
WHEN 用户提交有效凭据,
系统 SHALL 认证用户并创建会话。

#### Scenario: 登录成功
GIVEN 一个已注册用户，邮箱为 "user@example.com"
AND 用户拥有正确密码 "SecurePass123"
WHEN 用户提交登录表单
THEN 系统创建已认证会话
AND 重定向用户至仪表盘
AND 设置 24 小时过期的会话 Cookie

#### Scenario: 密码错误
GIVEN 一个已注册用户，邮箱为 "user@example.com"
AND 用户提供错误密码 "WrongPass"
WHEN 用户提交登录表单
THEN 系统拒绝登录尝试
AND 显示错误信息 "Invalid email or password"
AND 不创建会话

#### Scenario: 账户被锁定
GIVEN 该账户因失败尝试而被锁定
WHEN 用户提交任意凭据
THEN 系统拒绝登录尝试
AND 显示错误信息 "Account locked. Contact support."
```

## 需求模式

### 模式 1：数据校验

```markdown
### Requirement: 邮箱格式校验
WHEN 用户输入邮箱地址,
系统 SHALL 验证其格式符合 RFC 5322 标准。

#### Scenario: 合法邮箱
GIVEN 用户输入邮箱 "test@example.com"
WHEN 表单提交
THEN 系统接受该邮箱

#### Scenario: 格式非法
GIVEN 用户输入 "not-an-email"
WHEN 表单提交
THEN 系统显示错误 "Invalid email format"
```

### 模式 2：授权

```markdown
### Requirement: 删除权限
WHERE 用户尝试删除资源,
系统 SHALL 验证用户拥有资源或具备管理员权限。

#### Scenario: 所有者删除
GIVEN 用户拥有文档 ID 123
WHEN 用户请求删除文档 123
THEN 系统删除该文档

#### Scenario: 非所有者被阻止
GIVEN 用户不拥有文档 ID 456
AND 用户不具备管理员权限
WHEN 用户请求删除文档 456
THEN 系统返回 HTTP 403 Forbidden
```

### 模式 3：状态流转

```markdown
### Requirement: 订单处理
WHEN 订单被创建,
系统 SHALL 按状态流转：pending → processing → shipped → delivered。

#### Scenario: 标准流程
GIVEN 新订单处于 "pending" 状态
WHEN 支付确认
THEN 系统流转至 "processing"
WHEN 物品发货
THEN 系统流转至 "shipped"
WHEN 确认送达
THEN 系统流转至 "delivered"
```

## 反模式避免

### ❌ 需求含糊

**坏示例**：
```markdown
### Requirement: 高性能
系统应该很快。
```

**好示例**：
```markdown
### Requirement: API 响应时间
WHEN 发起 API 请求,
系统 SHALL 在 95% 的请求中于 200 毫秒内响应。

#### Scenario: 正常负载
GIVEN 系统处于正常负载（< 100 请求/秒）
WHEN 发起 API 请求
THEN 响应时间小于 200ms
```

### ❌ 缺少场景

**坏示例**：
```markdown
### Requirement: 文件上传
WHEN 用户上传文件,
系统 SHALL 存储它。
```

**好示例**：
```markdown
### Requirement: 文件上传
WHEN 用户上传小于 10MB 的文件,
系统 SHALL 将其存储到 S3 并返回 URL。

#### Scenario: 上传成功
GIVEN 用户选择一个 5MB 的 PDF 文件
WHEN 上传完成
THEN 系统将文件存储到 S3
AND 返回 1 小时有效的签名 URL

#### Scenario: 文件过大
GIVEN 用户选择一个 15MB 的视频文件
WHEN 尝试上传
THEN 系统拒绝该文件
AND 显示错误 "File size exceeds 10MB limit"
```

### ❌ 在需求中写实现细节

**坏示例**：
```markdown
### Requirement: 密码存储
系统 SHALL 使用 bcrypt，工作因子为 12，并将哈希存储在用户表。
```

**好示例**：
```markdown
### Requirement: 安全的密码存储
WHEN 用户设置密码,
系统 SHALL 在存储前使用业界标准的不可逆哈希进行处理。

#### Scenario: 创建密码
GIVEN 用户设置密码 "SecurePass123"
WHEN 系统处理该密码
THEN 系统仅存储密码的加密哈希
AND 丢弃明文密码
AND 为每位用户使用唯一盐值
```

（关于 bcrypt/工作因子的实现选择应写在设计文档，而非需求中）

## 完整示例：用户注册

```markdown
## ADDED Requirements

### Requirement: 账户创建
WHEN 用户提交包含有效数据的注册表单,
系统 SHALL 创建新账户并发送验证邮件。

#### Scenario: 注册成功
GIVEN 用户提供邮箱 "new@example.com"
AND 提供密码 "SecurePass123"
AND 提供姓名 "John Doe"
AND 该邮箱尚未被注册
WHEN 用户提交注册表单
THEN 系统创建新用户账户
AND 向 "new@example.com" 发送验证邮件
AND 显示信息 "Check your email to verify your account"
AND 重定向至登录页

#### Scenario: 邮箱重复
GIVEN 用户提供邮箱 "existing@example.com"
AND 该邮箱已被注册
WHEN 用户提交注册表单
THEN 系统拒绝注册
AND 显示错误 "This email is already registered"
AND 不发送邮件

#### Scenario: 密码过弱
GIVEN 用户提供密码 "123"
WHEN 用户提交注册表单
THEN 系统拒绝注册
AND 显示错误 "Password must be at least 8 characters"

### Requirement: 邮件验证
WHEN 用户点击验证链接,
系统 SHALL 在令牌有效且未过期时激活账户。

#### Scenario: 令牌有效
GIVEN 用户收到验证邮件
AND 验证令牌未超过 24 小时
WHEN 用户点击验证链接
THEN 系统激活账户
AND 显示信息 "Account verified successfully"
AND 重定向至登录页

#### Scenario: 令牌过期
GIVEN 验证令牌已超过 24 小时
WHEN 用户点击验证链接
THEN 系统拒绝验证
AND 显示信息 "Verification link expired. Request a new one."
```

## 摘要清单

编写需求时：
- [ ] 使用 SHALL 表示具约束性需求
- [ ] 包含触发子句（WHEN/IF/WHERE/WHILE）
- [ ] 写清动作与结果
- [ ] 至少包含一个正向场景
- [ ] 包含错误/边界场景
- [ ] 场景使用 Given/When/Then 格式
- [ ] 避免实现细节
- [ ] 使需求可测试