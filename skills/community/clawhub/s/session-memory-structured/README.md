# Session Memory Structured

一个用于 OpenClaw 的会话纪要 Hook。

它会在你执行 `/new` 或 `/reset` 时，回看刚结束的那段会话，自动提炼成一份四段式结构化纪要，并按日期追加写入工作区下的 `memory/YYYY-MM-DD.md`。

这个项目的目标不是“替代长期记忆系统”，而是把**刚结束的一段会话**做成稳定、可追溯、方便后续继续工作的归档。

---

## 它会做什么

触发时会整理四块内容：

1. 本次会话做了什么
2. 新确认的偏好 / 规则 / 决定
3. 重要但暂不沉淀为长期记忆的上下文
4. 未完成事项 / 下次继续点

输出结果会写入：

- `[WORKSPACE]/memory/YYYY-MM-DD.md`

---

## 触发时机

本 Hook **只在以下事件触发**：

- `command:new`
- `command:reset`

也就是说，它的设计目标是：**在你开启新会话时，为上一个会话补一份结构化纪要**。

---

## 目录结构

最小可用目录：

- `handler.js`：Hook 主逻辑
- `skill.md`：技能元信息
- `README.md`：使用说明

---

## 安装与配置

### 1) 复制文件

将本目录放到你的 OpenClaw 工作区中，例如：

- `workspace/hooks/session-memory-structured/`

### 2) 填写占位配置

打开 `handler.js`，搜索 `[EDIT HERE]`，替换以下占位符：

- `<YOUR_AGENT_ID>`：你的 agent ID，例如 `main`
- `<YOUR_PROVIDER_ID>`：你实际使用的 provider ID，例如 `openai-codex`、`volcengine-plan` 等

这两个值用于：

- 定位本机的 Session 记录
- 读取本机 `models.json` 中对应 provider 的模型配置

### 3) 在 OpenClaw 中挂载 Hook

在你的 `openclaw.json` 或 `openclaw.yaml` 中，把这个 Hook 挂到 `command:new` 和 `command:reset` 事件。

示例：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/session-memory-structured/handler.js",
          "export": "default"
        },
        {
          "event": "command:reset",
          "module": "./hooks/session-memory-structured/handler.js",
          "export": "default"
        }
      ]
    }
  }
}
```

---

## 隐私与安全边界

这部分我写直白一点。

### 本项目**不会**做的事

- 不会在仓库里硬编码你的 API Key
- 不会把 API Key 明文写回到这个目录
- 不会主动把纪要结果同步到第三方文档或数据库

### 本项目**会**做的事

- 会读取你本机 OpenClaw 的 Session 文件
- 会读取你本机 `models.json` 中对应 provider 的 `baseUrl` 和 `apiKey`
- 会把筛选后的会话文本发送给你配置的模型服务，用于生成结构化纪要
- 会把生成结果写入你的工作区 `memory/YYYY-MM-DD.md`

### 你应该知道的边界

如果你配置的模型服务是外部云服务，那么**会话内容会被发送到该服务**进行总结。

所以它不是“完全离线”的本地归档工具，而是：

- **本地读取会话**
- **调用你自己的模型配置做总结**
- **本地落盘保存结果**

如果你的会话里包含敏感信息，请先确认：

- 你信任所使用的模型服务商
- 你的 `models.json` 指向的是你愿意发送数据的服务

---

## 适用场景

适合这些情况：

- 你经常用 `/new` 或 `/reset` 切会话
- 你想保留“刚刚这段对话到底做了什么”的稳定纪要
- 你希望下一段工作能快速续上，而不是靠模型临场回忆

不太适合这些情况：

- 你要求严格离线、绝不把内容发给模型服务
- 你希望它直接替代长期记忆数据库
- 你需要跨多 agent、多工作区的通用记忆治理方案

---

## 已知限制

- 当前实现依赖 OpenClaw 本地目录结构
- 需要手动填写 `AGENT_ID` 与 `PROVIDER_ID`
- 总结质量取决于你配置的模型与 provider
- 默认只截取最近一部分消息（见 `MAX_MESSAGES`）进行整理

---

## 发布到 ClawHub 前建议

如果你要二次分发或继续改造，建议至少检查：

- 是否仍然使用了占位符，而不是你自己的真实配置
- README 是否清楚说明了“会发送会话内容给模型服务”
- 触发事件是否与你的实际实现一致
- 输出路径是否符合你的工作区约定

---

如果这个 Hook 刚好对你有用，拿去改、拿去接自己的记忆流都行。核心思路就一句：**别让刚结束的会话白白蒸发。**
