# 绑定账号（Guest → 注册用户升级）

当用户表达"绑定账号"、"注册"、"升级 guest"、"绑定邮箱"等意图时读取本文件。执行前必须已经完成 `environment-and-credentials.md`（确保有可用的 API Key）。

## 核心概念

- Guest 用户通过 `POST /api/v1/agent-guest-key` 获取的临时 API Key，绑定邮箱后升级为注册用户
- **API Key 不变**：绑定只是在同一个 user record 上添加 email，`user.id` 和 `api_key` 都保持不变
- 绑定后用户可以用邮箱登录 ShareOne 网站 dashboard 管理文件
- 整个流程由 agent 代劳，用户不需要打开浏览器

## 流程

### 1. 获取用户邮箱

如果用户还没有提供邮箱，询问：

> 请提供您的邮箱地址，我来帮您绑定账号。绑定后您的 API Key 不变，还可以用邮箱登录 ShareOne 网站管理文件。

### 2. 发送验证码

```bash
node scripts/bind_account.js --send --email <用户邮箱>
```

按输出 token 处理：

- `CODE_SENT`：通知用户查看邮箱：
  > 验证码已发送到 `<邮箱>`，请查看邮箱（含垃圾箱），告诉我 6 位数字验证码。
- `ERROR:EMAIL_ALREADY_LINKED`：该邮箱已被其他账号使用。告知用户并建议使用其他邮箱，或直接用该邮箱登录网站。
- `ERROR:COOLDOWN`：发送冷却中，请等待 30 秒后重试。
- `ERROR:RATE_LIMIT`：频率限制，稍后再试。
- `ERROR:KEY_NOT_FOUND`：API Key 不存在，需要先通过 `ensure_credentials.js` 获取凭据。

### 3. 等待用户回复验证码

暂停操作，等待用户告知 6 位验证码。

### 4. 验证并绑定

```bash
node scripts/bind_account.js --verify --email <用户邮箱> --code <验证码>
```

按输出 token 处理：

- `BIND_SUCCESS`：绑定成功。向用户确认：
  > 账号绑定成功！您的邮箱 `<邮箱>` 已与当前 API Key 关联。API Key 不变，您现在可以用这个邮箱登录 ShareOne 网站管理分享的文件。
- `ERROR:INVALID_CODE`：验证码错误，请用户检查后重新输入。不需要重新发送验证码。
- `ERROR:CODE_EXPIRED`：验证码已过期（5 分钟有效），需要重新发送。回到第 2 步。
- `ERROR:TOO_MANY_ATTEMPTS`：验证码尝试次数过多（最多 5 次），需要重新发送。回到第 2 步。
- `ERROR:EMAIL_ALREADY_LINKED`：邮箱已被其他账号使用。建议使用其他邮箱。
- `ERROR:KEY_NOT_FOUND`：API Key 无效或 guest 账号不存在。

## 不要做的事

- 不要让用户打开浏览器去网站绑定——整个流程在对话中完成。
- 不要在绑定后生成新的 API Key——绑定不改变 key。
- 不要在用户没有明确要求时主动发起绑定流程（但在首次创建 guest key 后可以简短提示）。
