# 交互式注册与已有用户登录

权威引导入口：`GET https://api.shizixi.com/api/v3/agent/bootstrap`。

## 先判断用户状态

先询问用户是否已经注册，不猜测邮箱或账号状态：

- 已注册：走“邮箱验证码登录”。
- 未注册：展示当前条款与隐私链接，用户同意后走“邮箱验证码注册”。
- 不确定：可先尝试登录验证码；如果服务明确返回邮箱未注册，再说明原因并征得用户确认后改走注册。不要连续发送两类验证码。

## 已注册用户

1. 询问邮箱，并明确征得“发送登录验证码”的确认。
2. `POST /api/v3/auth/email/send-code`

```json
{"email":"用户输入的邮箱","purpose":"login"}
```

3. 询问用户收到的六位验证码。
4. `POST /api/v3/auth/email/verify`

```json
{"email":"用户输入的邮箱","code":"用户输入的验证码","purpose":"login"}
```

5. 登录会保留原账号，不创建重复用户。接口会把当前可用 Key 返回给 Agent；把它当作敏感响应处理，在本会话使用或交给平台受保护的 Secret/凭据存储，禁止在对话中回显。

## 新用户

1. 从 bootstrap 读取 `terms_version`、条款和隐私地址并展示给用户。
2. 用户确认发送验证码后，调用：

```json
{"email":"用户输入的邮箱","purpose":"register"}
```

3. 用户输入六位验证码并明确接受当前条款后，调用 `POST /api/v3/auth/agent/register`：

```json
{
  "email":"用户输入的邮箱",
  "code":"用户输入的验证码",
  "nickname":"可选昵称",
  "accept_terms":true,
  "terms_version":"bootstrap 返回的精确版本",
  "agree_news_push":false
}
```

4. API Key 由注册接口直接返回给 Agent，可在本会话立即使用。若平台支持受保护 Secret，则在用户授权后保存并尽量缩短明文在临时变量中的停留时间；没有安全 Secret 存储时只保留当前会话能力，并明确告知用户下次需重新验证码登录，不能把密钥写入普通文件。

## 自动获取与跨会话保存

- Agent 不需要用户手工复制 API Key：注册或登录成功响应会自动返回 Key。
- 当前会话可用 `Authorization: Bearer <API Key>` 调用小石公开能力；不得把真实 Key 写进示例命令、日志或报告。
- 只有 Agent 平台提供受保护 Secret/凭据存储时，才能在用户授权后自动跨会话保存。
- 平台没有 Secret 存储时，不得为了“自动保存”把 Key 写入 Skill、系统提示词、普通文件、聊天记录或长期记忆；下次用邮箱验证码重新登录即可重新取得同一账号能力。

## 已注册用户的 Key 失效或本地 Key 过旧

当需要认证的接口返回 `401` 且错误明确指向 Key 无效、过期或本地保存值不再可用时：

1. 立即停止重试旧 Key，并清除当前请求中的旧 Authorization 值。
2. 说明“账号不会重建，只通过邮箱验证取回当前账号的最新 Key”，并询问用户是否同意发送登录验证码。
3. 用户确认后，用原账号邮箱调用 `/api/v3/auth/email/send-code`，`purpose=login`；随后询问六位验证码并调用 `/api/v3/auth/email/verify`。
4. 登录响应会自动返回当前账号可用的 Key。不要在对话中展示；原子替换平台受保护 Secret，失败时保留旧 Secret 的备份状态但不再调用。
5. 用新 Key 对 `GET /api/v3/auth/api-key/check` 做一次验证。只有返回 `valid=true` 且 `active=true` 才恢复原任务。
6. `403`、账号停用或验证码登录本身失败时停止，不调用注册接口、不自动调用 `/api-key/regenerate`、不循环发送邮件。

只有“用户明确要求重新生成 Key”时，才可在有效登录 Session 下单独调用 regenerate；普通 401 恢复流程只取回当前 Key，不进行轮换。

## 失败与停止条件

- `409 已注册`：切换到登录流程，不重复注册。
- `404 未注册`：征得用户确认后切换到注册流程。
- `429`：遵守 `Retry-After`，本轮停止发送；不换 IP、不循环重试。
- 验证码错误或过期：说明需要重新发送，只有用户再次确认后才能发送一次。
- `403` 或账号停用：停止并让用户通过官网处理，不绕过限制。
- API Key、验证码、Session Token 都不得出现在日志、错误报告、截图、Skill 或 Prompt 中。
