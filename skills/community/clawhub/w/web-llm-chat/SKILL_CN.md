---
name: web-llm-chat
description: 通过 Chrome Relay 扩展与网页端大模型对话。免费使用强大的联网搜索和 RAG 能力，无需 API 费用。当前支持 Qwen AI (chat.qwen.ai)。适用于联网搜索、深度研究、多轮对话、获取第二意见、对比 AI 回复或委托复杂推理任务。需要在浏览器中打开 LLM 聊天标签页并连接 Chrome Relay 扩展。触发词包括 "ask Qwen", "search with Qwen", "Qwen search", "deep research with Qwen", "Qwen research", "web LLM search", "browser AI chat", "free AI search", "Qwen怎么说", "去问Qwen", "Qwen 搜索", "Qwen 研究", "用 Qwen 深度研究"。
---

# Web LLM Chat 技能

通过 Chrome Relay 扩展以编程方式与网页端大模型交互。本技能支持自动化对话，包括简单查询和多轮研究工作流。

**当前支持：** Qwen AI (chat.qwen.ai) — 更多模型即将支持。

## 为什么需要这个技能？

### 痛点

- **搜索 API 昂贵**：Brave Search API、Tavily 等服务需要 API 密钥和付费订阅，产生持续成本。
- **研究能力有限**：传统搜索 API 只返回原始结果，缺乏现代大模型的推理和综合能力。
- **质量与成本的权衡**：获得高质量、有深度的研究往往需要昂贵的 API 调用或大量人工。

### 机会

现代网页端大模型（如 Qwen）提供了：

- **强大的内置搜索**：原生联网搜索，实时获取信息
- **RAG 能力**：自动检索增强生成，确保回答有据可依
- **深度研究功能**：多源综合与引用
- **商业级质量**：由大公司支持的产品，持续迭代改进

### 解决方案

本技能利用 OpenClaw 的 Chrome Relay：

- **免费访问网页大模型**：使用网页界面，无需 API 费用
- **自动化研究流程**：让 Agent 进行多轮调研
- **更高质量的结果**：以更低成本享受商业大模型能力
- **支持对比验证**：交叉参考其他 AI 回复

**一句话总结**：用 OpenClaw 编排强大的网页大模型，成本远低于 API，研究质量优于原始搜索 API。

## 功能特性

- **发送消息**：向网页端大模型发送消息并接收回复
- **多种输出格式**：纯文本、Markdown（保留代码块、表格、列表）或原始 HTML
- **发送就绪检测**：等待页面准备好接收下一个问题
- **智能提取**：基于锚点的提取，只获取最新回复
- **研究模式**：Agent 编排的多轮对话

## 支持的模型

| 模型 | 状态 | 说明 |
|-----|------|------|
| Qwen AI (chat.qwen.ai) | ✅ 已支持 | 完整支持搜索、RAG 和多轮对话 |
| 更多模型 | 🚧 即将支持 | 提交 Issue 申请支持其他网页端大模型 |

## 环境要求

- Chrome Relay 扩展已连接到 Qwen Chat 标签页 (`chat.qwen.ai/*`)
- Gateway 运行在 `127.0.0.1:18789`（默认）
- Node.js 已安装 `ws` 包

## 安装

使用你喜欢的包管理器安装 `ws` 包：

```bash
# npm
npm install ws

# yarn
yarn add ws

# pnpm
pnpm add ws
```

## 快速开始

### 检查连接状态

```bash
node scripts/qwen_chat.js status
```

### 发送消息

```bash
# 纯文本（默认）
node scripts/qwen_chat.js send "什么是机器学习？"

# 自定义等待时间（用于长回复）
node scripts/qwen_chat.js send "详细解释 RAG" --wait 120

# 获取 Markdown 格式回复（保留格式）
node scripts/qwen_chat.js send "写一个 Python 函数" --format markdown

# 获取原始 HTML
node scripts/qwen_chat.js send "创建一个表格" --format html
```

### 读取当前页面内容

```bash
node scripts/qwen_chat.js read
```

## 命令参考

### `status`

检查 Chrome Relay 是否已连接，Qwen 标签页是否激活。

```bash
node scripts/qwen_chat.js status
```

输出示例：
```
Extension: ✅ Connected
Qwen tab: ✅ Qwen Chat
  URL: https://chat.qwen.ai/c/...
```

### `send`

向 Qwen 发送消息并接收回复。

```bash
node scripts/qwen_chat.js send "你的消息" [选项]
```

**选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--wait N` | 最大等待时间（秒） | 45 |
| `--format text\|markdown\|html` | 输出格式 | text |
| `--debug-extract` | 显示提取调试信息 | 关闭 |

**输出格式：**

- `text` — 纯文本输出
- `markdown` — 保留代码块、表格、列表、标题等格式
- `html` — 页面原始 HTML

### `read`

读取当前页面内容（用于调试或查看对话历史）。

```bash
node scripts/qwen_chat.js read
```

## 工作原理

### 回复提取

脚本使用稳健的提取策略：

1. **发送就绪检测**：等待页面准备好接收下一个问题（输入框可编辑、发送按钮可用）
2. **锚点提取**：以用户消息为锚点，定位并提取最新回复
3. **内容稳定**：等待内容稳定后再提取

### 为什么不用 Thinking 指示器？

- Thinking 指示器可能视觉卡住，但回复已完成
- 发送就绪检测更可靠：如果能发送下一个问题，说明上一个回复已完成
- 不受 Thinking 指示器 UI 变化的影响

### 为什么不用 Body 长度差值？

- Qwen 页面可能重新布局，导致 `bodyLen` 不可预测地变化
- 锚点提取对页面重排更稳健
- 只提取实际回复内容，不包含噪声

## 研究模式（Agent 编排）

对于多轮研究，建议使用 Agent 编排模式，而非固定的 `research` 命令。这样 Agent 可以根据 Qwen 的回复动态控制对话。

### 工作流程

```
1. 确定研究主题
2. 提第一个问题（开放式，让 Qwen 展开）
3. 阅读 Qwen 回复
4. 分析回复：
   - 哪个点值得深入？
   - 哪个说法需要交叉验证？
   - 有没有矛盾或遗漏？
5. 基于分析追问
6. 重复步骤 3-5，共 5-10 轮
7. 最后一轮：请 Qwen 总结，Agent 也整理自己的总结
```

### 每轮操作示例

```bash
# Agent 发送问题并等待回复
node scripts/qwen_chat.js send "RLHF 的关键挑战是什么？" --wait 120

# 如需要，Agent 可以读取完整页面
node scripts/qwen_chat.js read
```

### 追问策略

好的追问来自 Qwen 的回复：

| 回答模式 | 追问方向 |
|---------|---------|
| 提到数据/统计 | "原始来源是什么？样本量多大？" |
| 给出观点但无证据 | "有研究支持这个说法吗？" |
| 提到争议 | "反对意见的核心论据是什么？" |
| 说"可能/也许" | "在什么条件下成立？什么条件下不成立？" |
| 列举多个因素 | "最关键的是哪个？为什么？" |
| 提到案例 | "这个案例被其他研究者质疑过吗？" |
| 跑题/泛泛而谈 | "回到核心问题，具体来说..." |

### 最佳实践

- **不要预设问题清单**：根据回复动态生成问题
- **允许跑偏**：如果 Qwen 提到意外但有趣的点，可以追下去
- **适当挑战**：不必总是同意 Qwen，可以提出反对意见
- **保持连贯**：追问时简短引用上轮关键点
- **控制轮数**：5-10 轮最佳；太少深入不了，太多边际收益递减
- **诚实处理超时**：如果脚本超时，如实报告，不要编造内容
- **调整等待时间**：搜索类问题用 `--wait 180`，简单问题 `--wait 60` 足够

## 调试

### 启用提取调试

```bash
node scripts/qwen_chat.js send "测试消息" --wait 90 --debug-extract
```

这将显示：
- 基线和最新 body 长度
- 检测到的叶子元素数量
- 使用的提取路径
- 原始和最终内容长度

### 常见问题

| 问题 | 解决方案 |
|-----|---------|
| 扩展断开连接 | 检查 Chrome 扩展徽章是否显示 `ON` |
| 找不到 Qwen 标签页 | 打开 `chat.qwen.ai` 并连接扩展 |
| 回复未捕获 | 增加 `--wait` 时间，使用 `--debug-extract` 诊断 |
| Markdown 格式异常 | 代码块使用 Monaco Editor；提取会自动处理 |

## 配置

### 认证令牌

脚本自动从 OpenClaw 配置中派生 relay 令牌。配置优先级：

1. `E:\.openclaw\.openclaw\openclaw.json` (Windows)
2. `~/.openclaw/.openclaw/openclaw.json` (Unix)

### Gateway 端口

- Gateway: `18789`
- Relay: `18792` (Gateway + 3)

## 限制

- 需要在浏览器中登录 Qwen
- 一次只能控制一个标签页
- 不支持流式输出 — 等待完整回复后才返回

## 文件结构

```
qwen-chat/
├── SKILL.md                    # 英文文档
├── SKILL_CN.md                 # 中文文档（本文件）
├── scripts/
│   ├── qwen_chat.js           # 主脚本
│   ├── _diagnose_selectors.js # 诊断工具
│   └── _analyze_format.js     # 格式分析
└── references/
    └── chrome-relay.md        # Chrome Relay 配置指南
```

## 相关链接

- [Chrome Relay 配置](references/chrome-relay.md) — 详细的 relay 配置说明

## 许可证

详见 [LICENSE](LICENSE) 文件。