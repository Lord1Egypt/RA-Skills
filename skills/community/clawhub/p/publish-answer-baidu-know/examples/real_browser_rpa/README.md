# Real Browser RPA Example

这是一个真实网站浏览器 RPA skill 的可复制参考实现，适用于需要登录、人工验证、搜索、滚动加载、采集和入库的场景。

**说明：**

- 本示例是通用模板，不绑定具体平台。
- 示例抽象自已跑通的真实浏览器 RPA skill（抖音视频链接采集），但代码已改成中性示例命名。
- 新 skill 开发时可以复制本目录，再替换目标站点、选择器、解析逻辑和业务字段。

## 适用场景

- 真实网站操作（非 sandbox / mock）
- 需要登录态与 persistent Chrome/Edge profile
- 需要通过 account-manager 管理账号和 `profile_dir`
- 需要处理人工登录、滑块验证码、短信验证码
- 需要关键词搜索、滚动加载、采集可见条目
- 需要结构化日志、用户友好的停止原因、失败留痕（截图/视频）

## 目录结构

```
real_browser_rpa/
├── README.md
├── scripts/
│   ├── service/
│   │   ├── account_client.py      # subprocess 调用 account-manager
│   │   ├── browser_session.py     # 系统 Chrome + persistent context
│   │   ├── human_verification.py  # 滑块/短信/保存登录弹窗检测（不依赖 task_rpa 错误类型）
│   │   ├── task_rpa.py            # RPA 主流程
│   │   └── task_service.py        # 轻量编排（示例无 DB）
│   └── util/
│       ├── constants.py           # 平台常量、selector 占位
│       └── logging.py             # 结构化日志与脱敏
└── tests/
    ├── test_human_verification.py # 验证码误判防护
    └── test_stop_reason.py        # 停止原因文案
```

## 核心流程

1. **pick account** — 通过 `account_client.pick_web_account()` 获取 `profile_dir` 与租约
2. **启动浏览器** — `launch_persistent_context` + `new_page()` + `page.goto(start_url)`
3. **人工验证（启动后）** — 检测滑块/短信，等待用户完成
4. **等待登录** — 检测登录按钮消失 / 登录态 marker 出现
5. **保存登录弹窗** — 等待“是否保存登录信息”倒计时消失
6. **人工验证（登录后）** — 再次检测
7. **搜索** — 定位搜索框 → 输入关键词 → 点击搜索
8. **等待结果容器** — `#search-result-container`（示例 selector）
9. **滚动采集循环** — 采集可见条目 → 判断 stop_reason → 滚动加载
10. **返回结果** — `ScrapeRunResult` + `format_stop_reason_for_user()`
11. **释放租约** — `finally` 中 `release_lease()`

## 开发新 skill 时如何复制

1. **先阅读**本 README 及下方「Copy map」「复制边界」章节
2. 按 copy map **选择性复制**到新技能 `scripts/`（**不要**整包照搬 `examples/real_browser_rpa/`）
3. 修改 `util/constants.py` 中的 `TARGET_PLATFORM`、`DEFAULT_START_URL`、selector 常量
4. 替换 `task_rpa.py` 中的登录态 marker、搜索框/结果解析逻辑（**必须 F12 实测**）
5. 替换 `human_verification.py` 中的验证码 selector（若目标站点 DOM 不同）
6. 在 `task_service.py` 中接入真实 DB、任务日志、RpaVideoSession
7. 在新技能根目录补齐 `scripts/main.py` CLI；`SKILL.md` 与根 `README.md` 按模板主目录规则编写，**不要**复制本 README

## Copy map（复制到新技能 `scripts/`）

| 来源（examples） | 目标（新技能） | 说明 |
|---|---|---|
| `examples/real_browser_rpa/scripts/service/browser_session.py` | `scripts/service/browser_session.py` | persistent context 启动范式 |
| `examples/real_browser_rpa/scripts/service/account_client.py` | `scripts/service/account_client.py` | account-manager CLI 集中封装 |
| `examples/real_browser_rpa/scripts/service/human_verification.py` | `scripts/service/human_verification.py` | 人工验证等待 |
| `examples/real_browser_rpa/scripts/service/task_rpa.py` | `scripts/service/<业务名>_rpa.py` 或 `scripts/service/task_rpa.py` | RPA 主流程，按业务改名 |
| `examples/real_browser_rpa/scripts/service/task_service.py` | `scripts/service/task_service.py` | 参考并合并编排层 |
| `examples/real_browser_rpa/scripts/util/constants.py` | `scripts/util/constants.py` | 平台常量与 selector（须替换） |
| `examples/real_browser_rpa/scripts/util/logging.py` | `scripts/util/logging.py` | 可选，按需合并 |
| `examples/real_browser_rpa/tests/` | `tests/` | 可按需复制测试思路 |
| `examples/real_browser_rpa/README.md` | — | **只读参考**，不复制为新技能根 README |

**复制时必须替换：** selector、URL、平台名称、账号平台字段、slug、logger 名等业务标识。**不要**照搬示例字段到其他平台。

**浏览器与启动约束：**

- **不要**在技能内安装 Playwright；浏览器与 Python 包由宿主/runtime 提供
- `launch_persistent_context` 的 `args` **只放 Chrome 参数**；**不要把 URL 放进 `args`**
- 页面必须通过 `new_page()` + `goto()`，或通过真实地址栏/点击进入

## 复制边界：哪些能复制，哪些必须替换

### 可以直接参考/复制的

- `browser_session.py` 的启动结构：**persistent context → new_page → goto**
- `human_verification.py` 的人工验证等待模式（容器级检测 + 等待人工，不自动破解）
- `task_rpa.py` 的流程分层、结构化日志点、`stop_reason` 设计
- `account_client.py` 的 account-manager CLI **集中封装**方式（subprocess 仅限此文件）
- `tests/test_human_verification.py` 的误判防护测试思路

### 必须替换的

- `SKILL_SLUG`
- `TARGET_PLATFORM`
- `LEASE_HOLDER`
- `DEFAULT_START_URL`
- `SEARCH_INPUT_SELECTORS` / `SEARCH_BUTTON_SELECTOR`
- `RESULT_CONTAINER_SELECTOR` / `RESULT_ITEM_SELECTOR`
- `SCROLL_CONTAINER_SELECTORS`
- `RESULT_END_TEXT`
- `LOGGED_IN_SELECTORS` / `LOGGED_OUT_SELECTOR`（见下方说明）
- `_parse_item_locator()` 业务字段解析
- 用户可见中文文案
- 数据库写入逻辑
- 任务日志逻辑
- 录屏/截图业务标题

### 禁止照抄的

- 不要照抄目标站点 selector（示例 selector 不等于真实 DOM）
- 不要照抄平台名、slug、logger 名
- 不要依赖 `D:\OpenClaw\client-commons\account-manager\scripts\main.py` 等开发机绝对路径作为生产依赖
- 不要把示例里的 result selector 当成真实站点 selector
- 不要把示例代码原样发布为业务 skill
- 不要把真实账号、手机号、cookie、token 写入代码或 README

### 登录 selector 说明

`task_rpa.py` 中的 `LOGGED_IN_SELECTORS` 与 `LOGGED_OUT_SELECTOR` **只是示例**，偏中文「登录」按钮和常见站点结构。复制到新 skill 后：

- **必须**用目标站点 F12 / DOM 实测后替换
- **不允许**凭经验猜 selector
- **不允许**因为示例在本机曾跑通就直接照搬到其他平台

### account-manager 路径解析说明

`account_client.py` 末尾的 `D:\OpenClaw\client-commons\account-manager\scripts\main.py` 是**开发环境兜底路径**，仅用于模板/本机调试。复制到真实 skill 后：

- **优先**通过 `ACCOUNT_MANAGER_ROOT`、Platform Kit `get_sibling_skills_root` 或宿主运行环境解析 account-manager
- **不要**把个人机器路径作为生产依赖

## 必须保留的安全原则

- **不 import account-manager 内部模块** — 只通过 CLI/subprocess 调用
- **不自动破解验证码** — 滑块/短信只检测 + 等待人工完成
- **日志脱敏** — 不输出完整手机号/账号
- **租约释放** — `pick-web --lease` 后必须在 `finally` 释放
- **失败留痕** — 真实 skill 应在关键失败点截图（示例中已留注释位）

## 常见坑

| 坑 | 正确做法 |
|---|---|
| 直接 `import account_manager.service...` | 通过 `subprocess` 调用 `account-manager/scripts/main.py` |
| 把 URL 放进 `launch_persistent_context(args=[url])` | `args` 只放 Chrome 参数；URL 用 `page.goto(start_url)` |
| 启动后直接操作 DOM | 先 `context.new_page()` 再 `page.goto()` |
| 用整页 `body.inner_text()` 判断验证码 | 限定在 `[role='dialog']`、`.vc-captcha-verify` 等容器 |
| 搜索结果含“验证码教程”文字就误判 | 单元测试覆盖：无验证 DOM 时不应 `present=True` |
| 无结构化日志 | 关键节点打 `rpa_start` / `browser_ready` / `collect_round` 等 |
| 把 CLI 参数暴露给普通用户 | 用户说明放根 `README.md`；运行契约与触发规则放 `SKILL.md`（LLM/平台入口） |

## 需要替换的内容清单

| 文件 | 替换项 |
|---|---|
| `util/constants.py` | `SKILL_SLUG`、`TARGET_PLATFORM`、`DEFAULT_START_URL`、所有 selector |
| `browser_session.py` | `get_start_url()` 配置来源、stealth 脚本（可选） |
| `human_verification.py` | `SLIDER_SELECTORS`、`SMS_SELECTORS`、`DIALOG_TEXT_CONTAINERS` |
| `task_rpa.py` | `LOGGED_IN_SELECTORS`、`LOGGED_OUT_SELECTOR`、`_parse_item_locator()` |
| `account_client.py` | `PLACEHOLDER_PLATFORM`、`LEASE_HOLDER`、账号 setup 文案 |
| `task_service.py` | 接入 DB、任务日志、entitlement、视频留痕 |

## 依赖说明

本目录是 **示例**，不影响 skill-template 根目录运行。真实 skill 需要：

- Python 3.10+
- Python 包 `playwright`：属于**宿主共享 runtime** 的通用能力；技能侧**不要**在 `requirements.txt` 中重复声明，也**不要**在代码或脚本中执行 `pip install playwright`
- 真实 skill **默认使用系统 Chrome/Edge**，**不使用** Playwright 下载的内置 Chromium
- 技能侧**不要**执行 `playwright install`、`playwright install chromium` 或类似命令
- 若本地独立开发环境缺少 Playwright Python 包，只能作为开发机临时环境补装；**生产/宿主运行**由共享 runtime 解决
- `jiangchang_skill_core`（如 `find_chrome_executable` 等，由 platform-kit 提供）
- 兄弟 skill `account-manager`

## 运行测试

```bash
cd examples/real_browser_rpa
python -m pytest tests/ -v
```

测试为纯函数/Mock DOM，**不需要启动真实浏览器**。

## 当前状态

- 示例代码已就绪，可直接作为新 skill 复制起点。
- 未绑定具体平台业务字段；selector 为占位示例。
- 未接入真实数据库与 CLI 入口。
