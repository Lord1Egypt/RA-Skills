# simplify-code

An agent skill that simplifies, cleans up and refactors existing code in any mainstream language (JS/TS, Python, Java, Go, Rust, C#, C/C++, PHP, SQL, Bash…) **while preserving behavior and public APIs**.

一个 Agent 技能：在**不改变行为和公共 API** 的前提下，简化、整理、重构各主流语言的现有代码（简化代码、去重复、减少嵌套、消除代码坏味道）。

## Evaluation / 评测

Agent model `glm-5.3-flash-external` via miniagent, 2026-10-19, skill v1.1.0. 7 cases, mostly behavior traps checked by hidden test harnesses. One run per case.

| | With skill | Baseline (no skill) |
|---|---|---|
| Assertions | **28 / 31** (6/7 cases all-pass) | 20 / 31 (2/7) |

- **Wins are on behavior traps:**
  - Java `toMap` duplicates: 5/5 vs 2/5.
  - TS `Promise.all` ordering: 5/5 vs 3/5.
  - Negative page index: 3/3 vs 2/3.
  - Go code that is already minimal (left alone): 5/5 vs 4/5.
- **Triggering** (24 mixed queries, 4 skills installed): 5/6 recall, 0 false triggers. The miss was a "flatten these nested ifs" request that read no skill.
- **Caveats:**
  - The JS falsy-defaults trap timed out at 900s (2/5). A retry at 1800s finished in 898s but still scored 3/5, because it applied `==`→`===`, which broke the hidden harness.
  - Runs with the skill are about 2.6× slower than without (4,263s vs 1,647s total).
  - Only 1 of 7 runs stated a mode.
  - Each case ran once.

被测模型 `glm-5.3-flash-external`（miniagent），2026-10-19，v1.1.0，7 个用例，每例 1 次。

- **得分：** 有技能 **28/31**，无技能 20/31。
- **主要提升：** 在行为陷阱上（toMap 重复键、Promise.all 顺序等）。
- **不足：** JS 假值默认值用例超时（2/5）；在 1800s 下重试仍为 3/5（错误地把 `==` 改成 `===`）。另外，有技能时更慢。

## Install / 安装

- ClawHub: https://clawhub.ai/linkxzhou/simplify-code-all
- SkillHub: https://skillhub.cn/skills/user_16e7431e/simplify-code-all
- GitHub:

```bash
git clone --depth 1 https://github.com/linkxzhou/simplify-code.git ~/.claude/skills/simplify-code
```

## Structure / 结构

```
SKILL.md        # Skill definition / 技能定义
references/     # Rules, language notes, behavior traps, examples / 规则、语言要点、行为陷阱、示例
evals/          # Eval cases and fixtures / 评测用例与样例文件
```
