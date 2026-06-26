---
name: wecom-quickstart-cn
version: 1.0.0
description: |
  企业微信快速集成配置 - 5分钟连接 OpenClaw 与企业微信，解锁群机器人、应用消息、客户管理。适合：企业用户、微信生态、客户服务。
metadata:
  openclaw:
    emoji: "企"
    version: 1.0.0
    requires:
      bins: ["curl"]
---

# 企业微信快速集成配置

**目标**：5 分钟内完成 OpenClaw + 企业微信集成，开始自动化办公。

---

## 🚀 快速开始（3 步）

### 第一步：创建企业微信应用

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame)
2. 应用管理 → 自建应用 → 创建应用
3. 填写信息：
   - **应用名称**：OpenClaw Assistant
   - **应用logo**：自定义或默认
   - **可见范围**：选择部门/人员
4. 创建后记录：
   - `AgentId`
   - `Secret`

### 第二步：获取企业凭证

在「我的企业」页面获取：
- `CorpId` - 企业 ID
- 在「客户联系」→「API」获取 `Customer Secret`（可选，用于客户管理）

### 第三步：配置 OpenClaw

在 OpenClaw 配置文件 `~/.openclaw/config.yml` 添加：

```yaml
channels:
  wecom:
    enabled: true
    corpId: "wx1234567890abcdef"      # 企业 ID
    agentId: 1000001                   # 应用 AgentId
    secret: "xxxxxxxxxxxxxxxxxxxxxxxx"  # 应用 Secret
```

然后重启 OpenClaw：
```bash
openclaw gateway restart
```

---

## ✅ 验证集成

在 OpenClaw 对话中测试：

```
发送企业微信消息到用户 @user_id：测试成功，OpenClaw 已连接！
```

如果企业微信收到消息，集成完成！

---

## 📋 常见使用场景

### 场景 1：群机器人消息推送

**指令**：
```
发送企业微信群消息：项目进度更新：完成 80%
```

**OpenClaw 会自动**：
1. 调用群机器人 Webhook
2. 发送 Markdown 格式消息
3. 支持 @指定成员

### 场景 2：客户服务自动化

**指令**：
```
监控企业微信客户消息，自动回复常见问题
```

**OpenClaw 会自动**：
1. 接收客户消息
2. 匹配知识库
3. 发送智能回复

### 场景 3：审批流程集成

**指令**：
```
当有新审批时，发送企业微信通知给审批人
```

**OpenClaw 会自动**：
1. 监控审批状态
2. 推送通知给相关人员
3. 记录审批日志

---

## 🔧 高级配置

### 群机器人配置

在企业微信群中添加群机器人：

```yaml
channels:
  wecom:
    enabled: true
    corpId: "wx1234567890abcdef"
    agentId: 1000001
    secret: "xxx"
    groupBots:
      - name: "开发群"
        webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
      - name: "运维群"
        webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"
```

### 多应用支持

如果需要管理多个应用：

```yaml
channels:
  wecom:
    enabled: true
    corpId: "wx1234567890abcdef"
    apps:
      - name: "OpenClaw Assistant"
        agentId: 1000001
        secret: "xxx"
      - name: "HR Bot"
        agentId: 1000002
        secret: "yyy"
```

---

## 🐛 故障排查

### 问题 1：消息发送失败

**错误**：`invalid corpId or secret`

**解决**：
1. 检查 CorpId 是否正确（「我的企业」页面）
2. 检查 Secret 是否正确（应用详情页）
3. 确认应用已发布且可见范围正确

### 问题 2：群机器人无法推送

**错误**：`webhook url invalid`

**解决**：
1. 检查 Webhook URL 格式
2. 确认机器人未被删除
3. 测试 URL 可达性：
   ```bash
   curl -X POST "YOUR_WEBHOOK_URL" \
     -H "Content-Type: application/json" \
     -d '{"msgtype":"text","text":{"content":"测试"}}'
   ```

### 问题 3：客户消息接收失败

**错误**：`no callback url`

**解决**：
1. 在企业微信后台配置回调 URL
2. 设置可信域名
3. 启用客户联系 API

---

## 📚 企业微信 API 参考

### 应用消息发送

```bash
POST https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN

{
  "touser": "UserID",
  "msgtype": "text",
  "agentid": 1000001,
  "text": {
    "content": "这是一条应用消息"
  }
}
```

### 群机器人消息

```bash
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=KEY

{
  "msgtype": "markdown",
  "markdown": {
    "content": "### 标题\n**粗体**\n- 列表项"
  }
}
```

---

## 💰 定价参考

- **基础集成**：¥99（应用创建 + 消息发送）
- **企业定制**：¥299（群机器人 + 客户管理 + 自动化）
- **全托管服务**：¥999/月（OpenClaw 托管 + 企业微信集成 + 技术支持）

---

## 🆘 获取帮助

- **企业微信开发文档**：https://developer.work.weixin.qq.com/document
- **OpenClaw 文档**：https://docs.openclaw.ai
- **OpenClaw 社区**：https://discord.com/invite/clawd

---

**创建时间**：2026-03-21
**作者**：OpenClaw 中文生态
**版本**：1.0.0