# Simulator Browser RPA Example

这是一个**仿真浏览器 RPA** 的可复制参考实现：在可控 sandbox 页面上，通过 **async Playwright** 完成门户门闩、两步登录、表单填写、PIN 弹窗、结果解析。

本示例抽象自已跑通的「工行批量提交类」浏览器自动化 skill 的工程范式，但已**去业务化**——不包含真实银行/真实资金语义，也**不是** Amazon 或任何生产技能的复制。

## 适合什么场景

- 自有 **行业仿真系统** / `sandbox.jc2009.com` / 本地 `sandbox/demo_app.html`
- 需要 **浏览器 RPA** 做端到端演示或回归
- 表单较复杂：门户 HITL、多步登录、Tab 切换、动态增行、PIN 弹窗、成功页解析
- 需要 **adapter 分层**：`mock`（CI）与 `simulator_rpa`（半集成）可切换

## 不适合什么场景

- **真实第三方网站 + 高风控 + 人工验证码** → 优先看 [`../real_browser_rpa/README.md`](../real_browser_rpa/README.md)
- 目标系统有稳定 **官方 API** → 不要硬写浏览器 RPA
- **不要把本示例的业务字段、selector、sandbox URL 原样复制**到你的 skill

## 目录结构

```
simulator_browser_rpa/
├── README.md
├── sandbox/
│   └── demo_app.html              # 本地仿真页面（门户门闩 + 批量提交教学 DOM）
├── scripts/
│   ├── service/
│   │   ├── browser_session.py     # async 启动 persistent context（不含 goto）
│   │   ├── account_client.py      # account-manager subprocess（对齐 real_browser_rpa）
│   │   ├── simulator_playwright.py # RPA 主流程（厚）
│   │   ├── task_service.py        # async 编排层
│   │   └── adapter/
│   │       ├── base.py            # BatchItem / BatchSubmitResult 契约
│   │       ├── mock.py            # mock/unit 档
│   │       ├── simulator_rpa.py   # 薄 adapter：pick / lease / 委托 RPA
│   │       └── __init__.py        # select_adapter
│   └── util/
│       ├── constants.py
│       └── logging.py
└── tests/
    ├── test_adapter_dispatch.py
    ├── test_no_rpa_helpers_import.py
    ├── test_simulator_rpa_unit.py
    └── test_stop_reason.py
```

## 文件职责

| 文件 | 职责 |
|---|---|
| `browser_session.py` | async 系统 Chrome/Edge + launch args；**不在此 goto** |
| `account_client.py` | **唯一** account-manager subprocess 封装（`pick_web_account` / `release_lease`） |
| `simulator_playwright.py` | 门户轮询、登录、批量表单、PIN、解析 `batch_id`、截图 |
| `adapter/simulator_rpa.py` | **薄** adapter：pick 账号、lease、委托 RPA、`finally release_lease` |
| `adapter/mock.py` | 不启浏览器，供 unit/mock/CI |
| `task_service.py` | async 校验输入 → 选 adapter → `await submit_batch` |
| `sandbox/demo_app.html` | 可控 DOM；含可选门户门闩 + 原批量提交流程 |

## 核心流程

1. `await run_batch_submit(target, items)` 校验参数
2. `select_adapter()` 按 `OPENCLAW_TEST_TARGET` 选择 mock 或 simulator RPA
3. `simulator_rpa` 档：`SimulatorBrowserRpaAdapter.submit_batch` 内 `pick_web_account(sim_batch)` → `submit_batch_rpa` → `release_lease`
4. RPA：门户门闩（若可见则 HITL 轮询）→ 登录两步 → 批量页 → 填表 → 提交 → PIN → 解析 `batch_id`
5. 失败截图（有 `artifacts_dir` 时）→ 返回 `BatchSubmitResult`

## 两档仿真目标

| 档位 | 目标 | 说明 |
|---|---|---|
| 本地教学 | `sandbox/demo_app.html`（`file://`） | 结构教学 + mock 单测默认 |
| 线上联调 | `https://sandbox.jc2009.com/...` | 设 `SIMULATOR_BASE_URL` + account-manager `sim_batch` 账号 |

联调时账号 `url` 用行业根路径，**不要**写 `/login` 子路径；`auth_strategy=per_session_manual`。

## account-manager 注册示例（泛化）

```bash
python .../account-manager/scripts/main.py account add-web \
  --platform sim_batch \
  --login-id demo001 \
  --url file:///.../demo_app.html \
  --environment simulator \
  --auth-strategy per_session_manual
```

线上 sandbox 时将 `--url` 换为 `https://sandbox.jc2009.com/...` 占位路径（按团队部署填写）。

**PIN/密码演示值**：RPA 从 account 的 `login_id` 取账号；`password` / `token_pin` 允许从 account 字段或环境变量 `SIMULATOR_PASSWORD` / `SIMULATOR_TOKEN_PIN` 回退；验证码固定演示值 `0000`（仅 sandbox 用）。

## Copy map（复制到新技能 `scripts/`）

| 来源（examples） | 目标（新技能） | 说明 |
|---|---|---|
| `browser_session.py` | `scripts/service/browser_session.py` | async；URL 仅 `page.goto`，不进 launch args |
| `account_client.py` | `scripts/service/account_client.py` | subprocess，对齐 `real_browser_rpa` |
| `simulator_playwright.py` | `scripts/service/<platform>_playwright.py` | RPA 主流程（厚） |
| `adapter/` | `scripts/service/<domain>_adapter/` | 薄 `simulator_rpa` + mock |
| `task_service.py` | `scripts/service/task_service.py` | async 编排 |
| `util/constants.py` | `scripts/util/constants.py` | 须替换 `TARGET_PLATFORM` 等业务常量 |
| `tests/` | `tests/` | 可按需复制 dispatch / unit / 禁止 import 守护 |
| `sandbox/demo_app.html` | — | **仅仿真测试**，不进入生产 skill |

## 明确禁止

- **不要** `import account-manager` 内部模块（`rpa_helpers`、`inject_account_manager_scripts_path`、`get_account_credential`）
- **不要** sync Playwright 用于完整 RPA 主路径
- **不要在** `task_service.py` / RPA 主流程里散落 account-manager subprocess
- **不要在技能侧**执行 `playwright install` / `pip install playwright`
- **不要把 URL 放进** `launch_persistent_context(args=[...])`
- **不要** vendor `scripts/jiangchang_skill_core/`
- **不要**照抄 slug、logger 名、演示账号到生产 skill

> 旧版 `pick_simulator_account()` / `SimulatorAccount` / `set_credentials()` 已废弃；账号统一由 account-manager 下发。

## 联调检查表

- [ ] 数据目录 `.env` 中 `OPENCLAW_TEST_TARGET=simulator_rpa`（非 mock）
- [ ] account-manager：`platform ensure` + 账号 `active` + 有 `profile_dir`
- [ ] 目标 sandbox UI 已部署（跨团队）
- [ ] 失败先查 `rpa-artifacts/` 截图，再查 Chrome profile 缓存（可用 `--user-data-dir` 手工打开清站点数据）
- [ ] 默认 `tests/run_tests.py` / 本 example `pytest` 仍全部通过（mock 离线）

## 依赖说明

- Python 3.10+
- Python 包 `playwright`：由**宿主共享 runtime** 提供；技能侧不要 `pip install playwright`
- 默认使用**系统 Chrome/Edge**；技能侧不要 `playwright install`
- `jiangchang_skill_core.runtime_env.find_chrome_executable`（可选）

## 环境变量（示例）

| 变量 | 说明 |
|---|---|
| `OPENCLAW_TEST_TARGET` | `mock`/`unit` → Mock；`simulator_rpa` → 仿真 RPA |
| `SIMULATOR_BASE_URL` | 仿真页 URL；默认本地 `demo_app.html` 的 file URI |
| `SIMULATOR_PASSWORD` / `SIMULATOR_TOKEN_PIN` | 演示密码/PIN 回退（账号字段优先） |
| `PORTAL_LOGIN_WAIT_SEC` | 门户 HITL 超时（默认 120） |
| `OPENCLAW_BROWSER_HEADLESS` | `0` 默认有头；`1` 无头（CI 可用） |

## 运行测试

```bash
cd examples/simulator_browser_rpa
python -m pytest tests/ -v
```

测试为 mock/纯函数，**不启动真实浏览器**。

## 当前状态

- async Playwright + 薄 adapter + `simulator_playwright.py` 工程范式已对齐 `real_browser_rpa`。
- 未接入完整 CLI、数据库与 entitlement。
