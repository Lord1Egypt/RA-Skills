# WHUT 工作流约定

处理 `whut.ai-augmented.com` / `*.whut.ai-augmented.com` 页面时，先执行：

```bash
./scripts/whut-open "目标URL"
```

如果没有给 URL，则执行：

```bash
./scripts/whut-open
```

## 目的

- 从环境变量或本地 secret 文件读取账号密码
- 自动关闭挡住登录的弹窗
- 自动填账号密码并提交
- 登录成功后自动抓取当前页面文本
- 如果有题目则自动填写并提交
- 如果有题目则自动填写并提交
- 将抓取结果保存到 `latest_page_dump.json`
- 确保后续 `agent-browser` 操作建立在已登录状态上

## 凭据格式

可选本地文件：`./local/whut_ai_secret.json`

```json
{
  "username": "你的账号",
  "password": "你的密码"
}
```

也可以直接使用环境变量：

```bash
export WHUT_USERNAME='你的账号'
export WHUT_PASSWORD='你的密码'
```

## 后续操作原则

1. 先登录，再 `snapshot` / `click` / `fill` / `get`
2. 登录完成后，优先读取 `latest_page_dump.json` 获取当前页面文本
3. 如果跳回认证页，重新执行 `./scripts/whut-open`
4. 如果 ref 失效，先重新 `snapshot -i --json`
5. 如果有题目则自动填写并提交