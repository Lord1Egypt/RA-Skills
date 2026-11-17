# Changelog

All notable changes to this skill are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/).

本文件只记**版本变更本身**（改了什么、为什么改）。执行时要用的步骤、判据、排障指引一律不在这里：

| 内容 | 位置 |
|---|---|
| 执行步骤与硬规则 | `SKILL.md` |
| 完整退出码表、code 清单、故障判断 | `references/error-handling.md` |
| 选择器、JS 片段、CDP 坐标、踩坑成因 | `references/flow-internals.md` |
| 卡片生成器参数与主题 | `references/card-generator-usage.md` |

> 下面历史条目里有不少 root cause 推演（如 v1.6.2 为什么批量 `setFileInputFiles` 不行）。
> 那些是当时的排查记录，**对应的现行操作口径都已写入上面三个 reference**；两者冲突时以 reference 为准。

### v2.0.7 (2026-11-10)

**撤销 v2.0.6 的封面误改 + UGLIC 深度检查修复。**

- **Revert（严重）**：v2.0.6 把封面失败描述从「exit 60 中止」改成「只告警继续发」是**错的**。
  我当时误拿了 `video-multi-release/scripts/xhs.mjs`（那个确实只告警）的行为，套到本 skill 的
  `scripts/publish_note.mjs` 上——两个是**不同脚本**。本 skill 的 `publish_note.mjs:586`
  实际是 `fail('set-cover', r.code, EXIT.COVER, ...)`，即 **exit 60 中止**。三处文档已全部改回，
  并在 SKILL.md §3 加「别和 video 的 xhs.mjs 混淆」的显式区分，防止再次误改。
- **教训**：改「文档 vs 代码」一致性前，必须先确认对照的是**同一个脚本**。跨 skill 复用同名逻辑时尤其危险。

### v2.0.6 (2026-11-10)

**CHANGELOG 归位 + 表格竖线转义。**

- **Chore**：CHANGELOG 顶部加「本文件只记版本变更」声明与 reference 指引表；确认本文件无「唯一执行源」
  （逐条比对 `uploadFile` / `setFileInputFiles` / `note-manage` / `published=true` / `E_DRAFT_COUNT_UNREADABLE`
  等 9 个关键字，均在 SKILL.md 或 references 有对应）。
- **Fix（渲染错列）**：`references/flow-internals.md` 表格里 `` `!m || m.offsetParent === null` `` 的
  竖线未转义，把表格列劈开。改为 `\|\|`。
- **Reverted in v2.0.7**：本轮曾把封面失败描述改为「只告警继续发」，**该修改有误，已在 v2.0.7 撤销**。

### v2.0.5 (2026-11-10)

第二轮 UGLIC 审计。**4 个 ERR 全部实测复现**，另修 11 项一致性问题。

**ERR**

1. **快速复用示例照抄必失败**：多行 `MEDIA_DIR="..."` 只是 shell 赋值，脚本作为独立子进程读不到，
   全部变成空值。实测 `bash -c 'echo $MEDIA_DIR'` 输出空 → 脚本报 `E_PARAM_MISSING`。
   加 `export`，并在注释里写明原因；一行式前缀赋值本来就等效于 export，补了说明。
2. **图文示例语法断裂**：`--illustration ./my-illust.svg \   # 注释` —— 续行符后跟行内注释，
   后续参数变成独立命令。实测报 `command not found: --theme`。注释移到上一行。
3. **draft 成功判据说法不准**：「核对失败只告警不判失败」只对 IndexedDB 那步成立；
   草稿箱计数读不到时脚本**直接 `exit 80`**（`E_DRAFT_COUNT_UNREADABLE`）。已精确区分两步。
4. **封面失败退出码写错**：flow-internals 3c 写 `exit 1`，实际 `exit 60`（`EXIT.COVER`）。

**一致性**

- **流程链总览重复两遍**（重构拼接时的疏漏），删一份
- **§3b 与 §3c 自相矛盾**：3b 说「要换封面得手动操作，脚本不处理」，3c 却在讲脚本怎么处理。
  改为「不传 `COVER_IMAGE` 就完全不碰，传了走 §3c」
- **登录判定文件写错**：说内置于 `publish_note.sh`，实际在 `.mjs` 的 auth 步骤
- **`photo-background.md` 标题写「四种主题」但表里只有 3 行**，补 `history` 一行
- **退出码速查漏 11**（依赖缺失）
- **参数个数写「20 个」**，实际 argparse 31 个 → 改为「常用参数 + `--help` 看全量」
- **图文等待时长写「最后再等 10s」**，代码是 `wait(6)` × N + `wait(4)` → 改为 4s
- **`stage` 没写不释放 space 的后果** → 补「需手动 `completeTaskSpace`，否则常驻」
- **封面表格少一个 `|`**，整块渲染错乱 → 修正
- **`publish-method.md` 有 4 处已证伪做法**（v1.x 时代的方法论）：
  ① 推荐「CDP 批量 setFileInputFiles + 手动触发 input/change」——实测只留空占位符，正确是 `uploadFile()` 逐张；
  ② 发布判据写跳转 `note-manage`——该路径已 404，主判据是 `published=true`；
  ③ 「正文里的 #话题 会被自动识别」——实际必须从下拉点选；
  ④ 整体流程图标「上传图片（CDP 批量）」。
  前两处就地加 🔴 修正块并说明原因，后两处直接改正；文件头加过期声明与「冲突以 SKILL.md 为准」。

**判定为误报、未改**：frontmatter 超字段（同 video，平台支持且本机多数 skill 如此）；
目录里有 README/CHANGELOG（glic-check 自己也带）；`card-generator/__pycache__/`（`.gitignore` 已覆盖）。

### v2.0.4 (2026-11-10)

文档结构重构（U 维度瘦身）。**SKILL.md 673 → 320 行**，信息零丢失——纯搬家 + 去重。

- **重构**：`## 核心流程` 从 333 行压到 78 行。原 8 步里的 JS 实现片段、选择器、CDP 坐标、
  踩坑展开全部移入新建的 `references/flow-internals.md`（397 行），主文档只保留
  「每步做成了没有」的客观判据 + 一句坑。这是关键改动：那 173 行 JS 是
  `publish_note.mjs`（854 行）的镜像，agent 执行时根本不照着抄。
- **重构**：卡片生成器用法（主题表 29 行、参数表 20 行、图文布局说明）移入
  `references/card-generator-usage.md`，主文档留两条可跑通的示例 + 主题速查 + 链接。
- **去重**：`## 注意事项` 52 → 27 行。**22 条编号原样保留**（正文有「见第 15 条」这类引用），
  已并入核心流程的条目压缩成一句话 + `→ §N` 指路；技术细节型条目（11 废草稿清理 /
  12 发布后无法远程验证 / 13 登录检测判据 / 14 用户接管硬停止 / 22 图片上传三信号）
  的完整成因移入 `flow-internals.md` 的附录。
- **去重**：`## 脚本架构` 23 → 12 行；`## 媒体类型自动判断` 的「两条路径差异」表移入
  `flow-internals.md`（主文档只留判定表、约束与封面规则）。
- **修正**：`Resources` 里 `photo-background.md` 仍写「3 种氛围主题」，实为 4 种。
- **校验**：99 个技术锚点（选择器 / CSS 类 / 正则 / 退出码 / 参数名）逐一比对，
  原文信息 0 丢失；4 个内部文件链接、2 个锚点链接、`见 §N`、`第 15 条` 引用全部可解析；
  代码围栏成对、表格列数一致、注意事项编号连续。

### v2.0.3 (2026-11-10)

UGLIC 审计修复。

- **Fix（假成功）**：`card_generator.py` 渲染失败不传导退出码——`-o <目录>` 时没产出任何 PNG，仍打印「输出: /tmp」并 `exit 0`。现在失败与「文件不存在」都 `exit 1`。
- **Fix**：图文笔记 + `COVER_IMAGE` 会先做文件校验，传个不存在的路径直接 `E_COVER_NOT_FOUND`/exit 10，与文档「图文模式忽略该参数」不符。改为先置空再校验。
- **Fix**：`--text-x-ratio` 配 `anchor=middle` 时文字可能被画布左右裁掉——居中分支补了 `[w/2, 1-w/2]` 边界约束。
- **Fix**：`--text-y-ratio` 落进安全区外时静默无效（0.05/0.10/0.15/0.20 出图完全相同）。现在打一行 stderr 告警并给出实际生效值。
- **Fix**：主题表被一段正文从中间劈开，29 个主题里有 25 行脱离表格、渲染成裸文本。注记已移到表后。
- **Fix**：参数表缺本轮新增的 4 个参数（`--font-main` / `--text-y-ratio` / `--text-x-ratio` / `--text-anchor`），补行并标注默认值与取值域。
- **Fix**：主题数 6 处不一致（README 4 处写 28、SKILL 正文「3 种氛围主题」、`card_generator.py` 注释「= 25 种」）。全部对齐 29 / 4。
- **Fix**：`SEL`/`T` 写「9 个选择器 / 9 个超时（毫秒）」，实际 14 / 8，且 `spaReady` 单位是秒。
- **Fix**：注意事项 #18 说「点草稿箱面板是校验草稿最直接的方式」，#21 说「该入口点了不展开、别再走这条路」。合并为「一律走 IndexedDB」。
- **Fix**：`stage` 没在「收尾模式」里定义（只在代码注释里），且不释放 space。补定义 + cleanup 命令。
- **Fix**：`publish_note.sh` 无条件把 `~/.local/bin` 前置到 PATH，会顶掉调用方自选的 ego-browser（审计时桩脚本就被顶掉、真启动了浏览器）。改为仅在找不到时追加。
- **Docs**：图文示例标注「插画需自备」；`error-handling.md` 的 step 表补 `precheck`。

### v2.0.2 (2026-11-10)

**为历史题材口播视频补卡片能力**（由 `video-multi-release` 的 A1/A2 需求驱动；本 skill 的生成器被跨 skill 复用，故一并版本化）。

- **Feature**: 新增第 29 个主题 `history` —— 暗色电影感配色 + 本机古风书法字体栈，默认 `Baoli SC`（报隶）优先，回退 `Weibei SC Bold` / `Libian SC` / `Kaiti SC`。此前只有 `cinematic`（宋体印刷感），历史题材气质不对。
- **Feature**: 新增 `--font-main` 覆盖参数，优先级高于主题自带字体；`resolve_theme()` 里显式指定的字体不会被主题值覆盖。
- **Feature**: 新增 `--text-y-ratio` / `--text-x-ratio` / `--text-anchor`，文字块会自动 clamp 在顶部标签与底部页码之间的安全区。原来 `start_y` 硬编码垂直居中，与 AI 历史插画的居中主体必然撞车（实测 18 张里 3 张压住人物头部）。
- **Fix**: `anchor=start/end` 且极端 x_ratio 时把起点收进可行域，避免文字块延伸到 1.25W / -0.25W；安全区上下界交叉时不再整段跳过 clamp（原来会压到页脚）。
- **Compat**: 三个位置参数都有默认值，不传时 `start_y` 仍等于改造前的居中值；`--font-main` 不传时不改主题字体。默认路径无回归。
- **Docs**: SKILL.md 主题数 28 → 29、照片背景主题 3 → 4，主题表补 `history`，并写明「位置参数仅 `text` 布局生效」与字体选型实测结论。
- **Validation**: 18 张历史卡片实生成 + 全检联系表逐张复核；`--list-themes` 输出 29 行；`python3 -m py_compile` 通过。

### v2.0.1 (2026-11-09)

**修一个会让整条发布流程白跑的上传判定缺陷**：图文上传连续三次误报 `E_IMAGE_UPLOAD_TIMEOUT`（`cdnImages:6 / editCount:"" / expected:8`），而页面上 8 张图早已全部上传成功，每次都要人工接管收尾。

- **Fix（根因）**: `editCount` 解析失效。旧实现按行找含「图片编辑」的文本行，再 `split('/')[0]` 取数字；但小红书把标签和数字渲染在**两行**（`图片编辑\n8/18`），取到的是标签本身，滤完是空串，`parseInt("") = NaN`，主判据恒不成立，实际只剩 CDN 计数在兜底。
- **Fix**: CDN 计数未排除非内容图。旧实现扫全页 `img[src*=xhscdn.com]`，把用户头像（`sns-avatar-qc.xhscdn.com`）、UI 图（`fe-img-qc` / `growth-img`）一起数进去，数字不可信——实测 3 张图时只数到 2，8 张时数到 6。
- **Feature**: 改为三信号任一命中即通过——① 跨行正则解析「图片编辑 N/18」；② 结构判据，数编辑区里 `textContent === '编辑'` 的叶子节点；③ CDN 计数（已排除 `avatar`）。失败块同时回显 `editCount / editEntries / cdnImages`，便于一眼看出是"真没传上"还是"判定又过时了"。
- **Docs**: SKILL.md 注意事项新增第 22 条，写清两个硬伤的成因、现行判定口径，以及"`editCount` 已达标就不必重跑、直接接管收尾"的排查原则。
- **Validation（stage 模式，3 张图，不发布）**: `images ready: {"done":true,"editCount":"3/18","editEntries":3,"cdnImages":2,"expected":3}`，`✔ upload-media (22044ms)`，全流程 `exit 0`，整轮 43s（修复前在同一步骤 2m41s 后失败）。

### v2.0.0 (2026-11-02)

**主版本号变更原因**：脚本从单文件拆成 `.sh` + `.mjs` 两个文件，只拷贝 `publish_note.sh` 会直接 `E_DEP_MJS` 退出；退出码从「0 / 非 0」细分为 12 档。对外参数（`MEDIA_DIR` / `TITLE` / `BODY` / `TOPICS` / `MODE` / `COVER_IMAGE` / `MEDIA_TYPE`）语义不变，`IMAGE_DIR`/`IMAGES` 别名仍可用。

- **Feature**: draft 模式新增**端到端草稿核对**——直接读浏览器 IndexedDB 的 `draft-database-v1` → `video-draft` / `image-draft`，按 `timeStamp` 取最新一条、递归提取 `title` 字段，与本次标题比对。成功时输出 `draft verified: 标题「…」，保存于 …`，能证明「内容真的存进去了」，而不只是计数 +1。
- **Fix**: 放弃上一版「点草稿箱面板核对」的做法——小红书把草稿入口从左侧栏挪到了右上角 `.header-draft`，点击后不一定展开面板，会导致核对静默失败。IndexedDB 读法不受 UI 改版影响。
- **Validation (真实跑完整流程，draft 模式，不发布)**：
  - 图文 3 张：`exit 0`，`draft count 13→14`，`draft verified: 标题「图文-2.0.0验证」，保存于 2026/11/2 17:57:51（库内共 5 条）`
  - 视频 + 自定义封面：`exit 0`，`draft count 14→15`，封面 CDN URL 变化，`draft verified: 标题「视频-2.0.0验证」，保存于 2026/11/2 17:58:42（库内共 10 条）`
- **Note**: 本 skill 仅作个人工作流维护，**不再发布到 clawhub 与 skillhub.cn**，只同步 GitHub。

### v1.10.0 (2026-11-02)

**运维性重构：稳定 + 可维护 + 失败可续**。功能与 v1.9.0 一致，不改任何对外参数语义。

- **Refactor**: 脚本拆成两层，`scripts/publish_note.sh`（入口层，参数/校验/编排）+ `scripts/publish_note.mjs`（流程层，浏览器操作）。`.mjs` 可单独 `node --check`，不再需要从 bash heredoc 里改 JS。
- **Refactor**: `.mjs` 顶部集中两张表——`SEL`（9 个选择器）、`T`（9 个超时），改版维护只需动这两处。
- **Feature**: 分层退出码。`0` 成功 / `10` 参数 / `11` 依赖 / `20` 登录 / `21` 上传页 / `30` 素材上传 / `40` 填表 / `50` 话题 / `60` 封面 / `70` 提交 / `80` 提交后校验 / `90` 内部异常。agent 可以直接按码判断该重跑还是该找人。
- **Feature**: 结构化失败输出。每个失败点输出 `step / code / exit / message / detail / what_now / space / takeover / cleanup`，`what_now` 是给人看的可执行下一步，不再只有一行 `ERROR: xxx`。
- **Feature**: 失败默认保留现场（`KEEP_ON_FAIL=1`）。失败时 task space 不销毁、页面留着、ownership 转 user，可直接接管排查；新增 `KEEP_ON_FAIL=0` 可关闭。
- **Feature**: 每步耗时打点（`✔ step (1234ms)`），慢在哪一眼可见；每次运行写 `/tmp/xhs-publish-<ts>-<pid>.log`。
- **Feature**: 提交前回读校验——标题写入后读回比对，正文写入后校验长度，避免"看着填了其实没进去"。
- **Feature**: 话题逐个失败重试一次（下拉偶尔不出现），仍失败才整体报 `E_TOPIC_NOT_ATTACHED`。
- **Fix (关键)**: 封面成功判定改为**端到端**——比对操作前后封面缩略图的 CDN URL 是否变化。此前只校验"编辑器弹窗已关闭"，图片未渲染完就点完成时弹窗照样关闭，会误报成功（v1.9.0 的隐患）。
- **Fix**: 不要用 `input.files.length > 0` 判断封面图是否写入——小红书上传组件接收文件后会立刻清空 `input.files`，该检测永远读到 0。改为固定等待渲染 + URL 终检。
- **Fix**: 图文分支 `js()` 模板字符串漏写 `${}`，导致 `filePaths` 变量被当字面量发到浏览器，报 `ReferenceError: filePaths is not defined`。
- **Fix**: `node --check` 校验 `.mjs`；`.sh` 去掉 `set -e`（否则失败时跳过汇总输出），退出码显式透传。
- **Docs**: SKILL.md 新增「脚本架构」「失败处理」两章（含退出码速查、失败块示例、现场接管命令、日志位置）；核心流程改为与 step 名对齐。
- **Fix (UGLIC 审查发现)**: `KEEP_ON_FAIL` 保留的空间 ownership 会变成 `user`，接管必须用 `claimTaskSpace`，但脚本输出和文档此前写的是 `takeOverTaskSpace`（后者只适用于 agent 自己结束、ownership 仍为 agent 的空间）。agent 照做会走死路。已统一改为 `claimTaskSpace` 并说明两者区别，涉及失败块、stage 成功块、登录提示、注意事项第 14 条。
- **Refactor (渐进披露)**: SKILL.md 766 → 651 行。新增两个按需加载的 reference：
  - `references/error-handling.md` — 完整退出码表、全部 code 清单、step 名对照、常见故障判断
  - `references/photo-background.md` — 照片背景卡片章节整体移出（129 行 → 12 行摘要）
  - frontmatter `description` 从 1276 字节压到 738 字节（超 1024 会超出 agent 上下文预算）
- **Chore**: 删除未使用常量 `T.coverApply`；clarify 参数文件路径固定、不可并发跑同一 skill 的两个实例。
- **验证**:
  - 视频 + 自定义封面（stage）：`exit 0`，封面缩略图 URL 由 `...ydCmJYiVd5Q...` 变为 `...nnsDi7LwKuW...`，视觉确认为第 2 张卡片
  - 图文 3 张 + 传入 COVER_IMAGE（stage）：`exit 0`，`cdnImages 6`，启动提示「封面: 忽略（COVER_IMAGE 仅对视频笔记生效）」
  - 参数分支 6 例全部 `exit 10`：缺参数 / 类型未知 / 文件不存在 / 封面不存在 / MODE 非法 / 标题含单引号
  - 两个真实 bug 由这套机制暴露并修复：封面 URL 未变仍报成功、图文 `filePaths` 未定义

### v1.9.0 (2026-11-02)

- **Feature**: 视频笔记支持**自定义封面**。新增 `COVER_IMAGE` 参数（绝对路径），留空则完全保留小红书默认的第一帧。
  - 自动链路：CDP 派发真实 `mouseMoved` 悬停 `.cover` 缩略图 → 点 `.cover-edit-entry`（「编辑封面」）→ 向封面编辑器新出现的 `input[type="file"][accept*="image/png"]` 上传图片 → `scrollIntoView` 后点「完成」→ 校验 `.d-modal.cover-modal` 已关闭。
  - 任一环节失败即 `exit 1` 中止，不会带着错误封面继续发布。
  - `COVER_IMAGE` 仅对视频笔记生效；图文模式传入会在启动提示中标注「忽略」。
  - 失败前已校验：文件存在、扩展名属于图片集合，均在启动浏览器之前完成。
- **Root cause (为什么不能直接点)**：`.cover-edit-entry` 平时 `boundingRect` 为 `0×0`，只有 CSS `:hover` 生效才渲染。`el.click()`、`scrollIntoView`、文本定位全部无效——必须用 CDP 发真实鼠标移动。「完成」按钮在视口外右侧（`innerWidth: 900` 时 `x≈1128`），需先滚动。
- **Fix**: 首屏自动弹出的 `.pk-cover-guide-tooltip` / `.pk-cover-guide` 会遮挡封面区域，脚本进入封面流程前先 `display: none`（纯视觉层，不影响提交数据）。
- **Docs**: SKILL.md 新增 3c「设置视频封面」小节（四步链路 + 选择器对照表 + 校验信号）、注意事项新增第 20 条；快速复用补充 `COVER_IMAGE` 示例。
- **验证**: 22.8s mp4 + `card_05.png` 作封面，stage 模式实测 `Cover result: OK`，回到编辑页封面缩略图显示第 5 张卡片，并出现「✅ 封面效果评估通过，未发现封面质量问题」。

### v1.8.0 (2026-11-02)

- **Feature**: 支持**视频笔记**，并与图文**自动区分**。
  - 新增 `MEDIA_DIR` / `MEDIA_FILES` 参数（`IMAGE_DIR` / `IMAGES` 保留为别名，老调用不破）。
  - 按第一个文件的扩展名判定类型：`.mp4/.mov/.flv/.f4v/.mkv/.rm/.rmvb/.m4v/.mpg/.mpeg/.ts` → 视频；`.png/.jpg/.jpeg/.webp/.heic/.bmp` → 图文。判定与约束校验放在启动浏览器**之前**，失败不产生废草稿。
  - 新增 `MEDIA_TYPE=auto|image|video` 可强制指定类型。
  - 新增视频上传分支：单文件 `uploadFile()` + 转码轮询（「重新上传」+ 标题输入框同时出现即完成，最多 40×3s）；图文分支逻辑保持不变。
  - 约束：视频一次只能 1 个文件，图文最多 18 张，混合类型直接报错。
- **Fix (根因纠正)**: 旧脚本无法用于视频，**不是 ego-browser 升级导致 API 失效**。实测 ego-browser 0.6.2.5 同时提供旧全局函数与新 TaskSpace/Page 两套 API，旧函数（`useOrCreateTaskSpace`/`js`/`fillInput`/`uploadFile`/`completeTaskSpace` 等）全部存在且整条流程可跑通；`ego-browser skill` 指南 v2.1.0 只列新 API 是文档收敛，不是移除。真实原因是脚本三处硬编码只认图文：① 强制点「上传图文」tab；② 选择器 `[accept*=".png"]` 匹配不到视频 input（`accept=".mp4,..."`）；③ 最多 18 张 + CDN 缩略图校验不适用于单视频。
- **Fix (视频页编辑器)**: 图文页与视频页的编辑器现在都是 tiptap ProseMirror（`div.tiptap`）。脚本改为按 `div.tiptap` → `[contenteditable="true"]` 顺序探测，不再写死。
- **Fix (话题错位)**: tiptap 不响应 `Control+End`，光标停在原处会把 `#话题` 插进正文中间（表现为「给同#人生感悟样走在这段路上的人」）。改为每次插入话题前用 Selection API（`selectNodeContents` + `collapse(false)`）显式把光标收敛到末尾。
- **Docs**: SKILL.md 新增「媒体类型自动判断」章节（含两条路径差异对照表）、重写第 2 步为「切换到对应上传 tab」、第 3 步拆为图文/视频两小节、补充 tiptap 光标定位与 `xhs-publish-btn` 拦截指针事件的说明、新增 API 双轨对照表、注意事项新增第 16–19 条（选择器不可混用 / 视频需等转码 / `.header-draft` 需真实点击 / `note-manage` 已 404）。
- **验证**: 两条路径均实测跑通（stage 模式，未提交）——
  - 视频：10.3MB / 22.8s mp4，第 0 次轮询即 `readyState:4` + 「重新上传」出现，标题/正文/2 个话题全部精确挂载。
  - 图文：3 张 2160×2880 png，`图片编辑 3/18`、`cdnImages 6`，标题/正文/2 个话题正常。
  - `bash -n` 语法检查通过；类型误判（.txt）、多视频文件两种错误分支均在启动浏览器前退出。

### v1.7.2 (2026-10-27)

- **铁律（Docs）**: SKILL.md 新增「发布前必读」提醒与「注意事项」第 15 条——**内容严禁出现任何引流信息**：卡片图片、标题、正文、话题中不得出现「微信搜索」「公众号」「加微信」「扫码」等引流文案，也不得放置二维码图片，否则有封号风险；只允许 `@账号名` 软性署名，靠内容质量与评论区互动自然导流。
- **Meta**: frontmatter 补充 `slug` 与 `displayName`（skillhub.cn 发布硬性要求）。

### v1.7.1 (2026-10-09)

- **Fix (root cause)**: `scripts/publish_note.sh` 修复「登录态过期被误判为已登录」导致报错信息误导的根因。
  - 旧判定 `text.includes('登录') && !text.includes('发布')` 在登录态过期时必然误判：小红书登录页导航里同样含「发布」「上传图文」等字样，脚本却认为已登录，继续往下走到`uploadFile()` 才抛 `ElementResolutionError: input[type="file"][accept*=".png"] not found`，真实原因（401）被完全掩盖，排查绕远路。
  - 改为**双重判据**：① `location.href` 不含 `/login`（登录态过期会 302 到 `/login?source=&redirectReason=401&lastUrl=…`）；② 侧栏存在「笔记管理」或「草稿箱」入口。
  - 失败日志同时输出 `reason`（`redirected_to_login` / `no_manage_entry`）与当前 URL，并提示手动登录路径。
- **Docs**: SKILL.md「注意事项」新增第 13 条——登录检测必须用 URL 判定（含正确判定代码块），第 14 条——用户手动登录会触发「用户接管 task space」硬停止，须等用户回复 continue 后用 `takeOverTaskSpace(spaceId)` 接管，不可自行重试或夺回。
- **验证**：`bash -n` + 提取 nodejs 段 `node --check` 通过；已登录真实页面回归测试新判定为 `true`，与旧判定一致无回归。

### v1.7.0 (2026-08-18)

- **Feature**: 新增 **stage 模式**（`MODE=stage`）。用户要求「准备好页面我自己发布 / 不要暂存离开 / 留在页面就行」时走此模式。
  - 上传图片 + 填标题正文 + 挂话题标签后**原地停下**，不触发 `_onSave()` 也不触发 `_onPublish()`。
  - 页面和 task space **保持开启**（不调 `completeTaskSpace`），用户到 ego-browser 中自行检查后手动点发布。
  - 每次执行 `stage` 模式新开一个独立页面（unique task space name + `Date.now()`），互不干扰。
  - 适用场景：用户不信任草稿箱（草稿存浏览器本地不跨设备）、想亲眼确认内容无误后再点发布。

### v1.6.3 (2026-08-18)

- **Docs**: SKILL.md「注意事项」新增第 11 条——重复发布/存草稿会累积「暂无笔记标题」废草稿，并记录清理方法与确认弹窗的**真实删除按钮**选择器。
  - 小红书创作平台每次进入图文编辑页并发生导航/重渲染，会自动存若干空草稿（标题「暂无笔记标题」）；`draft` 模式重跑多篇后草稿箱会堆积大量废草稿。
  - 清理：草稿箱 → 图文笔记 tab → 每个废草稿点 `.draft-actions` 最后一个 `.btn`（删除）→ 确认弹窗。
  - ⚠️ 确认弹窗删除按钮是真实 `<button class="...model-footer-confirm-btn draft-delete-popconfirm-btn-footer-confirm">删除</button>`；点 footer 容器 `<div class="modal-footer-buttons">`（文本也是「取消 删除」）是空操作，不删。文案含「草稿删除后不可找回」。

### v1.6.2 (2026-08-18)

- **Fix (root cause)**: `scripts/publish_note.sh` 修复图片上传「只留空占位符、计数有但图不进编辑器」的根因。
  - 实测发现：即便 v1.6.1 已补 `change` 事件，批量 `DOM.setFileInputFiles`（含逐个串行 CDP `setFileInputFiles`）仍只产生「图片编辑 N/18」的假计数，**编辑器内 `img` 数为 0**，CDN 无真实上传。
  - 真因：小红书上传组件对批量文件输入做特殊拦截，只有走浏览器原生文件选择（`uploadFile()` 单文件循环，每个文件独立触发一次选择）才会真正起传。
  - 改写上传块为 `uploadFile('input[type="file"][accept*=".png"]', fp)` **逐张循环**，每传一张 `wait(6)`；最终 `wait(10)` 等 CDN 回源。实测计数稳定 1,2,3… 递增，发布后 `editCount=10`、`imgCount=11`（10 图 + 加图位）。
  - 选择器统一收敛为 `input[type="file"][accept*=".png"]`（原 `input.upload-input` 偶不命中）。
- **Fix**: 上传校验 + 草稿箱校验改用 `document.body.innerText.split('\n')` 逐行匹配（非正则），`js()` Runtime.evaluate 不支持正则字面量 `/…/`，会抛 "Invalid regular expression: missing /"。通过解析 `图片编辑 N/18` 行取 `editCount`、`草稿箱(N)` 行取草稿数；失败 `ERROR` 退出。
- **Fix**: 全部失败分支 `completeTaskSpace(task.id, { keep: true })` 改为 `{ keep: false }`，避免失败 task space 残留占用；task space 名改为 `'publish xhs note ' + Date.now()` 防用户接管冲突。
- **Docs**: SKILL.md「上传图片」章节重写，明确 `uploadFile()` 单文件循环（替代旧 CDP 批量 + change 事件思路），并把「批量 `DOM.setFileInputFiles` 只留空占位符」列为最高优先级坑点 #9；校验改用 `editCount`（N）+ `xhscdn.com`/`spectrum/` 预览计数。`references/publish-method.md` 同步。
- **Docs**: 修正 v1.6.1 条目中关于「补 change 事件即可修复上传」的表述——实测不充分，v1.6.2 才是真因修复。

### v1.6.1 (2026-08-18)

- **Fix**: `scripts/publish_note.sh` 修复图片上传只留空占位符的问题。
  - `DOM.setFileInputFiles` 设置文件后新增手动触发 `input` + `change` 事件，否则 Vue 不会开始实际上传。
  - 新增上传校验：等待 12 秒后统计 `xhscdn.com` / `spectrum/` 预览图数量，若小于上传张数则报错退出并保留 task space 供排查。
- **Docs**: SKILL.md「上传图片」章节重写，明确 CDP 批量上传必须触发 change 事件并校验 CDN 预览图；注意事项新增「图片上传必须校验」条目。
- **Docs**: 注意事项中进一步强调 draft 模式草稿存于当前浏览器本地、不跨浏览器/设备，只有发布后的笔记才进入账号云端。

### v1.6.0 (2026-08-18)

- **Feature**: 新增**存草稿模式**（draft）。用户要求「存草稿 / 推到草稿箱 / 自己点发布」时走此模式。
  - `scripts/publish_note.sh` 新增 `MODE` 参数：`publish`（默认，直接发布）/` draft`（存草稿箱）。
  - 收尾步骤按 `MODE` 分支：发布调 `host._onPublish()`，存草稿调 `host._onSave()`。
  - 存草稿校验改为「草稿箱(N)」计数 +1（正则 `草稿箱\((\d+)\)`），因为草稿模式页面不跳转。
- **Fix / Pitfall**: 固化已验证坑点——小红书**没有「存草稿」按钮**，发布页右下角文字是「暂存离开」，且同样藏在 `<xhs-publish-btn>` 闭渲染组件内，DOM/坐标/`snapshotText` 全部抓不到；必须直接调实例方法 `_onSave()`。SKILL.md 第 6、7 步与 `references/publish-method.md` 第 7b 节同步记录原理与失败方案对比表。

### v1.5.2 (2026-08-02)

- **Fix**: `card_generator.py` 的 `image-text` 布局 footer 不再固定 `height * 0.82`，而是根据文字块实际底部动态计算，避免账号署名和装饰横线与正文最后一行重叠。
- **Fix**: 卡片底部署名统一为 `@雨夜心灯` 格式。

### v1.5.1 (2026-08-02)

- **Fix**: 话题标签改为从下拉列表真实选中，而非直接粘贴纯文本 `#话题`。
  - `scripts/publish_note.sh` 新增 `TOPICS` 参数（逗号分隔，不带 `#`）。
  - 发布流程：输入正文 → 逐个输入 `#话题` 触发建议下拉 → 点击匹配项（优先精确匹配，否则选首个）→ 完成真正的话题挂载。
  - SKILL.md 同步更新「填写正文与话题标签」章节，说明为什么不能直接粘贴 `#话题`。

### v1.5.0 (2026-08-01)

- **Feature**: 新增**照片背景卡片**功能——支持满幅照片作为底图，文字压在图片上，带暗色遮罩、模糊、降饱和、胶片颗粒等效果。
- **3 个照片氛围主题**：`cinematic`（暗色电影感）、`film`（胶片颗粒）、`journal`（书页氛围）。每个主题预设遮罩强度、颜色、颗粒和降饱和参数。
- **New CLI args**:
  - `--background PATH` — 满幅背景照片路径（`.png`/`.jpg`/`.webp`），自动 center-crop 铺满
  - `--scrim FLOAT` — 暗色遮罩强度 `0–0.92`（默认取主题预设）
  - `--blur FLOAT` — 背景高斯模糊半径（默认 `0`）
  - `--desaturate [FLOAT]` — 背景降饱和 `0–1`；不带值时取 `0.65`
  - `--grain FLOAT` — 胶片颗粒强度 `0–0.4`
- **Auto bright-text reversal**: 非照片主题传入 `--background` 时，文字/辅助色自动反转为亮色，无需手动切换主题。
- **Photo layer stack**: SVG 底层新增 defs（滤镜 + 渐变）→ 照片 image → 暗色渐变遮罩 → 可选颗粒 → 前景投影组。背景图 base64 内嵌，与插画加载逻辑一致。
- **Text shadow filter**: 照片背景下整组前景元素统一加 `feDropShadow` 投影，保证任意画面上文字清晰可读。
- **Scrim gradient**: 暗色遮罩使用线性渐变（上下两端更重），保护顶部标签和底部页脚在亮区照片上仍可读。
- **Total themes**: **28**（25 纯色/渐变 + 3 照片背景）。
- **Docs**: SKILL.md 新增「照片背景卡片」完整章节：工作原理图解、三种主题对比表、CLI 用法示例、Agent 工作流模板。

### v1.4.0 (2026-08-01)

- **Feature**: 新增「图文卡片」布局（`--layout image-text`），与现有「纯文字」布局（`--layout text`，默认）并列可选。
- **Image-text layout**: 顶部插画 + 窄列居中文字（默认宽度 65%）+ 底部署名短横线 + 账号，整体延续温暖简笔哲思风。
- **New theme**: `warm_illust`（温暖简笔哲思），配色与截图示例一致：米白底 `#FAF7F2`、黑线稿、琥珀色 `#D4A84B` 点缀。
- **New CLI args**:
  - `--layout {text,image-text}` — 切换布局
  - `--illustration PATH` — image-text 布局的插画文件（支持 `.svg` / `.png` / `.jpg`）
  - `--image-text-width RATIO` — 文字区宽度占比（0.5–0.8，默认 0.65）
- **SVG illustration handling**: 自动提取 SVG 第一个 `<g>` 元素，移除原 `transform` 后居中放置，避免与卡片坐标叠加偏移。
- **Raster illustration handling**: PNG/JPG 转 base64 data URI，按最大 55% 宽度 / 32% 高度等比缩放（`preserveAspectRatio="xMidYMid meet"`）。
- **Docs**: SKILL.md 与 README 主题画廊更新为 25 种主题，新增图文布局用法示例。

### v1.3.3 (2026-08-01)

- **Audit Fix**: UGLIC + skill-release-audit 两轮审计发现的全部 ERR/WARN 修复。
- **Fix (I1/U1)**: SKILL.md body 版本号 `1.3.0` 与 frontmatter `1.3.2` 不一致 → 统一为 `1.3.3`。
- **Fix (L1/C1)**: 删除 `NODE_BIN`/`NODE_PATH` 死代码（硬编码的用户级绝对路径，全文件无引用）。
- **Fix (L2)**: 清理 `build_svg()` 中废弃的 `gradient_defs`/`gradient_id` 逻辑（SVG 侧渐变从未生效，实际由 CSS 处理）。
- **Fix (U2)**: 删除 4 个 `--show-*` 无操作 CLI 标志（`action="store_true", default=True` 永远为 True），只保留 `--hide-*`。
- **Fix (U3)**: Dependencies 表新增 Google Chrome / Chromium 依赖声明。
- **Fix (I2)**: 删除过期审计报告 `AUDIT-2026-07-31.md`（引用 v1.1.0，未被 SKILL.md 引用）。
- **Fix (I3)**: 删除 `__pycache__/` 构建产物。
- **Fix (C2)**: `render_png()` 改用 `try/finally` 确保临时 HTML 文件在 Chrome 崩溃时也能清理。
- **Fix (audit 模块6)**: 本地 skill 目录补齐 `README.md` 和 `LICENSE`（从 GitHub 仓库同步）。
- **Known**: I4 frontmatter 额外字段 (`version`/`bins`/`metadata`) 保留——ClawHub 发布需要，strict YAML 解析器可能报 warning 但不影响功能。

### v1.3.2 (2026-07-31)

- **Fix**: `doodle` theme font now uses **ZCOOL KuaiLe** (站酷快乐体) from Google Fonts — a playful, rounded Chinese display font that matches the hand-drawn doodle decorations. Previously Caveat/Permanent Marker are Latin-only and silently fell back to system Songti/PingFang, which broke the playful style.
- **Fix**: `steampunk` theme font now uses **Rye** (Western vintage slab) + **Noto Serif SC** from Google Fonts. Previously PingFang SC/Georgia looked too clean and modern for the dark brass/gear aesthetic; the new combination gives a vintage print feel consistent with steampunk.
- **Docs**: README theme preview images regenerated for doodle and steampunk to reflect the new typography.

### v1.3.1 (2026-07-31)

- **Fix**: XiaoHongShu style now has **two distinct modes** as originally documented in `text-to-elegant-image` repo: `xhs` = clean/formal mode, `xhs_rich` = lively/rich mode. Previously only the clean variant was implemented.
- **Mode A (`xhs`)**: white background + faint 45° red pinstripes + minimal dot accents — high breathing room for knowledge notes.
- **Mode B (`xhs_rich`)**: warm-pink gradient + hand-account dot pattern + glassmorphism blobs + three-segment gradient wave line — playful life-guide feel.
- **Total themes**: **24** (18 repo styles, with xhs split into A/B + 4 young-people + 1 warm original).
- **CLI**: added `--list-themes` to print all 24 themes and their display names.
- **Docs**: SKILL.md theme table updated to reflect all 24 themes and xhs/xhs_rich distinction.

### v1.3.0 (2026-07-31)

- **Breaking**: Port ALL 18 styles from `text-to-elegant-image` repo into the unified card generator. Total themes: **23** (18 repo + 4 young-people + 1 warm original).
- **Themes added**: cyberpunk, elegant, apple, cowork, newspaper, bloomberg, ink, steampunk, xhs, morandi (upgraded), glass, palace (upgraded), fresh, earthy, dreamy, macaron, carbon, vivid.
- **Each theme** extracts original repo's color palette, font stack, Google Fonts declaration, and decorative elements — all adapted to the unified layout (tag + centered text + footer).
- **Decorations**: 15 unique decoration styles (grid lines, scan lines, ink splashes, gears, glass blobs, leaves, sparkles, dots, etc.) — each theme has its own visual signature.
- **Google Fonts**: Themes requiring special fonts (palace: Ma Shan Zheng + ZCOOL XiaoWei; morandi/glass/fresh/earthy/dreamy/macaron/carbon/vivid: Inter; doodle: Caveat + Permanent Marker) all load via multi-mirror CDN fallback.

### v1.2.7 (2026-07-31)

- **Fix**: Remove the horizontal line above subtitle text in all themes. Subtitle now displays as `— 副标题 —` without the extra separator line above it, matching the user's reference screenshot style more closely.

### v1.2.6 (2026-07-31)

- **Feature**: Multi-mirror Google Fonts fallback for China network — `build_html()` now generates `<link>` tags for 3 CDN sources simultaneously: `fonts.loli.net` (community mirror), `fonts.googleapis.cn` (Google official China mirror), `fonts.googleapis.com` (original). Browser uses whichever loads first.
- **Feature**: JS-based font loading detection — after 3s timeout, checks `document.fonts.check()` for each declared font; if not loaded, dynamically injects mirror CSS as last resort
- **Why**: Google Fonts CDN (`fonts.googleapis.com`) is frequently blocked or extremely slow in mainland China, causing Chrome headless to fall back to system fonts and ruin theme-specific typography (e.g., palace theme falling back to Songti instead of Ma Shan Zheng calligraphy)

### v1.2.5 (2026-07-31)

- **Feature**: Google Fonts CDN loading in `build_html()` — themes declare `google_fonts` list, HTML auto-generates `<link>` tags to load fonts from `fonts.googleapis.com` regardless of local installation
- **Feature**: Add `palace` theme (故宫金红) — uses Ma Shan Zheng + ZCOOL XiaoWei calligraphic fonts from Google Fonts, gold-on-dark-red palette, corner ornaments and seal stamp decoration
- **Feature**: Add `morandi` theme (莫兰迪灰) — uses Inter from Google Fonts, desaturated muted palette
- **Improvement**: `doodle` theme now loads Caveat + Permanent Marker from Google Fonts for authentic hand-drawn feel
- **Fix**: Chrome `--virtual-time-budget=10000` added to ensure web fonts are fully loaded before screenshot capture
- **Architecture**: Every theme has `google_fonts` field (empty list = system fonts only), preventing silent fallback to wrong fonts

### v1.2.4 (2026-07-31)

- **Fix**: Card generator now auto-scales font size based on text length and line count to prevent overflow/cropping
- **Improvement**: Theme-specific font stacks for better style matching
  - `warm`/`minimal`: Songti SC serif (elegant/warm)
  - `y2k`: geometric sans-serif (tech/cool)
  - `doodle`: Chalkduster/Bradley Hand/Marker Felt with Kaiti fallback (hand-drawn feel)
  - `pop`: bold sans-serif (energetic)

### v1.2.3 (2026-07-31)

- **Feature**: Add built-in card generator (`references/card-generator/card_generator.py`) with 5 themes
  - `warm`（温暖哲思）、`minimal`（极简日系）、`y2k`（Y2K 千禧潮酷）、`doodle`（手绘涂鸦）、`pop`（渐变波普）
- **Feature**: Unified card layout matching classic XHS quote card style: top tag + quote marks, centered large text, bottom divider, page number and account
- **Feature**: Customizable footer parameters: `--hide-page-number`, `--hide-account`, `--hide-tag`, `--hide-subtitle`, `--page-number`, `--total-pages`, `--account`
- **Documentation**: Add card generation usage to SKILL.md

### v1.2.2 (2026-07-31)

- **Fix**: Support both UI entry points for entering image note page — try top "上传图文" tab first, fall back to "发布笔记" dropdown menu. Uses `input.upload-input` presence as the success check.
- **Fix**: Correct v1.2.0 changelog — both top tab and dropdown menu are valid, not a UI deprecation

### v1.2.1 (2026-07-31)

- **Fix**: Frontmatter dependency declaration for skill-release-audit
  - Add `bins: [ego-browser, node]`
  - Move env vars to `metadata.openclaw.requires.env`

### v1.2.0 (2026-07-31)

- **Fix**: Add support for top "上传图文" tab as an alternative entry point (both tab and dropdown menu work)
- **Fix**: Update publish success verification to also recognize `published=true` URL parameter
- **Fix**: Increase post-upload wait from 8s to 10s for more reliable image processing

### v1.1.0 (2026-07-31)

- **Security**: Fix shell variable injection risk in `publish_note.sh` — all user parameters now passed via `process.env` instead of shell heredoc expansion
- **Documentation**: Add formal Dependencies section with installation instructions and verification steps
- **Documentation**: Add reference load timing guidance for `references/publish-method.md`
- **Documentation**: Strengthen guardrail statements (advisory → mandatory)
- **Documentation**: Update Repository URL to multi-skill repo `better-office-work-flow`
- **Documentation**: Add input validation for TITLE (no single quotes) and BODY (no backticks/`${`)

### v1.0.0 (2026-07-31)

- Initial open-source release
