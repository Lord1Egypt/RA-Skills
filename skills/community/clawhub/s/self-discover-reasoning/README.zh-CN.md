<div align="center">

# 🔍 Self-Discover Skill

**AI 智能体的自组合推理结构。**

*让 AI 在解题之前，先发现最优推理策略。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-blue)](https://openclaw.ai)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple)](https://claude.ai)
[![Cursor](https://img.shields.io/badge/Cursor-compatible-orange)](https://cursor.sh)
[![GitHub Copilot](https://img.shields.io/badge/Copilot-compatible-lightblue)](https://github.com/features/copilot)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-green)](https://github.com/openai/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-compatible-4285F4)](https://ai.google.dev)
[![Windsurf](https://img.shields.io/badge/Windsurf-compatible-00D4AA)](https://codeium.com/windsurf)
[![JetBrains](https://img.shields.io/badge/JetBrains-compatible-000)](https://www.jetbrains.com/ai/)
[![Benchmarked](https://img.shields.io/badge/benchmarked-25%25%20improvement-green)](BENCHMARK.md)

**[English](README.md)** | **中文**

</div>

---

## 它做什么

大多数 AI 推理用单一策略（通常是"一步步思考"）。这个 Skill 让 AI **为每个具体任务发现最优推理结构**：

```
选择 → 适配 → 实现 → 求解
```

基于同行评审研究：相比思维链提升最高 **32%**，超过自一致性 **20%+**，计算量还少 10-40 倍（Zhou et al., 2024, ICML）。

**一个文件。零依赖。零 API 成本。** 宿主 AI 自己组合推理结构。

---

## 实测效果

在 **5 个类别的 20 个问题**上基准测试，采用受控的前后对比评估。→ [完整报告](BENCHMARK.md)

| 指标 | 结果 |
|--------|--------|
| **整体提升** | **+25.3%** |
| 得到改善的问题 | 20/20（100%） |
| 单题最大提升 | +48.2% |

**各维度提升：**

| 维度 | Δ |
|-----------|---|
| 推理深度 | +31.5% |
| 结构质量 | +28.8% |
| 答案准确性 | +24.2% |
| 问题覆盖度 | +23.7% |
| 可执行性 | +22.0% |
| 效率 | +19.5% |

📖 [阅读完整基准报告 →](BENCHMARK.md)

---

## 优化前后对比

<details>
<summary><b>示例 1 — 复杂调试</b></summary>

**用户：** *"我的微服务在高负载下间歇性抛 503。时好时坏，看不出规律。"*

**❌ 无 Self-Discover：**
> 听起来是容量问题。负载下服务可能资源不够。检查峰值时段的 CPU 和内存。可能需要水平扩容或优化代码。也查一下数据库连接——连接池耗尽是常见原因。考虑加熔断和重试。

**✅ 有 Self-Discover：**
> 选定模块：分解、因果分析、假设检验、约束满足
>
> **根因候选（按可能性排序）：**
>
> | # | 假设 | 待查证据 | 修复 |
> |---|-----------|-------------------|-----|
> | 1 | 连接池耗尽 | 503 期间 `SHOW STATUS LIKE 'Threads_connected'` | 增大连接池 + 加超时 |
> | 2 | 线程池饱和 | `wrk -t12 -c400` + 监控 `ActiveThreads` | 换异步 I/O 或加 worker |
> | 3 | 下游超时级联 | 503 窗口内查上游 P99 延迟 | 加熔断、快速失败 |
>
> **调试序列：**
> ```bash
> # 1. 确认与负载相关
> watch -n1 'curl -s -o /dev/null -w "%{http_code}" http://service/health'
> # 2. 503 窗口内查连接数
> netstat -an | grep ESTABLISHED | wc -l
> # 3. 对照连接池配置
> grep -i pool application.yml
> ```

</details>

<details>
<summary><b>示例 2 — 架构决策</b></summary>

**用户：** *"实时通知用 WebSocket 还是 SSE？"*

**❌ 无 Self-Discover：**
> 都能做实时。WebSocket 双向，SSE 只能服务器到客户端。只要服务器推送就选 SSE，更简单。客户端也要发消息就用 WebSocket。考虑兼容性——SSE 到处能用，WebSocket 可能遇代理问题。

**✅ 有 Self-Discover：**
> 选定模块：对比分析、约束满足、系统思维
>
> | 因素 | SSE | WebSocket | 胜者 |
> |--------|-----|-----------|--------|
> | 方向 | 服务器→客户端 | 双向 | 看场景 |
> | 重连 | 自动（内置） | 手动（心跳+重连） | SSE |
> | 协议 | HTTP/1.1+（简单） | Upgrade 握手（复杂） | SSE |
> | 二进制数据 | 不支持（纯文本） | 支持 | WS |
> | 负载均衡兼容 | 原生 HTTP | 需粘性会话/配置 | SSE |
> | 扩展 | 简单（无状态连接） | 较难（有状态） | SSE |
>
> **通知场景（服务器→客户端、文本、要可靠）：选 SSE。**
>
> ```javascript
> // 服务器 (Express)
> app.get('/notifications', (req, res) => {
>   res.setHeader('Content-Type', 'text/event-stream');
>   res.setHeader('Cache-Control', 'no-cache');
>   const push = (data) => res.write(`data: ${JSON.stringify(data)}\n\n`);
>   subscribe(req.user.id, push);
>   req.on('close', () => unsubscribe(req.user.id, push));
> });
> ```
> 只有需要客户端→服务器实时（协同编辑、游戏）才用 WebSocket。

</details>

<details>
<summary><b>示例 3 — 数学题</b></summary>

**用户：** *"球拍和球一共 $1.10。球拍比球贵 $1.00。球多少钱？"*

**❌ 无 Self-Discover：**
> 球 $0.10。球拍贵 $1.00，所以 $1.10。合计 $1.10。✓

**✅ 有 Self-Discover：**
> 选定模块：批判性思维、约束满足、假设检验
>
> **建立约束：**
> - 球拍 + 球 = $1.10
> - 球拍 = 球 + $1.00
>
> **代入：**（球 + $1.00）+ 球 = $1.10 → 2 × 球 = $0.10 → **球 = $0.05**
>
> **验证：** 球拍 = $0.05 + $1.00 = $1.05。合计 = $1.05 + $0.05 = $1.10 ✓
>
> 直觉答案（$0.10）不成立：$0.10 + $1.10 = $1.20 ≠ $1.10。

</details>

---

## 工作原理

### 20 个种子推理模块

| # | 模块 | 最适合 |
|---|--------|----------|
| 1 | **逐步思考** | 顺序流程 |
| 2 | **分解** | 多部分问题 |
| 3 | **批判性思维** | 评估断言 |
| 4 | **反思性思维** | 深度分析 |
| 5 | **创造性思维** | 开放式设计 |
| 6 | **模式识别** | 数据、序列 |
| 7 | **类比推理** | 迁移学习 |
| 8 | **因果分析** | 调试、诊断 |
| 9 | **约束满足** | 优化问题 |
| 10 | **抽象** | 架构、泛化 |
| ... | *SKILL.md 中还有 10 个* | |

### 4 个深度级别（自动选择）

| 级别 | 适用场景 | 模块数 | Token 成本 |
|:-----:|------|:-------:|:----------:|
| **0** | 简单问答 | 0 | +0% |
| **1** | 大多数对话 | 1-2 | ~10% |
| **2** | 复杂技术问题 | 3-5 | ~25% |
| **3** | 高风险 / 完整发现 | 4-7 | ~40% |

无需配置。智能体根据任务复杂度自动选择合适的深度。

### 跨任务结构迁移

发现的推理结构可在相似任务间迁移——用 `memory/discovered-structures.md` 缓存复用。基于 Zhou et al. 的发现：结构可跨模型家族迁移。

---

## 安装

<details>
<summary><b>OpenClaw（推荐）</b></summary>

```bash
# 复制到 skills 目录
cp -r self-discover-skill/ ~/.openclaw/skills/
```

完成。OpenClaw 自动检测 skill。

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
# 复制到项目
cp -r self-discover-skill/ skills/

# 添加到 CLAUDE.md
echo "Read and follow skills/self-discover-skill/SKILL.md" >> CLAUDE.md
```

</details>

<details>
<summary><b>Cursor</b></summary>

```bash
# 复制到项目根目录
cp -r self-discover-skill/ skills/

# 添加到 .cursorrules
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .cursorrules
```

</details>

<details>
<summary><b>Gemini CLI</b></summary>

```bash
# 复制到项目，添加到 GEMINI.md
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> GEMINI.md
```

</details>

<details>
<summary><b>GitHub Copilot</b></summary>

```bash
# 添加到仓库的 Copilot 指令
mkdir -p skills && cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .github/copilot-instructions.md
```

</details>

<details>
<summary><b>Codex CLI (OpenAI)</b></summary>

```bash
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> AGENTS.md
```

</details>

<details>
<summary><b>Windsurf</b></summary>

```bash
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .windsurfrules
```

</details>

<details>
<summary><b>Cline / AI 编程助手</b></summary>

把 `self-discover-skill/` 复制进项目，在助手的自定义指令中引用 `SKILL.md`。

</details>

<details>
<summary><b>JetBrains AI / Junie</b></summary>

1. 打开 Settings → Tools → AI Assistant → System Instructions
2. 添加：`Read and follow skills/self-discover-skill/SKILL.md`
3. 把 skill 文件夹放在项目根目录

</details>

<details>
<summary><b>Zed</b></summary>

1. 打开 Zed 设置
2. 添加到 context 或 assistant 指令：
```
Read and follow skills/self-discover-skill/SKILL.md
```

</details>

<details>
<summary><b>Kiro</b></summary>

1. 把 skill 文件夹加入项目
2. 在 Kiro 的指令配置中引用

</details>

<details>
<summary><b>OpenCode</b></summary>

1. 把 skill 文件夹加入项目
2. 添加到 `AGENTS.md`：`Read and follow skills/self-discover-skill/SKILL.md`

</details>

<details>
<summary><b>ChatGPT Custom GPT</b></summary>

1. 打开你的 GPT → Settings → Instructions
2. 粘贴 `SKILL.md` 的内容
3. 保存

**注意：** SKILL.md 内置了无文件访问环境的内联模板——所有深度级别都可用。结构记忆仅对话内有效（无持久化）。

</details>

<details>
<summary><b>任意 AI 工具</b></summary>

把 `SKILL.md` 复制进你的系统提示或指令文件。只需要这一个文件。

</details>

---

## 平台兼容性

**热门平台（按使用量排序）：**

| 平台 | 评级 | 结构记忆 | 说明 |
|----------|:------:|:----------------:|-------|
| **Claude Code** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 2026 年第一编程智能体，完整支持 |
| **Cursor** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | $2B ARR 的 AI IDE，完整支持 |
| **GitHub Copilot** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 用户量最大，完整支持 |
| **Codex CLI** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | OpenAI 编程智能体，完整支持 |
| **ChatGPT** | ⭐⭐⭐⭐ | ⚠️ 仅对话内 | 内联模板自动加载，全级别可用 |

<details>
<summary><b>展开全部 14 个支持平台</b></summary>

| 平台 | 评级 | 结构记忆 | 安装 |
|----------|:------:|:----------------:|---------|
| **OpenClaw** | ⭐⭐⭐⭐⭐ | ✅ `memory/` 目录 | 复制到 `skills/`，自动检测 |
| **Claude Code** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 复制进项目，加到 `CLAUDE.md` |
| **Cursor** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 复制进项目，加到 `.cursorrules` |
| **GitHub Copilot** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 加到 `.github/copilot-instructions.md` |
| **Codex CLI** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 加到 `AGENTS.md` |
| **Gemini CLI** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 加到 `GEMINI.md` |
| **Windsurf** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 加到 `.windsurfrules` |
| **Cline** | ⭐⭐⭐⭐⭐ | ✅ 文件写入 | 加到自定义指令 |
| **JetBrains AI / Junie** | ⭐⭐⭐⭐½ | ✅ 文件写入 | 加到 AI Assistant 指令 |
| **Aider** | ⭐⭐⭐⭐ | ✅ 文件写入 | 放进项目，用 `--file` 引用 |
| **Zed** | ⭐⭐⭐⭐ | ✅ 文件写入 | 加到 Zed 设置 |
| **ChatGPT GPT** | ⭐⭐⭐⭐ | ⚠️ 仅对话内 | 把 SKILL.md 粘贴进 GPT Instructions |
| **Kiro** | ⭐⭐⭐⭐ | ✅ 文件写入 | 加到 Kiro 指令 |
| **OpenCode** | ⭐⭐⭐⭐ | ✅ 文件写入 | 加到 AGENTS.md |

</details>

---

## 学术基础

| 论文 | 年份 | 我们用了什么 |
|-------|:----:|-------------|
| **SELF-DISCOVER** — Zhou et al. | 2024 | 核心的选择→适配→实现→求解框架 |
| **Chain of Thought** — Wei et al. | 2022 | 基线单模块推理 |
| **Self-Consistency** — Wang et al. | 2022 | 对比目标（Self-Discover 用更少算力胜出） |
| **Least-to-Most Prompting** — Zhou et al. | 2022 | 分解模块灵感 |
| **Tree of Thoughts** — Yao et al. | 2023 | 多路径推理对比 |
| **Step-Back Prompting** — Zheng et al. | 2023 | 原理先行推理模块 |
| **OPRO** — Yang et al. | 2023 | 优化提示词对比 |

完整文献：[`references/sources.md`](references/sources.md)

---

## 文件结构

```
self-discover-skill/
├── SKILL.md                          # 核心指令（唯一必需文件）
├── README.md                         # 英文说明（本文件为中文版）
├── LICENSE                           # MIT
└── references/
    ├── sources.md                    # 学术来源与链接
    └── discovery-templates.md        # 按深度级别即用的发现模板
```

---

<div align="center">

**推理的艺术不在答案，而在发现通往答案的结构。**

如果这个 Skill 提升了你 AI 的推理质量，欢迎点个 ⭐。
