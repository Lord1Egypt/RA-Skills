---
name: software-tester
description: "Professional software-testing skill for AI coding agents. Use this skill when a user needs to write, run, design, or strategize tests: unit tests (Python pytest or JS Jest/Vitest), end-to-end tests (Playwright), API tests (REST/GraphQL), performance or load tests (k6/Locust), security tests (OWASP API Top 10), visual regression, contract testing, or to design a test strategy, coverage gates, or a TDD workflow. Triggers include 'write tests for X', 'increase coverage to 100 percent', 'test this API', 'E2E the login flow', 'add a load test', 'set up a CI coverage gate', 'TDD this feature', 'find untested code', 'review our test strategy'."
agent_created: true
metadata:
  version: 2.0.0
  category: 软件测试
  difficulty: 专家
  architecture: superpower
---

# Software Tester

> 把 AI 编程助手变成一名能覆盖测试金字塔全层的专业测试工程搭档：从单测、E2E、API，到性能、安全、可视化回归与契约测试，并具备测试策略与 CI 质量门禁的设计能力。

## 何时使用

在以下任一情况触发本技能：

- 需要为某模块/函数**编写单元测试**（Python 或 JavaScript/TypeScript）
- 需要**端到端**验证一个用户流程（登录、下单、表单提交等）
- 需要**测试 REST/GraphQL API** 的参数、鉴权、异常与响应
- 需要**提升覆盖率**或定位未覆盖代码行
- 需要**设计测试策略**（测试金字塔、覆盖率目标、CI 门禁、测试债）
- 需要用 **TDD** 方式开发一个功能
- 需要**性能/压测**、**安全测试**、**可视化回归**或**契约测试**
- 需要生成**测试计划 / 测试矩阵 / 测试报告**

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。SKILL.md 仅作路由，**按需**读取以下 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 | 关键词（grep 线索） |
|------|------|---------------------|
| 单元测试 / 覆盖率 | [references/unit-testing.md](references/unit-testing.md) | pytest, jest, vitest, coverage, 覆盖率, 单测 |
| 端到端测试 | [references/e2e-testing.md](references/e2e-testing.md) | playwright, e2e, 端到端, 快照, page object |
| React 前端组件测试 | [references/react-frontend-testing.md](references/react-frontend-testing.md) | react, 前端, 组件, rtl, jest, vitest, 交互 |
| API 测试 | [references/api-testing.md](references/api-testing.md) | rest, graphql, 接口, 鉴权, 参数校验 |
| 测试策略 / 覆盖率治理 | [references/test-strategy.md](references/test-strategy.md) | 金字塔, 策略, CI 门禁, 测试债, coverage gate |
| TDD 工作流 | [references/tdd.md](references/tdd.md) | 测试驱动, red-green-refactor, 先写测试 |
| 性能 / 压测 | [references/performance-testing.md](references/performance-testing.md) | k6, locust, 压测, 性能, 吞吐, p95 |
| 安全测试 | [references/security-testing.md](references/security-testing.md) | owasp, 注入, 越权, 安全, fuzz |
| 可视化回归 | [references/visual-regression.md](references/visual-regression.md) | 截图比对, visual regression, percy, 像素 diff |
| 契约测试 | [references/contract-testing.md](references/contract-testing.md) | pact, 契约, consumer-driven, 接口契约 |
| 测试报告 / 风险 | [references/reporting.md](references/reporting.md) | 测试报告, 风险, 通过率, 质量门禁 |
| 失败分诊 / 提缺陷前 | [references/failure-triage.md](references/failure-triage.md) | 测试失败, 红了, flaky, 环境问题, 根因, 提 issue |
| 代码审查 | [references/code-review-playbook.md](references/code-review-playbook.md) | code review, 代码审查, 评审, diff, 复查, PR |

## 细粒度子技能（可单独安装）

`skills/` 下的子技能可通过 skills.sh 单独安装使用，路径长期稳定、不会改名：

| 子技能 | 路径 | 适用 |
|--------|------|------|
| api-testing | [skills/api-testing](skills/api-testing/SKILL.md) | REST/GraphQL 请求构造、状态码与响应校验 |
| e2e-testing | [skills/e2e-testing](skills/e2e-testing/SKILL.md) | Playwright 页面交互、快照定位、表单与截图 |
| react-frontend-testing | [skills/react-frontend-testing](skills/react-frontend-testing/SKILL.md) | React 组件 RTL 渲染、user-event 交互、查询与 mock |
| test-coverage | [skills/test-coverage](skills/test-coverage/SKILL.md) | 覆盖率目标、测试金字塔、CI 集成与类型选择 |
| unit-test-writer | [skills/unit-test-writer](skills/unit-test-writer/SKILL.md) | pytest 覆盖率驱动补测，逐步逼近 100% |
| performance-testing | [skills/performance-testing](skills/performance-testing/SKILL.md) | k6/Locust 负载/压力/尖峰/容量，p95 门禁 |
| security-testing | [skills/security-testing](skills/security-testing/SKILL.md) | OWASP API Top 10 越权/注入/鉴权验证 |
| code-review | [skills/code-review](skills/code-review/SKILL.md) | 代码评审：缺陷/安全/性能/可读性聚焦，PR 复查清单 |

子技能是轻量入口；需要完整方法论时回到上表的 `references/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/run_coverage.py <path> --lang python|js` — 运行覆盖率，输出逐行未覆盖项与汇总
- `scripts/gen_test_plan.py --name <模块> --features f1,f2,...` — 生成测试计划 Markdown
- `scripts/test_matrix.py --method POST --path /x --params a,b` — 生成 API 测试矩阵（正常/边界/异常）
- `scripts/e2e_scaffold.py --name <流程> --steps "打开 /login;输入 账号 hope;点击 提交"` — 生成 Playwright 测试骨架（动词后必须带参数，步骤语法见 [references/e2e-testing.md](references/e2e-testing.md)）

运行示例：

```bash
python3 scripts/run_coverage.py ./src --lang python
python3 scripts/gen_test_plan.py --name 支付模块 --features 创建订单,退款,对账
python3 scripts/test_matrix.py --method POST --path /api/login --params username,password
python3 scripts/e2e_scaffold.py --name 登录流程 \
  --steps "打开 /login;输入 账号 hope;输入 密码 secret;点击 提交;断言跳转 /dashboard"
```

> `e2e_scaffold.py` 只解析「动词 + 完整参数」的步骤；缺参数或非路径目标会降级为 `// TODO:` 注释并在 stderr 告警，
> **不会**替你猜断言目标。步骤语法与降级规则见 [references/e2e-testing.md](references/e2e-testing.md) 的「脚本加速」一节。

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/ci-coverage.yml](assets/ci-coverage.yml) — CI 覆盖率门禁配置（GitHub Actions 风格，可平移到其他平台）
- [assets/test-plan-template.md](assets/test-plan-template.md) — 测试计划模板
- [assets/playwright.config.template.ts](assets/playwright.config.template.ts) — Playwright 配置模板
- [assets/jest.config.template.js](assets/jest.config.template.js) — Jest/Vitest 覆盖率配置模板

## 核心原则（始终遵循）

1. **测试先行**：能先写测试就先写，TDD 优先于补测试。
2. **测试金字塔**：单测 70% / 集成 20% / E2E 10%；不要倒金字塔。
3. **覆盖 ≠ 质量**：100% 行覆盖不保证无 bug；要测边界、异常、性能退化与并发。
4. **可运行可重复**：每个技能产出的测试代码必须能直接运行，脚本必须确定性。
5. **精准定位**：先读对应 `references/` playbook 再动手，不要凭记忆猜框架命令。
6. **明确边界**：性能/安全/压测属于专项，结果以报告呈现，不替 QA 团队做策略拍板。
