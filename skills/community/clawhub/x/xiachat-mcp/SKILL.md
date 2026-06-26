---
name: xiachat-mcp
description: XiaChat MCP 集成 — AI 人格匹配、分身预聊天、Soul Square 角色聊天，Claude 直接调用 / XiaChat MCP — AI personality matching, avatar pre-chat, Soul Square persona chat in Claude. Use when user wants to find compatible people, create personality profiles, start AI avatar conversations, or chat with AI personas.
allowed-tools: Bash, Read
---

# XiaChat MCP — AI 人格匹配社交工具 / AI Personality Matching Tools

> **[XiaChat (xiachat.com)](https://xiachat.com)** — AI 人格匹配社交平台，用 SOUL 档案找到最合拍的人

将 XiaChat 的 AI 人格匹配、分身预聊天、Soul Square 等能力接入 Claude Desktop、Cursor 等 MCP 客户端。通过 SOUL.json 人格档案进行向量+LLM 双重评分匹配，AI 分身先替你聊 5 轮试探兼容性，满意后再接管真人对话。

## Setup / 配置

### 1. 获取 API Key

注册 [XiaChat](https://xiachat.com) 账号，在 [设置页](https://xiachat.com/settings/api) 获取 API Key（格式：`xk_...`）。

### 2. MCP 配置

```json
{
  "mcpServers": {
    "xiachat": {
      "command": "npx",
      "args": ["-y", "@xiachat/mcp-server"],
      "env": {
        "XIACHAT_API_KEY": "xk_your_api_key"
      }
    }
  }
}
```

配置完成后重启客户端即可使用。

## 工具列表 (11 Tools)

### SOUL 档案管理

#### 1. `soul_create` — 创建人格档案

从姓名、性格测试或聊天记录生成 SOUL.json 人格档案。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 显示名称 |
| `quiz_answers` | object | | Big Five 性格测试答案 |
| `chat_text` | string | | 聊天导出文本，提取沟通风格 |
| `soul_md` | string | | OpenClaw SOUL.md 内容 |

**示例**: `soul_create({ name: "Alice", chat_text: "聊天记录..." })`

#### 2. `soul_import` — 导入 SOUL.md

将 OpenClaw SOUL.md 格式转换为 XiaChat SOUL.json。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `soul_md` | string | ✅ | 完整 SOUL.md 文件内容 |

#### 3. `soul_export` — 导出 SOUL.md

将 SOUL.json 导出为 OpenClaw SOUL.md 格式。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `user_id` | string | | 用户 ID（默认当前用户） |

### 人格匹配

#### 4. `match_find` — 寻找匹配

向量+LLM 双重评分，找到人格最兼容的匹配。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `top_n` | number | | 返回数量 1-20，默认 5 |
| `match_type` | enum | | friend / dating / work / any（默认 any） |

**返回**: 匹配列表，含兼容性分数、维度分析（兴趣/价值观/风格）、匹配类型、原因

#### 5. `match_score` — 计算兼容性

计算两个 SOUL 档案的兼容性评分。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `soul_a` | string | ✅ | 第一个 SOUL.json（JSON 字符串） |
| `soul_b` | string | ✅ | 第二个 SOUL.json（JSON 字符串） |

**返回**: 总分、维度分数（兴趣%/价值观%/风格%）、匹配类型、原因

### 分身预聊天

#### 6. `prechat_start` — 启动预聊天

AI 分身替你和匹配对象先聊 5 轮，试探兼容性。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `match_id` | string | ✅ | match_find 返回的匹配 ID |

#### 7. `prechat_status` — 查询预聊天进度

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prechat_id` | string | ✅ | prechat_start 返回的预聊天 ID |

**返回**: 状态、已完成轮次/5、预计完成时间

#### 8. `prechat_report` — 获取预聊天报告

获取 AI 分身预聊天的完整评估报告。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prechat_id` | string | ✅ | 预聊天 ID |

**返回**: 质量评分、摘要、亮点、对话记录、是否推荐继续

#### 9. `prechat_handoff` — 接管对话

满意后接管 AI 分身，开始真人聊天。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prechat_id` | string | ✅ | 预聊天 ID |

**返回**: 聊天室 ID、接管说明

### Soul Square

#### 10. `square_list` — 浏览 AI 角色

浏览 Soul Square 中的 AI 人格角色。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `category` | enum | | philosopher / artist / scientist / creator / coach / all（默认 all） |
| `limit` | number | | 返回数量 1-50，默认 10 |

#### 11. `square_chat` — 与 AI 角色聊天

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `persona_id` | string | ✅ | 角色 ID |
| `message` | string | ✅ | 用户消息 |
| `session_id` | string | | 会话 ID（续聊） |

### 信用分

#### `soul_credit` — 查询 SOUL 信用分

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `user_id` | string | | 用户 ID（默认当前用户） |

**返回**: 总分/100，细分维度（完整度、社交历史、一致性、社区贡献）

## MCP Prompts（引导式工作流）

| Prompt 名 | 说明 |
|-----------|------|
| `find-match` | 引导完成：检查 SOUL → 寻找匹配 → 启动预聊天 → 查看报告 |
| `soul-checkup` | 引导完成：导出 SOUL → 检查信用分 → 识别改进点 |

## MCP Resource

| URI | 类型 | 说明 |
|-----|------|------|
| `xiachat://schema/soul.json` | JSON Schema | SOUL.json 格式规范 |

## 典型工作流

### 完整匹配流程
`soul_create(name)` → `match_find(type: "dating", top: 3)` → `prechat_start(match_id)` → `prechat_status(id)` → `prechat_report(id)` → `prechat_handoff(id)`

### OpenClaw SOUL 同步
`soul_import(soul_md)` → 在 XiaChat 使用 → `soul_export()` → 更新 SOUL.md

### Soul Square 探索
`square_list(category: "philosopher")` → `square_chat(persona_id, message)` → 续聊 `square_chat(persona_id, message, session_id)`

## 注意事项

- **API Key 必需**：所有工具需要 `XIACHAT_API_KEY`（`xk_...` 格式）
- **预聊天 5 轮制**：AI 分身固定聊 5 轮后生成报告，不可中途干预
- **OpenClaw 兼容**：SOUL.md ↔ SOUL.json 双向转换，与 OpenClaw 生态互通
- **匹配类型**：friend（友谊）、dating（约会）、work（工作）、any（任意）

## 在线体验

- [XiaChat 首页](https://xiachat.com) — AI 人格匹配社交平台
- [Soul Square](https://xiachat.com/square) — AI 角色广场
- [SOUL 档案](https://xiachat.com/soul) — 创建你的人格档案
- [匹配中心](https://xiachat.com/match) — 寻找兼容的人
- [API 设置](https://xiachat.com/settings/api) — 获取 API Key

---
Powered by [XiaChat](https://xiachat.com) — AI 人格匹配社交平台
