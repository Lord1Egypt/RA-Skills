# 使用手册

所有脚本统一约定：**stdout 只输出一个 JSON 对象**，人可读的提示一律不打印到 stdout。
`ok = false` 时看 `error.code` 与 `error.message`；用户主动取消（`CANCELED`）是正常结果，不要重试。

调用模板（Skill 内部统一用这一种写法，避免执行策略问题）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill目录>\scripts\<脚本>.ps1" <参数>
```

---

## license.ps1 — 申请定位授权（按次计费）

`uia.ps1` / `grid.ps1` / `pick.ps1` 这三个**会产出坐标**的脚本，每次执行前都会校验本地授权。没有有效授权时返回 `error.code = NO_PERMIT`，不会执行定位。所以取坐标前先申请：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill目录>\scripts\license.ps1" -Action locate
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `-Action` | `locate` | 动作类型，取值 `locate` / `act` |
| `-MachineId` | 本机计算机名 | 覆盖设备标识（一般不用传） |
| `-Status` | — | 只查看本地授权状态，不联网、不发起申请 |
| `-Reset` | — | 清除本地授权（用于排障） |

**返回（成功，含免费额度）**

```json
{ "ok": true, "permit": "xxx", "expiresAt": "2026-09-20T09:47:03+08:00",
  "ttlSeconds": 600, "reason": "free_quota", "freeQuotaLeft": 2, "machineId": "PC-01" }
```

**返回（需要付费，退出码 3）**

```json
{ "ok": false,
  "error": { "code": "PAYMENT_REQUIRED", "message": "本次定位需支付 0.10 CNY，请在支付宝中完成授权支付后重试" },
  "bill": { "amount": "0.10", "currency": "CNY", "goodsName": "屏幕坐标定位·单次授权",
            "outTradeNo": "ORDER_1789867998989_61ef1000", "payBefore": "2026-09-20T09:38:18+08:00",
            "resourceId": "coord://locate/locate", "serviceId": "API_xxx", "sellerId": "2088xxx" } }
```

**拿到 `PAYMENT_REQUIRED` 时对用户这么说**（照抄即可，不要自行编造价格）：

> 这台设备的 10 次免费定位已用完。这次定位需要支付 **0.10 元**（订单号 `ORDER_xxx`，请在 `payBefore` 之前完成）。
> 支付完成后告诉我，我立刻继续取坐标。**在您确认支付之前，我不会执行任何定位动作。**

然后等用户明确回复已支付，再重新执行一次 `license.ps1 -Action locate`。

**计费规则（务必让用户知晓，避免争执）**

- 一次授权 = 一次**成功**定位：脚本失败（如 `NO_TARGET`）或用户取消（`CANCELED`）都不计费，可在同一次授权内继续重试或换档降级
- 一旦某个脚本成功返回坐标，本次授权即被消费，下一次取坐标需重新申请
- 授权有效期 **10 分钟**，过期需重新申请（未成功定位则不扣费）
- `capture.ps1`（纯截图）与 `act.ps1`（执行鼠标动作）**不计费**

```powershell
# 查看当前授权状态（不联网）
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill目录>\scripts\license.ps1" -Status
# {"ok":true,"hasPermit":true,"permit":"T-BqdPXX...","consumed":false,"secondsLeft":593,"usable":true}
```

---

## capture.ps1 — 截图

| 参数 | 默认 | 说明 |
|---|---|---|
| `-Mode` | `full` | `full` 整个虚拟屏幕 / `monitor` 单块屏 / `region` 指定区域 / `window` 指定窗口 |
| `-Monitor` | `0` | `monitor` 模式下选择第几块屏，顺序见返回的 `monitors` |
| `-X -Y -W -H` | `0` | `region` 模式的区域，**绝对屏幕坐标** |
| `-WindowTitle` | 空 | `window` 模式的标题模糊匹配 |
| `-Out` | 自动 | 输出路径，默认写到 `%TEMP%\screen-coord-locator\` |
| `-Format` | `png` | `png` / `jpg` |
| `-Scale` | `1.0` | 缩放倍率，截图很大想省 token 时可设 `0.5` |

**关键返回字段**

- `image.path` — 底图路径
- `origin.x / origin.y` — 这张图左上角对应的绝对屏幕坐标
- `virtualScreen` — 多屏拼接范围，副屏在主屏左侧时 `x` 为负，这是正常的
- `monitors[]` — 每块屏的 `bounds`、`dpi`、`scale`

**换算规则**：`屏幕坐标 = 图内像素坐标 + origin`

---

## grid.ps1 — 叠加坐标标尺

| 参数 | 默认 | 说明 |
|---|---|---|
| `-Image` | 必填 | 要叠加的底图路径 |
| `-Spacing` | `100` | 细网格间距（像素） |
| `-MajorEvery` | `5` | 每 N 格一条粗线并标数字 |
| `-OriginX -OriginY` | `0` | 底图左上角对应的屏幕坐标，传 capture 返回的 `origin` 即可 |
| `-NoLabels` | 关 | 不画数字标签 |
| `-MaxLabels` | `400` | 标签数量上限，防止图上糊满数字 |

返回的 `image.path` 是叠加后的图，标签上写的**已经是绝对屏幕坐标**，模型读图后不需要再做加法。

给模型的推荐提示词：

> 这张截图带有坐标标尺，顶部和左侧的数字是该列/该行的绝对屏幕坐标。
> 请先读出目标元素左右两条相邻刻度，再用插值估算它的中心点，最后只输出 JSON：`{"x":..,"y":..}`

---

## uia.ps1 — 控件树自动定位（优先用这个）

| 参数 | 说明 |
|---|---|
| `-Action windows` | 列出当前可见的顶层窗口；加 `-Handle` 只返回该窗口 |
| `-Action find` | 在前 `-MaxWindows` 个窗口里检索控件，配合下面的过滤参数 |
| `-Action tree` | 展开指定 `-Handle` 的窗口控件树 |
| `-Action point` | 反查：这个坐标上是什么控件 |
| `-NameContains` | 名称模糊匹配，如 `-NameContains 发送` |
| `-TypeContains` | 控件类型，如 `Button`、`Edit`、`MenuItem` |
| `-AutomationIdContains` | 按开发者的控件 ID 匹配，最精确 |
| `-Handle` | 指定窗口句柄；`tree` / `windows` 模式都生效（句柄不存在返回 `NO_TARGET`） |
| `-X -Y` | `point` 模式指定坐标 |
| `-MaxDepth` | 遍历深度，默认 6 |
| `-MaxElements` | 遍历上限，默认 600，防止在大程序上卡死 |
| `-IncludeOffscreen` | 连最小化/隐藏的元素也返回 |

> 注意：`find` / `tree` 一旦使用了 `-NameContains` / `-TypeContains` / `-AutomationIdContains`，**顶层窗口也要通过同样的匹配**才会出现在结果里，否则会混入所有无关窗口。不带任何过滤条件时是完整枚举，行为不变。
>
> `find` 指定了过滤条件却零命中时返回 `NO_TARGET`（不是空数组），且**不消耗本次授权**——可以换个关键词用同一份授权继续检索。

**返回字段**

- `rect` — `{x, y, width, height}`，绝对屏幕坐标
- `center` — 直接可点的中心点
- `usable` — `false` 表示这是最小化或已隐藏的窗口，坐标无效
- `process` — 所属进程名，用来确认找对了程序

**典型调用**

```powershell
# 第一步：先看看现在有哪些窗口
uia.ps1 -Action windows

# 第二步：在微信里找"发送"按钮
uia.ps1 -Action find -NameContains "发送" -TypeContains Button

# 反查：鼠标当前指的这个点是什么控件
uia.ps1 -Action point -X 1523 -Y 890
```

**限制**：游戏、自绘界面、部分 Electron 应用的内部网页内容不暴露 UI Automation 树，
这类目标 `find` 会落空，此时降级到「capture + grid 读图」或「pick 人工点选」。

---

## pick.ps1 — 人工点选 / 框选

| 参数 | 默认 | 说明 |
|---|---|---|
| `-Mode` | `point` | `point` 点选一个点 / `rect` 拖拽框选一个矩形 |
| `-TimeoutMs` | `0`（不限） | 超时自动取消，**无人值守场景务必设置** |
| `-MagnifierSize` | `205` | 放大镜边长（像素） |
| `-MagnifierZoom` | `5` | 放大倍率 |
| `-NoVeil` | 关 | 不加半透明遮罩，屏幕保持原样 |
| `-AllowRightClickPick` | 关 | 右键也当作确定（目标是右键菜单时用） |

交互：左键确定；右键或 ESC 取消；`rect` 模式按住左键拖拽。

**注意**：启动瞬间会先抓一张桌面底图给放大镜用，所以放大镜显示的是启动那一刻的画面。
如果用户中途切换了窗口，放大镜里的内容不会跟着变，但坐标读数始终是实时的。

---

## act.ps1 — 执行动作

| 参数 | 说明 |
|---|---|
| `-Action` | `move` / `click` / `doubleclick` / `rightclick` / `middleclick` / `drag` / `wheel` |
| `-X -Y` | 目标坐标（绝对屏幕坐标） |
| `-X2 -Y2` | `drag` 的终点 |
| `-WheelDelta` | 滚轮量，默认 `-120`（向下滚一格），正值向上 |
| `-HoldMs` | 按下到抬起间隔，默认 30ms |
| `-Steps` | `drag` 的插值步数，默认 12 |
| `-DryRun` | 只校验不真的动鼠标 |

**真实点击前务必先确认**：`act.ps1` 会真的动用户的鼠标，调用前要么由用户明确发起，
要么先用 `-DryRun` 验证参数。

---

## 三种定位方式的取舍

| 场景 | 用哪个 |
|---|---|
| 目标是标准按钮 / 输入框 / 菜单 | `uia.ps1 -Action find` |
| 目标是网页内容、图片里的一块 | `capture` → `grid` → 模型读图 |
| 目标是游戏、自绘控件，或要求零误差 | `pick.ps1` 让用户点一下 |
| 找到了坐标，要真的点下去 | `act.ps1` |
| 想知道某个坐标上是什么 | `uia.ps1 -Action point` |

## 常见问题

**坐标总差一截？**
几乎都是 DPI 缩放造成的。本技能已声明 Per-Monitor DPI Aware，返回的是物理像素。
如果你的下游工具用的是逻辑像素，需要乘以 `monitors[].scale`。

**副屏在左边，坐标是负的？**
正常。虚拟屏幕以主屏左上角为原点，副屏在左侧时 x 为负，直接把负数交给 `SetCursorPos` 即可，**不要取绝对值**。

**`find` 找不到明明就在眼前的按钮？**
先 `-Action windows` 确认窗口是不是 `usable=false`（被最小化了）；再确认目标程序是否暴露 UIA 树。
都不行就走 `capture + grid` 或 `pick`。

**截图文件堆积？**
都在 `%TEMP%\screen-coord-locator\`，定期清空即可，不影响本技能运行。
