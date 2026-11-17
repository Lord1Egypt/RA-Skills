[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

# skill-admission-gate · 技能上架安全闸门 / Skill Admission Gate

## English

The security gate before installing or listing a skill: run a deterministic security review — destructive commands, remote execution, data exfiltration, prompt injection, covert behavior, obfuscated payloads and scope overrun — and output "graded findings + gate verdict + package fingerprint evidence". Call it when reviewing third-party skills, installing skills of unknown provenance, running pre-release screening on in-house skills, doing supply-chain security assessment, or needing evidence that "this package is untampered and risk-assessed". Three core things: ① scan all files per the rule set and grade hits (BLOCK/WARN); ② accept-risk declarations (`.admission-allow.json`, must be signed); ③ emit package fingerprint and file hashes as evidenced artifacts.

### Usage
- **AI agent**: read `SKILL.md` (frontmatter name/description decides applicability; body is the execution steps).
- **Human reader**: read `SKILL.md` and `AGENTS.md`.

### Files
- `SKILL.md` — main specification
- `AGENTS.md` — agent instructions
- `llms.txt` — machine-readable index
- `LICENSE` / `LICENSE.md` — license

## 中文

技能上架安全闸门——一个技能/插件在安装或上架前，先跑确定性安全审查：查破坏性命令、远程执行、数据外泄、提示注入、隐蔽行为、混淆载荷与作用域越界，产出「分级发现 + 闸门判定 + 包指纹证据」。当需要审查第三方 skill、安装来源不明的技能、给自研技能做发布前安检、做供应链安全评估、或需要出具"该包未被篡改且已评估风险"的证据时调用。核心三件事：①按规则集扫全部文件并分级（BLOCK/WARN）②支持"已接受风险"声明（.admission-allow.json，须署名留痕）③输出包指纹与文件哈希作为"有证"产物。

### 使用
- **AI 代理**：读取 `SKILL.md`（frontmatter 的 name/description 决定是否适用；正文为执行步骤）。
- **人类读者**：读取 `SKILL.md` 与 `AGENTS.md`。

### 文件
- `SKILL.md` — 主说明书
- `AGENTS.md` — AI 代理说明书
- `llms.txt` — AI 可读索引
- `LICENSE` / `LICENSE.md` — 许可声明

<!-- 生成：2026-10-15 · 技能骨架批量升级；双语化：2026-10-17 -->
