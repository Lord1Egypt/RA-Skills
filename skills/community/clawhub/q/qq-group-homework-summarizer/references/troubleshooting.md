# 故障排查与逆向记录

## 1. `browser_start_session` 必然失败 —— 会话协议跨代不兼容

> ⚠️ **版本分界（2026-11-10 补充）**：本节结论只适用于 **CLI 1.5.4 + 旧版扩展**。
> **1.6.x 起已改为会话模型**：`get_session_id` 只 mint 一个 `T-xxxx` 令牌，
> 必须紧接着 `browser_start_session --sessionId <令牌>` 建会话，否则
> `browser_go_to_url` / `browser_eval_content_js` 会报
> `Session "T-..." does not exist or has been released`。
> 本 skill 的 `qq_hw.py` 已自动处理；旧版「跳过建会话」的做法不要再用于新版。

### 现象
```
qqbrowser-skill browser_start_session --sessionId task-xxx
→ 无输出，退出码 1
```

### 根因（已逆向确认）
- CLI 1.5.4 的 `start_session` 走 **type 协议**：
  `{"type":"start_session","sessionId":...,"callPlatform":"win","callMode":"normal"}`
- QQ 浏览器 21.7.7001.400 内置扩展**只支持 `actionName` + `actionParams` 业务命令**，
  且**完全没有会话生命周期**（扩展源码里搜不到 `start_session`）。
- 扩展收到 type 协议消息后取不到 `actionParams` → `JSON.parse(undefined)` →
  回包 `{'actionResult': 'executeCommand error: Invalid JSON format in command: undefined'}`

### 解法
**绕开会话层，直接调业务命令**（`browser_go_to_url` / `browser_eval_content_js` / `browser_screenshot`）。
业务命令用 `actionName+actionParams`，扩展能正常处理。

### 如何自行验证扩展协议
解包扩展 CRX（它是 zip，从 `PK\x03\x04` 处切分即可）：

```python
raw = open(crx,'rb').read()
zf = zipfile.ZipFile(io.BytesIO(raw[raw.find(b'PK\x03\x04'):]))
```

自动化扩展路径：
`<QQ浏览器安装目录>/<版本>/Extensions/aaplhnhcdcgkjbijfkjdbfmiagjojdjf.crx`
→ `assets/background.js`，搜 `actionParams` / `executeCommand` 即可看到协议解析逻辑。

## 2. pip 镜像滞后（表现为版本诡异地低）

### 现象
```bash
pip index versions qqbrowser-skill   # 显示 LATEST: 1.5.3  ← 镜像滞后
```
实际 pypi.org 上是 1.5.4。版本落后会直接导致协议不匹配（见 §1）。

### 正确安装流程（先比对版本 → 按结果选源 → 失败回退阿里云）
```bash
# ① 官方源最新版
pip index versions qqbrowser-skill --index-url https://pypi.org/simple
# ② 本地镜像源版本
pip index versions qqbrowser-skill
```
- 两源**一致** → 用本地镜像源（更快）：`pip install --upgrade qqbrowser-skill`
- **不一致** → 用官方源：`pip install --index-url https://pypi.org/simple --upgrade qqbrowser-skill`
- 安装**失败** → 改用阿里云镜像源：`pip install --index-url https://mirrors.aliyun.com/pypi/simple/ --upgrade qqbrowser-skill`

## 3. 解析 CLI 输出：双重 JSON 转义

`browser_eval_content_js` 的返回被嵌在 CLI 的 `actionResult` 字符串里，
**引号被转义成 `\"`，换行被转义成 `\\n`（三层）**。

正确提取（见 `scripts/qq_hw.py` 的 `extract_result`）：
1. 定位 `"Result: "` 之后、`">>>>>"` 之前的内容
2. `json.loads('"' + chunk + '"')` 解第一层
3. 若仍失败，退回 `replace('\\"','"').replace('\\\\','\\')`

⚠️ **不要用** `encode().decode('unicode_escape')` —— 它会把 UTF-8 中文当 ASCII 处理，产生乱码。

⚠️ 注意 CLI 输出里有**两个** `Result:`：
- `Action result: ... Result: <你的 JS 返回值>` ← 要这个
- `Action Result: No page navigation triggered.` ← 不要这个（`"Result: "` 会误匹配）

## 4. Word COM 统计页数的坑

```powershell
$doc.ComputeStatistics(2)   # 2 = wdStatisticPages
```

三个坑：
1. **中文文件名可能干扰 COM** → 先 `Copy-Item` 到 ASCII 临时路径再打开
2. **catch 里再调 `$word.Quit()` 会抛 RPC 错误并覆盖真实异常** → 先记录异常再 Quit
3. 残留的 `winword.exe` 进程会让后续调用失败 → 必要时 `Stop-Process -Name winword -Force`

## 5. PowerShell 工具不回传 stdout

本环境下 PowerShell 工具的 stdout 不显示。**一律让脚本把结果写入文件**，再用 Read 读取。

## 6. 单页约束为什么这么难

`Heading 2` / `List Number` 样式自带 `space_before/after` 和 **1.15 倍行距**，
在段落级别设 `space_after=0` 压不住，必须改**样式本身**：

```python
st = doc.styles['Heading 2']
st.paragraph_format.space_before = st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing = 1.0
```

再加上：页边距 0.8cm、表格单元格边距清零（`w:tblCellMar` 全设 0），才压得进一页。

## 7. 图片体积

原图可能高达 8192×6144。用 PIL 压到长边 1400px / quality 82，
docx 从 **2.75MB → 0.6MB**，视觉无损。

## 8. 沙箱

浏览器自动化必须 `dangerouslyDisableSandbox: true`，否则：
```
[safe-delete][SAFE_DELETE_FAIL_CLOSED] reason: windows-sandbox-recycle-bin-unavailable
```
该告警本身通常无害（`serve --daemon` 带此告警仍能启动成功），
但 `browser_start_session` 遇到它会直接退出。

## 9. 详情接口偶发 `retcode:2001`（`ptlogin-ex verify fail`）—— 列表接口已含完整文本

### 现象
`day` 子命令调 `get_hw_detail.fcg` 时，部分（或全部）作业返回：
```json
{"retcode":2001,"msg":"ptlogin-ex verify fail[filter]. uin:xxxx"}
```
而列表接口 `get_hw_list.fcg`（`cmd=21`）始终正常。bkn 从 `performance.getEntriesByType('resource')` 能正常探到，说明是**详情接口的二次风控**，不是 bkn 失效。

### 关键事实
**列表接口返回的 `content.c[]` 已包含完整的 `str` 文本**（标题、科目、正文都齐），
只有 `img` 类型会缺 `url`（图片 URL 仅在详情接口里）。所以纯文本作业理论上可用列表文本，
但**仍优先引导登录**——否则含图作业会丢图、生成残缺文档。

### 根因（已完全查清，见 §11）

有两种成因，先分辨再处理：

1. **尚未在 https://qun.qq.com/#/login 完成登录** → 详情接口的 ptlogin-ex 校验失败；
   列表接口校验较松故仍可用。
2. **已登录，但 `bkn` 缓存过期**（重新登录后 skey 变了、`qq_hw.json` 里还是旧值）
   → 重探一次 bkn 即可，**不要让用户重复登录**。

> 早期笔记里「是详情接口的二次风控，不是 bkn 失效」的说法**不准确**，已废弃。

### 解法（已合入 `scripts/qq_hw.py`）
- `cmd_list` / `cmd_day` 检测到 `retcode==2001` 或返回含 `verify fail` 时，调 `_prompt_login()`：
  自动 `browser_go_to_url` 打开 `https://qun.qq.com/#/login`，并打印醒目提示让用户点击「登录」，返回码 2。
- **不再静默回退**：未登录时直接提示登录，不生成残缺文档；用户登录成功后重跑命令即可。
- `build_docx` 仍对缺 `c` 字段的条目做 `.get("c", [])` 容错，避免异常数据 KeyError。

## 10. docx → PDF（Word COM）的中文路径坑

### 现象（四个坑，逐个踩过）
1. 直接 `SaveAs` 到**中文路径** → Word COM **静默吞掉**，文件没生成也不报错
2. 用 `$env:TEMP` 当临时目录 → 它返回 `HANLEY~1` 这类 **8.3 短路径**，`SaveAs` 报
   「值不在预期的范围内」
3. 中文路径经 `powershell -File x.ps1 -Docx <中文路径>` **命令行参数传递** →
   被按系统编码解码成乱码，`Documents.Open` 找不到文件（表现为 `SAVE_FAIL` / rc=3）
4. here-string 写成**单行** `@'...'@` → 报 `UnexpectedCharactersAfterHereStringHeader`
   （here-string 的结束符必须独占一行，不能单行闭合）

### 解法（已合入 `cmd_pdf`）
1. 路径**不作为命令行参数传递**，而是作为**字面量写入 UTF-8 BOM 的临时 ps1**
   （`_conv_pdf_run.ps1`）；PowerShell `-File` 读文件时按 UTF-8 正确解码中文
2. 路径用**普通单引号**包裹，不要用 here-string
3. `SaveAs` 到**项目目录下的 ASCII 临时名** `_tmp_conv.pdf`（避开 8.3 短路径与中文名），
   再 `Copy-Item` 回中文名
4. `$w.Quit()` 放 `finally` 并吞掉 RPC 异常（`0x800706BE` 无害，不影响产物）

### 页数校验
PDF 由 docx 转出，二者分页一致 —— 用 `pages` 子命令校验 **docx** 为 `PAGES=1` 即可，
PDF 必然也是单页。

> 更快的校验方式（无需 Word）：用 `pypdf` 直接读 PDF 页数与文本，
> 既验证页数也验证内容完整：
> ```python
> from pypdf import PdfReader
> r = PdfReader('作业_<日期>.pdf'); print(len(r.pages), r.pages[0].extract_text()[:400])
> ```

## 11. 登录态三态判定（2026-09-01～09-03 高频踩坑）

`verify fail` 有**两种不同成因**，处理方式完全不同，必须先分辨再动手。详见 SKILL.md
「登录态：三态判定与恢复」章节。这里只记录排查命令与判读细节。

### 排查顺序

```bash
# ① 接口侧（失败先重试一次，排除偶发抖动）
python scripts/qq_hw.py day <日期> --refresh

# ② 浏览器侧 —— 区分「没登录」和「已登录但 bkn 过期」的唯一可靠依据
qqbrowser-skill browser_go_to_url --url "https://qun.qq.com/#/login"
qqbrowser-skill browser_eval_content_js --script "document.body.innerText.slice(0,300)"
```

### innerText 判读

| 返回 | 含义 |
|------|------|
| `QQ群\n\nQQ登录` | **未登录** → 引导用户登录，登录后**先重探 bkn** 再拉数据 |
| 跳转到 `#/member-manage/base-manage`，带昵称 +「退出」 | **已登录** → 只需重探 bkn |

### 为什么要重探 bkn

`qq_hw.json` 缓存着旧会话的 bkn，重新登录后 skey 变了但缓存没刷新，
此时接口照样报 verify fail。**重探后 bkn 数值会变化**（实测两次取值不同）。

### 失效规律

- 一天内可失效多次（09-02、09-03 均出现「15 点失效 → 16 点自愈」）
- 也会中途掉线（09-03：16:17 正常 → 17:19 失效 → 重新登录后 18:08 正常）
- → 定时任务的**每一轮都必须重新校验**，不能沿用上一轮结论

## 12. MCP 工具延迟注册：模糊搜索搜不到 `mcp__agent-mail__*`

### 现象（2026-09-02 16:23 误判）

```
ToolSearch(queries=["send email", "agent mail"])   → 只返回 agent_mail_upload_attachment
                                                      / agent_mail_download_attachment
DeferExecuteTool("mcp__agent-mail__SendMessage")   → not found
```
据此得出错误结论「本次会话没有发信工具」，导致发送失败、白跑一轮。

### 根因

MCP 工具是**按需延迟注册**的。`ToolSearch(queries=[...])` 的模糊索引只覆盖**内置 deferred 工具**，
搜不到 `mcp__agent-mail__*` 这类 MCP 工具。

### 解法

用 **`tool_names` 精确名**加载，一次就能拿到完整 schema：

```
ToolSearch(tool_names=["mcp__agent-mail__SendMessage", "mcp__agent-mail__GetMe"])
```

### 相关教训

不要因为工具「找不到」就去 `app.asar` 里翻 HTTP 端点 ——
本机没有承载这些连接器的本地 HTTP 服务，纯属浪费时间。

### 🆕 缺席是「按轮次」的，不是服务没启用（2026-09-04 完整复盘）

同一台机器、同一任务：

| 时间 | 现象 |
|------|------|
| 17:00 | `SendMessage` 完全搜不到，附件已上传 → 发送失败 |
| 17:30 | 复探仍然搜不到（精确名 / 变体名 / 模糊都试过），确认非偶然 |
| 17:41 | 用户**新开一轮对话**后精确名 ToolSearch **立刻命中**，补发成功 |

期间 `~/.workbuddy/mcp.json` 自始至终没有 agent-mail 条目，但连接器状态一直显示 connected。
→ **MCP 工具随会话动态注册；`mcp.json` 里查不到 ≠ 没启用。**

因此无人值守时的正确应对：

1. 先探发信工具；探不到 → **产物落盘 + 告警 + 结束本轮**
2. 等下一轮调度自动重试，或等用户介入（新开一轮通常就好）
3. ❌ 不判定「服务未启用」 ❌ 不改 `mcp.json` ❌ 不自建 HTTP 绕过 ❌ 不反复重试

### SendMessage 参数坑

| 参数 | 坑 |
|------|-----|
| `to` | 是**对象数组** `[{"email": "..."}]`，不是字符串数组 |
| `body` | **不能传空字符串**（报 40001 校验失败），想留空就传**一个空格** |
| `skip_confirmation` | 已预先授权的场景传 `true`，否则返回 `CONFIRMATION_REQUIRED` |

### 回退通道状态

`wecom-cli mail send` **长期**返回 **850003（机器人「邮件」权限过期）**
（2026-09-02 起连续多日未恢复）。注意这与「消息」权限是两套，**消息能发不代表邮件能发**。
→ **不要把它当兜底通道**：失败时最多试一次确认状态，随即转「告警 + 等下一轮」。
优先走 Agent Mail。

## 13. 定时任务运维

### 🚩 rrule 平台限制：一条规则只能表达一个「HH:MM」

`BYHOUR` / `BYMINUTE` **只接受单个整数**，传逗号列表直接报
`BYHOUR must be an integer between 0 and 23` / `BYMINUTE must be an integer between 0 and 59`；
**只有 `BYDAY` 支持列表**。

❌ 下面这条**看着合理但平台不接受**（早期笔记里出现过，已废弃）：

```
FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15,16,17,18;BYMINUTE=0,30
```

❌ `FREQ=HOURLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR;BYMINUTE=0,30` 是**工作日全天 24h 每半小时**
（48 次/天）。只在 15:00-18:30 干活的话约 40 次空转。

✅ 一个时间点一条 automation，例如 8 条覆盖 15:00/15:30/…/18:30：

```
FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15;BYMINUTE=0
FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15;BYMINUTE=30
...
```

> 拆多条时把**最关键那轮沿用原 automation id**（历史运维上下文绑在 id 上），其余新建。
> 每条 prompt 必须**自包含**，环境要点（解释器/CLI 绝对路径、打印邮箱、bkn 处理）要写全。

### 产物复用：别每轮都重做

上一轮生成过 `作业_<日期>.docx` / `.pdf` 就直接复用发送，**不要重新拉数据重生成**。
重跑 `day --refresh` 还会覆盖 `hw_day_<日期>.json`，把手动补录的条目冲掉。

### 卡在发信时：一轮只探一次

`mcp__agent-mail__SendMessage` 缺席是**按轮次**的（见 §12），一轮里反复重试不会让它出现。
探测不到 → 产物落盘 + 告警 + 等下一轮，停手。

### 幂等标记

发送成功后立即写 `hw_auto_sent_<日期>.flag`；下一轮开头检查到就跳过。
**两条邮件通道都失败时绝不写标记**，否则当天再也发不出去。

### 企微推送兜底

`sessions list` 常年返回 `sessions_count: 0`，找不到目标会话时，
用 `wecom-cli identity whoami` 的**授权真人用户 ID** 作为 `chat_id` 发给用户本人。
`wecom-cli` 报 850003 时如实报告，不要用 curl / Python 绕过。

### 老师用「消息」布置作业

接口只能拉到「群作业」，用普通消息布置的科目拉不到 → 手动补进 `hw_day_<日期>.json`
（补完**不要再跑 `day --refresh`**，否则被覆盖）。细节见 SKILL.md 步骤 3。

## 14. CLI 被服务端强制下线：`blocked until you upgrade`（2026-09-04）

### 现象

所有浏览器子命令（含 `status`）都返回：

```
❌ Browser skill commands are blocked until you upgrade
```

### 为什么危险

症状与「扩展协议不兼容」（§1）和「未登录」（§11）**高度相似**，
极易把整轮定时任务耗在查扩展、或让用户反复登录上——实际跟这两者都无关。

### 解法（三步，缺一不可）

```bash
pip install --index-url https://pypi.org/simple --upgrade qqbrowser-skill   # ① 官方源，镜像滞后装完还是旧版
qqbrowser-skill stop                                                        # ② 旧 daemon 仍在跑旧代码
qqbrowser-skill serve --daemon                                              # ③ 重启
```

`scripts/qq_hw.py` 已在 `_run()` 里内置检测：命中该提示会直接打印上述指引并以退出码 3 结束，
不会让你误判成未登录。

### 升级后的新现象：`Connected clients` 恒为 0

1.5.6 的 `status` 里连接数统计不准，**但业务命令照常可用**。
→ **不要死等 `clients ≥ 1`**，直接跑一次业务命令（或 `doctor`）验证连通性。
（早期笔记里「等 clients≥1 再探测 bkn」的说法在 1.5.6 上会导致永久卡住，已废弃。）

## 15. 用错解释器：`ModuleNotFoundError: No module named 'docx'`

### 现象

`bkn` / `list` / `day` 都正常，一到 `docx` 就报缺 `docx` / `PIL` 模块，
但明明 `pip install python-docx pillow` 装过。

### 根因

依赖装在**隔离 venv** 里，而命令用的是 **base 解释器**。两者是不同环境：

| 解释器 | python-docx / pillow / pypdf |
|--------|------------------------------|
| `.../python/versions/3.13.x/python.exe`（base） | ❌ 全都没有 |
| `.../python/envs/default/Scripts/python.exe`（venv） | ✅ 全都有 |

### 解法

**始终用与 `qqbrowser-skill` 同目录的 python**（即 `QQB_CLI` 所在 `Scripts/` 下的 `python.exe`）。
`doctor` 检测到依赖缺失时会自动算出并提示这个路径。

### 脚本已内置兜底，不必改调用方

`docx` 子命令里加了 `_ensure_venv()`：发现当前解释器缺 `python-docx` / `pillow` 时，
**自动切到 `QQB_CLI` 同目录的 venv 解释器重跑**（打印一行提示，stdout 与退出码原样透传，
用 `QQHW_REEXEC` 环境变量防递归）。

实测（2026-09-04）：用 base 解释器调 `docx 2026-09-04` → 自动切换 → 产物 89187 B，
与用 venv 直跑**完全一致**。

→ 已配好的定时任务 prompt 里若写死了 base 解释器，**不用批量去改**，脚本自己会兜住。
（实现细节：用 `subprocess.run` + `sys.exit(rc)`，不用 `os.execve` ——
后者在 Windows 上进程替换语义不可靠，实测会丢输出、产物也可能不落盘。）

## 16. 中文路径：分场景，别一刀切

| 场景 | 中文路径能否直用 |
|------|-----------------|
| `agent_mail_upload_attachment` 上传附件 | ✅ 直接传中文绝对路径（2026-09-04 实测通过） |
| `SendMessage` / 企微邮件的 `file_path` | ✅ 同上 |
| PowerShell `-File x.ps1 -Docx <中文路径>`（Word COM 转 PDF、count_pages） | ❌ 按系统编码解码成乱码 → 先 `cp` 成 ASCII 名（见 §10） |

不要因为 §10 的坑就把**所有**中文路径都转 ASCII——上传附件那一步完全没必要。

## 17. 登录态自动恢复：扩展不重连新 daemon（2026-11-10 端到端定位）

**现象**：`bkn` 还能取到值，但 `day --refresh` 报 `ptlogin-ex verify fail`；
随后所有 `browser_*` 命令都返回 `Waiting for client connection timed out after 60s`，
`daemon.log` 连续几十行「等待客户端连接」，而 QQ 浏览器进程明明还在。

**根因三重叠加**：

1. **no-kill patch 的副作用**：补丁在「浏览器已运行但缺 `--x5use-automatic-in-tab`」
   时选择保留现有进程（保护登录态）。用户手动开的浏览器因此不加载自动化扩展 →
   扩展永不连接 `ws://127.0.0.1:8765`。早期能成功是因为当时一个浏览器进程都没有，
   daemon 亲自拉起了首个带 flag 的实例。
2. **单实例转发**：直接再执行 `QQBrowser.exe --x5use-automatic-in-tab ...`
   会被转发到已有会话（日志出现「在现有的浏览器会话中打开」），flag 根本不生效。
   → 必须用独立 `--user-data-dir=<新目录>` 起真正独立的实例，且不强杀用户窗口。
3. **`#qlogin_list` 在跨域 iframe**（`xui.ptlogin2.qq.com/cgi-bin/xlogin`，
   name=`login_frame`）里。CLI 的 `browser_snapshot` / `browser_find_and_act`
   只看顶层 frame，`browser_eval_content_js` 无 frame 参数、`contentDocument` 为 null。
   → 把该 xlogin URL **在顶层打开**，快捷登录列表才进入主 DOM
   （依赖本机 QQ 客户端登录态，与浏览器 profile 无关，独立 profile 也能渲染）。

**解法**：`scripts/autologin.py` 在**单次调用内**跑完
`daemon 启动 → 扩展连上 → 顶层打开 xlogin →
browser_find_and_act --by css --value "#qlogin_list a" --action click →
登录验证 → bkn / day --refresh`。
必须单次的理由：daemon 跨调用会被平台清理，扩展不会重连新 daemon。

⚠️ 选择器别写成 `#qlogin a` —— 容器里第一个 `<a>` 是「QQ 手机版」下载链接，
会打开新标签页。`browser_eval_content_js` 禁用 `document.cookie`
（报 `forbidden API`），探测 JS 里不要碰；`bkn` 用 performance 资源条目，安全。

**验证标志**：点击后跳到 `qun.qq.com/#/member-manage/base-manage`（含账号昵称与退出按钮）；
再访问 `#/login` 被自动重定向；`bkn` / `day --refresh` 能拉到数据。

**无焦点启动（硬性约束）**：新增拉起的进程不得改变桌面焦点。
`scripts/focusless.py` 的四层防御见 SKILL.md §1c；`qq_hw.py` 的
`ensure_focusless_patch()` 还把 `SW_SHOWNOACTIVATE` + 去掉 `--start-maximized`
注入 x5use 的 `_start_qqbrowser_win()`，覆盖 daemon 冷启动自动拉起浏览器的分支。
日志里出现 `[FocusGuard] ... 焦点保持不变` 即为通过。

旁路噪声：本机安全策略会拦截 `wmic.exe`（`daemon_server.py` 扫自身进程用），
`status` / `get_session_id` / 业务命令仍正常；**不要绕过、不要改 `mcp.json`**。
