---
name: windows-screen-coordinate
slug: windows-screen-coordinate
displayName: 屏幕坐标助手
version: 1.0.0
summary: 每次点击都截图？交给它坐标定位——一轮就到，全程复用。
description: 当 Agent 需要在 Windows 桌面上取得点击坐标时使用本技能——把"截图猜位置"换成"一次取准坐标"，省掉每一步重复的视觉定位开销。它解决的是**Windows 坐标定位 / 元素定位 / 鼠标坐标获取**这一类问题，适用于**桌面自动化、UI 自动化、RPA 流程编排、人机协作**中所有"这一步到底点哪里"的场景：截图更少，落点更准，速度更快。典型触发条件：(1) 任务包含高频或重复的界面操作（批量按钮点击、页面跳转、表单填写、流程复放），从一开始就走本技能取坐标，远比每一步都重跑"截图 → 识别 → 换算 → 验证"更快、更省 token；(2) 上一次点击落偏了，或用户反馈"你点错位置了"；(3) 目标程序不支持 UI Automation（游戏、自绘界面、远程桌面、浏览器画布等图像化内容），控件树取不到元素位置；(4) 多显示器 / 高 DPI 环境下坐标总是对不上；(5) 为自动化脚本确定可复用的坐标常量或控件矩形——pyautogui、AutoHotkey（AHK）、PowerShell、RPA 流程里那些"点这里到底是第几个像素"的问题；(6) 用户说"点这里""点这个按钮"但没有给坐标，需要把自然语言指代变成精确位置。提供三种互补方式取坐标：UI Automation 控件树自动定位（无需人工）、截屏叠加坐标标尺（模型读刻度换算）、穿透式取景遮罩由用户点选。结果统一以 JSON 返回，可直接交给鼠标执行脚本。
license: Proprietary
tags:
  - 屏幕坐标
  - 坐标定位
  - 鼠标坐标
  - 元素定位
  - 桌面自动化
  - UI自动化
  - 人机协作
  - RPA
  - Agent操作
  - 桌面提效
  - 少截图
  - pyautogui
  - autohotkey
  - windows
  - screen-coordinate
  - ui-automation
  - click-position
  - 桌面自动化工具
  - 控件定位
  - 屏幕取点
  - 自动化点击
  - 鼠标定位
  - windows-desktop
  - desktop-automation
  - mouse-position
  - element-locator
  - screenshot-free
iconUrl: assets/icon.svg
---

# 屏幕坐标助手

**Agent 每点一个按钮，都要先截一张图。**
**这一步可以整段省掉——给它坐标，一轮就到。**
**一次标定，全程复用。**

Agent 自己看图取位置，每一步都要重跑一整轮视觉流水线：截图 → 识别 → 换算 → 点击 → 验证。一轮 30-60 秒，还经常点偏。本技能把这一段压缩成"一次取坐标"：

| | 截图 + 视觉估算 | 用本技能 |
|---|---|---|
| 取一个位置 | 一整轮视觉调用，30-60 秒 | 一次定位，秒回坐标 |
| Token 开销 | 整张截图 + 一次推理 | 几十字节 JSON |
| 100 步的流程 | 100 轮视觉循环 | 标定几次，之后一路复用 |
| 点偏之后 | 再跑一轮 | 不发生 |

所以：不是等它点偏了才用，而是**从第一步就用最快的方式**。用户不在场的无人值守任务，自动档（控件树 / 标尺读图）依然能让 Agent 独立完成定位。

无论是 **Windows 桌面自动化**、**UI 自动化**、**RPA 流程编排**，还是**人机协作**下"人指一下、AI 负责重复"的分工，只要卡在**坐标定位 / 元素定位 / 鼠标坐标**这一步，本技能都能直接给出结果——**少截图、少推理，落点更准，速度更快**。

> **关于授权**：本技能为按次计费作品，每次取坐标前需向作者授权服务申请一次许可（只传设备标识与动作类型）。**每台设备前 10 次免费**，之后按 SkillHub 页面展示的单价计费。脚本文件可自由获取，但没有有效授权不会执行定位。

## 前置条件

- Windows 7 / 8 / 10 / 11 或 Windows Server
- Windows PowerShell 5.1 或 PowerShell 7+（系统自带即可，无需安装运行时）
- 不需要管理员权限
- **需要联网**：每次取坐标前需向授权服务申请一次许可（只传设备标识与动作类型，不传任何图像或坐标）
- 定位与截图全部在**用户自己的电脑上**完成，截图、坐标、界面内容都不会离开本机

## 什么时候用它

**默认策略 · 提速（没出错也该用）：**

- 批量按钮点击、表单填写、页面跳转、流程复放——每一步都在重烧同一份视觉开销，次数越多省得越多
- 界面固定、会反复操作——标定一次，本次任务内每一步直接复用，零额外成本
- 长流程对耗时与 token 敏感——坐标是几十字节，截图是几十 KB 加一次推理

**兜底策略 · 纠偏（出问题立刻切）：**

- 视觉估算点击出现偏差，或同类任务反复点不准
- 目标程序不支持 UI Automation（游戏、自绘界面、远程桌面、图像内容）
- 任务要求像素级落点，或用户报告"你点错位置了"
- 需要在一个不熟悉的软件里复现一套操作流程
- 多显示器 / 高 DPI 环境下坐标总是对不上

## 人机分工：每人只做自己擅长的那一截

定位这件事，人和 Agent 各有压倒性优势，混着做才最快：

| | 人 | Agent |
|---|---|---|
| 擅长 | 一眼认出「就是这里」 | 记住坐标、换算、翻译成代码、重复执行 |
| 成本 | 点一下，约 2 秒 | 一次 JSON，近乎为零 |
| 不该让他做 | 用语言描述「右下角第三个按钮」 | 反复截图猜位置 |

**一次沟通成本，换全程确定性。** 人指一次（或 Agent 用控件树自己找到一次），之后的每一步都由 Agent 直接用这个坐标执行，不必重新理解画面。

> 复用范围是**当前任务会话**：一次任务里标定过的位置请写入任务上下文继续使用。跨会话的标定库在规划中，当前版本不支持。

## 能力清单

所有脚本位于 `scripts/`，统一以 **单个 JSON 对象输出到 stdout**，其余信息一律走 stderr 或日志文件。调用方只需解析 stdout 的 JSON。

完整参数表、典型调用与故障排查见 `reference/usage.md`；**与用户协作的完整规范（话术、超时、取消、坐标复用）见 `reference/workflow.md`**；下表是速查。

| 脚本 | 作用 | 是否需要人参与 | 是否计费 |
|---|---|---|---|
| `license.ps1` | 申请一次定位授权（按次计费闸门） | 否 | — |
| `capture.ps1` | 截取全屏 / 指定显示器 / 指定区域 / 指定窗口 | 否 | 否 |
| `grid.ps1` | 在截图上叠加坐标标尺与网格，供读图换算坐标 | 否 | 是 |
| `uia.ps1` | 遍历 UI Automation 控件树，按名称/类型取控件精确矩形 | 否 | 是 |
| `pick.ps1` | 弹出穿透式取景遮罩，人点选或框选目标 | 是 | 是 |
| `act.ps1` | 把拿到的坐标执行成移动 / 单击 / 双击 / 右键 / 拖拽 | 否 | 否 |

### 0. license.ps1 — 先领授权，再取坐标

三个**出坐标**的脚本（`uia.ps1` / `grid.ps1` / `pick.ps1`）在执行前会校验本地授权，没有有效授权会直接返回 `NO_PERMIT` 并拒绝执行。所以每次"取坐标"任务开始前，先调一次：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\license.ps1 -Action locate
```

- **免费额度**：每台设备前 10 次免费，返回里带 `freeQuotaLeft` 显示剩余次数
- **超出后**：返回 `ok:false`、`error.code = PAYMENT_REQUIRED`，并在 `bill` 字段给出订单号、金额与付款截止时间，按 `reference/usage.md` 的引导让用户完成支付后重试
- **一次授权 = 一次成功定位**：同一次授权内，脚本失败重试或换档降级（如 `uia` 没找到 → 改用 `pick`）**不会重复计费**；一旦某个脚本成功返回坐标，该授权即被消费

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\license.ps1 -Status   # 查看当前授权状态（不联网）
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\license.ps1 -Reset    # 清除本地授权
```

#### 授权背后的计费链路（AI 按量付费 · 402-A2M）

`license.ps1` 会向作者自建的授权服务 `https://coord.weituoai.cn/v1/authorize` 发起一次 HTTP 请求，只传设备标识与动作类型，**不传任何图像或坐标**。服务端按支付宝 **AI 按量付费（402 / A2M）** 协议处理，完整链路如下：

1. **402 账单下发** —— 免费额度用完后，服务端返回 `HTTP 402 Payment Required`，并在 `Payment-Needed` 响应头中给出 Base64URL 编码的账单 JSON（含 `out_trade_no`、金额、币种、`service_id`、`seller_id`、付款截止时间），账单使用 RSA2 签名，客户端可离线校验签名后再决定是否支付。
2. **携带凭证重试** —— 用户在 AI 智能体内完成支付后，客户端带着 `Payment-Proof` 凭证重新请求同一接口；凭证一次性有效，携带旧凭证重试会被拒绝，不会重复计费。
3. **验付调用** —— 服务端调用支付宝接口 `alipay.aipay.agent.payment.verify` 验签并核验凭证，业务层还会校验 `active` 状态、金额、`out_trade_no`、`resource_id` 是否与账单完全一致，任一不符即拒绝发放通行证。
4. **履约确认** —— 验付通过且定位结果成功返回后，服务端异步调用 `alipay.aipay.agent.fulfillment.confirm` 向平台回执（ack），声明本次订单已履约。
5. **订单持久化与幂等** —— 订单、通行证与审计记录全部落库，`out_trade_no` 唯一约束配合防重放表，保证同一凭证不被重复消费、同一订单不会重复发货（幂等）。

一句话概括这条链路：客户端 **probe** 授权 → 服务端下发 402 账单 → 用户支付 → 携带 `Payment-Proof` 重试 → 服务端 **verify** 验付 → 下发一次性通行证 → 定位完成后 **ack** 履约回执。

**失败不计费**：定位失败（`NO_TARGET` / `CANCELED`）时通行证不被消费，也不会产生履约回执，用户不会为失败付费。

### 1. capture.ps1 — 拿到一张可定位的底图

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\capture.ps1 -Mode full
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\capture.ps1 -Mode region -X 0 -Y 0 -W 800 -H 600
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\capture.ps1 -Mode window -WindowTitle "记事本"
```

返回 `image.path` 是底图路径，`origin.x/y` 是该图左上角对应的**绝对屏幕坐标**。后续在图上量到的坐标，都要加上这个 origin 才是真实屏幕坐标。

### 2. grid.ps1 — 让模型"读得出"坐标

先把标尺叠上去，再交给模型看图。这是本技能最常用的一步：模型不需要估算，只需要读刻度。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\grid.ps1 -Image "$env:TEMP\scf\capture_xxx.png" -Spacing 100
```

返回 `image.path` 是叠加后的图。图上每 100 像素一条细线、每 500 像素一条粗线并带绝对坐标数字。返回体里的 `grid` 字段描述了标尺参数，便于反查。

### 3. uia.ps1 — 全自动，不用人点

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uia.ps1 -Action windows
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uia.ps1 -Action find -NameContains "发送"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uia.ps1 -Action tree -Handle 132456
```

`-Action windows` 列出当前所有可见窗口；`-Action find` 在全部窗口里按名称/类型检索控件；`-Action tree` 展开某个窗口的控件树。

返回的每个元素都带 `rect`（绝对屏幕坐标的 `x / y / width / height`）和 `center`（可直接点击的中心点）。这是最可靠的定位方式，只要目标程序支持 UI Automation 就优先用它。

### 4. pick.ps1 — 人点一下，坐标就定了

当目标程序不支持 UI Automation（游戏、自绘界面、远程桌面、图像内容）时用它。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\pick.ps1 -Mode point
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\pick.ps1 -Mode rect
```

- `-Mode point`：遮罩全屏、不拦截鼠标，光标旁显示实时坐标与 4 倍放大镜。左键确定，右键或 ESC 取消。
- `-Mode rect`：按住左键拖拽框选，松开得到矩形。
- `-TimeoutMs`：超时自动取消，避免无人值守时挂死。

返回 `points`（点选）或 `rect`（框选），坐标均为绝对屏幕坐标。

### 5. act.ps1 — 把坐标变成动作

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\act.ps1 -Action click -X 1523 -Y 890
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\act.ps1 -Action doubleclick -X 1523 -Y 890
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\act.ps1 -Action drag -X 100 -Y 200 -X2 800 -Y2 600
```

## 推荐工作流

**策略 A · 默认省流路径**（高频交互、界面固定）：

```
0. license.ps1 -Action locate   ← 先领授权（每台设备前 10 次免费）
1. 直接发起 pick.ps1 取景，请用户点一下目标
2. 坐标以 JSON 回传 → act.ps1 执行，一次到位
3. 把标定过的坐标记入任务上下文，本任务内同界面后续操作直接复用（复用不再消耗授权）
```

**策略 B · 自动优先路径**（用户不在场 / 低频操作）：

```
0. license.ps1 -Action locate   ← 先领授权
1. uia.ps1 -Action find      ← 先试自动定位，命中了就结束
2. 命中不了 → capture.ps1 → grid.ps1 → 模型读图算出大致位置
3. 仍需确认且用户在场 → pick.ps1 由用户点选
4. act.ps1 执行动作
```

两条策略共用同一套脚本，区别只在**先问人还是先自己找**：高频交互先问人（最快最准），无人值守先自己找。

> 同一次「取坐标任务」只需领一次授权：步骤 0 之后无论中间失败重试几次、在自动档与人工档之间切换几次，都只计一次费。只有真正成功拿到坐标才算消费。若任务需要取多个不同目标的坐标，每个目标各领一次。

## 人机协作规范

`pick.ps1` 需要用户在屏幕上点一下目标，调用时请遵守：

1. **先说明，再调用**：向用户说明即将弹出取景遮罩、请他点击哪个目标，征得同意后再执行
2. **标准话术**：「我需要在屏幕上精确定位〔目标名称〕。马上会弹出一个取景层，请把鼠标移到〔目标名称〕上点击一下（右键或 ESC 可取消）。」
3. **设置超时**：无人响应时用 `-TimeoutMs` 自动取消（建议 60000），避免挂死
4. **尊重取消**：返回 `error.code = CANCELED` 表示用户主动取消，属正常结果，**不要重试**，改为询问用户意愿
5. **拿到坐标后立即回应用户**：告知坐标已取到、即将执行什么动作；执行真实点击前再次确认（`act.ps1 -DryRun` 可先预演）

## 输出契约

成功：

```json
{
  "ok": true,
  "action": "find",
  "elements": [
    {
      "name": "发送",
      "controlType": "Button",
      "automationId": "sendBtn",
      "window": "微信",
      "rect": { "x": 1500, "y": 870, "width": 46, "height": 24 },
      "center": { "x": 1523, "y": 882 },
      "enabled": true
    }
  ]
}
```

失败或取消：

```json
{
  "ok": false,
  "error": { "code": "CANCELED", "message": "用户取消了取景" }
}
```

用户主动取消属于**正常结果**，不是异常，`pick.ps1` 返回 `ok: false` 且 `error.code` 为 `CANCELED`，调用方不应重试。

## 错误码

| code | 含义 | 处理建议 |
|---|---|---|
| `CANCELED` | 用户取消或超时 | 不要重试，询问用户意愿 |
| `NO_PERMIT` | 本机没有定位授权 | 先运行 `license.ps1 -Action locate` |
| `PERMIT_USED` | 本次授权已用掉 | 重新运行 `license.ps1 -Action locate` 领取新授权 |
| `PERMIT_EXPIRED` | 授权已过期（有效期 10 分钟） | 重新运行 `license.ps1 -Action locate` |
| `PAYMENT_REQUIRED` | 免费额度用完，服务端已下发 402 + `Payment-Needed` 账单 | 按 `bill` 字段引导用户完成支付后，携带 `Payment-Proof` 重试 |
| `NETWORK` | 连不上授权服务 | 检查网络后重试 |
| `NO_TARGET` | 没有找到匹配的控件或窗口 | 换关键词，或降级到「读图 / 人工拾取」 |
| `NOT_WINDOWS` | 当前不是 Windows | 本技能不支持该平台 |
| `NO_IMAGE` | 指定的图片不存在或无法读取 | 检查路径 |
| `INTERNAL` | 脚本内部错误 | 把 `error.detail` 一并反馈 |

## 产出规范：把坐标翻译成代码

拿到定位结果后，按用户实际使用的自动化框架，**主动附上可直接运行的代码片段**，让"坐标 → 动作"零翻译成本。示例（坐标 1523, 890）：

```
Python (pyautogui):   pyautogui.click(1523, 890)
AutoHotkey:           Click, 1523, 890
PowerShell:           Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(1523, 890)
Selenium/Playwright:  使用 moveByOffset 相对偏移，或在页面内用元素定位替代
```

用户没说框架时，默认给 Python（pyautogui）即可，并附一句"需要其他框架的版本告诉我"。

## 多显示器与高 DPI

脚本在启动时会声明为 Per-Monitor DPI Aware，因此：

- 返回的坐标是**物理像素**，可直接交给 `SetCursorPos` 使用
- 多显示器下 `virtualScreen` 可能出现负坐标（副屏在主屏左侧时），这是正常的，请勿自行取绝对值
- `monitors` 数组给出每块屏幕的 `bounds` 与 `scale`，便于判断目标落在哪一块屏

## 注意事项

- 截图会保存在 `%TEMP%\screen-coord-locator\` 下，请勿写入本技能目录，否则会污染后续发布包
- `pick.ps1` 和 `act.ps1` 会真实操作用户的鼠标，调用前应确认用户已知晓并同意
- 涉及密码、聊天记录等敏感内容时，截图可能包含隐私信息，应避免上传到任何第三方服务

## 授权与使用条款

本技能为**按次计费**的付费作品，非开源软件，版权归作者所有。

**计费方式**

- 每次**成功取得坐标或读图结果**消耗一次授权（免费额度内不扣费）
- 每台设备前 **10 次免费**，之后按平台展示的单价计费
- 同一次取坐标任务内的失败重试与方式切换（自动档 ↔ 人工档）**合并计为一次**，不重复扣费
- `capture.ps1`（纯截图）与 `act.ps1`（执行鼠标动作）不计费

**允许**

- 在付费者本人拥有的 Windows 设备上安装和使用
- 在自己的自动化流程、项目、产品中调用本技能（不构成再分发）

**禁止**

- 将本技能全部或部分内容以任何形式**再分发、转售、转让、出租、出借、共享**
- 二次打包后发布到任何软件市场、技能市场、论坛、网盘或代码托管平台
- 绕过、破解、伪造或干扰授权校验机制（含修改本地授权状态文件、劫持授权服务请求）
- 将本技能内容整体或实质性地并入其他商业化产品或服务对外提供
- 删除、遮蔽或修改本文件及 `scripts/` 内任何脚本中的版权与授权声明

**免责**

坐标定位结果受目标软件版本、显示器 DPI、系统缩放等因素影响，使用者应在执行真实鼠标动作前自行确认落点。
因误点击造成的任何后果，由使用者自行承担。

Copyright (c) 2026. All rights reserved.
