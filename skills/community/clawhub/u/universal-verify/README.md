# universal-verify

An agent skill that verifies, tests, and critiques AI-generated output (code, articles, images, video, slides, documents, and web UI) before calling it done. It runs deterministic checks, specialist scorers, and isolated judges, then fixes and re-checks in a bounded loop so a human only reviews the few undecidable items. This skill judges output; it does not generate it.

一个 Agent 技能：在宣称完成前，对 AI 生成的代码、文章、图像、视频、幻灯片、文档和 Web UI 进行核验、测试与批评。它先跑确定性检查、专项评分和隔离评审，再在有界循环中修复并复检，让人只处理少数无法自动裁定的项。本技能只评判产物，不负责生成。

## 何时使用

在生成任务即将宣布完成时使用，或当用户提到 verify、test、review、QA、quality check、self-check、aesthetic review、去AI味、验证、测试、审美把关、质检时使用，即使用户没有点名本 skill。

工作流：先写验收清单，再按产物类型选用 `references/` 下的领域包，并按 L1 / L2 / L3 强度分层检查。

## 目录结构

- `SKILL.md` — 主指令
- `references/` — 代码、文本、图像、视频、文档/UI 领域包与报告格式
- `scripts/` — 去 AI 味词法检查、占位符扫描、改写前后主张对比
- `evals/` — 评估用例与样例文件

## Install / 安装

```bash
npx skills add linkxzhou/universal-verify
```

Or clone:

```bash
git clone --depth 1 https://github.com/linkxzhou/universal-verify.git ~/.claude/skills/universal-verify
```

- GitHub: https://github.com/linkxzhou/universal-verify

## License

MIT
