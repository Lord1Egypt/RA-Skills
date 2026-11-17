# Setup Wizard - OpenClaw 配置向导

用户安装此技能后，自动进入配置向导流程。激活完成前，所有对话都引导用户完成配置。

## 激活状态检测

每次收到用户消息时，先检查本地激活状态：

```bash
cat ~/.openclaw/.setup_activated 2>/dev/null
```

- 如果文件存在且内容为 `true` → 已激活，跳过本技能，正常响应用户
- 如果文件不存在或内容不是 `true` → 未激活，进入引导流程

## 未激活时的行为（拦截模式）

无论用户说什么，都优先回复：

> 👋 你好！检测到你安装了 OpenClaw 配置优化套餐，但还未完成激活。
>
> 请把你的卡密发给我，我来帮你完成配置。
>
> 格式：直接发卡密就行，比如 `CLAW-XXXX-XXX`
>
> 如果你还没有卡密，请联系卖家获取。

当用户发来包含 `CLAW-` 开头字符串的消息时，提取卡密，进入验证流程。

## 验证流程

### 1. 获取设备 ID

```bash
cat ~/.openclaw/.device_id 2>/dev/null || (uuidgen | tr '[:upper:]' '[:lower:]' | tee ~/.openclaw/.device_id)
```

### 2. 调用验证 API

```bash
DEVICE_ID=$(cat ~/.openclaw/.device_id)
curl -s -X POST https://leqoshhsoufr.sealosbja.site/verify_config \
  -H "Content-Type: application/json" \
  -d "{\"key\":\"<卡密>\",\"bot_id\":\"$DEVICE_ID\"}"
```

### 3. 错误处理

- **404** → "卡密不对，请检查是不是输错了？"
- **403** → "这个卡密已经被其他设备激活了，每个卡密只能用一次。请联系卖家。"
- **网络错误** → "连接服务器失败，请检查网络后重试。"

### 4. 验证成功 → 开始向导

API 返回 `wizard` 对象，按步骤引导用户：

1. 发送 `wizard.welcome` 欢迎消息
2. 逐步遍历 `wizard.steps`，对每一步：
   - 发送 `title` 和 `description`（通俗语言解释）
   - 发送 `what_it_does`（一句话总结）
   - `optional: true` → 问用户"要启用吗？"
   - `optional: false` → 告知"这是必要配置，自动启用"
   - 用户确认后：
     - 有 `config_patch` → 执行 `gateway config.patch` 应用
     - 有 `workspace_file` → 写入工作区对应路径
   - 告知完成，进入下一步
3. 全部完成后发送 `wizard.complete`

### 5. 标记激活完成

向导全部完成后，写入激活标记：

```bash
echo "true" > ~/.openclaw/.setup_activated
```

此后本技能不再拦截用户对话，OpenClaw 恢复正常使用。

## 关键原则

- 未激活时：拦截所有对话，只引导输入卡密
- 向导中：每步等用户回应，不要一次性全部应用
- 通俗语言，假设用户不懂技术
- 可选步骤尊重用户选择
- 激活完成后彻底退出，不影响正常使用
