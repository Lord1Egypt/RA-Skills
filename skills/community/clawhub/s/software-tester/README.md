# software-tester（超级技能 · Superpowers 架构）

> 一个完整的软件测试技能：让 AI 编程助手成为覆盖测试金字塔全层的专业测试工程搭档。

采用 **Superpowers 架构**：薄 `SKILL.md` 作路由，`references/` 存放按需加载的完整 playbook，`scripts/` 提供确定性可重复脚本，`assets/` 提供即取即用的配置与模板。上下文按需渐进式加载（progressive disclosure）。

## 覆盖能力

| 域 | Playbook | 关键工具 |
|----|----------|----------|
| 单元测试 / 覆盖率 | [references/unit-testing.md](references/unit-testing.md) | pytest / Jest / Vitest |
| 端到端 | [references/e2e-testing.md](references/e2e-testing.md) | Playwright Test |
| React 前端组件测试 | [references/react-frontend-testing.md](references/react-frontend-testing.md) | React Testing Library / Jest / Vitest |
| API 测试 | [references/api-testing.md](references/api-testing.md) | REST / GraphQL |
| 测试策略 / 治理 | [references/test-strategy.md](references/test-strategy.md) | 金字塔 / CI 门禁 |
| TDD | [references/tdd.md](references/tdd.md) | red-green-refactor |
| 性能 / 压测 | [references/performance-testing.md](references/performance-testing.md) | k6 / Locust |
| 安全测试 | [references/security-testing.md](references/security-testing.md) | OWASP API Top 10 |
| 可视化回归 | [references/visual-regression.md](references/visual-regression.md) | Playwright / Percy |
| 契约测试 | [references/contract-testing.md](references/contract-testing.md) | Pact (CDC) |
| 报告 / 风险 | [references/reporting.md](references/reporting.md) | 计划 / 矩阵 / 风险 |
| 失败分诊 | [references/failure-triage.md](references/failure-triage.md) | 根因定位 / flaky / 提缺陷前自检 |
| 代码审查 | [references/code-review-playbook.md](references/code-review-playbook.md) | AI 代码评审 / PR 复查 |

## 细粒度子技能

可整库安装，也可只取其中一个：

| 技能 | 说明 | 来源 |
|------|------|------|
| `unit-test-writer` | Pytest 覆盖率：运行测试、发现未覆盖行、补到 100% | derived |
| `api-testing` | REST/GraphQL：请求构造、状态码验证、响应检查 | derived |
| `e2e-testing` | Playwright 浏览器自动化：交互、快照定位、截图 | derived |
| `react-frontend-testing` | React 组件 RTL 渲染、user-event 交互、查询与 mock | derived |
| `test-coverage` | 测试策略：覆盖率目标、测试金字塔、CI 集成 | derived |
| `performance-testing` | k6/Locust 负载/压力/尖峰/容量，p95 门禁 | derived |
| `security-testing` | OWASP API Top 10 越权/注入/鉴权验证 | original |
| `code-review` | 代码评审：缺陷/安全/性能/可读性聚焦，PR 复查清单 | derived |

## 安装

### 安装完整技能库（推荐，含 references / scripts / assets）

```bash
npx skills add skills-repo/software-tester -g -y
```

### 只安装某个细粒度子技能

```bash
npx skills add skills-repo/software-tester@unit-test-writer -g -y
npx skills add skills-repo/software-tester@api-testing -g -y
npx skills add skills-repo/software-tester@e2e-testing -g -y
npx skills add skills-repo/software-tester@react-frontend-testing -g -y
npx skills add skills-repo/software-tester@test-coverage -g -y
npx skills add skills-repo/software-tester@performance-testing -g -y
npx skills add skills-repo/software-tester@security-testing -g -y
npx skills add skills-repo/software-tester@code-review -g -y
```

## 目录结构

```
software-tester/
├── SKILL.md                 # 薄路由：触发词 + 能力索引 + 脚本/资源索引 + 核心原则
├── README.md                # 本文件
├── AGENTS.md                # AI 助手使用指引
├── references/              # 13 个按需加载的 playbook
├── skills/                  # 8 个可单独安装的细粒度子技能
├── scripts/                 # 确定性脚本
│   ├── run_coverage.py      # 运行覆盖率并汇总未覆盖行
│   ├── gen_test_plan.py     # 生成测试计划
│   ├── test_matrix.py       # 生成 API 测试矩阵
│   └── e2e_scaffold.py      # 生成 Playwright 测试骨架
└── assets/                  # 模板与配置
    ├── ci-coverage.yml
    ├── test-plan-template.md
    ├── playwright.config.template.ts
    └── jest.config.template.js
```

## 快速开始

```bash
# 覆盖率
python3 scripts/run_coverage.py ./src --lang python
# 测试计划
python3 scripts/gen_test_plan.py --name 支付模块 --features 创建订单,退款
# API 测试矩阵
python3 scripts/test_matrix.py --method POST --path /api/login --params username,password --auth
# E2E 骨架
python3 scripts/e2e_scaffold.py --name 登录流程 --steps "打开 /login;输入 账号 hope;点击 提交"
```

## 设计原则

1. 测试先行（TDD 优先）
2. 测试金字塔（单测 70% / 集成 20% / E2E 10%）
3. 覆盖 ≠ 质量
4. 产出可运行、脚本确定
5. 先读对应 playbook 再动手
6. 专项结果以报告呈现，不替 QA 拍板策略

## 许可

MIT
