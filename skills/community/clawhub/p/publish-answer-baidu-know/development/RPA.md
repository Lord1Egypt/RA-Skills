# RPA 操作标准（浏览器 / 桌面 / 手机）

> 本文是团队 RPA 开发的**统一标准**。任何需要"自动操作软件界面"的 skill，都应先读这份文档，按这里的选型和范式落地，不要每个项目重新踩坑。

我们开发的各类 skill，本质上都是在替人操作三类界面：**浏览器、桌面软件、手机软件**。三类的底层技术不同，但**工程范式相同**：保持登录态、有头运行、拟人操作、失败存证、人工兜底。

---

## 0. 三端通用范式（先看这个）

无论操作哪类界面，都遵循同一套约定：

| 约定 | 说明 |
|------|------|
| **保持登录态** | 复用持久化 Profile / session，避免每次重新登录触发风控；账号由 account-manager 下发，不硬编码 |
| **有头运行** | 默认有头（headless 易被识别 / 难人工介入）；`OPENCLAW_BROWSER_HEADLESS=1` 仅给 CI |
| **拟人操作** | 真实事件（isTrusted=true），逐字输入、随机延迟、贝塞尔鼠标轨迹；严禁 JS 直接设值/JS 点击/JS 跳转 |
| **步骤间随机等待** | 每两步操作之间 `random_delay(min,max)`，区间由 `.env` 配置（默认 1~5s） |
| **人工兜底（HITL）** | 滑块 / 短信验证码 / 人脸 / U盾 / 动态口令 → **停下来轮询等人工**，超时报 `ERROR:XXX_NEED_HUMAN`，绝不自动硬闯 |
| **失败存证** | 失败必截图，合规场景全程录屏，统一存 `{数据目录}/rpa-artifacts/{batch_id}/{tag}_{ts}.png` |
| **选择器纪律** | 语义选择器优先（id/name/text/aria）；**F12 确认后再写，严禁凭记忆猜 DOM** |
| **统一错误码** | `ERROR:REQUIRE_LOGIN` / `ERROR:CAPTCHA_NEED_HUMAN` / `ERROR:RATE_LIMITED` / `ERROR:LOGIN_TIMEOUT` 等，见下方错误码表 |
| **幂等 / 断点续跑** | 批量操作记录"已处理到第几条"，崩溃后能续跑、不重复提交 |

> 三端各自实现一个会话抽象 `RpaSession`（launch / login / act / screenshot / close），上层 skill 不感知是浏览器还是手机。

---

## 1. 浏览器（标准已成熟）

**选型：Playwright + 系统 Chrome/Edge。** 这是团队验证最充分的一条线（标杆技能 `1688-scrape-contacts`、`receive-order` 已落地）。

### 1.0 生产路径（优先）

| 项 | 标准 |
|----|------|
| 浏览器 | **优先系统 Chrome/Edge** + `launch_persistent_context`，`channel="chrome"` 或 Edge；不用内置 Chromium，**技能内不要 `playwright install`** |
| 登录态 | 持久 Profile 目录；账号、profile、lease **统一走 account-manager**（或对应兄弟技能），不硬编码密码 |
| CDP | **仅作诊断 / 桌面宿主类场景**；**不要**作为强风控站点的默认生产路径 |
| 行为 | 模拟真实用户：真实点击、键盘、鼠标、地址栏输入；**不要**拼接搜索结果 URL、DOM 注入、`el.value=`、JS 跳转 |
| 模式 | 默认有头 `OPENCLAW_BROWSER_HEADLESS=0`；无头仅 CI |
| 反检测 | stealth 默认开 `OPENCLAW_PLAYWRIGHT_STEALTH=1`（见 1.1） |

### 1.1 Playwright 启动标准

1. **默认有头**：`OPENCLAW_BROWSER_HEADLESS=0`（`.env.example` 默认值）。
2. **stealth 默认开**：`OPENCLAW_PLAYWRIGHT_STEALTH=1`；通过 `add_init_script` 注入指纹淡化脚本。
3. **不要在技能里自行安装 playwright**；由宿主共享 runtime 提供。
4. **不要默认传 `--no-sandbox`**（除非特定容器环境且已评估风险）。
5. **不要默认传 `--disable-blink-features=AutomationControlled`**；platform-kit stealth 已覆盖，额外 flag 可能适得其反。
6. **可以** `ignore_default_args=["--enable-automation"]`（platform-kit `launch_persistent_browser` 已处理）。
7. **强风控平台**：优先真实点击、键盘、鼠标、地址栏、持久 profile；**不要**直接拼接搜索结果 URL 或 DOM 注入。

指纹淡化（stealth）典型项：`navigator.webdriver=undefined`、`chrome.runtime`、`permissions.query`、`plugins`、`languages` 等。共享实现见 `jiangchang_skill_core.rpa`（platform-kit **>= 1.0.17**）。

**拟人操作**（必做）：

- 输入：逐字符 `keyboard.type(delay=90~240ms)`，**先真实点击聚焦再输入，绝不 `el.value=`**。
- 鼠标：贝塞尔曲线轨迹 + 微抖动；进场随机晃动。
- 导航：用真实点击触发，**不要 `window.location.href=` / JS 点击跳转**。
- 翻页：真实点击翻页控件，注意排除禁用态。
- 延迟：每步之间 `random_delay`（`.env` 中 `STEP_DELAY_MIN/MAX`）。

### 1.2 页面启动标准

**`launch_persistent_context` 的 `args` 只能放 Chrome 启动参数**（例如 `--start-maximized`、`--disable-blink-features=AutomationControlled` 等）。

**绝对不要把 `https://...` 这类 URL 放进 `args`。** 否则 Playwright 会报错：

```
BrowserType.launch_persistent_context: Arguments can not specify page to be opened
```

**正确做法（生产路径）：**

1. `launch_persistent_context(user_data_dir=profile_dir, executable_path=chrome, args=chrome_args, ...)`
2. `page = await context.new_page()`
3. `await page.goto(start_url, wait_until="domcontentloaded", timeout=60000)`

对强风控站点，如果需要更拟人，可以启动后通过**地址栏输入 / 真实点击进入**目标页，但**仍然不能把 URL 塞进 launch args**。

完整参考实现见：

- `examples/real_browser_rpa/README.md`（**开发真实浏览器 RPA 类 skill 时必须先读**）
- `examples/real_browser_rpa/scripts/service/browser_session.py`

**生产路径不要依赖 CDP 接管现有页面**；CDP 仅用于诊断或桌面宿主已打开浏览器的场景。

### 1.3 HITL / 验证码

- 自动处理失败时**允许等待人工**：滑块、短信、人脸、U盾、动态口令等。
- 等待人工验证时必须有：**字幕 step**（用户可见动作说明）、**结构化日志**、**超时**（`HUMAN_WAIT_TIMEOUT`）。
- 检测到风控页（URL/DOM 特征）→ 抛 `ERROR:CAPTCHA_NEED_HUMAN`，轮询等待或超时，**不要强行绕过平台安全机制**。
- **不要自动操作滑块**。

> 共享库：`jiangchang_skill_core.rpa.wait_for_captcha_pass`；**真实浏览器 RPA 成功案例**见 `examples/real_browser_rpa/`：
>
> - 先读 `examples/real_browser_rpa/README.md`
> - 再参考 `examples/real_browser_rpa/scripts/service/human_verification.py`
> - 再参考 `examples/real_browser_rpa/scripts/service/task_rpa.py`

### 1.4 Playwright 与安装边界

- Playwright 是宿主共享 runtime 提供的通用 Python 包能力；**正式 skill 不负责安装**。
- skill 侧**禁止**在 `requirements.txt`、安装脚本、运行脚本、根 `README.md` 用户说明中加入 `playwright install`、`pip install playwright` 或任何自动安装浏览器驱动的逻辑。
- 真实浏览器 RPA 默认使用**系统 Chrome/Edge**，由宿主/runtime 管理。
- **不要**执行 `playwright install chromium`、`playwright install chrome` 等浏览器驱动安装命令。
- 仅当**本地独立开发环境排障**时，开发者可手工检查或补装 Python 包 `playwright`；该操作**不得**进入 skill 交付文件与自动流程。

页面启动仍遵循 1.2：`launch_persistent_context` 的 `args` 只能放 Chrome 启动参数，**不能把 URL 塞进 `args`**；打开页面必须通过 `new_page()` + `goto()`，或通过真实地址栏/点击进入。

### 引用方式

共享实现位于宿主共享 runtime 安装的 `jiangchang-platform-kit`（`jiangchang_skill_core.rpa`）。复制后的业务技能直接 import，**技能仓库不得保留 rpa 公共代码副本**：

```python
from jiangchang_skill_core.rpa import (
    launch_persistent_browser,
    anti_detect,
    wait_for_captcha_pass,
    capture_failure,
    errors,
)
from jiangchang_skill_core.rpa.stealth import stealth_enabled, STEALTH_INIT_SCRIPT
```

- `RpaVideoSession` 来自 platform-kit **>= 1.0.17**；ffmpeg、背景音乐、media-assets 由 platform-kit 统一解析；已提供前置/后置缓冲、字幕、TTS 旁白、背景音乐循环、结尾淡出。
- `health` 对上述资源做只读诊断，不下载、不修复。

### 1.5 真实浏览器 RPA 示例（必读）

开发**真实网站 + 浏览器操作 + 登录态/验证码/滚动采集**类 skill 时：

1. **必须先阅读** `examples/real_browser_rpa/README.md`
2. 再参考以下代码：
   - `examples/real_browser_rpa/scripts/service/browser_session.py` — persistent context 启动
   - `examples/real_browser_rpa/scripts/service/human_verification.py` — 人工验证等待
   - `examples/real_browser_rpa/scripts/service/task_rpa.py` — RPA 主流程
   - `examples/real_browser_rpa/scripts/service/account_client.py` — account-manager CLI 封装

仿真浏览器 RPA 的 adapter 分层权威参考见 `examples/simulator_browser_rpa/`（含 async `simulator_playwright.py`、薄 `simulator_rpa` adapter、`account_client.py` subprocess），**不能**替代真实浏览器 RPA 规范。

### 1.6 仿真浏览器 RPA 示例（必读）

开发**自有仿真页面 / sandbox / 可控 DOM 的浏览器 RPA**（表单填写、批量提交、弹窗确认）时：

1. **必须先阅读** `examples/simulator_browser_rpa/README.md`
2. 再参考：
   - `examples/simulator_browser_rpa/scripts/service/browser_session.py` — async persistent context（**不含 goto**）
   - `examples/simulator_browser_rpa/scripts/service/simulator_playwright.py` — RPA 主流程（厚）
   - `examples/simulator_browser_rpa/scripts/service/adapter/`（薄 `simulator_rpa` + mock + dispatch）
   - `examples/simulator_browser_rpa/scripts/service/account_client.py` — account-manager subprocess
   - `examples/simulator_browser_rpa/scripts/service/task_service.py` — async 编排
   - `examples/simulator_browser_rpa/sandbox/demo_app.html`

> **先选类型再写代码**：真实第三方网站 → `real_browser_rpa`；自有 sandbox / 行业仿真 → `simulator_browser_rpa`。不要跨类型照抄 selector 或业务流程。

### 1.7 行业仿真平台浏览器 RPA（jc2009 类）

适用：**自有或共享 `sandbox.jc2009.com` 等行业仿真平台**，不是真实高风控第三方站。

工程范式与 §1.5 相同：

| 项 | 标准 |
|----|------|
| Playwright | **async** 贯穿；禁止 sync Playwright 用于完整 RPA 主路径 |
| 分层 | **薄 adapter** + `{domain}_playwright.py`（示例：`simulator_playwright.py`）+ `account_client.py` subprocess |
| 登录 | **双层**：门户 HITL（`#portal-user` / `#portal-pass` 类泛化 DOM）+ 业务系统登录（技能内自写） |
| 账号 | `url` 用行业根，不用 `/login`；`auth_strategy=per_session_manual`；`pick_web_account` + `release_lease` |
| 禁止 | **不要** `import account-manager` 的 `rpa_helpers` 等内部模块 |
| Selector | 用户可见文案 / `get_by_role` / `name` 优先；`data-testid` 有则用、无则 fallback；共享 sandbox **不要求**为技能加 testid |
| Profile | Chrome persistent profile 可能缓存旧 SPA → 联调排障：手工 `--user-data-dir` 清站点数据 |

权威 example：**修正后的** `examples/simulator_browser_rpa/`（不是任何生产技能仓库）。

---

## 2. 桌面软件（Windows 原生程序）

**选型：pywinauto（UIA backend）为主 + 图像识别兜底。**

桌面端常见于 ERP 客户端、网银控件、银企直连等本地程序。优先走可访问性树（控件 ID/名字），坐标点击只做最后兜底。

| 技术 | 优先级 | 适用 / 说明 |
|------|--------|------|
| **pywinauto（`backend="uia"`）** | ✅ 首选 | 基于微软 UI Automation 树，拿控件 AutomationId/Name/ControlType，**稳定、不依赖屏幕坐标**，纯 Python |
| **FlaUI**（经 pythonnet 调 .NET） | 备选 | UIA 拿不到的复杂/自绘控件时更完整，但需引入 .NET 运行时 |
| **Playwright** | 特例 | 目标是 **Electron 套壳应用**（很多新 SaaS 客户端）时，可当浏览器驱动 |
| **PyAutoGUI / SikuliX（图像识别）** | ⚠️ 兜底 | 控件树完全拿不到时（Flash/远程桌面/纯自绘 UI）；**靠截图找图+坐标，分辨率/缩放一变就崩**，仅最后手段 |

### 桌面端注意事项

- **窗口聚焦/置顶**：操作前确保目标窗口前置，避免误操作其它窗口。
- **DPI/缩放**：图像识别方案必须固定显示缩放比例；UIA 方案不受影响（优先用 UIA 即是为此）。
- **存证**：同样要失败截图（截目标窗口/全屏），存到 `rpa-artifacts`。
- **人工兜底**：U盾插拔、动态口令、人脸 → 停下等人工，超时 `ERROR:XXX_NEED_HUMAN`。

```bash
pip install pywinauto        # UIA 自动化
# 图像兜底：pip install pyautogui opencv-python
```

> 状态：桌面端选型为推荐标准，**尚待真实项目实战验证**，落地时回补踩坑记录到本文。

---

## 3. 手机软件（USB 连接电脑）

**选型：Android 用 uiautomator2（或 Appium）；iOS 用 Appium + WebDriverAgent（需 Mac）。** 底层都是经 USB 的 ADB / WDA。

| 平台 | 技术 | 优先级 | 说明 |
|------|------|--------|------|
| **Android** | **uiautomator2**（python 原生） | ✅ 首选 | ADB over USB，直接拿控件树点击/输入，比 Appium 轻快，纯 Python |
| Android | **Appium**（uiautomator2 driver） | 备选 | 需要跨平台统一接口、或团队已有 Appium 资产时用 |
| Android | **Airtest + Poco**（网易开源） | 兜底 | 图像+控件混合，自带 IDE 可录制；控件树拿不到时用 |
| **iOS** | **Appium + WebDriverAgent（XCUITest）** | 唯一可行 | **必须有一台 Mac 做中转**，Windows host 无法直接驱动 iOS |
| 投屏/人工介入 | **scrcpy** | 辅助 | USB 投屏到电脑，配合人工过验证码/人脸 |

### 手机端注意事项

- **设备就绪检查**：`adb devices` 确认已授权连接；放进 `doctor` 自检。
- **登录态**：靠 App 自身保持登录，必要时引导人工首登一次。
- **人工兜底**：短信验证码、人脸、指纹 → scrcpy 投屏让人工完成，程序轮询等待。
- **存证**：失败时 `adb screencap` / Appium 截图存 `rpa-artifacts`。

```bash
# Android（首选）
pip install uiautomator2
python -m uiautomator2 init   # 初始化设备端 agent
# 或统一走 Appium：pip install Appium-Python-Client（另需 Appium Server）
```

> 状态：手机端选型为推荐标准，**尚待真实项目实战验证**，落地时回补踩坑记录到本文。

---

## 4. 统一错误码（RPA 场景）

skill 退出/抛错统一用 `ERROR:` 前缀 + 稳定码，方便宿主与上层判断与重试：

| 错误码 | 含义 | 上层处理建议 |
|--------|------|------|
| `ERROR:REQUIRE_LOGIN` | 未登录 / 登录态失效 | 触发登录流程 |
| `ERROR:LOGIN_TIMEOUT` | 等待人工登录超时 | 提示用户重跑并及时操作 |
| `ERROR:CAPTCHA_NEED_HUMAN` | 命中滑块/验证码拦截 | 暂停等人工，或转人工队列 |
| `ERROR:RATE_LIMITED` | 触发频控 | 退避后重试 |
| `ERROR:MISSING_BROWSER` | 未检测到 Chrome/Edge | 提示安装 |
| `ERROR:DEVICE_NOT_READY` | 手机未连接/未授权 | 检查 USB/ADB |
| `ERROR:WINDOW_NOT_FOUND` | 桌面目标窗口未找到 | 检查程序是否启动 |

---

## 5. 存证与录屏规范

### 5.1 截图存证

- **路径**：`{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{slug}/rpa-artifacts/{batch_id}/{tag}_{timestamp}.png`
- **失败必截图**：受 `OPENCLAW_ARTIFACTS_ON_FAILURE`（默认开）控制。
- **Playwright 不负责录屏**，仅浏览器自动化。
- **常见 tag**：`before_submit` / `after_submit` / `captcha` / `login_fail` / `error`。

### 5.2 RPA 视频 step 标准

字幕是**用户可见动作说明**，不是技术日志。step 要贴近真实动作，不要只在大流程入口打点。

推荐关键动作示例（按业务裁剪）：

- 启动浏览器
- 打开首页
- 检查登录状态
- 定位输入框
- 输入关键词：xxx
- 点击搜索
- 等待结果
- 打开详情页
- 提取信息
- 写入结果
- 任务完成

技术诊断、重复跳过、DB 写入可以显示但**通常不需要旁白**。

`title` / `closing_title` 必须由 skill 传入**中文业务文案**（如「开始执行示例任务」「示例任务执行完成」）。

### 5.3 录屏成片标准

- RPA skill 默认 `OPENCLAW_RECORD_VIDEO=1`。
- 使用 platform-kit 的 **`RpaVideoSession`**；**skill 不要自行合成视频**（不要自己调 ffmpeg 拼 MP4）。
- `OPENCLAW_RECORD_VIDEO=0` 时 session 无副作用（不启 ffmpeg、不写字幕文件）。
- **ffmpeg 是唯一录屏器**（Windows：`gdigrab` + `desktop`）。
- **最终视频**：`{skill_data_dir}/videos/{skill_slug}_{yyyyMMdd_HHmmss}_{batch_id}.mp4`
- **中间产物**：`rpa-artifacts/{batch_id}/capture.mp4`、`subtitles/`、`logs/` 等。
- 任务完成后 CLI / `result_summary` 应包含：`video_path`、`raw_video`、`video_log`、`video_warnings`、`music_path`、`voiceover_path`、`audio_warnings`（见 `scripts/service/task_run_support.py`）。

模板最小示范见 `scripts/service/task_service.py` 的 `_run_template_demo()`。

---

## 相关文档

- `ADAPTER.md` — 真实/仿真 × API/RPA 的四档适配器模式
- `CONFIG.md` — `.env` 配置规范与首次落盘机制
- `RUNTIME.md` — 运行时目录与环境变量约定
