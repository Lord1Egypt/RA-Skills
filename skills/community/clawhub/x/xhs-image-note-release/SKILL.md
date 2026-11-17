---
name: xhs-image-note-release
description: >
  小红书笔记自动发布（图文 + 视频，按扩展名自动判断）。ego-browser 驱动全流程：
  上传素材（图文逐张 / 视频单文件+转码轮询）、填标题正文、挂话题、设自定义封面
  （COVER_IMAGE，留空用第一帧）、发布或存草稿。带分层退出码与结构化失败输出，
  失败默认保留浏览器现场可直接接管。
  三种收尾：publish 直接发 / draft 存草稿 / stage 只准备页面。
  附 29 种样式卡片生成器（含照片背景氛围与历史古风主题），参数自由配置。
  触发词：发小红书、发布图文笔记、发布视频笔记、小红书发帖、存草稿、推到草稿箱。
  前置依赖：ego-browser (ego-lite) 运行中，小红书已登录。
slug: xhs-image-note-release
displayName: 小红书笔记发布（图文/视频）
version: 2.0.7
bins: [node, python3]
---

- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-office-work

# xhs-image-note-release

通过 ego-browser 自动化发布小红书笔记。覆盖从打开创作平台到发布成功的完整流程，包含素材批量上传、标题/正文填写、话题标签、一键发布等。**图文与视频两条路径自动选择**，详见「媒体类型自动判断」。附带 29 种多样式风格卡片生成器（含 4 种照片背景氛围主题），卡片参数可自由配置。

## 媒体类型自动判断（v1.8.0 新增）

`publish_note.sh` 按第一个文件的扩展名决定走哪条路径，不需要手动指定：

| 扩展名 | 判定 | 上传入口 | file input 选择器 |
|--------|------|----------|-------------------|
| `.mp4` `.mov` `.flv` `.f4v` `.mkv` `.rm` `.rmvb` `.m4v` `.mpg` `.mpeg` `.ts` | `video` | 上传视频 tab | `input[type="file"][accept*=".mp4"]` |
| `.png` `.jpg` `.jpeg` `.webp` `.heic` `.bmp` | `image` | 上传图文 tab | `input[type="file"][accept*=".png"]` |

约束：**视频一次只能 1 个文件；图文最多 18 张**。判定失败或混合类型时脚本在启动浏览器之前就报错退出（不会产生废草稿）。要强制指定用 `MEDIA_TYPE=video` 或 `MEDIA_TYPE=image`。

两条路径在**落地页、上传方式、完成判定、等待时长、封面**五处不同，逐项对照见 [flow-internals](references/flow-internals.md#图文-vs-视频的差异)。主文档只需记住：视频不用切 tab、图文要切；图文逐张传、视频一次传完再等转码。

封面选用规则：`COVER_IMAGE` 留空 → 完全不碰，走小红书默认第一帧；传了图 → 走四步替换链路。**该参数只在视频模式生效**，图文模式会忽略并在启动时提示。

## Dependencies

本技能依赖以下外部工具/技能，**必须在使用前安装并配置**：

| 依赖 | 类型 | 用途 | 安装方式 | 验证 |
|------|------|------|----------|------|
| **ego-browser** (ego-lite) | CLI 工具 + Skill | 浏览器自动化引擎，提供 CDP、snapshot、fillInput 等 API | 参考 [ego-browser skill](https://github.com/Songhonglei/better-office-work) 安装 | `ego-browser --version` 能正常输出版本号 |
| **小红书账号** | 平台账号 | 需在 ego-lite 浏览器中已登录小红书 | 手动在 ego-lite 中登录 creator.xiaohongshu.com | 打开创作平台能看到发布按钮 |
| **Google Chrome / Chromium** | 系统浏览器 | 卡片生成器 (`references/card-generator/card_generator.py`) 使用 Chrome headless 渲染 PNG | macOS: 从 [google.com/chrome](https://www.google.com/chrome/) 安装；Linux: `apt install chromium-browser` | 终端运行 `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version` 或 `chromium --version` |
| **Python 3.8+** | 运行时 | 运行卡片生成器脚本，仅用标准库，无需 pip 安装任何包 | macOS 自带；Linux: `apt install python3` | `python3 --version` 输出 ≥ 3.8 |

> **特别提示（仅 WorkBuddy 环境）**：较新版本的 WorkBuddy 需先关闭沙箱功能（设置 → 关闭沙箱），否则运行 ego-browser 会被中断。这**不是本技能的依赖**——在终端或其他 Agent 中直接运行本技能无需任何沙箱相关操作。
>
> **ego-browser API（2026-11-02 核实）**：ego-browser 0.6.2.x **同时提供两套 API，且都能正常调用**。`ego-browser skill` 打印的指南 v2.1.0 只列了新的一套，容易被误判成旧 API 已被移除——实测旧全局函数全部存在且整条流程可跑通。
>
> | 全局函数（本技能使用） | TaskSpace/Page 对象 API |
> |---|---|
> | `useOrCreateTaskSpace(name)` | `taskSpace(name)` |
> | `openOrReuseTab(url, {wait, timeout})` | `page.goto(url)` |
> | `js(codeString)` | `page.evaluate(fn, arg)` |
> | `fillInput(sel, value)` | `page.fill(sel, value)` |
> | `typeText(text)` | `page.keyboard.insertText(text)` |
> | `click(refOrSel, {label})` | `page.click(sel)` |
> | `uploadFile(sel, absPath)` | `page.setInputFiles(sel, [absPath])` |
> | `pageInfo()` | `page.url()` / `page.info()` |
> | `captureScreenshot()` | `page.screenshot({path})` |
> | `wait(n)`（**单位：秒**） | `page.waitForTimeout(ms)`（**单位：毫秒**） |
> | `completeTaskSpace(id, {keep})` | `task.finish({ keep: [...] })` |
>
> 本技能继续使用全局函数：`uploadFile()` 的逐文件上传语义直接关系到「图文批量只留空占位」这个坑，换新 API 需要重新验证多图批量上传。**注意 `wait()` 是秒，新 API 是毫秒，混用会差 1000 倍。**
>
> 上述 API 需先 `Skill("ego-browser")` 加载后使用。

## 前置条件

1. **ego-lite 已安装且运行中** — ego-browser CLI 依赖 ego-lite app 提供的浏览器环境
2. **小红书已登录** — ego-browser 继承用户登录态，需在 ego-lite 中手动登录小红书一次
3. **已加载 ego-browser 技能** — 先 `Skill("ego-browser")` 加载浏览器操作技能

> ⚠️ **发布前必读**：笔记内容（卡片图片、标题、正文、话题）中**严禁出现任何引流信息**——「微信搜索」「公众号」「加微信」「扫码」等文案或二维码图片一律不得出现，极易封号。只允许 @账号名 这类软性署名。发布前逐张检查图片和文案。详见「注意事项」第 15 条。

> **特别提示（仅 WorkBuddy 环境）**：较新版本的 WorkBuddy 需先关闭沙箱功能（设置 → 关闭沙箱），否则运行 ego-browser 会被中断。这不是本技能的依赖，在终端或其他 Agent 中直接运行无需此操作。

## 核心流程

**跑 `publish_note.sh` 就会自动走完下面 8 步，不需要手写浏览器脚本。** 这一节告诉你每步「做成了没有」的客观判据，用来判断一次运行停在哪、要不要接管。

```
[sh] 按扩展名校验参数 → [mjs] 打开平台 → 登录检查 → 切 tab → 传素材
     → 设封面(可选) → 填标题/正文/话题 → 提交 → 校验 → 清理
```

**收尾模式（MODE）**：

| 值 | 行为 | 成功判据 |
|---|---|---|
| `publish`（默认） | 调 `_onPublish()` 真发 | URL 含 `published=true` |
| `draft` | 调 `_onSave()` 存本地草稿箱 | 草稿箱计数 +1 或 IndexedDB 读到该标题 |
| `stage` | 填完就停，不提交、**也不释放 space** | 内容已就位（需人工点发布）|

用户说「存草稿 / 推到草稿箱 / 自己点发布」→ `draft`；说「发小红书 / 发布」→ `publish`；说「先给我看看」→ `stage`。

### 1. 打开创作平台

`/publish/publish` 落地后是 Vue SPA，`<div id="app">` 初始为空，**必须 `await wait(15)`**，`waitForNetworkIdle` 不够。

### 2. 切到对应上传 tab

落地页**默认就是「上传视频」**，所以视频不用切、图文要切。判据是**目标 file input 是否已存在**，不要靠页面文案猜。页面可能用顶部 tab，也可能用「发布笔记」下拉，脚本两种都兼容。

| 类型 | file input 选择器 |
|---|---|
| 视频 | `input[type="file"][accept*=".mp4"]` |
| 图文 | `input[type="file"][accept*=".png"]` |

> 两者不能混用。用 `.png` 选择器传视频会抛 `ElementResolutionError`，看起来像浏览器坏了，其实是走错了上传路径。

### 3. 上传素材

**图文**：必须 `uploadFile()` **逐张**上传（每张等 6s，全部传完再等 4s）。批量 `DOM.setFileInputFiles` 只会留下空占位符——编辑器显示「图片编辑 10/18」，但缩略图是空的，存草稿后图片不存在。最多 18 张，路径必须绝对。

**视频**：只有一个 input、无 multiple，`uploadFile()` 一次传完，然后**等转码**。判据是「重新上传」文案 **和** 标题输入框**同时**出现（最多轮询约 2 分钟）。页面上 `video` 元素可能有 4 个（预览/封面候选），**别用数量判定**。

**封面（仅视频，`COVER_IMAGE` 可选）**：留空就完全不碰，走小红书默认第一帧。传了图就走四步替换链路，其中「编辑封面」按钮平时 `boundingRect` 是 `0×0`，**必须先用 CDP 派发真实 `mouseMoved` 悬停**才渲染出来——`el.click()`、`scrollIntoView`、`getByText` 全部无效。任一环节失败脚本 `exit 60` 中止，不会带错误封面继续发。

> ⚠️ 别和 `video-multi-release` 搞混：那个 skill 的 `scripts/xhs.mjs` 封面失败是**只告警继续发**，
> 本 skill 的 `scripts/publish_note.mjs` 是 **exit 60 中止**。两套脚本各自独立，行为不同是有意的。

### 4. 填标题

`fillInput()` 写入后回读比对。**标题严禁含单引号**（会插进 JS 单引号字符串，中断脚本）。

### 5. 填正文与挂话题

正文是 tiptap ProseMirror 富文本。两个硬约束：

- **用 `js()` 里的 `el.focus()` 定位编辑器，不要用 click**——`<xhs-publish-btn>` 浮层会拦截指针事件（`ElementResolutionError: intercepts pointer events`）。
- **话题必须从下拉列表点选**。直接粘贴 `#话题1 #话题2` 只生成纯文本，不会真正挂上话题词条。每次输 `#` 前要用 Selection API 把光标收敛到末尾（tiptap 不认 `Control+End`，否则话题会插进正文中间）。

**正文严禁含反引号和 `${`**（会插进 JS 模板字符串，中断脚本）。

### 6. 提交

发布/存草稿是同一个自定义组件 `<xhs-publish-btn>`，常规选择器和坐标点击都打不中（closed Shadow DOM，`snapshotText` 也抓不到文本），**只能调它内部方法**：

```js
host._onPublish()   // 发布
host._onSave()      // 存草稿
```

> **没有「存草稿」按钮。** 按钮真实文本是**「暂存离开」**，按「存草稿」去找永远找不到，页面也不会有任何变化。

### 7. 校验

`publish`：等 URL 出现 `published=true`（脚本主判据）。`note-manage` 只作旧行为兜底——该路径直接访问已 404，**别手工拼 URL 去确认**，走侧栏「笔记管理」入口。

`draft`：页面**不跳转**（草稿存当前浏览器本地，不是云端）。脚本先读「草稿箱(N)」计数——**读不到就 `exit 80`**（`E_DRAFT_COUNT_UNREADABLE`，因为连保存成功与否都无法确认）；读到了再直读 IndexedDB（`draft-database-v1`）按时间取最新一条比对标题，成功打印 `draft verified: 标题「…」，保存于 …`。**IndexedDB 核对失败只告警**（本地库结构可能再变），不推翻已确认的保存。

### 8. 清理

成功时 `completeTaskSpace(id, { keep: false })`；失败默认保留现场（`KEEP_ON_FAIL=1`），空间不销毁、页面留着可直接接管。

> **每步的选择器、JS 片段、CDP 坐标、踩坑成因见 [references/flow-internals.md](references/flow-internals.md)** —— 只在改选择器、改版维护、排查 DOM 结构时读，日常发布不需要。

## 脚本架构（v1.10.0 重构）

```
scripts/
├── publish_note.sh    # 入口层：参数解析 / 校验 / 调起浏览器
└── publish_note.mjs   # 流程层：所有浏览器操作，可单独 node --check
```

**分工原则**：一切「不需要浏览器就能判断」的事都放在 `.sh`（默认值、必填项、特殊字符、素材类型、文件存在性、数量上限）。**所有校验在启动浏览器之前完成**，判错直接 `exit 10`，零副作用——不会留废草稿、不会占 task space。

`.mjs` 只做浏览器操作，参数经固定路径 `/tmp/xhs_publish_params.json` 传递（ego-browser 的 nodejs 环境**不继承 shell 环境变量**）。**该路径固定，不要并发跑两个实例**，否则参数互相覆盖、内容串台；批量发多条必须串行，间隔 ≥5 分钟。

改版维护通常只动 `.mjs` 顶部两张表：`SEL`（14 个选择器）/ `T`（8 个超时，仅 `spaReady` 用秒、其余毫秒）。写 `js()` 模板串时引用 Node 变量必须写 `${var}`，漏了会变成浏览器端 `ReferenceError`（本项目踩过：`filePaths.length` 漏插值）。

## 失败处理

失败时输出结构化块，照着 `what_now` 做即可：

```
=== FAILED ===
step     : set-cover
code     : E_COVER_NOT_APPLIED
exit     : 60
what_now :
  1. 封面缩略图 URL 没变，图片没真正替换
  2. 重跑一次通常成功；连续失败就改用默认第一帧
space    : 12（页面已保留）
takeover : ego-browser nodejs -e "await claimTaskSpace(12)"
=== END FAILED ===
```

退出码速查：`0` 成功 · `10` 参数（改完重跑，无副作用） · `11` 依赖缺失（缺 mjs/ffmpeg/ego-browser） · `20` 登录 · `21` 上传页 · `30` 素材上传 · `40` 填表 · `50` 话题 · `60` 封面 · `70` 提交 · `80` 提交后待确认（**别立即重发**） · `90` 内部异常。

失败默认保留现场（`KEEP_ON_FAIL=1`），空间不销毁、页面留着，可直接接管排查；传 `KEEP_ON_FAIL=0` 关闭。每次运行日志在 `/tmp/xhs-publish-<ts>-<pid>.log`。

> **完整退出码表、code 清单、step 名对照、常见故障判断见 [references/error-handling.md](references/error-handling.md)** —— 只在脚本返回非零时按需加载，正常流程无需读。

## 快速复用

### 发布已有素材（图文 or 视频）

修改 `scripts/publish_note.sh` 顶部参数，或直接用环境变量传入。**类型不需要声明**，按扩展名自动判断。

图文：
```bash
# 必须 export：脚本是独立子进程，光赋值不导出，它读到的全是空值。
export MEDIA_DIR="/path/to/assets"
export MEDIA_FILES="img1.png,img2.png,img3.png"   # 最多 18 张
export TITLE="标题"
export BODY='正文内容'
export TOPICS="话题1,话题2,话题3"
export MODE="publish"   # publish=直接发布；draft=存草稿箱；stage=只准备好内容停在页面

bash ~/.workbuddy/skills/xhs-image-note-release/scripts/publish_note.sh
```

视频：
```bash
export MEDIA_DIR="/path/to/assets"
export MEDIA_FILES="video.mp4"                     # 视频只能 1 个
export COVER_IMAGE="/path/to/cover.png"            # 可选，留空=默认第一帧
export TITLE="标题"
export BODY='正文内容'
export TOPICS="话题1,话题2"
export MODE="stage"

bash ~/.workbuddy/skills/xhs-image-note-release/scripts/publish_note.sh
```

一行式（前缀赋值自带导出，等效于 export）：
```bash
MEDIA_DIR=/abs/path MEDIA_FILES=video.mp4 TITLE="标题" BODY='正文' TOPICS="话题1,话题2" MODE=stage \
  bash ~/.workbuddy/skills/xhs-image-note-release/scripts/publish_note.sh
```

参数演进说明（v1.8.0）：`IMAGE_DIR` / `IMAGES` 仍可作为 `MEDIA_DIR` / `MEDIA_FILES` 的别名使用，老调用方式不破。新增 `MEDIA_TYPE=image|video` 用于强制指定（默认 `auto`）。

封面参数（v1.9.0）：新增 `COVER_IMAGE`，仅对视频笔记生效；留空则保留小红书默认的第一帧。

> **draft 模式说明**：`MODE="draft"` 时脚本走 `_onSave()` 存草稿箱，不实际发布。用户可在小红书创作平台「草稿箱」里自行检查并点发布。多笔记场景建议先全部存草稿，再手动间隔 ≥5 分钟逐一发布以避风控。

> **draft 的自动核对**（v2.0.0）：存完草稿后脚本会直接读浏览器 IndexedDB（`draft-database-v1` → `video-draft` / `image-draft`），按时间取最新一条比对标题，成功时打印 `draft verified: 标题「…」，保存于 …`。这比「点草稿箱面板看」可靠——小红书把草稿入口从左侧栏挪到了右上角，点击不一定能展开。核对失败只告警不判失败，因为本地库结构可能再变。

### 先用卡片生成器做图，再发布

本技能附带统一风格卡片生成器（`references/card-generator/card_generator.py`），29 种主题、纯文字/图文两种布局、可选照片背景。仅用 Python 标准库 + 本机 Chrome headless，无需 pip 安装。

```bash
CG=~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py

# 纯文字卡片
python3 "$CG" --theme warm --tag "人生随笔" \
  --lines "周五了\n你还活着吗\n去外面走走" \
  --subtitle "关于活着" --page-number 1 --total-pages 6 \
  --account "@雨夜心灯" -o ./card.png

# 照片背景卡片（暗色遮罩 + 文字投影，配 --background）
python3 "$CG" --theme history --background ./bg.png \
  --lines "坑的是方士\n不是儒生" --account "@雨夜心灯" -o ./card.png

python3 "$CG" --list-themes    # 打印全部 29 个主题
```

主题速查：照片背景 `cinematic` / `film` / `journal` / `history`（**必须配 `--background`**）；生活 `warm` / `xhs` / `xhs_rich` / `morandi` / `fresh`；科技 `cyberpunk` / `apple` / `cowork` / `carbon`；文艺 `ink` / `palace` / `elegant` / `newspaper` / `steampunk`。

> **完整主题表、全部 CLI 参数、图文布局（`--layout image-text`）、批量出图见 [references/card-generator-usage.md](references/card-generator-usage.md)** —— 只在真要做图时加载。照片背景的图层栈原理另见 [references/photo-background.md](references/photo-background.md)。

出图后把目录填进 `MEDIA_DIR`、文件名列进 `MEDIA_FILES`，直接跑 `publish_note.sh` 发布。

## 照片背景卡片（v1.5.0 新增）

满幅照片作底图 + 暗色遮罩 + 文字投影。4 种氛围主题：`cinematic`（暗色电影感）/ `film`（胶片颗粒）/ `journal`（书页氛围）/ `history`（历史古风）；核心参数 `--background` `--scrim` `--blur` `--desaturate` `--grain`。

```bash
CG=~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py
python3 "$CG" --theme cinematic --background ./bg.png --lines "文案" --account "@雨夜心灯" -o card.png
```

> **完整说明见 [references/photo-background.md](references/photo-background.md)** —— 含图层栈原理、三种主题参数表、CLI 全示例、批量工作流。只在需要做照片背景卡片时加载。

## 注意事项

编号沿用历史（正文有「见第 N 条」的交叉引用），已并入核心流程的条目只留一句提示。

1. **沙箱（仅 WorkBuddy）**：报 `from the default agent sandbox` 就去设置里关沙箱，重试。其它环境无需此操作。
2. **SPA 渲染**：首次加载等 15 秒，别用 `waitForNetworkIdle` 替代 → 核心流程 §1
3. **话题标签**：`TOPICS` 里每个话题都要走「输 `#` → 下拉点选」，**不要在 `BODY` 里写 `#话题`** → §5
4. **发布频率**：**严禁**短时间连续发多篇，判定风控后可能限流甚至封号。建议间隔 ≥5 分钟。
5. **权限设置**：需要设公开/仅自己可见时，在「填完正文」到「点发布」之间操作。
6. **标题特殊字符**：**严禁单引号** → §4
7. **正文特殊字符**：**严禁反引号和 `${`** → §5
8. **存草稿**：小红书没有「存草稿」按钮，右下角是「暂存离开」；草稿存**当前浏览器本地**，不跨设备、不跨浏览器，清缓存就没了。只有发布后的笔记才进账号云端 → §6
9. **图片必须真正落盘**：批量 `setFileInputFiles` 只留空占位，必须 `uploadFile()` 逐张 → §3
10. **多篇批量**：间隔 ≥5 分钟，或全部先存草稿再手动逐一发。
11. **重复跑会堆「暂无笔记标题」废草稿**：`draft` 模式每跑一次可能副产几条空草稿，清理要在「草稿箱 → 图文笔记」里点**每条最后一个 `.btn`**，且确认弹窗必须点真正的 `<button>`（`.draft-delete-popconfirm-btn-footer-confirm`），点 footer 容器是空操作。完整步骤见 [flow-internals](references/flow-internals.md#附注意事项里的技术细节)。
12. **发布后无法再远程验证**：脚本结束时 `completeTaskSpace({keep:false})` 会连登录态一起销毁，之后新建空间不继承 cookie（打开创作者平台直接跳登录墙）。要查「已发布」列表**必须在同一 space 内、`completeTaskSpace` 之前**做。发布成功以业务级证据为准：CDN 落盘 + 话题全部 `clicked:true` + URL 含 `published=true`；视觉终检请用户在 App 内看。
13. **登录检测必须用 URL 判定**：401 会 302 到 `creator.xiaohongshu.com/login?redirectReason=401`，而**登录页导航里也有「发布」「上传图文」字样**，靠文字包含判断会把 401 误判成已登录，然后在 `uploadFile()` 抛 `ElementResolutionError`、真实原因被掩盖。内置判据是「URL 含 `/login` → 未登录」+「侧栏有『笔记管理/草稿箱』入口 → 已登录」双重校验。**发布前先在 ego-lite 手动登录**，别指望脚本自动过登录墙。
14. **用户手动登录会触发硬停止**：登录由用户在 ego-lite 完成，会把 space 的 ownership 切给用户，此后所有浏览器命令报 `The user has taken control of this task space`。这是**硬停止，不可自行绕过**：不要重试、不要夺回，等用户回复「继续」后用 `claimTaskSpace(原 spaceId)` 认领再重跑（`takeOverTaskSpace` 只适用于 ownership 仍是 agent 的情况）。
15. **⚠️ 铁律：内容里严禁出现任何引流信息**：卡片文案、标题、正文、话题、图片中**都不得**出现「微信搜索」「微信公众号」「加我微信」「扫码关注」等，也**不得**放二维码——小红书对站外引流判定极严，直接引流极易**封号**。只允许 `@账号名` 这类软性署名。发布前逐张检查图片和文案。
16. **图文与视频的选择器不能混用** → §2
17. **视频必须等转码**：「重新上传」+ 标题框**同时**出现才算好，别用 `video` 元素数量判定 → §3
18. **草稿校验别走「点开面板」**：`.header-draft` 在 `js()` 里 `el.click()` 不展开，实测真实 click 与 CDP 鼠标事件也无反应。校验一律走 IndexedDB → §7
19. **`/publish/note-manage` 和 `?tab=draft` 都已 404**：别拼 URL 找笔记管理，从侧栏进。另外根路径 `/` 会跳 `/login`，但 `/publish/publish` 登录态正常——别被根路径重定向误导成「未登录」。→ §7
20. **自定义封面必须真实 hover**：`.cover-edit-entry` 平时 `0×0`，只有 CDP `mouseMoved` 能触发；「完成」按钮在视口外要先 `scrollIntoView`；首屏 `.pk-cover-guide-tooltip` 会遮挡，先 `display:none`。→ §3
21. **草稿箱入口在右上角**（2026-11-02 改版）：左侧栏已没有「草稿箱(N)」，`.header-draft` 挪到 `upload-container` 的 header（约 `x=980, y=81`）。用户要看草稿，让他自己点。
22. **图片上传完成判定有三个信号**：①「图片编辑 N/18」用**跨行**正则 `/图片编辑[\s:：]{0,6}(\d{1,2})\s*\/\s*(\d{1,2})/`（标签和数字渲染在两行，按行解析会得到空串）；② 数编辑区里 `textContent === '编辑'` 的叶子节点；③ CDN 图数但**排除 `avatar`**（否则头像、UI 图会被算进去）。任一 ≥ 张数即通过。失败块里若 `detail.editCount` 已是 `N/18` 且 ≥ expected，说明图其实传好了、只是判据没跟上改版，**按 space 接管手动收尾，别重跑**。

## Resources

### scripts/
- `scripts/publish_note.sh` — 入口层，图文/视频自动判断，改参数后直接跑（见「快速复用」）
- `scripts/publish_note.mjs` — 流程层，所有浏览器操作，可用 `node --check` 单独校验

### references/
- `references/error-handling.md` — 完整退出码表、全部错误码清单、step 名对照、常见故障判断（登录失效 / 上传超时 / 封面未生效 / 提交未确认）。**按需加载**：只在脚本返回非零退出码、或排查历史运行时读；正常运行无需加载
- `references/flow-internals.md` — 8 个流程步骤的选择器、JS 片段、CDP 坐标与踩坑成因，外加「注意事项」里技术细节型条目的完整版。**按需加载**：只在改选择器、改版维护、排查 DOM 结构时读；日常发布不需要
- `references/card-generator-usage.md` — 卡片生成器的完整 29 个主题表、常用参数说明、图文布局规则、批量出图工作流（全量参数用 `--help` 看，31 个）。**按需加载**：只在要做图时读
- `references/photo-background.md` — 照片背景卡片的图层栈原理、4 种氛围主题参数、CLI 全示例、批量工作流。**按需加载**：只在要做「照片压字」氛围卡片时读
- `references/publish-method.md` — 完整方法文档，含 `_onPublish`/`_onSave` 两种收尾方案的失败方案对比表、技术原理与「暂存离开」坑点详解。**按需加载**：当需要了解发布/存草稿按钮各失败方案的完整对比、或需要排查发布/存草稿相关问题时阅读此文件；正常流程无需提前加载
