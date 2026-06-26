# ShipGuard 🛡️

**Ship with confidence. Every time.**

> A gate-driven development workflow skill for AI-assisted software projects.
> Stop your AI from silently breaking production.

---

## The Problem

You're using AI to build software. You say one thing, the AI changes 10 files, restarts 3 containers, and you have no idea what just broke — until a user reports it.

**ShipGuard fixes this.**

## How It Works

Six gates. Every change goes through them. No exceptions.

```
Request → [G0 Intake+TC] → [G1 Impact] → [G2 Build] → [G3 QA] → [G4 Regression] → [G5 Lessons] → Closed
```

| Gate | What happens |
|------|-------------|
| **G0** | AI restates the requirement in concrete terms + defines Test Cases. You confirm before any code is written. |
| **G1** | AI lists every file it will touch, risk level, DB migrations, restart requirements. You confirm. |
| **G2** | AI builds. Scope creep = immediate stop + escalation notice. |
| **G3** | AI executes the exact TCs from G0. Pass/fail per item. |
| **G4** | AI generates a regression map based on what changed. Full checklist. |
| **G5** | AI extracts lessons, updates `hard-rules.md`. Loaded automatically next session. |

## Key Features

- **Test Cases at intake** — defined in G0, executed in G3. Not invented after the fact.
- **Task type classification** — UI tweak / Bug fix / Feature / Product change / Architecture. Each type has strict scope boundaries. A bug fix cannot touch the UI. A UI tweak cannot touch business logic.
- **Auto-execute vs confirm** — low-risk UI changes happen immediately. Critical path changes always require confirmation.
- **Project memory** — `hard-rules.md` and `lessons.md` persist across AI sessions. The AI learns your project's rules permanently.
- **Project onboarding** — first use triggers an 8-question setup that generates `PROJECT.md` with your critical paths, protected modules, and hard rules.

## Install

```bash
# Via ClawHub
clawhub install morelapAI/shipguard

# Or clone directly
git clone https://github.com/morelapAI/shipguard
```

## Project Structure

After associating ShipGuard with your project:

```
your-project/
  .dev-workflow/
    PROJECT.md              # Critical paths, protected modules, hard rules
    CHANGELOG.md            # Auto-maintained
    requirements/           # NR-YYYYMMDD-NN.md per requirement
    changes/                # CR-YYYYMMDD-NN.md per change
    test-cases/
      all-test-cases.md     # Cumulative TC registry
    regression/             # Regression results per CR
    lessons/
      hard-rules.md         # Permanent rules, loaded every session
      lessons.md            # Dated lessons log
```

## Example: What G0 looks like

```
【需求理解卡 #NR-20260524-01】
原始需求：子账号列表隐藏空状态区域
任务类型：🎨 UI微调
执行策略：直接执行

理解：无数据时不渲染表格，只显示自定义提示文字
范围：SubAccounts.vue 展示逻辑
排除：不涉及后端、不涉及其他页面

Test Cases：
  TC-01【正常流程】选择无数据母账号 → 表格区域消失，显示「暂无记录」
  TC-02【正常流程】选择有数据母账号 → 表格正常显示
  TC-03【边界条件】切换母账号 → 旧数据清空，新数据正确加载
  TC-04【异常流程】网络错误 → 显示错误提示，不显示空表格

✅ 确认后开始 / ❌ 有误，请纠正
```

## Philosophy

- No code before confirmed plan
- No merge before verified delivery  
- No close before regression
- No surprise, ever

## License

MIT — use it, fork it, improve it.

---

*Built with [OpenClaw](https://openclaw.ai) · Published on [ClawHub](https://clawhub.ai/morelapAI/shipguard)*
