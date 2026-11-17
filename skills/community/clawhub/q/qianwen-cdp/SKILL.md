---
name: qianwen-cdp
display_name: 千问浏览器原生 CDP 驱动
description: 用原生 Chrome DevTools Protocol
  驱动千问浏览器（qianwen.exe），复用真实登录态做办公自动化。当用户要让"千问浏览器"自动打开网页、填表、点击、抓取内容、截图，或提到
  xbrowser/agent-browser 驱动千问失败时，使用本技能。
---

# 千问浏览器原生 CDP 驱动

## 为什么不用 xbrowser / agent-browser

**xbrowser（底层 agent-browser）驱动不了千问**。实测 `agent-browser --cdp <port>` 连千问（真实或干净 profile 都试过）后，驱动**已存在的页面 target** 会静默/挂死（空 profile 跑 2m35s 零输出，最终报 `Auto-launch failed ...:9407`）。xb 的 `run.cjs` 对本地浏览器一律传 `--cdp`，所以 **`xb run --browser qianwen` 彻底走不通**，不要浪费时间在这条路上。

## 根因 & 解法（已验证）

- 千问对「外部 CDP 连接」操作**已存在的页面 target**（通义千问桌面页、AI插件页等）一律静默。
- 但用 **browser 级 WebSocket → `Target.createTarget` 自己新建的页面 target 完全可控**（Runtime / DOM / Input 全可用）。
- 因此驱动千问必须「**原生 CDP + 自建新 target**」，绝不用 `--cdp` 连旧实例。

## 工具

`qw.cjs`（本 skill 目录内）。依赖 `ws` 模块（环境变量 `QW_WS_PATH` 指定，或自动探测 `~/.workbuddy/skills/xbrowser/...` / `~/.openclaw/tools/xbrowser/...` 常见位置）。

调用示例（用 managed node）：
```
NODE="C:/Users/<用户名>/.workbuddy/binaries/node/versions/22.22.2/node.exe"
$NODE qw.cjs check                                   # 先诊断：9666 是否就绪 / 千问是否在跑
$NODE qw.cjs ensure                                  # 9666 在就直接连（不起实例）；不在则提示用 launch 或自行从 lnk 打开
$NODE qw.cjs launch                                  # 仅当确认要起实例时：先优雅关在跑的千问，再起带 9666 的
$NODE qw.cjs open "https://www.baidu.com"            # 新建 tab 并导航，输出 targetId
$NODE qw.cjs navigate <id> "https://..."             # 已有 tab 导航
$NODE qw.cjs eval <id> "document.title"              # 执行 JS
$NODE qw.cjs snapshot <id> [css选择器]               # 取标题/文本/链接/输入框
$NODE qw.cjs click <id> "#su"                         # 点击元素（按坐标派发鼠标事件）
$NODE qw.cjs type <id> "#kw" "机器人 ROS2"            # 向输入框填入文本
$NODE qw.cjs screenshot <id> [out.png]               # 截图
$NODE qw.cjs list                                    # 列出所有 target
$NODE qw.cjs close <id>                              # 关闭 tab
$NODE qw.cjs relaunch                                # 实例挂掉时：taskkill + 重拉 9666
```

每个命令都是独立进程，连接到**常驻的千问 CDP 实例**（默认 9666）操作，所以可多次调用串起多步自动化。

## 关键常量

- 千问 exe：`C:\Users\<用户名>\AppData\Local\Programs\QianwenApp\qianwen.exe`（Chromium 130；环境变量 `QW_EXE` 可覆盖）
- 真实 profile：`C:\Users\<用户名>\AppData\Local\Qianwen\User Data`（**登录态/标签页在这里**，驱动走的也是这个实例；环境变量 `QW_PROFILE` 可覆盖）
- CDP 固定端口：`9666`（`cdp_default_port` 是 9407，是 agent-browser 默认回退端口，报错里见到的就是它）

## 已验证的端到端能力

open 百度 → type 搜索框 → click 搜索 → 搜索结果正文读出 ✅。即「开页 + 输入 + 点击 + 读内容」真实交互全通。

### 读钉钉文档「多维表」（已验证 2026-08-04）

钉钉多维表（`alidocs.dingtalk.com/i/nodes/<nodeId>?...sheetId=...`）在千问里由**同域 iframe `#wiki-notable-iframe`** 承载，`contentDocument` 可直接读（非跨域）。数据不是 canvas，是真实 DOM：`[role=grid]` 网格 + 虚拟化行/列（只渲染可见窗口）。

读取步骤：
1. `qw.cjs list` 找标题含「多维表」的 page target（取 id）。
2. `qw.cjs eval <id> "document.getElementById('wiki-notable-iframe').contentDocument.querySelector('[role=grid]').innerText"` → 直接拿整表文本（表头+可见行）。
3. 取行数/列数：`contentDocument` 内 `querySelectorAll('[role=row]')` / `[role=cell]`。
4. **全表需翻页/滚动累加**：虚拟化只渲染窗口（实测约 42 行/次），要对 iframe 内网格容器逐屏 scroll 并拼接，才能拿全量行。
- 注意：钉钉文档外层 page 的 `innerText` 只含左侧知识库文件树，「研发项目管理多维表」本身是 iframe 里的 grid，必须进 iframe 读。
- 该表即记忆里的「ROS软件项目管理表」：nodeId=`amweZ92PV6mrnN5mIeGyNM3GWxEKBD6p`、sheet=`O4kXTnQ`，字段≈项目名称/负责人/优先级/项目进度细节登记/进度示意/小批量跟进。

### 读微信读书正文（实测 2026-08-04）

微信读书网页版（`weread.qq.com`）分两层：

1. **目录 / 章节标题 / 元数据**：纯 DOM 文本，可读。全书 TOC 可直接从 `.wr_page_reader`（style/script 剔除后）`textContent` 抽出。
2. **正文 prose**：页面栅格化为 canvas（`.readerChapterContent` 里有 `renderTargetContainer` + `<canvas>`），直接 DOM `textContent` 只能拿到「JS复制代码」等 UI 文本，**正文不暴露为文本**。想读正文必须 `qw.cjs screenshot` 截取页面 → OCR。
   - `innerText` 返回 0/空：微信读书把每一页做成绝对定位的「页」块，Chromium 的 `innerText` 算不出可见文本。
   - 读整本书：截图每一页 + OCR，或利用 weread 的「文本选择/复制」层（如果存在）逐段模拟选中，成本更高。
   - 环境：工作目录有 `chi_sim.traineddata`（中文 OCR 数据），但本机缺 tesseract 主程序，装完后即可 OCR。

## 坑（必记）

0. **🚨 重要更正（2026-07-30）**：`49666` 端口**不是千问**！它是 **svchost.exe（Windows 系统服务，PID 2400）** 监听的，与千问无关（曾误判为"千问内部端口/日常实例"，已纠正）。千问自身 CDP 端口固定 **9666**。
   - **lnk 注入早已生效**：4 个千问快捷方式（开始菜单 / 桌面 / 任务栏 / Quick Launch）的 ARGS 均含 `--remote-debugging-port=9666`（**UTF16 编码**，ASCII `grep "9666"` 搜不到，必须用 LNK 二进制解析确认，曾因此误判"未注入"）。日常千问从 lnk 双击即带 9666。
   - **🚨 核心纪律（老板明确要求）：老板的快捷方式/自启动/菜单入口已全注入 9666，日常千问本就该自带 CDP 端口。脚本启动前必须先 `check` 现状：**
     1. **9666 已在监听 → 直接连，绝对不另起实例**（最常见情况，连老板日常千问即可）。
     2. **9666 没在、但千问在跑（无端口）→ 不要 spawn 第二个实例**（单例冲突、占窗口、刷回收站）。提示老板关掉后从带 9666 的 lnk 重开，或显式调 `launch`（launch 会先优雅关在跑的千问再起）。
     3. **9666 没在、千问也没跑 → 让老板从 lnk/菜单/自启动打开（自带 9666），或显式 `launch`。**
     - **`ensure` 已改为「只连不起」**：9666 在即 `alreadyUp` 直连；不在则返回 `needLaunch` 提示，不再 spawn 裸实例。`launch` 才是真正起实例的命令，且会先关在跑的千问避免单例冲突。
     - ⚠️ PowerShell `Start-Process` 在 WorkBuddy 沙箱里拉不起 GUI 进程，不要自己 Start-Process。
   - **回收站刷文件（千问自身行为，2026-07-30 确认）**：只要千问在跑，就持续把临时缓存/上报文件（`1'jssdkidx'/'pctrace'/'api'/'jserr'`、Browser_*.ulog、network.mojom、DXCACHE-*）以「可恢复删除」移入回收站 → 回收站一直涨。**这是千问客户端自身行为，并非强杀导致**（强杀只是加剧脏残留）。关掉千问即停止增长。治标=定时清回收站；根治=反馈千问团队/关闭诊断上报。
   - **🚨 不要起后台千问实例占单例锁**：`qw.cjs ensure` 起的 9666 实例若一直不关，会占着 SingletonLock + 显示，导致用户从桌面双击图标走单例激活这个无正常窗口的后台实例 → 表现为「打不开/看不到登录态」。**需驱动千问时优先连已有实例；临时起用完即关（Browser.close / Stop-Process 不带 -Force）**，绝不留后台孤儿实例。
   - `patch_lnk.py` 已落库，用于检视/补注入 lnk 端口（正确解析 LNK 二进制，绕开被拦的 WScript.Shell COM）。

1. **必须建新 target**：永远用 `open`/`Target.createTarget` 开新 tab，别去驱动千问自带的桌面页（静默）。
2. **实例挂掉恢复**：千问主进程可被 `Stop-Process -Force` 杀掉，但 `WpkService` 孤儿进程（`--type=utility`，引用真实 profile）从 WorkBuddy 沙箱**杀不掉**（taskkill 返回 exit 1）。它们不占主 SingletonLock，新主实例仍能起，只是堆积会拖慢冷启动。恢复用 `qw.cjs relaunch`。
3. **路径正斜杠**：千问对 `--user-data-dir` 反斜杠路径会秒退，必须正斜杠（脚本内已处理）。
4. **强制窗口模式**：千问无头不稳定，必须 headed（脚本内已默认）。
5. 登录态由真实 profile 保留 → 自动化时**就是老板本人已登录的千问**，对外操作（发消息/发帖）仍遵循"先问再动"。
6. **诊断登录态看 `Default/Network/Cookies`**：新版 Chromium(M120+) 把 Cookies 从 `Default/Cookies` 移到 `Default/Network/Cookies`。查 `Default/Cookies` 不存在是正常现象，会误判「登录态丢失」；真正判断登录态完好与否要读 `Network/Cookies`（大小正常即未丢）。
7. **对外「清理/关闭/删文件」操作极度谨慎**：曾因反复强杀/清回收站/删 User Data 文件把老板日常千问搞到「打不开」。动手前先确认影响范围，拿证据说话，不嘴硬。

## 何时用

用户要在千问里做自动操作（查资料、填表、抓页面、定时任务等），且要求保留登录态。直接调 `qw.cjs`，不要走 xbrowser。
