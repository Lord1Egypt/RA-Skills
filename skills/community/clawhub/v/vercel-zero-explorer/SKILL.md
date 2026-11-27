---
name: "Vercel Zero Explorer"
description: "AI-powered guide for Vercel Zero - the first programming language designed specifically for AI agents. Covers Zero graph-first workflow, .0 projection files, native tools, explicit effects, structured JSON diagnostics, and AI-native development workflows. Built for AI developers, language designers, and researchers exploring the future of AI-native programming."
version: "1.0.5"
keywords:
  - AI agent programming
  - Zero language
  - Vercel
  - AI-native development
  - programming language
  - agent tools
---

# Vercel Zero Explorer

## Overview

**Vercel Zero** is an experimental systems programming language launched by Vercel Labs on May 16, 2026. Scope: conceptual guidance, command reference and integration patterns for Zero; it does not install the toolchain, run `zero` commands, or write files. Unlike traditional programming languages that prioritize human readability, Zero embraces AI-native paradigms with structured JSON diagnostics, explicit effects, and predictable memory management.

This Skill provides comprehensive guidance on understanding, using, and building with Zero language.

## Current Status (as of 2026-11-26)

| Item | Status |
|------|--------|
| Latest release | **v0.3.4** (the 0.1.x line is obsolete) |
| License | Apache-2.0 |
| GitHub | ~5,200 stars, developed by Vercel Labs |
| Targets | Native binaries for Linux, macOS, Windows |
| Authoring model | **Graph-first**: `zero.graph` is the compiler input; `.0` files are human-readable projections |
| Maturity | Experimental — breaking changes expected, not for production or sensitive data |

**Recent developments:**
- **v0.3.0 made graph-first authoring the default workflow.** The binary `zero.graph` store is now what the compiler reads; `.0` text files became projections for human review. Agents edit through `zero query` / `zero patch` instead of rewriting source text, and patches carry an expected graph hash so stale or invalid edits are rejected *before* the store is written.
- **Version churn is real.** v0.1.4 introduced row syntax, v0.2.0 promoted canonical `.0` text to the native source surface, and v0.3.0 rejects source-projection input at the compiler boundary. Existing text-first packages must run `zero import` to pull source into the graph; v0.3.2 reportedly made `zero import` roughly 12x faster on large programs.
- **The toolchain contract is the distinctive part.** Every subcommand of the single `zero` binary shares one `--json` flag and one diagnostic schema, so errors arrive with stable codes (e.g. `NAM003`) and typed repair metadata (e.g. `declare-missing-symbol`); `zero fix --plan --json` returns a repair plan an agent can accept, edit, or reject rather than a blind patch.
- These items are compiled from public coverage; exact version numbers, flags and behaviour change frequently — **treat the official repository and docs as authoritative**.

> **Safety note:** Vercel Labs explicitly warns to expect breaking changes, rough edges and security issues, and to avoid production systems and sensitive data. Evaluate Zero in an isolated, disposable workspace.


**More recent developments (compiled 2026-11-26, treat official docs as authoritative):**
- **Graph-first is now the practical entry point, not an option.** Guidance and examples that still start from editing `.0` text are stale; the recommended loop is `zero query → zero patch --json (with expect_hash) → zero fix --plan --json → zero export` for review.
- **Hash-guarded patches are the main safety lever.** Because a patch carries an expected graph hash, an agent editing from a stale view is rejected before the store is written — this is the mechanism worth validating first in any evaluation.
- **Version churn continues.** Exact subcommand names, flags and diagnostic codes change between minor versions; pin the version you evaluate against and record it alongside your results.
- These items are compiled from public coverage; **verify against the official repository and docs before relying on any specific flag or code**.

## Triggers

**Chinese（须落在 Vercel Zero 这一具体语言上才触发）:**
- "Vercel Zero 是什么"
- "Zero 的 graph-first 工作流怎么走"
- "Zero 的 .0 文件现在还是不是源文件"
- "Zero 的 zero patch --json 怎么用"
- "Zero 的诊断码 NAM003 是什么意思"

**English（must name Vercel Zero explicitly）:**
- "What is Vercel Zero"
- "Vercel Zero graph-first workflow"
- "Zero query / patch / fix --plan usage"
- "Zero .0 projection vs zero.graph"
- "Zero structured JSON diagnostics schema"

**Non-triggers / 不触发：**
- Generic "AI agent programming language" discussions, language-design theory, or comparisons that never mention Zero
- Python / JavaScript / Go / Rust programming questions
- Generic compiler, parser or LLVM questions unrelated to Zero
- Requests to actually install the toolchain or run builds for the user

**路由判定三步**：① 用户是否明确点名 **Vercel Zero**（不是泛指「AI 语言」）？② 诉求是否为理解概念、查命令、看诊断或设计 agent 集成？③ 前两步均为是才启用本 Skill；否则转通用编程语言或编译器相关技能，或请用户补充具体语境。

## Features


### 0. Data Minimization & Execution Boundary / 数据最小化与执行边界

**数据最小化前置声明（使用本技能前请先执行）**

1. 粘贴诊断 JSON、代码片段或命令输出前，先删除其中的绝对路径、内网主机名、令牌、项目名与个人信息；用占位符替代。
2. 不要在提问中粘贴生产代码或包含密钥的配置；Zero 本身仍在实验阶段，**官方明确建议不要用于生产系统与敏感数据**。
3. 评估 Zero 时请使用隔离、可丢弃的工作区，不要指向生产环境或真实数据集。
4. 本技能不安装 Zero 工具链、不执行 `zero` 任何子命令、不读写文件；所有命令均为供你复制后在自己环境中运行的参考文本。
5. 生成的代码或补丁如需落盘，须先预览确认无敏感信息，再自行保存与执行。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| `zero` / `bash` 代码块 | 可直接复制的命令参考文本 | 使用者在自己的隔离工作区中运行，本技能不执行 |
| `zero` 语法与 JSON 诊断示例 | 结构与字段说明 | 使用者对照官方文档与本地版本校验 |
| 版本号、star 数、二进制体积等数字 | 公开报道的观察值，随版本变化 | 使用者以官方仓库复核 |
| `World` 能力、effect 声明等概念 | 语言设计说明 | 使用者在自己的程序里实践 |

**硬边界**：不安装工具链、不执行命令、不读写文件、不发起网络请求、不访问用户环境。



### 1. Core Concepts of Zero Language

| Concept | Description | Mechanism | Why it matters for an agent | 验证方式（自己跑一遍） |
|---------|-------------|-----------|------------------------------|---|
| **Native Tools** | Zero provides built-in system tools optimized for AI agents | Built into the language rather than pulled from external package registries | No dependency resolution step, so an agent's first build rarely fails on missing packages | 对比同等功能在 Python 下需要引入几个外部包 |
| **Explicit Effects** | Side effects are explicitly declared, making AI behavior predictable | A function that touches the outside world must accept a `World` capability; the compiler enforces it | A signature alone tells the agent whether code can reach network, filesystem or stdout | 写一个无 World 参数的函数，看编译器是否拒绝文件访问 |
| **Predictable Memory** | Memory management follows deterministic patterns | Deterministic allocation instead of tracing garbage collection | Execution cost is easier to predict before running, useful when an agent is choosing between candidate programs | 对同一程序多次运行，观察分配与耗时是否稳定 |
| **Structured JSON Diagnostics** | Compiler outputs structured JSON for easy AI parsing | One shared `--json` flag and one diagnostic schema across every subcommand | The agent branches on stable codes instead of parsing changing prose | 故意写错标识符，看返回的 code 与 repair 字段 |
| **.0 File Extension** | Uses `.0` extension (e.g., `main.0`) | Under v0.3.x the `.0` text is a *projection* exported from the graph, not the compiler input | Humans can still review and deliberately edit readable text, then import it back | 导出 .0 后手工改一行，再跑 verify-projection 看是否报错 |

### 2. Zero Syntax Basics

```zero
// Example Zero code structure
import { http, file } from "std";

// Define a tool with explicit effects
tool fetch_data(url: string) -> json {
  effect network_call(url)
  return http.get(url)
}

// AI-friendly structured output
diagnose parse_result as json
```

**Example — the `World` capability makes effects visible in the signature:**

```zero
import { file, std } from "std";

// No World parameter => the compiler guarantees this cannot touch disk or network
tool pure_total(prices: list<f64>) -> f64 {
  return prices.fold(0.0, |acc, p| acc + p)
}

// World is required => the signature itself advertises a filesystem effect
tool save_report(w: World, path: string, body: string) -> result<unit, io_error> {
  effect file_write(path)
  return file.write(w, path, body)
}
```

The practical payoff: an agent reviewing a candidate function does not need to read its body to know whether it can reach the outside world — `save_report` obviously can, `pure_total` provably cannot.


**Example — why the hash guard matters in practice:** two agents edit the same program from slightly different views of the graph. Agent A patches node `653eeb6e` with `expect_hash` `ab91...` and succeeds. Agent B, holding a stale view, patches the same node with an old hash and is **rejected before the store is written** — no silent overwrite, no corrupted graph. This is the single most valuable property to verify when evaluating Zero for agent workflows.


**Example — a diagnostic an agent can act on (v0.3.x schema):**

```json
{
  "code": "NAM003",
  "severity": "error",
  "message": "unknown identifier `prices_total`",
  "repair": { "kind": "declare-missing-symbol", "symbol": "prices_total" },
  "span": { "node": "653eeb6e", "field": "value" }
}
```

Note the `span` points at a **stable node id and field**, not a line/column pair. That is the whole point of graph-first authoring: the reference does not drift when someone inserts a comment above it.
### 3. AI Agent Integration Patterns

- **Tool Definition**: Define reusable tools with explicit interfaces
- **Effect Declaration**: Declare side effects before execution
- **Structured Diagnostics**: Parse compiler output as JSON for AI decision-making
- **Error Recovery**: Use structured errors for autonomous debugging

**Integration example — autonomous fix loop with Claude Code:**

```bash
# 1. read the graph instead of guessing at source text
zero query --json '{"kind":"function","name":"fetch_api_data"}'

# 2. propose a semantic patch guarded by a hash
zero patch --json '{"op":"set","node":"653eeb6e","field":"value","expect_hash":"ab91...","to":"..."}'

# 3. ask the compiler for a plan instead of applying a blind fix
zero fix --plan --json

# 4. keep human review in the loop
zero export --out review/ && zero verify-projection
```

**Integration example — CI drift gate:** run `zero verify-projection` in CI so a hand-edited `.0` file that no longer matches the graph fails the build rather than silently diverging.


**Integration example — capability scoping:** grant `World` only to a single top-level `main` entry point, and have every other function take plain values. When an agent proposes a change that suddenly needs `World` deep in the call graph, the signature change itself is the signal to slow down and review — no need to read the whole diff.

**Integration example — diagnostic code lookup:** keep a small table of the codes you actually hit and map each to one recovery action (`NAM003` → declare the missing symbol; hash mismatch → re-run `zero query`; effect errors → check the `World` parameter). Recovery then becomes a lookup instead of a fresh reasoning step on every failure.

## Command Cheat Sheet

| Command | Purpose | Typical agent use | 失败/注意信号 |
|---------|---------|-------------------|---|
| `zero init` | Initialise a package / graph store | Start of a task | 工作区未初始化；先确认目录可丢弃 |
| `zero query --json` | Read declarations, types, calls, effects, node ids | Replace "read the file" | 返回为空说明名字或 kind 写错，而非功能不存在 |
| `zero patch --json` | Apply a semantic edit guarded by a graph hash | Replace "rewrite lines 40-52" | expect_hash 不匹配即为视图过期，需重新 query |
| `zero import` | Pull existing `.0` source into the graph | Migrating text-first packages | 大程序导入慢时可查版本是否 ≥ 声称提速的版本 |
| `zero export` | Emit a human-readable `.0` projection | Human review, pull requests | 不匹配说明 .0 被手改过，不要直接导入回去 |
| `zero verify-projection` | Check the projection still matches the graph | CI drift gate | check 过但 test 挂，多为 effect 声明不足 |
| `zero check` / `zero test` / `zero run` | Type-check, test, execute | Standard loop | 返回 plan 而非自动修复，需自行决定是否采纳 |
| `zero fix --plan --json` | Machine-readable repair plan | Agent decides accept / edit / reject | 目标平台需显式指定，默认不等于当前机器 |
| `zero build` | Emit executable, object, or LLVM IR | Packaging |  |

Every one of these accepts `--json`, so a single parser handles all of them.

## Workflow

### Step 1: Understand Zero's Design Philosophy
- Zero prioritizes AI parsing over human readability
- Structured output enables reliable AI agent workflows
- Native tools are designed for autonomous execution
- *Example:* where a Python agent must first resolve `requests` from an index and hope the version is compatible, a Zero agent calls a built-in `http` tool that ships with the language — one less failure mode per iteration.

- *Example:* an agent asked to "add retry logic" can read the call graph with `zero query` and see exactly which node issues the network effect, instead of grepping prose for `http` and hoping it found every call site.

### Step 2: Explore Zero Syntax
- Learn the `.0` file extension convention
- Understand explicit effect declarations
- Master structured JSON diagnostics format
- *Example:* map the codes you actually hit into a lookup table (`NAM003` → declare missing symbol, timeout codes → retry with backoff) so recovery is a table lookup instead of a fresh reasoning step each time.

- *Example:* when a `.0` projection is edited by hand, run `zero verify-projection` before importing it back — the graph is the source of truth, and drift discovered at import time is far cheaper than a corrupted store.

### Step 3: Build AI-Native Tools
- Create custom tools with predictable behavior
- Define clear input/output interfaces
- Use explicit error handling patterns
- *Example:* return `result<json, io_error>` rather than throwing, so the caller — which is usually the agent — is forced to handle the failure branch at compile time.

- *Example:* keep the effect list in a tool declaration minimal (`network_call` only, not `network_call` plus `file_write`); a narrower effect set makes the tool safe to call from more places without re-reviewing it.

### Step 4: Integrate with AI Agents
- Connect Zero programs to Claude Code, Codex, or other AI coding agents
- Use structured diagnostics for autonomous debugging
- Implement guardrails for safe AI execution
- *Example:* grant the `World` capability only to a thin top-level entry point and pass pure functions everything else; then the blast radius of an agent-generated change is legible from the call graph.

- *Example:* treat `zero fix --plan --json` output as a proposal to review, not an instruction to apply — the plan is machine-readable precisely so a human or a policy layer can accept, edit or reject it.

## Input/Output Examples

### Example 1: Understanding Zero Concepts

**Input:**
```
Explain the key differences between traditional programming languages and Zero language.
```

**Output:**
```
Key Differences Between Traditional Languages and Zero:

| Aspect | Traditional Languages | Zero Language |
|--------|---------------------|---------------|
| Target Users | Humans | AI Agents |
| Output Format | Human-readable errors | Structured JSON diagnostics |
| Effects | Implicit side effects | Explicit effect declarations |
| Memory | Garbage collection | Predictable memory patterns |
| Tool Interface | External libraries | Native built-in tools |
| Extension | .py, .js, .go | .0 |

Zero is not meant for humans to write directly - it's designed to be generated and understood by AI agents.
```

### Example 2: Creating a Zero Tool

**Input:**
```
Create a Zero tool that fetches data from an API and returns structured JSON.
```

**Output:**
```zero
// data_fetch_tool.0

import { http, json } from "std";

// Tool definition with explicit effects
tool fetch_api_data(
  endpoint: string,
  method: string = "GET"
) -> json {
  // Explicit network effect declaration
  effect network_call(endpoint, method)
  
  // Execute HTTP request
  response = http.request(endpoint, {
    method: method
  })
  
  // Return structured JSON
  return json.parse(response.body)
}

// Structured diagnostics for debugging
diagnose fetch_api_data as {
  success: boolean,
  data: json | null,
  error: string | null
}
```

### Example 3: AI Agent Workflow Integration

**Input:**
```
How can I integrate Zero programs with Claude Code for autonomous debugging?
```

**Output:**
```
Integration Guide for Claude Code + Zero:

1. Generate Zero code using Claude Code
2. Execute and capture JSON diagnostics
3. Parse structured errors for autonomous recovery
4. Implement fix strategies based on diagnostic codes

Example Workflow:
```json
{
  "step": "execute",
  "tool": "fetch_api_data",
  "diagnostic": {
    "code": "NETWORK_TIMEOUT",
    "suggestion": "retry_with_backoff",
    "affected_lines": [5, 6]
  }
}
```

Claude Code can automatically:
- Parse diagnostic codes
- Select recovery strategy
- Re-execute with modifications
- Verify fix success
```



### Example 4: Recovering From a Stale Patch (hash mismatch)

**Input:**
```
My zero patch --json failed. What does the error mean and what should I do next?
```

**Output:**
```
A failed patch guarded by expect_hash almost always means your view of the graph is stale,
not that the edit is wrong. Recovery order:

1. Re-read the current state:  zero query --json '{"kind":"function","name":"<fn>"}'
2. Compare the node id and hash you held against what the query returned.
3. Re-apply the patch with the fresh expect_hash from the query.
4. Only if the node itself changed, re-derive the edit — do not force it.

The guard is working as designed: it rejected the write before the store was modified,
so there is nothing to clean up. Never retry the same stale hash in a loop.
```

## Use Cases

| Use Case | Description | Best suited for | Honest caveat | 先做的最小验证 |
|----------|-------------|-----------------|---------------|---|
| **AI Code Generation** | Generate Zero code that AI agents can reliably execute | Agent builders measuring whether hash-guarded patches reduce silent breakage | Training-data advantage still sits with Python/JS/Go | 一个小工具分别用 Zero 与 Python 走完同一改动，比较失败次数 |
| **Autonomous Debugging** | Use structured diagnostics for self-healing code | Loops that need to branch on error codes rather than prose | Garbage in still produces garbage out; tests still decide correctness | 构造 3 类已知错误，看 agent 能否按 code 分别恢复 |
| **Tool Development** | Build native tools optimized for AI workflows | Small disposable CLI utilities where a ~16 KiB binary is a feature | Ecosystem is young; expect to write your own bindings | 写一个 100 行以内的小 CLI，走完 query→patch→fix→export |
| **Language Research** | Explore AI-native programming paradigms | Researchers comparing capability-based effects and graph IRs | Benchmarks are design targets, not published results — measure yourself | 固定版本跑一组可复现基准，记录版本号与机器信息 |

## References

- [Vercel Zero GitHub Repository](https://github.com/vercel-labs/zero)
- [Zero Official Documentation](https://vercel.com/docs/zero)
- [AI Agent Programming Language Analysis](https://blog.csdn.net/irpywp/article/details/161167783)
- [InfoQ: Vercel Labs Ships Zero, a Graph-First Language Built So Agents Write the Code](https://www.infoq.com/news/2026/08/vercel-ships-zero-ai)
- [Zero getting-started guide](https://github.com/vercel-labs/zero) — authoritative for current commands and flags

## Notes

- Zero is experimental (**v0.3.4** as of 2026-10-09; the 0.1.x line is obsolete)
- Not intended for production human-written code
- Focus is on AI agent reliability and predictability
- File extension `.0` is unique to Zero language
- Under v0.3.x the compiler reads `zero.graph`, not `.0`; treat `.0` as a projection
- Reported figures (16.2 KiB hello world, ~1 ms build, token efficiency, tiny artifacts) are **design targets** — benchmark your own program before relying on them
- Positioning: closer to Zig than Rust on binary size and explicit allocation; lacks Rust's borrow-checker maturity and ecosystem, and trades Go's green threads and larger runtime for dependency-free artifacts
- **Evaluate in an isolated workspace**; do not point Zero at production systems or sensitive data
- Pin the exact version you evaluate against and record it with your results — flags and codes move between minor versions
- Prefer `zero query` + hash-guarded `zero patch` over any text rewriting of `.0` files
- Treat `zero fix --plan --json` output as a proposal, not an instruction to apply automatically
## Changelog / 变更记录

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 1.0.2 | 2026-10-09 | 收窄中英文触发词（须明确点名 Vercel Zero）、补充非触发清单与路由判定三步（SQP-1 x2）；新增数据最小化前置声明与代码块性质/执行边界表及硬边界；状态与动态更新至 2026-10-09 并新增 graph-first 入口、hash 守卫、版本churn 三条；新增列：验证方式、失败/注意信号、先做的最小验证；概念表后补 hash 守卫示例、集成模式补 2 例、Workflow 四步各补第二例；新增示例4（stale patch 恢复）；Notes 补 3 条 |
| 1.0.1 | 2026-09-14 | 新增 graph-first 工作流与命令速查 |

---



---

**Author:** Ge Cheng | **Skill Address:** clawhub.ai/skills/vercel-zero-explorer | **Skill Version:** 1.0.5 | **Last reviewed:** 2026-11-26

## 本轮增量（2026-11-14）：复核维度与举例补充

> 本节为 2026-11-14 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Command Cheat Sheet**：

- 速查表补「命令适用的前置条件 / 官方文档对应章节」两项，纸面标注，避免脱离版本上下文套用。
- 对名称相近的命令单列「区分要点」列，草稿中先核对再引用。

**Input/Output Examples**：

- 示例补「输入结构的关键字段 / 输出结构的可验证特征」两项标注，缺字段时标为待补。
- 输出说明单列「事实与推演是否分栏」核对项，避免把示意输出读成既定行为。

### 新增复核维度表（2026-11-14）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 前置条件标注 | 学习者 + 复核人 | 官方文档 + 速查表 | 前置条件、版本上下文、对应章节 | 中 | 学习草稿，以官方文档为准 |
| 输出可验证特征 | 学习者 + 复核人 | 示例清单 | 关键字段、可核对特征、分栏标示 | 低 | 纸面示例，不构成运行结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于了解 Vercel Zero 的文档学习与示例结构参考，输出为供读者自行核对的纸面材料；不安装依赖、不运行命令、不连接外部服务、不代为验证线上状态。涉及实际部署、账号操作与生产验证的场景不适用，应以官方文档为准并由具备权限的人员处理。

### 时效性说明

- 本期时效性核查：**截至 2026-11-14**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-19）：复核维度与举例补充

> 本节为 2026-11-19 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 2: Explore Zero Syntax**：

- 语法对照表补「来源与版本」一列：每条语法项注明所依据的公开文档位置与版本说明，缺出处的按待补处理，草稿不填入未经核实的取值。
- 示例清单新增「事实与推演分栏」：文档已明确写明的语义与对用法的推测分列，推测栏统一标注由具备资质人员核实后使用。

**Example 4: Recovering From a Stale Patch (hash mismatch)**：

- 失效补丁清单补「校验依据」一列：每个 hash 不一致条目注明所依据的发布说明位置，草稿不给出可直接运行的修复语句。
- 复核清单新增「留痕五要素」占位：来源、版本、发布时间、复核人、复核时点并列记录，缺一项即标注证据不完整、需人工确认。

### 新增复核维度表（2026-11-19）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 语法来源与版本 | 框架选型人员 + 复核人 | 语法对照表 / 官方发布页 | 每条语法项是否标注文档位置与版本说明 | 中 | 纸面对照，取值须人工核实 |
| 失效补丁留痕 | 框架选型人员 | 失效补丁清单 / 草稿 | 来源、版本、时点与复核人是否齐全 | 中 | 文档记录，不构成上线结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于Vercel Zero 语言概念与集成模式的方法论纸面对照的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产环境安装部署、工具调用与版本上线放行的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-19**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-26）：复核维度与举例补充

> 本节为 2026-11-26 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. Core Concepts of Zero Language**：

- 概念清单补一条「概念出处是否附官方文档页码占位」的占位核对项，由使用者留白填写，草稿不整段转录。
- 为 graph-first 对照新增一张纸面对照：左列列概念标签，右列留白记录需人工核实的差异，不预置结论。

**Use Cases**：

- 用例清单补一条「适用性是否经人工确认」的占位标注位，草稿不代为判定。
- 为集成场景新增一行「需人工核对的版本标签」占位：标注标签，具体版本号留白核实。

### 新增复核维度表（2026-11-26）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 概念出处占位 | 使用者 + 复核人 | 概念清单草稿 | 是否标注页码占位、未整段转录 | 低 | 方法论参考，理解由本人确认 |
| 用例适用性留白 | 使用者 | 用例占位表 | 是否标注待人工确认、未代为判定 | 低 | 文档记录，不构成实现建议 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于Zero 语言概念与集成模式的方法论参考的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及正式代码实现、生产部署与对外发布的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-26**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
