# 窗口、控件与浏览器操作

平台 Agent 通过屏幕自动化小助手桌面端增强屏幕理解、控制和自动化执行能力，本参考说明当前任务的操作方法。
账号登录、授权、凭据输入、支付和其他高风险操作
由用户在场完成；CLI、SDK 及外部工具均遵守 Skill 主入口的交接边界。

常用原生命令形态：

```text
cli task begin [--handle <窗口句柄>]
cli task observe
cli task find --text <文字>
cli task wait --text <文字> --timeout <秒> --interval <秒>
cli task click --point <x,y> --button left
cli task write --text <文字> --interval <秒>
cli task scroll --point <x,y> --amount <数值> --direction up|down|left|right
cli task hotkey <按键...>
cli task end
```

当 `cli capabilities` 列出 `ui.semantic-action` 时，标准桌面控件优先使用无障碍原生动作：

```text
cli ui act invoke --role button --name <名称>
cli ui act set-value --role text_field --name <名称> --value-stdin
cli ui act toggle --role checkbox --name <名称>
cli ui act select --role list_item --name <名称>
```

流程程序扩展使用对应的 `ctx.ui.invoke(...)`、`ctx.ui.set_value(...)`、`ctx.ui.toggle(...)`、
`ctx.ui.select(...)`，不得从扩展中启动 CLI。

只对当前已确认窗口中唯一、可见、启用且支持相应 UIA/AX 模式的控件使用。按钮和菜单用 `invoke`，
输入框用 `set-value`，复选框/开关用 `toggle`，列表、单选项或标签用 `select`。敏感值不得放入命令行；
密码控件不通过该普通接口写入。`verified: true` 只表示控件自身状态已按预期变化；`invoke` 返回
`requires_post_verification: true` 时必须重新读取页面、UIA、OCR 或屏幕状态确认业务结果。目标不唯一、
模式不支持或验证失败时，回到本次观察得到的坐标并使用鼠标键盘操作，禁止猜测或无限重试。

跨应用任务可在用户授权范围内直接启动应用，再确认新窗口；锚定窗口只是第一个坐标锚点，不是
全程限制：

```text
cli application launch --name "微信"
cli file open --path "C:\Users\用户\Documents\报告.docx"
cli window wait-selection --title "微信" --timeout 30
cli window activate --target <target_id>
cli window arrange --handles <handle1> <handle2> --layout columns
```

调用前必须确认 `cli capabilities` 列出 `application.launch` 和任务所需窗口动作。流程语言中优先
使用 `应用`、`找不到时：启动应用`、`打开应用【名称】`、新窗口登记和命名操作区域；执行到哪个
操作区域，底座就激活其绑定窗口。窗口允许重叠，也可排列，不得把锚定窗口误解为全流程排他锁。
`应用` 直接写为 Windows `.exe` 文件名且没有另写 `首选进程` 时，该文件名是严格进程条件；不得用
标题相同的其他应用窗口代替。纯浏览器增强步骤可以省略 `在`，因为它操作受管会话对象；普通
Chrome/Edge 窗口即使标题相同，也不能被当作已经打开的受管浏览器会话。
流程主动打开并登记的新应用窗口默认继承锚定窗口的位置和大小；受管浏览器窗口创建后也由底座
强制应用该区域。只有流程显式排列窗口或指定其他布局时，才覆盖这个默认摆放。
用户给出本地文档路径并要求打开时，若能力清单包含 `file.open`，直接使用
`cli file open --path <路径>`；流程使用 `打开文件【参数【文档路径】】`，程序扩展使用
`ctx.app.open_file(path)`。这三个入口都要求现有本地文件并使用系统默认关联应用，不使用 shell；
流程声明“读取文件、控制应用”，日志和结果不得记录完整路径。不要再用 Ctrl+O 和模拟输入绕行。
`打开浏览器会话` 步骤中的浏览器元素观察由底座延后到会话创建后作为就绪检查；不得在会话尚未
创建时先调用 `browser locate`。纯浏览器观察/验证步骤同样不要求桌面操作区域。
网页可见文字条件使用 `浏览器出现文字【文字】`，不要把普通文字写进 `浏览器出现元素【CSS selector】`。
登录或验证需要用户操作时使用 `失败：等待用户继续`；底座暂停并显示等待状态，用户点击主界面现有
“继续”按钮后立即复检，未满足则再次等待。
需要自动检测时使用 `失败：等待用户继续；10秒重试`；底座每 10 秒自动复检，用户点击“继续”可
提前唤醒。所有普通页面文字条件都必须使用文字语法，不能写进元素 selector。

浏览器增强提供独立的顶层 CLI，适合 Agent 完成一次性网页任务；命令和参数必须以当前
`browser --help` 与能力返回为准：

```text
browser status
browser open chrome|edge [--url <http/https URL>]
browser navigate --browser chrome|edge <http/https URL>
browser auth-status --browser chrome|edge
browser probe --browser chrome|edge --task-kind READ|LOCATE|ACT|FILL|SELECT|DOWNLOAD|VERIFY
browser outcome --browser chrome|edge --decision USE_DOM|ENHANCE_DOM|EXIT_DOM --task-kind <类型> --result success|failure [--verified] [--failure-type <类型>]
browser locate --browser chrome|edge [--selector <CSS>] [--match-text <文字>] [--limit <数量>] [--strategy-id <Probe 返回值>]
browser read|click|fill|select-text|copy|scroll|press|verify|download --browser chrome|edge ...
browser close chrome|edge
```

同一网页任务只在首次需要受管浏览器时执行一次 `browser open`，后续每一轮观察、操作和验证即使由
不同 CLI 进程执行，也必须通过同一个 `--browser chrome|edge` 复用该受管会话。不得把步骤包装成
`open → navigate/read/locate → close`，不得在每轮决策前再次 `open`，也不得由 Agent 自行使用
`browser open --new`。只有收到 `browser_session_expired` 时才允许重新 `open` 一次；收到
`browser_session_not_open` 时先执行 `browser status` 并报告状态，禁止无限重试。任务完成、失败或用户
停止时默认保留浏览器现场；只有用户要求关闭或流程明确声明关闭时才执行一次
`browser close chrome|edge`。除非用户明确要求结束整个浏览器增强服务，否则不加 `--stop-daemon`。

用户给出网址时直接执行一次 `browser open chrome|edge --url <网址>`，让小助手创建或复用受管会话并
进入页面。若结果为 `status=waiting_for_user`、`reason=login_required`，立即暂停网页操作，保留当前会话，
请用户在场亲自完成登录或身份验证。即使用户提供了凭据，也不代填、不记录、不继续截取凭据区域。
用户完成后执行 `browser auth-status --browser chrome|edge`，返回 `status=ready` 后再继续原会话。
受管 Profile 可保留网站登录状态；网站也可能使登录过期，按实际状态再次交接给用户。

`browser probe` 是浏览器增强组件内部的 **DOM 网页操作能力探测器**，只用于减少 Agent 在无效 DOM
路线上的试错。只有浏览器增强的动作契约与访问状态均有效、受管会话已打开且登录检查为 `ready` 时
才调用；没有安装、授权或启用浏览器增强时不得调用，也不得影响 OCR、UIA、鼠标键盘或普通屏幕自动化。
基础屏幕路径不需要、也不等待 DOM 能力探测。

需要 DOM 定位、结构化读取或页面操作时，在当前页面按任务类型调用一次 `browser probe --task-kind ...`。
域名 Profile 只分别记录 DOM 的读取、定位、操作和验证倾向，且只是弱先验；当前页面结果始终优先：
`USE_DOM` 使用普通 DOM；`ENHANCE_DOM` 只启用 Probe 明示的 iframe、Shadow DOM 等增强；`EXIT_DOM`
只表示停止 DOM 路线。收到 `EXIT_DOM` 后由 engine / Agent 根据任务、现场证据和可用能力，在 UIA、OCR、
CV、VLM 中选择理解方式，在 UIA Action 或 Mouse + Keyboard 中选择操作方式，再重新观察并验证。
Probe 不替 engine / Agent 选择非 DOM 路线，也不是新的执行者。
普通 `browser locate`、`ctx.browser.locate(...)` 和底层 `object.locate` 永远是直接定位，不受 Probe 的次数或
时间预算限制。只有 Agent 决定采用 Probe 策略，并显式传入 Probe 返回的 `strategy_id` 时，才使用
`browser locate --strategy-id ...` 或 `ctx.browser.locate_with_strategy(..., strategy_id=...)` 获取结构化策略状态。

Probe 会为 Agent 建立一个可选的 DOM 策略会话；只有显式携带 `strategy_id` 的策略定位计入同一目标最多
三次、总计约十秒的预算，所有普通定位原语都不承担全局重试策略。元素暂未加载可以有界 Retry；持续找不到、Canvas、DOM
不稳定、元素不可可靠操作、动作无响应或验证失败必须按结构化结果执行 `EXIT_DOM`，禁止换写法无限重试。
每个页面动作仍须重新观察并验证；只有验证通过才用 `browser outcome ... --result success --verified`
更新 Profile。动作返回成功但页面未达到目标状态时，记录 `--result failure --failure-type VERIFY_FAILED`。
Profile 只能保存域名级能力倾向，不保存 URL 路径、selector、XPath、坐标或具体操作步骤；连续失败应
降低置信度并允许旧 Profile 失效。切到屏幕路径后继续遵守观察—操作—验证规则。

`locate` 可用 `--limit` 限制候选数量；后续读取或操作在未提供已定位对象时必须匹配唯一目标，相关命令
明确支持 `--index` 时才可从多个候选中选择。`verify` 接受动作与期望 JSON。
浏览器接口报组件不可用时，保留诊断并按组件界面提示处理，不绕过检查或自行启动 Sidecar。

具体参数仍以 `cli capabilities` 为准。横向滚动必须使用 `--direction left|right`，不得以
`Shift+滚轮` 假冒。事件发送后若画面未变化，按 `no_change` 处理。

## 浏览器增强的就绪检查

可选能力的通用前提遵循 [Skill 主入口](../SKILL.md)；浏览器增强另需确认以下会话与动作条件。
普通窗口可直接使用屏幕/UIA，需要 DOM 时复用小助手的受管 Profile。

浏览器增强启动的是正常浏览器窗口，必须保留地址栏，供用户确认当前网址、登录状态和页面范围；只有“帮助中心”信息窗口可以使用无地址栏的应用窗口。若浏览器增强窗口没有地址栏，停止操作并报告启动配置异常。

浏览器增强开始前必须同时满足两项：`cli capabilities` 列出 `workflow.browser-enhancement@1`，且
`cli access list` 中 `browser_enhancement.status.effective` 为 `true`。前者证明当前桌面版本公开了
`ctx.browser` 动作契约，后者同时核对授权、组件安装、平台可用性和启用状态。只满足其中一项不能运行。
访问状态无效时，按 `reason` 和 `action` 解释未授权、未安装、不可用或未启用，并按界面引导配置。

开发、修改或验收浏览器增强流程时，还必须完整读取
[浏览器增强测试标准](browser-enhancement-testing.md)，按任务涉及的层级记录实际执行、跳过项和
证据；静态校验、隔离 Sidecar、正式在线组件和真实业务页面是不同验收层，不能互相代替。
