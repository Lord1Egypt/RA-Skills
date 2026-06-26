---
name: homepage
description: OpenClaw 主页插件 - 让访客在你的个人主页上与 AI 助手对话。支持多访客并发、上下文隔离，无需泄露敏感信息。
metadata: {"openclaw": {"emoji": "🏠", "requires": {"bins": ["python3"], "anyBins": ["uvicorn"]}}}
---

# 🏠 OpenClaw 主页插件

让用户拥有自己的个人主页，访客可以直接与 AI 助手对话。

---

## 一、插件架构

```
访客消息 → Java平台 → Python插件(/homepage/chat) → OpenClaw Agent → LLM
```

插件本质：**HTTP 桥接服务**，把 OpenClaw Agent 封装成标准 HTTP 接口。

---

## 二、用户配置（只需3件事）

### 2.1 创建 Agent

```bash
# 在 OpenClaw 中创建 Agent
# 名称如 "Alice客服"
# 模型选择 openclaw-default
```

### 2.2 上传公开知识库

- FAQ、产品介绍等
- **不要上传敏感信息**

### 2.3 生成 API Key

在插件配置中设置：
```yaml
agent:
  id: "agent_123"
  api_key: "xxx"
  model: "openclaw-default"
```

---

## 三、技能功能

### 3.1 初始化插件

首次使用时运行：

```bash
bash {baseDir}/scripts/init.sh
```

这会：
- 创建配置目录 `~/.openclaw/homepage/`
- 生成默认配置文件
- 安装依赖

### 3.2 配置插件

编辑配置文件：

```bash
open ~/.openclaw/homepage/config.yaml
```

必需配置：
- `agent.id`: 你的 Agent ID
- `agent.api_key`: API Key
- `agent.model`: 模型名称

### 3.3 启动插件服务

```bash
bash {baseDir}/scripts/start.sh
```

服务默认在 `http://localhost:8080` 运行

### 3.4 停止插件服务

```bash
bash {baseDir}/scripts/stop.sh
```

### 3.5 测试接口

```bash
bash {baseDir}/scripts/test.sh
```

---

## 四、调用方式

### 4.1 HTTP 接口

```
POST /homepage/chat
Headers: Authorization: Bearer <API_KEY>
Body: {
  "session_id": "visitor123",
  "message": "你好"
}
```

### 4.2 多访客隔离

通过 `session_id` 区分不同访客，实现上下文隔离。

---

## 五、OpenClaw Agent 使用

当用户问"有人在我主页留言"或查看主页消息时：

1. 读取日志：`bash {baseDir}/scripts/logs.sh`
2. 分析对话内容

---

## 六、扩展功能（未来）

- 敏感信息过滤
- 支持多 Agent / 多模型
- 日志统计、限流
- Redis 会话存储
