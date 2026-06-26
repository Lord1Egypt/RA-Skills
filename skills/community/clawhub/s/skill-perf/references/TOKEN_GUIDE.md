# Token 类型详解

> 本文档是 skill-perf 的参考资料，解释 OpenClaw sessions.json 中各 token 字段的含义，
> 以及它们在 skill 性能测量中的应用。

---

## 一、各字段含义

OpenClaw 在每个 session 结束后，将以下字段写入 `~/.openclaw/agents/*/sessions/sessions.json`：

### `inputTokens`

**本次请求新鲜发送（未命中 cache）的 input token 数量**，即扣除 cacheRead 后的净增量。

包含（Cron session 典型值约 5,000–10,000）：
- 本次触发的 skill SKILL.md 内容
- 用户任务消息
- 新增的工具调用请求/响应体
- 少量框架元数据（非缓存部分）

⚠️ `inputTokens` **不含** cacheRead 的部分——实际发给模型的总 input = `cacheRead + inputTokens`。

---

### `outputTokens`

**LLM 生成的 token 数量**，包含：
- Agent 的思考内容（reasoning/thinking tokens）
- 工具调用请求（tool call JSON）
- 最终回复文本

全价计费，无折扣。

---

### `cacheRead`

**命中 Prompt Cache 的 input token 数量**（system prompt + 工具描述的完整内容）。

OpenClaw 每次调用都会组装一个较大的 system prompt 并发给模型，内容包含（来源：[官方文档](https://docs.openclaw.ai/reference/token-use.md) + 本机 `systemPromptReport` 实测）：

| 构成部分 | 字符数（本机实测） | 说明 |
|---------|-----------------|------|
| **工具 JSON Schema**（44 个工具） | ~26,800 chars | 每个工具的完整参数定义，占大头 |
| **技能描述列表**（27 个 skill） | ~11,300 chars | 每个 skill 的 name+description，注入 system prompt |
| **Bootstrap 文件**（8 个文件） | ~5,600 chars | AGENTS.md / SOUL.md / TOOLS.md / IDENTITY.md / USER.md / HEARTBEAT.md / BOOTSTRAP.md / MEMORY.md |
| **框架层固定内容** | ~26,000 chars | 安全指令、运行时元数据、时区、Reply Tags 等 |
| **system prompt 合计** | **~32,300 chars** | 注：chars/4 只是粗估，Kimi tokenizer 实际可能 2× |

> ⚠️ **chars ≠ tokens（关键！）**
> `systemPromptReport` 里记录的 `systemPrompt.chars = 32,301`，若按英文 4 chars/token 估算只有 ~8,000 tokens。
> 但实测 `cacheRead = 127,232 tokens`——相差 ~15×！
>
> **原因**：`systemPromptReport.chars` 只记录了本 session 的字符数，而实际 Cron session 发送的完整 system prompt 包含了更多内部框架层内容（工具调用规范、推理指令、对话格式要求等），这些内容不体现在 chars 里，但在 tokenizer 处理后大幅膨胀。
>
> **实测对比**：
> - `skill-calibration`（最小 skill）→ `cacheRead = 35,328`
> - `html-extractor`（中等 skill，SKILL.md 1,537 tokens）→ `cacheRead = 127,232`
> - 差值 = **91,904 tokens**，与 SKILL.md 大小（1,537）完全不匹配
>
> **结论**：cacheRead 的大小主要由 **OpenClaw 框架层内部内容**决定（不对外暴露），Bootstrap 文件和 skill 描述只是其中很小的一部分。Bootstrap 文件贡献约 **1,400 tokens**，skill 描述约 **3,900 tokens**，合计 **~5,300 tokens**，仅占 cacheRead 的约 4%。

这部分内容**基本不变**，会被 LLM 服务商缓存。后续调用直接从 cache 读取，按折扣价计费（Kimi 为 0.1×，百炼隐式缓存为 0.2×，Anthropic 为 0.1×）。

> ⚠️ **cacheRead 大小不是固定常量**，与以下因素相关：
> - 安装了多少 skills（**主要影响因素**：skill 触发后 SKILL.md 全文会注入）
> - OpenClaw 版本（框架层内容升级后会变化）
> - 工具数量（每个工具的 JSON schema 都会注入）

| cacheRead 状态 | 含义 |
|---|---|
| `0` | 首次执行 or cache 已过期，system prompt 需重新写入 |
| `> 100,000` | Cache 热命中，大幅省钱 |

> **为什么 cacheRead 比 inputTokens 大这么多？**
> `inputTokens` 只含本次新发送的部分（任务消息，约 1,000–10,000），
> `cacheRead` 是已缓存的 system prompt 全量（约 35,000–130,000，取决于 skill），两者相加才是实际发给模型的总 input。

---

### `cacheWrite`

**本次写入 Prompt Cache 的 token 数量**，按约 **1.25×（125%）溢价**计费。

首次发送某段内容（或 cache 过期后重建）时触发写入。通常在第一次执行某个 Cron session 时较大，后续 cache 命中后为 0。

> `cacheWrite` 虽然贵，但写入一次后后续调用的 `cacheRead` 可以持续省钱，整体仍划算。

---

### `totalTokens`（⭐ 核心指标）

**实际计费的 token 总量**，计算方式（参考 Anthropic 官方 Prompt Caching 定价，实际系数因提供商而异）：

```
totalTokens ≈ cacheWrite  × 1.25   ← 写入缓存，溢价 25%（Anthropic 定价）
            + cacheRead   × 0.10   ← 读取缓存，折扣 90%（Anthropic 定价）
            + inputTokens × 1.0    ← 新鲜发送，全价
            + outputTokens × 1.0   ← LLM 生成，全价
```

> ⚠️ **来源说明**：1.25× 和 0.1× 来自 [Anthropic 官方定价](https://www.anthropic.com/pricing) 中的 Prompt Caching 系数。
> OpenClaw 实际经过的计费层可能不同（自有代理、Vertex AI、AWS Bedrock 等），导致实际误差约 16%：
> 估算 `127,232×0.1 + 6,378 + 585 ≈ 19,686`，实测 totalTokens = 23,416（差值原因不明确）。

**典型 Cron session（cache 热命中）数值示例：**
```
cacheRead    = 127,232  →  127,232 × 0.10 = 12,723
inputTokens  =   6,378  →    6,378 × 1.00 =  6,378
outputTokens =     585  →      585 × 1.00 =    585
cacheWrite   =       0
─────────────────────────────────────────────────────
totalTokens（估算）≈ 19,686   实测 = 23,416
```

这是**真实消耗/计费的数字**，也是 skill-perf 比较性能时使用的**唯一基准指标**。

---

## 二、字段关系示例

### 示例 A：html-extractor skill 实测（cache 热命中）

```
字段               值          含义
─────────────────────────────────────────────────────────────────
cacheRead     127,232   ← System prompt 全量命中 cache（工具描述+技能清单+框架）
inputTokens     6,378   ← 新发送：任务消息 + html-extractor SKILL.md（1,537 tokens）
outputTokens      585   ← LLM 生成内容
cacheWrite          0   ← 无写入（cache 未过期）
─────────────────────────────────────────────────────────────────
实际发给模型的 input = cacheRead + inputTokens = 133,610 tokens
totalTokens（计费） = 127,232×0.1 + 6,378×1.0 + 585×1.0 ≈ 19,686（实测 23,416）
```

**cache 命中率 = cacheRead / (cacheRead + inputTokens) = 127,232 / 133,610 ≈ 95.2%**

### 示例 B：首次执行（cache 冷启动）

```
字段               值          含义
─────────────────────────────────────────────────────────────────
cacheRead           0   ← 无缓存命中
cacheWrite    127,232   ← 首次写入 cache，按 1.25× 计费
inputTokens     6,378
outputTokens      585
─────────────────────────────────────────────────────────────────
totalTokens ≈ 127,232×1.25 + 6,378 + 585 = 166,003（贵很多！）
```

**结论：保持 cache 热是节省 token 的最重要手段。** `cacheRetention: long` + heartbeat 是关键配置。

---

## 三、系统底噪（System Noise）

### 什么是系统底噪？

即使 skill 本身只做最简单的事，每次 Cron isolated session 也会产生约 **18,000 totalTokens** 的固定开销，这就是系统底噪。

底噪的来源（基于 [OpenClaw 官方文档](https://docs.openclaw.ai/reference/token-use)）：

OpenClaw 在每次 run 时组装 system prompt，包含：

| 组成部分 | 说明 | 估算大小 |
|------|------|----------|
| Tool list + descriptions | 所有可用工具的短描述 | ~4–6 KB |
| Skills list (metadata) | 技能清单（仅 metadata，指令按需加载） | ~3–5 KB |
| Self-update instructions | 自更新指引 | ~1 KB |
| Workspace bootstrap files | AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, MEMORY.md 等 | ~8–12 KB |
| Time + reply tags + heartbeat | UTC/本地时间、回复标签、心跳行为 | ~1 KB |
| Runtime metadata | host/OS/model/thinking | ~0.5 KB |
| Agent reasoning | 推理思考（thinking tokens，计入 output） | ~1–3 KB |

合计约 **20–30 KB 原始输入**，考虑 prompt cache 折扣后约 **18,000 totalTokens**。

> 📖 官方参考：
> - [Token Use and Costs](https://docs.openclaw.ai/reference/token-use) — system prompt 构成、context window 计费规则
> - [Prompt Caching](https://docs.openclaw.ai/reference/prompt-caching) — cacheRetention 配置、cache 诊断工具
> - [Usage Tracking](https://docs.openclaw.ai/concepts/usage-tracking) — `/status`、`/usage` 查看用量
> - [AGENTS.md Template](https://docs.openclaw.ai/reference/templates/AGENTS) — workspace 文件规范

### 官方 Token 节省建议（来自 docs.openclaw.ai）

- 用 `/compact` 压缩长对话
- 裁剪大型工具输出
- 降低 `agents.defaults.imageMaxDimensionPx`（默认 1200）减少截图 token
- **保持 skill description 简短**（skill list 会注入 prompt）
- 对话探索阶段用小模型

### Bootstrap 文件截断限制

- 单文件最大：`agents.defaults.bootstrapMaxChars`（默认 **20,000** 字符）
- 总注入量上限：`agents.defaults.bootstrapTotalMaxChars`（默认 **150,000** 字符）
- `memory/*.md` 不会自动注入（按需通过 memory 工具加载）

### `--light-context` 降低底噪

官方 Cron CLI 支持 `--light-context` 参数（[docs](https://docs.openclaw.ai/cli/cron)）：

```bash
openclaw cron edit <job-id> --light-context
```

启用后，isolated job 的 bootstrap context **置空**（不注入 workspace 文件），可大幅降低底噪。
适合不需要读取 AGENTS.md / SOUL.md 的纯脚本任务。

### Prompt Cache 官方配置

```yaml
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "short"  # none | short | long
```

- `cacheRetention: "long"` + heartbeat `every: "55m"` → 保持 cache 热，降低 cache write 成本
- `cacheRetention: "none"` → 适合突发性通知 agent，避免无效 cache write
- 每个 agent 可独立配置：`agents.list[].params.cacheRetention`

### Cache 诊断工具

```yaml
diagnostics:
  cacheTrace:
    enabled: true
    filePath: "~/.openclaw/logs/cache-trace.jsonl"
```

或环境变量 `OPENCLAW_CACHE_TRACE=1` 启用，可查看逐 turn 的 cache 命中情况。

### Cron Session 保留策略

- `cron.sessionRetention`（默认 `24h`）自动清理已完成的 isolated session
- `cron.runLog.maxBytes` + `cron.runLog.keepLines` 控制运行日志大小

### ⚠️ 底噪与 PromptMode 强相关

OpenClaw 有三种 Prompt 模式，**不同 session 类型使用不同模式**，底噪差异显著：

| Session 类型 | PromptMode | 包含层 | 典型底噪 |
|---|---|---|---|
| **主对话** (`agent:main:main`) | `full` | 全部 9 层 | ~18,000 |
| **Cron session** (`agent:main:cron:xxx`) | `full` | 全部 9 层 | ~18,000 |
| **Subagent** (`agent:main:subagent:xxx`) | `minimal` | 省略 Layer 4+5 | ~7,000–12,000 |

判定规则：session key 以 `subagent:` 开头 → `minimal` mode，否则 → `full` mode。

**结论：用 Cron 标定的底噪（18,000）不能直接用于 Subagent 测量，需分别标定。**

### ⚠️ 底噪不是常量

底噪还与以下因素相关，**换一个 OpenClaw 环境（不同机器/账号/配置）就需要重新标定**：

| 影响因素 | 说明 |
|----------|------|
| OpenClaw 版本 | 不同版本的 system prompt 内容不同 |
| 安装的工具数量 | tool schemas 随工具增多而增大 |
| 被测 skill 的 SKILL.md 大小 | 每多 1,000 tokens 的 SKILL.md，底噪增加约 1,000 |
| 模型提供商 | 不同模型的计费折扣规则不同 |

### 底噪估算公式

```
底噪(your-skill) = 固定底噪(calibration_noise) + (your_skill_md_tokens - calibration_skill_md_tokens)
```

其中：
- `calibration_noise`：用 skill-calibration 标定出的底噪值（本机实测）
- `calibration_skill_md_tokens`：skill-calibration 的 SKILL.md 大小（338 tokens）
- `your_skill_md_tokens`：被测 skill 的 SKILL.md 大小（用 tiktoken 测量）

---

## 七、Kimi (Moonshot AI) 计费规则

> OpenClaw 国内版主要使用 Kimi 模型，其 token 计费与 Anthropic 有重要差异。

### 核心机制：自动 Prompt Cache

Kimi 使用**全自动**的 Prompt Cache，无需任何代码配置（不像 Claude 需要显式 `cache_control`）。系统自动检测重复前缀并复用缓存。

| 特性 | Kimi K2 / moonshot-v1 | Claude (Anthropic) |
|------|----------------------|-------------------|
| 自动缓存 | ✅ 全自动，无需配置 | ❌ 需显式 `cache_control` |
| cache hit 折扣 | **90%**（¥0.42 vs ¥4.20/M） | **90%**（$0.30 vs $3.00/M） |
| cache write 溢价 | 无单独计费（自动写入） | **+25%**（$3.75/M） |
| TTL | 自动缓存：未公开 | 默认 5 分钟，可选 1 小时 |

### Kimi 计费字段

Kimi API 使用 OpenAI 兼容格式，响应中的 usage 字段：

```json
{
  "usage": {
    "prompt_tokens": 133610,
    "prompt_tokens_details": {
      "cached_tokens": 127232    ← 对应 OpenClaw 的 cacheRead
    },
    "completion_tokens": 585,
    "total_tokens": 23416        ← 对应 OpenClaw 的 totalTokens
  }
}
```

> ⚠️ **注意**：Kimi 的 `prompt_tokens` 包含了全部发送的 input（含缓存部分），与 Anthropic 的 `inputTokens` 含义不同。Anthropic 的 `inputTokens` 只是新鲜发送的部分。

### Kimi totalTokens 估算公式

Kimi 没有单独的 `cacheWrite` 计费，自动缓存写入不收额外溢价：

```
totalTokens ≈ cached_tokens × 0.10    ← 命中缓存，90% 折扣
            + (prompt_tokens - cached_tokens) × 1.0   ← 未命中部分，全价
            + completion_tokens × 1.0  ← 输出，全价
```

**示例（与上文相同数据）：**
```
cached_tokens    = 127,232  →  127,232 × 0.10 = 12,723
new input tokens =   6,378  →    6,378 × 1.00 =  6,378
completion       =     585  →      585 × 1.00 =    585
──────────────────────────────────────────────────────
totalTokens（估算）≈ 19,686   实测 ≈ 23,416
```

> ⚠️ 同样存在约 16% 的估算误差（原因不明，可能是计费粒度或国内代理层差异）。

### Kimi 与 Anthropic 计费对比

| 指标 | Kimi K2 | Claude Sonnet |
|------|---------|---------------|
| 标准输入价 | ¥4.20/M ≈ $0.58/M | $3.00/M |
| 缓存命中价 | ¥0.42/M ≈ $0.06/M | $0.30/M |
| 缓存折扣率 | **90%** | **90%** |
| 缓存写入溢价 | **无**（全自动，不计费） | +25%（需手动配置） |
| 相对价格 | ~1/5 Claude | 基准 |

**Kimi 的优势**：自动缓存 + 无写入溢价 + 更低基础价格，对频繁重复调用的 OpenClaw Cron 场景极为友好。

### 如何判断 Kimi Cache 是否生效

通过 `sessions.json` 中的 `cacheRead` 字段判断：

```
cacheRead ≈ 0        → cache 冷启动，system prompt 完全重算，totalTokens 会较高
cacheRead ≈ 127,000  → cache 热命中，system prompt 复用，totalTokens 大幅降低
```

cache 未生效的常见原因：
- **首次运行**该 session（初次写入缓存）
- **OpenClaw 版本升级**导致 system prompt 内容变更
- **新增/删除 skill**导致 skillsSnapshot.prompt 变化
- **长时间未运行**导致 cache 过期（TTL 未公开，建议保持 heartbeat）

---

## 八、阿里云百炼 (Bailian) 计费规则

> 来源：[阿里云百炼 上下文缓存文档](https://help.aliyun.com/zh/model-studio/context-cache)
> 百炼（DashScope）是 OpenClaw 在国内使用的另一个主要平台，`modelProvider=bailian` 时适用此规则。

### 三种缓存模式对比

| 项目 | 显式缓存 | 隐式缓存 | Session 缓存 |
|------|---------|---------|-------------|
| 开启方式 | 手动添加 `cache_control` 标记 | **全自动，无法关闭** | header: `x-dashscope-session-cache: enable` |
| 创建缓存计费 | 标准输入单价 × **125%** | 标准输入单价 × **100%** | 标准输入单价 × **125%** |
| **命中缓存计费** | 标准输入单价 × **10%** | 标准输入单价 × **20%** | 标准输入单价 × **10%** |
| 最少缓存 Token | 1,024 | 256 | 1,024 |
| 缓存有效期 | 5 分钟（命中后重置） | 不确定（系统定期清理） | 5 分钟（命中后重置） |

### 与 Kimi / Anthropic 对比

| 特性 | 百炼隐式缓存（默认） | 百炼显式缓存 | Kimi（Moonshot 原生）| Anthropic |
|------|------------------|------------|---------------------|-----------|
| 缓存模式 | 全自动 | 手动 | 全自动 | 手动 |
| **cache read 折扣** | **80%**（× 0.20） | **90%**（× 0.10） | **90%**（× 0.10） | **90%**（× 0.10） |
| cache write 溢价 | 无（× 1.00） | × 1.25 | 无（自动） | × 1.25 |
| 最小缓存长度 | 256 tokens | 1,024 tokens | 未公开 | 1,024 tokens |

> ⚠️ **关键差异**：百炼**隐式缓存**命中折扣只有 **80%**（0.20×），低于 Kimi/Anthropic 的 90%（0.10×）。

### totalTokens 估算公式

**隐式缓存（OpenClaw 通过百炼时自动生效）：**
```
totalTokens ≈ cached_tokens × 0.20            ← 命中缓存，80% 折扣
            + (prompt_tokens - cached_tokens) × 1.0   ← 未命中，全价
            + completion_tokens × 1.0          ← 输出，全价
```

**显式缓存（需手动配置 cache_control）：**
```
totalTokens ≈ cache_creation_tokens × 1.25    ← 写入缓存，+25% 溢价
            + cached_tokens × 0.10             ← 命中缓存，90% 折扣
            + fresh_input_tokens × 1.0         ← 新鲜 input，全价
            + completion_tokens × 1.0          ← 输出，全价
```

### API 响应字段

百炼 OpenAI 兼容格式（`usage` 结构）：
```json
{
  "usage": {
    "prompt_tokens": 133610,
    "prompt_tokens_details": {
      "cached_tokens": 127232,               // 命中缓存（隐式/显式）→ 对应 cacheRead
      "cache_creation_input_tokens": 0       // 写入缓存（仅显式）→ 对应 cacheWrite
    },
    "completion_tokens": 585,
    "total_tokens": 23416                    // → 对应 totalTokens
  }
}
```

### OpenClaw + 百炼 kimi-k2.5 注意事项

百炼托管的 `kimi-k2.5` 走**百炼平台的隐式缓存**（0.20× hit），而非 Kimi 原生接口（0.10× hit）。

| 接入方式 | provider 标识 | cache read 系数 | 说明 |
|---------|--------------|----------------|------|
| Kimi 原生 API | `moonshot` / `kimi` | **0.10×** | 自动缓存，折扣 90% |
| 百炼托管 kimi-k2.5 | `bailian` + model 含 `kimi` | **0.20×** | 百炼隐式缓存，折扣 80% |
| 百炼托管 qwen 系列 | `bailian` + model 含 `qwen` | **0.20×** | 百炼隐式缓存，折扣 80% |

> 📌 当前 `report_html.py` 的 `_detect_billing_model()` 将 `bailian` 提供商统一识别为 `bailian`（0.20×），
> 与 Kimi 原生（0.10×）区分开。如 `cacheWrite > 0` 说明走了显式缓存，应改用 0.10× 计算。

---

## 九、如何确定本机底噪

每台机器/账号需要**独立标定**，流程：

1. **运行标定 job**：在 `cron/jobs.json` 中启用 `perf-calibration-test-001`，触发一次
2. **读取结果**：
   ```bash
   python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py sessions | grep perf-calibration
   ```
3. **保存标定结果**：
   ```bash
   python3 ~/.openclaw/skills/skill-perf/scripts/calibrate.py save --total <totalTokens>
   # 例如：
   python3 ~/.openclaw/skills/skill-perf/scripts/calibrate.py save --total 18927
   ```
4. 之后 snapshot.py 会自动读取本机标定值，不再使用硬编码的 18,000

---

## 九、净消耗计算

```
net_tokens = totalTokens(被测skill) - 底噪(被测skill)
           = totalTokens(被测skill) - calibration_noise - (skill_md_tokens - 338)
```

**比较同一 skill 两种方案时：**

```
方案A net = A.totalTokens - 底噪
方案B net = B.totalTokens - 底噪

差值 = A.net - B.net = A.totalTokens - B.totalTokens   ← 底噪完全抵消！
```

→ 对比测试时，**直接比较 totalTokens 的差值**即可，底噪不影响结论。

---

## 十、快速参考

| 场景 | 看哪个字段 | 说明 |
|------|-----------|------|
| 这次 skill 实际花了多少钱 | `totalTokens` | 计费口径，含 cache 折扣 |
| 实际发给模型的 input 有多少 | `cacheRead + inputTokens` | 通常约 133,000+ tokens |
| LLM 处理了多少新鲜内容 | `inputTokens` | 任务消息 + SKILL.md，约 5,000–10,000 |
| LLM 生成了多少内容 | `outputTokens` | 回复 + 工具调用 |
| Cache 是否生效 | `cacheRead > 100,000` | 越大越省钱（折扣 90%） |
| Cache 是否刚写入 | `cacheWrite > 0` | 首次/过期后，溢价 25% |
| skill 本身的净开销 | `totalTokens - 底噪` | 去除系统固定成本 |
| 比较两种方案哪个更省 | `A.totalTokens vs B.totalTokens` | 底噪相同可直接比 |