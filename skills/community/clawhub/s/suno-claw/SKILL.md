# SKILL.md — suno-claw

**来源:** https://github.com/jasonzhang-zzx/suno-claw  
**作者:** jasonzhang-zzx  
**许可证:** MIT

## 概述

一个基于 Suno AI（kie.ai API）的多代理创意工作流技能。模拟艺术创作的发散与收敛过程，通过迭代式信息解析与生成，逐步产出符合 Suno 输入标准的高质量歌曲。

**核心流程：** 灵感输入 → 信息收集 → 双轨解析（歌词/音乐性）× 3轮发散 → 封包为 Suno prompt → 渐进生成 → 试听反馈 → 记忆存档

## 流式输出规则

每个步骤开始和结束时，主代理须输出状态描述，让用户感知 Pipeline 进度：

| 步骤 | 开始时 | 结束时 |
|------|--------|--------|
| Step 1 收集 | `🎯 正在解析您的创意...` | `✨ 创意解析完成` |
| Step 2 Agent A | `✍️ 词作者正在工作...` | `✍️ 词作者完成（第X轮）` |
| Step 2 Agent B | `🎸 编曲师正在工作...` | `🎸 编曲师完成（第X轮）` |
| Step 3 封包 | `📦 正在封装提示词...` | `📦 封装完成` |
| Step 4 生成 | `🎵 Suno(kieAI) 正在创作...` | `🎵 创作完成` |
| Step 5 存档 | `💾 正在保存您的偏好...` | `💾 已存档` |

用户对生成结果评分/评价后，触发记忆存档环节。

---

## 目录结构

```
suno-claw/
├── SKILL.md                      # 本文件
├── workflow.md                   # 工作流详细说明
├── memory-system.md              # 记忆系统设计
├── prompts/
│   ├── collector.md              # 信息收集代理说明
│   ├── agent-a.md                # Agent A（歌词）子代理完整 Prompt（含角色+JSON Schema+格式规则）
│   ├── agent-b.md                # Agent B（音乐性）子代理完整 Prompt（含角色+JSON Schema+格式规则）
│   ├── executor-main.md          # 主代理执行器（Pipeline 总指挥，含调度逻辑）
│   ├── packager.md               # Suno 封包代理（JSON Schema + 校验规则）
│   └── generator.md               # kie.ai API 调用指南
├── scripts/
│   └── suno_generate.py          # kie.ai Suno API Python 调用脚本
└── memory/
    ├── history.json              # 交互历史（JSON，热数据）
    └── patterns.log              # 压缩模式日志（长期记忆）
```

---

## 执行层架构

```
主代理（executor-main.md 驱动）
    │
    ├── Step 1: 收集 + IS_INSTRUMENTAL 判断
    │       ↓
    ├── Step 2: sessions_spawn 并行调度子代理
    │       ├─ Agent A (agent-a.md) ──→ JSON 歌词结果
    │       └─ Agent B (agent-b.md) ──→ JSON 音乐性结果
    │           ↓ × 3轮（relevance: 1.0 → 0.7 → 0.5）
    ├── Step 3: 封包（packager）→ Suno Prompt × 3
    │       ↓
    ├── Step 4: 渐进生成
    │       ├─ python scripts/suno_generate.py --style_tags ... --lyrics ... --title ...
    │       ├─ 返回音频 URL + 歌词
    │       └─ 展示给用户 → 等待确认 → 下一轮
    │       ↓
    └── Step 5: 用户"喜欢" → 写入 history.json + patterns.log
```

---

## 核心概念

### 1. 相关性衰减（Relevance Decay）

| 轮次 | Relevance | 含义 |
|------|-----------|------|
| 第1轮 | 1.0 | 严格围绕原始创意，精准提炼 |
| 第2轮 | 0.7 | 适度延伸，引入关联元素，参考 HISTORY_SIGNAL |
| 第3轮 | 0.5 | 高度发散，探索远距联想，HISTORY_SIGNAL 参考价值最大 |

- **`RELEVANCE_LEVEL`** = 本轮输出相对于 `INFO_COLLECTION_TABLE` 的相关性强度
- **`HISTORY_SIGNAL`** = 来自 `patterns.log` 的历史偏好参考材料，子代理**自行判断**如何使用（不是约束指令）

### 2. IS_INSTRUMENTAL 双分支

| IS_INSTRUMENTAL | 唤醒的子代理 |
|----------------|------------|
| `false`（有歌词）| Agent A（歌词）+ Agent B（音乐性）并行 |
| `true`（纯音乐） | 仅 Agent B（音乐性） |

### 3. 渐进生成（用户确认制）

每步生成后**先展示试听，用户确认后再跑下一步**，有效节约 API 用量。

### 4. 记忆系统

- **热数据（history.json）**：完整交互快照，最近 50 条
- **长期记忆（patterns.log）**：成功标签模式压缩存档，无限积累
- **调用新任务时**：从 `patterns.log` 读取偏好，注入 Agent A/B 第2、3轮

---

## 触发条件

用户说"制作一首..."、"创作一首歌..."、"做一首...风格的歌"、"生成纯音乐"时触发。

---

## 输入

**用户原始创意**（字符串），例如：
- "制作一首 Kill This Love 风格的歌曲"
- "做一首西海岸 chill rap"
- "生成一段放松的钢琴纯音乐"

---

## 输出（每轮生成后）

1. **歌名**
2. **试听链接**（Suno 音频 URL）
3. **完整歌词**（含结构标签，仅 IS_INSTRUMENTAL=false 时）
4. **核心风格描述**（≤2句）

---

## 环境变量

**必需环境变量：**

| 变量 | 必填 | 说明 |
|------|:----:|------|
| `KIEAI_API_KEY` | ✅ | kie.ai API 密钥（https://kie.ai/api-key 获取） |

**可选环境变量：**

| 变量 | 必填 | 默认值 | 说明 |
|------|:----:|--------|------|
| `CALLBACK_URL` | ❌ | 空（不传） | 生成完成后的回调地址；若为空字符串则不传给 API，推荐使用内部可信端点 |

### 安全说明

- **SSL 验证**: 始终启用，不可禁用
- **CALLBACK_URL 建议**: 使用内部可控的回调服务，或留空（由 kie.ai 轮询）
- **避免**: 设为未知第三方地址，以免生成内容被意外泄露

### 记忆文件 Retention

| 文件 | 路径 | 保留策略 |
|------|------|----------|
| `history.json` | `memory/history.json` | 最近 50 条交互，超出后自动截断（仅保留最新） |
| `patterns.log` | `memory/patterns.log` | 聚合偏好模式；单文件上限 1MB，超出后轮转（保留最新） |

> **隐私提示**：以上文件包含你的歌词、风格偏好、生成记录。如需清理，删除对应文件即可。

---

## 质量门控

| 检查点 | 标准 | 失败处理 |
|--------|------|---------|
| Agent A JSON 解析 | 纯 JSON，无 markdown 块 | 重试，最多3次 |
| Agent A 格式校验 | 含 [Verse]+[Chorus]，无歌手名 | 重试当前轮次 |
| Agent B JSON 解析 | 纯 JSON，无 markdown 块 | 重试，最多3次 |
| Agent B 格式校验 | style_tags ≤ 115字符，无歌手名，≥3个乐器 | 重试当前轮次 |
| 封包校验 | style ≤ 115字符，title ≤ 80字符 | 自动修正 |
| API 失败 | 返回错误 JSON | 自动以更低相关性重试 |

---

## 主代理执行参考（executor-main.md）

当运行本技能时，主代理按照 `prompts/executor-main.md` 中的指引执行：

1. **sessions_spawn** 并行调度 Agent A + Agent B
2. 每轮 **JSON Schema 校验**（含歌手名检测正则）
3. 校验失败时**反馈错误给子代理，要求重做**
4. **python scripts/suno_generate.py** 调用 kie.ai API
5. **渐进展示 + 用户确认**后继续

---

## 相关技能

- `clawhub install suno` — Suno API 基础封装（参考 aimusicapi.ai）
- `clawhub install browser` — 浏览器自动化备用方案
