---
name: wb-buddy-checkin
description: 自动完成 WorkBuddy 桌面客户端「Buddy 加油站」每日签到与「派猫猫旅行」积分领取。API 直连方案（推荐）：读本机登录态直调官方接口，兼容 5.6.2+ 加密登录态（AES-256-GCM 信封自动解密）；GUI 坐标点击方案兜底（纯 ctypes 窗口置前 + 坐标点击 + 截图灰度校验，零第三方依赖）。猫猫旅行支持只读状态展示与先领后派全自动闭环（写操作需显式 --auto）。
agent_created: true
---

# wb-buddy-checkin —— WorkBuddy 每日签到 + 猫猫旅行

在 Windows 上自动完成 WorkBuddy「Buddy 加油站」每日签到（每日 100 积分）与「派猫猫旅行」闭环（每日 5-10 积分额外收益）。

**推荐执行顺序（2026-09-29 定稿）**：API 直连（秒级）→ 旅行 `--auto` 闭环 → 仅当 API 失败（exit 2）才回退 GUI 坐标点击。

## 何时使用

- 用户说「自动签到」「每天领 WorkBuddy 积分」「Buddy 加油站签到」。
- 配置定时任务，让它在每天固定时间（如 9:00）自动跑。
- 注意：这是**通用、可分享**的实现，**不包含任何个人身份、路径或通知目标**；若要把结果推送给某人（微信/钉钉等），由调用方在 skill 之外自行配置。

## 前置条件

- Windows 系统（脚本依赖 `ctypes.windll` / `user32` / `gdi32`）。
- Python 3（标准库即可，无需 `pip install` 任何包）。
- WorkBuddy 桌面客户端正在运行。
- 首次使用**必须校准坐标**（见 `references/calibration.md`），因为不同屏幕/布局下点击点不同。**这步跳过是移植后"只会点头像"的头号原因。**

## ⚠️ 移植给别人 / 第一次用：先做这件事

**先跑一次校准，再 `-run`**。脚本内置的坐标是作者屏幕的校准值，别人的屏幕八成对不上——头像在左下角还能蒙对，但加油站/领取位置一偏，后续点击全打空，看起来就像"只点了头像"。

校准有两种，**推荐用弹窗校准（通用、傻瓜、零依赖）**：

```bash
# 弹窗校准（推荐）：自动弹出一个悬浮窗，按提示把鼠标移到三个目标点，
# 每步倒计时结束自动记录，三步写 calibrate.json。无需终端/微信/任何外部通道。
python scripts/wb_mouse_checkin.py -calibrate-gui
```

无 GUI 环境（如某些精简 Python 没带 tkinter）时，退而用终端文字校准：

```bash
# 终端校准：把鼠标依次移到 头像 / Buddy加油站 / 立即领取 三个点，各按一次回车
python scripts/wb_mouse_checkin.py -calibrate
```

校准后直接：

```bash
python scripts/wb_mouse_checkin.py -run
```

> 没校准就 `-run`，脚本会红字警告"用的是示例默认坐标，大概率打空"，并打印算出的三个屏幕坐标供你对照。

## 使用方法

脚本位于 `scripts/`，**两套方案**：

### 方案 A：API 直连（推荐，2026-08-18 新增 / 2026-09-29 升级）

零 GUI 依赖，无窗口位置/DPI/更新横幅遮挡问题。读本地登录态直调官方接口：

```bash
# 查询状态 + 未签则领取（幂等）；优先 v2 端点（真实积分数据），失败自动回退旧端点
python scripts/wb_api_checkin.py

# 仅查询，不领取
python scripts/wb_api_checkin.py -status
```

退出码：`0`=成功/已签到 / `2`=失败（无登录态/解密不可用/接口异常）。

**原理**（2026-08-18 逆向自 app.asar + 实测验证；2026-09-29 兼容升级）：
- 登录态文件：`%LOCALAPPDATA%\CodeBuddyExtension\Data\Public\auth\workbuddy-desktop.info`（JSON；同一账号体系，WorkBuddy/CodeBuddy 通用）
- **5.6.2+ 加密登录态兼容（2026-09-29）**：新版把 `auth.accessToken` 改为 AES-256-GCM 信封 `{"$wbEncrypted":1,...}`，静态钥运行时驻留 WorkBuddy.exe 进程内存（磁盘无明文）。本脚本复用市场 skill **totorosir-workbuddy-score** 的解密引擎（`buddy_station.load_credentials`，MIT-0，密钥发现：环境变量→密钥文件→DPAPI/进程内存扫描→CDP），import 失败或未安装时明确报错 exit 2，由调用方回退 GUI。
- 端点（双端点，v2 优先）：
  - v2（数据真实）：`POST https://www.codebuddy.cn/v2/billing/meter/checkin-activity-status`（查询）、`POST /v2/billing/meter/daily-checkin`（领取，幂等）
  - legacy 回退：`POST https://copilot.tencent.com/billing/meter/checkin-status`、`POST /billing/meter/daily-checkin`（活动期外会返回 连续0/激活False 假数据，仅兜底）
- 认证：`Authorization: Bearer <accessToken>`；**billing 接口必须带浏览器 User-Agent**，否则服务端裸 400（2026-08-18 实测坑；travel 接口不校验 UA）

### 方案 A+：派猫猫旅行闭环（2026-09-29 新增）

```bash
# 只读状态展示（默认）：空闲/旅行中(倒计时)/已到达(可领积分)
python scripts/wb_travel.py

# 全自动闭环（写操作，先领后派）：arrived 则领取 → 重查 → idle 且未达每日上限则派出
python scripts/wb_travel.py --auto

# 指定派遣地点（1=咖啡馆 2=商场店铺 3=健身房 4=古镇客栈；缺省随机，收益无差异）
python scripts/wb_travel.py --auto --location 1

# 机器可读 JSON
python scripts/wb_travel.py --json
```

退出码：`0`=成功 / `2`=失败。**安全约束**：写操作仅 `--auto` 显式触发；派出前必查 `daily_limit_reached`，达上限绝不发写请求；到达后状态保持 `arrived` 不丢积分，下次运行自动补领。接口 host `https://www.workbuddy.cn`（不带 `/v2` 前缀），仅需 Bearer Token。

### 方案 B：GUI 坐标点击（原方案，兜底）

```bash
# 1) 干跑：打印窗口信息 + 计算好的点击坐标 + 校准状态告警，不点击
python scripts/wb_mouse_checkin.py

# 2) 真实签到（自动读取 calibrate.json；无则告警并退回示例坐标）
python scripts/wb_mouse_checkin.py -run

# 3) 弹窗校准（推荐）：悬浮窗倒计时自动采样鼠标，三步写 calibrate.json
python scripts/wb_mouse_checkin.py -calibrate-gui

# 3b) 终端校准（无 GUI 时）：鼠标移到三个目标点各按回车
python scripts/wb_mouse_checkin.py -calibrate
```

**推荐组合**（2026-09-29 定稿）：每日任务先跑方案 A（API，稳、快、秒级）+ 方案 A+（`wb_travel.py --auto` 旅行闭环）；API exit 2 时才回退方案 B（GUI 点击，覆盖登录态异常场景）。

退出码：`0`=成功（已处于「今日已领」） / `2`=失败（未领取、面板异常，或无更新横幅时的真实失败） / `3`=未找到 WorkBuddy 窗口 / `4`=更新重启中（已点「重启升级」但 180s 内未等到新窗口，脚本已写 `checkin_state.json` 续签标记，需外部定时任务在更新完成后接管续签）。

结果截图保存在脚本同目录 `checkin_result.png`，可用于人工确认或后续通知。

## 失败兜底与更新续签（2026-08-17 老板需求）

签到失败时脚本自动检查是否「更新横幅作祟」，是则完成更新并**继续签到**（最多 3 轮）：

```
attempt_checkin()  ← 单轮签到(前置横幅检测 + 头像→加油站→领取→灰度校验)
        │
        ├─ 成功 → 清除 checkin_state.json → 退出码 0
        │
        └─ 失败 → 截图 detect_update_overlay()
                     │
                     ├─ 检测到绿色[重启升级] → announce_move + click → mark_pending()
                     │       → 等应用重启(最长 180s, wait_for_new_window)
                     │             ├─ 新窗口出现 → 绑定 _target → 下一轮继续签到
                     │             └─ 超时      → 退出码 4 (checkin_state.json 留续签标记)
                     │
                     └─ 无横幅 → 真实失败 → 退出码 2
```

- **续签标记**：`scripts/checkin_state.json`（`{"pending": true, "reason": "...", "ts": "..."}`）。签到成功自动清除；应用更新重启中由脚本写入，供续签流程读取判断。
- **续签载体 = Windows 计划任务（关键，2026-08-17 老板质疑后修复）**：WorkBuddy 重启时，运行在它进程内的 agent 会话会**连带终止**——「等几分钟重跑」这类会话内逻辑不可靠。正确做法：脚本点「重启升级」后先 `schedule_resume_task()` 用 `schtasks /create` 注册 **8 分钟后**的 `-resume` 计划任务（`python wb_mouse_checkin.py -resume`）。该任务**独立于 WorkBuddy 进程**，重启不影响它；到点由独立 python 进程唤醒，`do_resume()` 检查续签标记 → 等 WorkBuddy 窗口出现（最长 600s）→ `attempt_checkin()` 补签 → 成功则清标记 + `cancel_resume_task()` 删任务。
- **双保险**：脚本点更新后本进程若还活着，会先自己等重启 180s 并续签（此时顺手删掉计划任务，避免重复）；只有等不到（进程随重启被杀）才靠计划任务兜底。
- **注意**：点「重启升级」后 WorkBuddy 会退出并重装新版本，旧窗口句柄失效；脚本用 `wait_for_new_window()`（轮询重新枚举）等新窗口，绑定后继续签到。

## 关键实现要点（避免重踩坑）

1. **所有 Win32 调用必须显式声明 `argtypes`**，`HWND` 按 `c_void_p`（64 位指针）传，回调签名用 `WINFUNCTYPE(BOOL, HWND, c_void_p)`。不声明会被 ctypes 默认按 32 位 `c_int` 截断，导致 `SetForegroundWindow`/`EnumWindows` 静默失败——表现为「窗口没置顶、点击打空」。
2. **可靠置前 = 解决"窗口不在前台"**：最小化先 `ShowWindow(SW_RESTORE)`（恢复后验证 `GetWindowRect` 已脱离 -32000 幽灵坐标，最多重试 3 次）→ `AttachThreadInput` 线程绑定绕过系统前台锁 → `SetForegroundWindow`。**不要用 `SetWindowPos(HWND_TOP)` 钉死窗口位置**——WorkBuddy 会主动把它移回原位置/改尺寸（实测移到 (831,411) 之类），反而导致坐标全乱。
3. **窗口枚举必须精确匹配标题**：本机可能同时存在「WorkBuddy」(主窗口) 与「WorkBuddy - 个人中心 - xxx」等子窗口。`if TARGET_TITLE in buf.value` 子串匹配会命中 z 序最前的子窗口（可能是最小化/未显示的幽灵窗口）→ 所有点击打空。修复：`if title == TARGET_TITLE` 精确匹配优先，找不到再兜底子串匹配。
4. **坐标原点用 `GetWindowRect` 的 left/top，不用 `ClientToScreen`**：实测点击头像弹出菜单后 `ClientToScreen` 返回 2× 错误值（`GetWindowRect` 正常 (619,169) 时它返回 (1238,338)），导致全部坐标翻倍打空——这是 2026-08-04 的**真正根因**。WorkBuddy 是无边框窗口（`Chrome_WidgetWin_1`，客户区 = 整个窗口），客户区原点 = 窗口左上角，用 `GetWindowRect` 永远稳定。**窗口被移去哪坐标就跟随到哪，天然免疫"窗口不在前台/被移动"**，根本不需要钉窗。
5. **脚本开头设置 DPI 感知**：`SetProcessDpiAwareness(2)`（per-monitor DPI aware），失败则回退 `SetProcessDPIAware()`。避免 Windows DPI 虚拟化导致 GetWindowRect/SetCursorPos 坐标系不一致（备用保险）。
6. **坐标用「相对客户区左下角」**（x=距左, y=距底），窗口任意缩放都命中，校准一次永久复用。
7. **校验用「近黑像素数」而非白字数**：灰底「今日已领」按钮也含白字，不能靠白字判定；黑底「立即领取」有大量近黑像素（r,g,b<70），灰按钮近黑像素≈0。用此区分，主题无关。
8. **中段校验防假阳性（必须保留）**：点完「Buddy 加油站」后先截图，`verify_claimed` 要求按钮位置是**黑像素**（`unclaimed`，即面板已打开、黑底「立即领取」按钮存在）才继续点领取。否则若面板没打开，最终截图是 WorkBuddy 主界面，`verify_claimed` 会在按钮位置采样到主界面灰色背景误判 `claimed` → 假阳性签到成功。
9. **截图优先 desktop-control-win 的 `screen-info.ps1`**（若存在），否则回退 `PrintWindow` 客户区截图；`PNG` 编解码全用标准库手写（支持所有 filter），无外部依赖。
10. **幽灵矩形防御（2026-08-06）**：点完加油站后窗口可能短暂进入最小化/恢复动画态，`GetWindowRect` 返回 `(-32000,-32000,160x28)` 幽灵矩形，直接把坐标算飞（立即领取点到屏幕外）。检测到 `wr.left < -10000` 时先 `IsIconic → SW_RESTORE` 重读一次，仍异常则保留上次有效坐标不更新全局。
11. **防"撞用户操作"三件套（2026-08-12）**：定时任务在用户正用电脑时跑，脚本点击会和用户实时鼠标操作打架（用户反馈"你控制鼠标时我在用，移动不到正确位置"）。解法不是更用力抢鼠标（`SetCursorPos` 本来就能强制移动），而是：
    - **`wait_mouse_idle()`**：接管前纯读取鼠标位置（`GetCursorPos` 不碰鼠标）连续采样，静止 2s 才接管（最多等 60s 超时不阻塞）。用户在用电脑时安静等待，绝不抢。
    - **`announce_move()`**：点头像前鼠标「飞向目标 → 移开右上角 → 飞回目标」两次可见位移（各停 0.5s），用户看到鼠标自己动就知道脚本要操作了，提前松手。
    - **`click_at()` 点击前停顿 0.4s**：`SetCursorPos` 后多留反应时间。
    - 调用顺序：`wait_mouse_idle()` → `focus()` → `announce_move(sa,...)` → `click_at(*sa,...)`
12. **更新提示（底部横幅）遮住头像自动处理（2026-08-17）**：WorkBuddy 有新版本时会弹出**横跨客户区底部的白色横幅**（左侧升级图标 + 文案"新版本就绪" + **绿色按钮「重启升级」** + 白色按钮「更新日志」 + 右侧 ×），横幅会**盖住左下角头像** → 脚本点头像实际点到横幅上 → 账户菜单不弹出 → 后续全错位 → 签到失败。老板 2026-08-17 提供实测截图确认形态。
    - **检测**：`focus()` 后、点头像前先截 `checkin_pre.png`；在客户区**底部 85%~100%** 区域扫描 **teal 色像素**（实测按钮 avgRGB=(95,208,169)，判定 `g>=150 and g-r>=40 and b>=90 and r<=180`），找最大 60px 簇（≥ 80 采样点）。teal 是品牌青绿，普通灰色 UI（g-r≈0）天然不命中，误判率低。
    - **处理**：检测到即 `announce_move + click_at` 点击（点的就是绿色「重启升级」，**不是**白色「更新日志」）；然后轮询 3s 间隔：
      - 旧窗口句柄 `IsWindow()` 失效（应用重启升级中）→ `wait_for_new_window`（最长 60s）找新窗口 → 重新绑定 `_target` → `'restarted'`，重新 focus + 截图确认无横幅后继续签到。
      - 横幅消失（`detect_update_overlay` 返回 None）→ `'done'`，重新 `focus + recompute_geometry` 后继续签到。
      - 超时 120s 仍异常 → 失败退出（避免定时任务长期卡住）。
    - **验证**：用 `checkin_after_ctrlw.png` 实测，检测中心 (333,1132) vs 按钮实际中心 (309,1141)，偏差 24px，落在按钮内部。

## 配置定时任务（示例）

在 WorkBuddy 自动化里建一个每日任务，prompt 大致为：

> 运行 `python scripts/wb_mouse_checkin.py -run`（脚本内置：窗口精确匹配 + 最小化恢复置前 + 固定坐标点击 + 中段校验面板是否打开 + 灰度校验是否已领）。
> 读 `checkin_result.png` 确认结果：灰色「今日已领」=完成；黑底「立即领取」仍在=失败。
> 按你的通知偏好（微信/钉钉等）把结果发给本人。**通知目标和通道由你自己的配置决定，本 skill 不内置任何推送。**

cwd 设为该 skill 的 `scripts/` 所在目录（或脚本实际位置）。

## 参考

- 坐标校准与常见问题：`references/calibration.md`
