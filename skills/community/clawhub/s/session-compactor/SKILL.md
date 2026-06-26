---
name: session-compactor
description: 自动会话压缩以优化 token 使用。当会话消息数超过阈值时，将早期历史压缩为结构化摘要，保留工具调用和关键事实。适用于长对话场景以节省上下文窗口。核心算法参考 claw-code 项目的 compact.rs 设计。
metadata: {
  "clawdbot": {
    "emoji": "🗜️",
    "requires": { "bins": ["node"] },
    "tools": [
      {
        "name": "compact_session",
        "description": "压缩当前会话历史以节省 tokens。自动检测 token 数，将早期消息替换为摘要",
        "inputSchema": {
          "type": "object",
          "properties": {
            "maxTokens": {
              "type": "number",
              "description": "触发压缩的 token 阈值 (默认从配置读取)"
            },
            "minMessagesToKeep": {
              "type": "number",
              "description": "最少保留的最新消息数 (默认 5)"
            },
            "force": {
              "type": "boolean",
              "description": "是否强制压缩 (即使未超阈值)"
            }
          }
        }
      }
    ]
  }
}
---

# Session Compactor

本技能提供自动化的会话压缩功能，解决长对话导致的 token 超限问题。

## 何时使用

- 会话消息数超过 30 条，接近模型上下文窗口限制
- 需要保留关键上下文但控制 token 消耗
- 手动调用以优化对话历史

## 快速开始

### 配置

在 `openclaw.config.json` 中启用:

```json
{
  "skills": {
    "session-compactor": {
      "enabled": true,
      "maxTokens": 3000,
      "minMessagesToKeep": 5,
      "autoCompact": true
    }
  }
}
```

### 自动模式

设置 `"autoCompact": true` 后，每次会话更新会自动检测并压缩。

### 手动调用

调用工具 `compact_session`:

```bash
openclaw tools call compact_session '{"force": false}'
```

## 工作原理

1. **Token 估算** - 使用启发式方法 (1 token ≈ 4 字符)
2. **触发检测** - 当前 tokens > maxTokens?
3. **选择目标** - 保留最新 `max(minKeep, total/3)` 条消息
4. **生成摘要** - 提取对话目标、工具调用、关键事实
5. **替换** - 用单条系统消息替代所有早期消息

压缩 **不可逆**，早期消息细节会丢失。

## 配置参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `maxTokens` | number | 3000 | 触发压缩的 token 阈值 |
| `minMessagesToKeep` | number | 5 | 至少保留的最新消息数 |
| `autoCompact` | boolean | true | 启用自动压缩 |
| `force` (工具参数) | boolean | false | 强制压缩（调用时） |

## 示例

### 压缩前

```json
[
  {"role":"user","content":"请分析赛力斯2025年报"},
  {"role":"assistant","content":"[tavily_search] 正在搜索..."},
  {"role":"user","content":"还要2024年对比数据"},
  {"role":"assistant","content":"[tavily_search] 已找到..."}
  // ... 继续累积到 50+ 条
]
```

### 压缩后

```json
[
  {"role":"system","content":"## 会话摘要 (已压缩早期 45 条消息)\n- 对话目标: 分析赛力斯2025年报...\n- 工具调用: 6 次..."},
  {"role":"user","content":"那么深信服的2025预测呢？"},
  {"role":"assistant","content":"继续..."}
  // ... 最新 16 条保持完整
]
```

## 技术实现

核心算法实现于 `scripts/compact_session.js`:

```javascript
const { compactSession } = require('./scripts/compact_session');

const result = await compactSession(messages, {
  maxTokens: 4000,
  force: false
});

console.log(result.compacteded); // true/false
console.log(result.savedTokens); // 节省的 token 数
```

详细设计文档见 `references/architecture.md`。

## 注意事项

⚠️ **压缩不可逆** - 早期消息细节永久丢失  
⚠️ **阈值设置** - 建议 maxTokens 设较高 (4000-6000) 避免过早压缩  
⚠️ **生产增强** - 考虑集成 LLM 生成高质量摘要

## 参考资料

- `references/architecture.md` - 详细设计说明
- claw-code 原始实现: `compact.rs` (https://github.com/instructkr/claw-code)

---
**版本**: 0.1.0  
**作者**: 小李 (基于 claw-code 分析实现)
