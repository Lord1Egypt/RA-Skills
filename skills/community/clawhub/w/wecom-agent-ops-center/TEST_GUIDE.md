# 企微 Agent Connector — 端到端测试指南

> 测试目标：企微用户发消息 → Connector 接收 → 调 Agent → 回复用户

---

## 前置条件

1. **企微智能机器人** 的 `BotID` 和 `Secret`
2. **Agent 端点** running（或用于测试的 Mock Agent）
3. **服务器** `https://www.hermesai.ltd` 可访问（配对+转换 API）

---

## 第一步：启动 Mock Agent（测试用）

```bash
cd wecom-connector
python3 mock-agent.py &
# 验证：
curl -s -X POST http://127.0.0.1:3001/chat \
  -H "Content-Type: application/json" \
  -d '{"content":"你好"}' | python3 -m json.tool
```

预期返回：
```json
{
  "content": "✅ Mock Agent 已收到你的消息！\n你发送的内容：你好\n...",
  "msg_type": "text"
}
```

---

## 第二步：配置 Connector

编辑 `config.yaml`：

```yaml
wecom:
  bot_id: "your_bot_id"
  bot_secret: "your_secret"
  callback_port: 3000

agent:
  endpoint: "http://127.0.0.1:3001/chat"  # Mock Agent 地址
  timeout_ms: 30000

converter:
  enabled: true
  api_base: "https://www.hermesai.ltd"
  api_key: "你的API密钥"
```

---

## 第三步：启动 Connector

```bash
cd wecom-connector
node connector.js
```

预期输出：
```
[connector] 企微 Agent Connector v1.1.0
[connector] 加载配置：wecom (BotID: xxx)
[connector] Agent 端点：http://127.0.0.1:3001/chat
[connector] 云端转换：已启用 (www.hermesai.ltd)
[ws-client] 正在连接企微 WebSocket...
[ws-client] ✅  WebSocket 连接成功
[ws-client] ✅  订阅成功（AI 机器人）
```

---

## 第四步：企微发消息测试

1. 打开企微，找到你的 AI 机器人
2. 发送消息：「你好」
3. 观察 Connector 终端输出：

```
[ws-client] 收到消息：你好
[agent-bridge] 调用 Agent：/chat
[agent-bridge] Agent 回复：✅ Mock Agent 已收到你的消息！...
[ws-client] 回复企微成功
```

4. 企微里应该看到机器人回复

---

## 第五步：P2P 配对测试（可选）

**Terminal 1 — Creator：**
```bash
cd wecom-connector
node connector.js pair
# 输出：
# 配对码：XXXX-XXXX
# 等待对方加入...
```

**Terminal 2 — Joiner：**
```bash
cd wecom-connector
node connector.js join XXXX-XXXX
# 输出：
# ✅ 配对成功！
# 与 creator 建立连接
```

**测试发送：**
```bash
# Terminal 2 发送
node connector.js send creator '{"type":"test","msg":"hello"}'

# Terminal 1 应该收到
# [p2p] 收到 peer 消息：{ "type": "test", "msg": "hello" }
```

---

## 常见问题排查

### 1. WebSocket 连接失败
```
[ws-client] ❌ 连接失败：ECONNREFUSED
```
- 检查 `bot_id` / `bot_secret` 是否正确
- 检查企微后台是否开启了 AI 机器人功能

### 2. 订阅返回错误
```
[ws-client] ❌ 订阅失败：invalid corpid
```
- `bot_secret` 格式错误，应该是 `corpid+corpsecret` 或类似格式
- 参考企微文档：https://developer.work.weixin.qq.com/document/path/101039

### 3. Agent 调用超时
```
[agent-bridge] ❌ Agent 调用超时（30000ms）
```
- 检查 Agent 端点是否可访问（`curl` 测试）
- 检查防火墙是否允许出站连接

### 4. 消息转换失败
```
[converter] Cloud failed, fallback local
```
- 检查 `https://www.hermesai.ltd` 是否可访问
- 检查 `api_key` 是否正确
- 用 `curl` 测试：`curl https://www.hermesai.ltd/health`

### 5. 企微收不到回复
- 检查 Connector 是否print 了「回复企微成功」
- 检查企微机器人是否有「主动回复」权限
- 检查是否消息类型不支持（如语音、文件）

---

## 下一步

测试通过后：
1. **打包 Skill**：`npm pack` → 生成 `.tgz` 文件
2. **上架 ClawHub**：上传 `.tgz` + `SKILL.md`
3. **生产部署**：将 `config.yaml` 里的 `agent.endpoint` 改为真实 Agent 地址
