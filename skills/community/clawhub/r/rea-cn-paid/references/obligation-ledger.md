# 义务账本指南（Reconstruction Obligation Ledger）

> 本文对应的英文原名是 **ReconstructionObligationLedger**，这是 REA 引擎**内建**的"诚实性"子系统，
> 不是本适配版新加的功能。它的作用只有一个：**强制把"已经搞明白的"和"仍然没搞明白的"分开记清楚**，
> 让 AI 在逆向结论里无法把"未知"伪装成"已知"。
>
> 你之前强调"LEDGERS.md 最该抄"——指的就是它。本文件把它在中文语境下的用法讲清楚。

---

## 1. 它是什么（为什么重要）

REA 在分析一个目标（二进制/安装包/JS 应用等）时，会一边取证一边建模。
但静态/被动分析**永远有边界**：有些行为只有运行时才能确证，有些代码路径无法从产物反推。

原版 `SKILL.en.md` 的两条硬纪律（第 7 步与第 157 行）直接要求：

- *Every conclusion must distinguish observations, inferences, and unknowns.*
  （每条结论必须区分：观测 / 推断 / 未知。）
- *Keep a concise finding ledger linking each conclusion to Evidence IDs,
  confidence/evidence type, search boundary, and remaining unknowns.*
  （维护一份简洁的发现账本，把每条结论关联到 Evidence ID、置信度/证据类型、搜索边界与剩余未知。）

引擎更进一步：它把这套纪律**实现成了结构化数据**——`ReconstructionObligationLedger`。
一句话：这是"AI 承认哪些没搞明白"的**机器可读账本**，是交付物里最该保留、也最该主动产出的那一篇。

---

## 2. 如何在中文 LLM 环境下正确产出账本（致命规则同工具契约）

1. **账本工具名必须逐字英文**，一字不改（见 `references/tool-invocation-contract.md`）：
   - `build_reconstruction_obligation_ledger`（生成重建义务账本）
   - `evaluate_reconstruction_coverage`（评估重建覆盖率）
   - `verify_reconstruction`（核验一条重建结论）
   - `import_managed_reconstruction`（导入受管重建记录）
2. **不要**把这些名字翻译成中文（"生成义务账本"之类在 `tool` 参数里一律无效）。
3. 不知道英文名 → 先查 `tool-manifest.json` 或 `references/glossary-zh-en.md`，**不要猜**。
4. 这四个工具均已纳入权威 170 工具清单（已与引擎 `tool_count: 170` 交叉验证）。

---

## 3. 使用节奏（把它变成习惯，而不是可选项）

- **调查进行中**：每得出一条结论，立刻在心里/在草稿里分类为「观测 / 推断 / 未知」，关联到对应的 Evidence ID。
- **调查收尾前（必做）**：调用 `build_reconstruction_obligation_ledger`，让引擎输出结构化账本——
  明确哪些重建义务已闭合（resolved）、哪些仍是开放义务（open / unknown）。
- **给用户的结论里**：用中文如实写出"已确认 X""基于证据推断 Y""**以下仍未知 / 未能从产物反推 Z**"。
  绝不允许把未知说成已知，也不允许用含糊措辞掩盖未决项。
- 如需量化"搞明白了多少"，用 `evaluate_reconstruction_coverage`；对某条关键结论存疑，用 `verify_reconstruction` 复核。

---

## 4. 与免责声明的关系

义务账本与 `DISCLAIMER.md` 是互补的：

- 免责声明界定**用途边界**（只用于研究学习/审计，禁用于破解）。
- 义务账本界定**认知边界**（AI 只陈述它真正取证到的，未搞明白的明确标注为未知）。

二者共同保证：本技能交付的每一条结论都**可溯源、可复核、不夸大**。

---

## 5. 中文呈现模板（建议）

> **已确认（观测/证据）**：……
> **推断（基于证据，置信度中）**：……
> **仍未知 / 开放义务**：……（来自 `build_reconstruction_obligation_ledger` 输出）
> **证据溯源**：Evidence ID `xxxx`、工具 `open_binary` / `analyze_function` 等。

---

*注：账本工具的具体输入/输出字段（schema）以引擎运行时通过 MCP 实际暴露的为准；
上文工具名经 `tool-manifest.json` 与引擎源码 `dist/server/registerApplicationTools/obligationLedger.js` 双重核对。*
