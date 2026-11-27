# Utility Assessment Module

**Status:** Active since v1.8.0
**Parent skill:** `safe-skill-advisor`
**Entry point:** `SKILL.md` → `## 🧭 Intent Routing`
**Independence:** this module has its own input handling, procedure, evidence model and report
format. It never calls, wraps or depends on the Security Advisor flow, and it does not change how
security questions are answered.

---

## 1. Purpose

Answer one question for an ordinary user:

> "If I install this ClawHub skill, what do I actually get that a plain chat model does not
> already give me?"

Every statement in the answer must be traceable to a public source, and everything that could not
be verified must be labelled as such.

## 2. Non-goals (hard boundaries)

- Never install, unpack, or execute the target skill, its scripts, its MCP server, or its tests.
- Never present static reading as a runtime test result. "The code contains X" ≠ "X works".
- Never fetch content behind a login, paywall, private repository, or token.
- Never quote credentials found in public material; replace them with `[REDACTED]`.
- Never invent metrics or scores (no "7/10 value score", no fake benchmark numbers).
- Never decide for the user whether a stated condition (price, account, API key) is acceptable —
  present the condition as a fact.

## 3. Input contract

| Input | Handling |
|---|---|
| `https://clawhub.ai/<owner>/<slug>` | Normalize to `<owner>/<slug>` |
| `https://clawhub.ai/skills/<slug>` | Normalize to slug; owner may be resolved from the page |
| `clawhub.ai/...` without scheme | Prepend `https://` |
| Link on another host (github.com, gist, blog, mirror) | Decline for stage 1: ClawHub links only. Do not fetch or guess |
| Skill name without link | Ask for the ClawHub link; do not guess which skill is meant |
| Two or more different links | Ask the user which one to assess; assess one at a time |

If the URL is well-formed but the page cannot be resolved, say so explicitly and stop —
do not substitute a similar skill.

## 4. Evidence collection

Collect only public material, in this order, and stop when the budget below is reached:

1. ClawHub skill page: name, owner, version, description, install count/rating if shown,
   security scan badges if shown, tags.
2. Repository link listed on that page (README, `SKILL.md`).
3. Files needed to judge claims: entry script, config files, package manifest, examples/tests.
4. Public docs or issues referenced by the page.

Budget: stop after ~10 fetched documents or when further files add no new claims. Do not crawl the
whole repository or the author's other projects.

If no fetch tool is available in the current environment, ask the user to paste the page text or
`SKILL.md`, and record that the material came from the user rather than from a live page.

## 5. Evidence grades

Tag every claim in the report with one of these grades:

| Grade | Meaning |
|---|---|
| **Confirmed** | Directly visible in a fetched public file or page (quote the file path / section) |
| **Inferred** | Reasonable conclusion from code or config, but the behaviour was not run |
| **Unverified** | Stated by the page or author but no supporting material was found |
| **Missing** | The page/skill does not state it at all |

Never upgrade an "Inferred" item to "Confirmed" because it looks plausible.

## 6. Analysis steps

### Step 6.1 — Capability inventory

List what the skill claims to do, in plain language, as numbered items. For each item record:
`claim → where it came from (page / README / SKILL.md / author note)`.

### Step 6.2 — Evidence mapping

For each claim, map the evidence:

| Claim | Evidence found | Grade |
|---|---|---|
| e.g. "extracts keywords" | `src/server.js` defines the tool and its parameters | Confirmed |
| e.g. "supports Chinese sentiment" | dictionary list present, accuracy unknown | Inferred |
| e.g. "handles 10k records/s" | no benchmark file or output in repo | Unverified |

Explicitly separate "the code defines this capability" from "this capability works well".

### Step 6.3 — Baseline comparison (the core question)

Compare the skill against what a plain chat model can already do. Answer each sub-question:

1. Can a chat model do this today without the skill? (yes / partly / no, with reasoning)
2. What does the skill add: a tool, a fixed workflow, curated data, automation, deterministic
   output, an external service, or nothing beyond a prompt?
3. Is the added part material (it changes what the user can do) or cosmetic (a wrapper, a template,
   or the same prompt in a nicer package)?
4. What is the ongoing cost of the addition: install, configuration, dependencies, account, money?

Rules for judgement:

- Complexity alone is not value. A large skill that re-implements a prompt adds little.
- A small skill that performs a real action a model cannot perform alone adds a lot.
- If the skill's only contribution is prompt text, say so plainly and explain what the prompt does
  better than a direct request — or that it does not.
- Do not reject a skill merely because a model can do part of the task.

### Step 6.4 — Conditions of use

Extract as facts:

- API key or token required (which provider, where it is read from)
- Third-party account or OAuth required
- Paid service, quota, or subscription required
- Runtime requirements (OS, Node/Python version, binaries, GPU, container)
- Configuration steps (env vars, config files, editing source)
- Other limits found in the material (data source limits, rate limits, language coverage,
  privacy caveats the author states)

If the material does not state a condition, mark it `Missing — not documented` rather than
assuming "no requirement".

## 7. Report format (user-facing)

Write in the user's language. Keep it readable by a non-developer; technical detail belongs in
short evidence notes, not in the main narrative.

```markdown
### Skill 基本信息
- 名称 / 作者 / 版本 / ClawHub 链接 / 评估时间

### 它能帮你做什么？
- 3–6 条，用日常语言描述实际用途

### 它有什么额外价值？
- 与直接用普通模型相比，真正多出来的东西（工具 / 流程 / 数据 / 自动化 / 稳定性）
- 如果额外价值很小，直接说明

### 使用前需要知道什么？
- API Key / 第三方账号 / 付费 / 运行环境 / 配置 / 其他限制
- 未在材料中说明的写"材料未说明"

### 安全情况
- 发现的风险点 + 证据 + 未验证的部分
- 不要省略，也不要夸大

### 最终建议
- 四选一：值得安装 / 谨慎考虑 / 不太值得安装 / 暂时无法判断
- 必须给出理由（2–5 句），并列出影响结论的关键证据与未验证项
```

The four-way recommendation must be explained, never reduced to a single word.

## 8. Recommendation rules

| Recommendation | When it applies |
|---|---|
| **值得安装** (Worth installing) | Confirmed capability that a model cannot do alone, conditions stated and ordinary, no material security concern found |
| **谨慎考虑** (Consider with caution) | Real value exists but with meaningful conditions (key, account, cost), or unresolved security questions, or partly unverified claims |
| **不太值得安装** (Probably not worth it) | The skill mostly restates prompt text, or claimed value is contradicted by the evidence |
| **暂时无法判断** (Cannot judge yet) | Public material is missing, the page is inaccessible, the code cannot be read, or key claims are unverifiable |

Security findings and utility findings are reported separately. A serious security finding cannot
be offset by high utility, and a low utility rating cannot hide a safety warning.

## 9. Security review (independent, compact)

Check the public material for:

1. File access far outside the skill directory, recursive delete/overwrite, writes to home or
   system paths.
2. Credential handling: reading env vars, key files, browser data, SSH keys; logging or
   transmitting secrets.
3. Network behaviour: outbound requests, uploads, telemetry, remote script download, `curl | bash`.
4. Command execution: shell calls, `eval`, dynamic imports, package postinstall scripts,
   privilege escalation.
5. Obfuscated or encoded payloads, password-protected archives, unexplained binaries.
6. Permission requests that are unnecessary for the stated function.

For each finding report: what, where (file/path), grade (Confirmed / Inferred / Unverified), impact.
If nothing is found, write "no issue found in the material reviewed" — never "this skill is safe".

## 10. Edge cases

| Situation | Required behaviour |
|---|---|
| Malformed / non-ClawHub link | Explain the accepted format; do not fetch; do not guess |
| Page inaccessible (404, timeout, region block) | Say it cannot be opened, give the URL, stop; offer a retry |
| Skill removed / delisted | State that it cannot be assessed; do not use cached or similar pages |
| Material incomplete (no README, no source) | Assess only what exists; mark the rest `Missing`; use "暂时无法判断" if the gap is central |
| Source files unreadable or minified | Report the limitation; do not decompile or execute; treat claims as `Unverified` |
| Requires API key / account | Describe the requirement; state that behaviour could not be verified without credentials |
| Description contradicts code | Show both sides with locations; prefer code evidence; note the contradiction |
| Cannot confirm whether a feature works | Mark `Unverified` and say what would be needed to confirm it (a runtime test the user can run) |
| User asks safety only | Do not produce this report; Security Advisor handles it |
| Multiple links | Ask which one; do not merge results |

## 11. Output rules

- Never claim a test was run. Phrase runtime claims as "not executed".
- Cite sources inline, e.g. `SKILL.md §Features`, `package.json`, `ClawHub page`.
- Keep credentials, tokens and personal data out of the report entirely.
- End with the recommendation and its reasons; never end with a bare verdict.
- If the user asks follow-ups about one claim, extend the same evidence table instead of writing a
  new report from scratch.

## 12. Handoff

- Security-only questions never enter this module.
- When the user asked for both value and safety, produce the Utility report and, separately, the
  Security Advisor answer defined in `SKILL.md` §§1–4. Do not merge the two verdicts.
- If this module cannot reach a conclusion, say so and hand the decision back to the user with the
  evidence collected.


