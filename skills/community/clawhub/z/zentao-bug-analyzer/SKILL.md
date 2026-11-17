---
name: zentao-bug-analyzer
description: "禅道缺陷自动分析：从飞书消息解析Bug链接，自动模块分类+分支定位+代码分析，Playwright评论+飞书通知双通道输出。"
---

# 禅道缺陷自动分析 (zentao-bug-analyzer)

禅道实例：`http://zentao.gxatek.com:20080/`（企业版 12.1）

## 环境依赖

本 Skill 依赖以下工具，**环境不具备时立即停止流程并飞书通知用户**，禁止用替代品硬撑：

| 工具 | 用途 | 安装方式 | 验证命令 |
|------|------|----------|----------|
| **ffmpeg** | 视频附件抽帧（步骤 4b） | `npm install @ffmpeg-installer/ffmpeg ffprobe-static --no-save` | `node -e "console.log(require('@ffmpeg-installer/ffmpeg').path)"` |
| **Node.js zlib** | 解压 Android logcat `.gz` 日志（步骤 4c） | Node.js 内置，无需安装 | `node -e "require('zlib')"` |
| **Playwright** | 禅道交互（5 个 scripts） | 已有 | — |
| **视觉模型** | 读取截图/视频帧中的系统时间 + 判断画面中 BUG 现象是否可见（步骤 4b 子步骤 3、4） | 由 AI 代理运行环境提供 | — |

**禁止的替代方案**：
- ❌ 用 winget 装系统级 ffmpeg（实测 `winget install Gyan.FFmpeg` 超时不可靠）
- ❌ 用 PowerShell `tar`、`System.IO.Compression.GZipStream` 或 .NET 工具解压 logcat `.gz`（兼容性 bug，会丢失大量日志）
- ❌ 用 PowerShell/.NET 替代品处理视频（参考 4c 关于 .NET 解压 bug 的教训）

> ⚠️ **视觉模型不可用时**：步骤 4b 子步骤 3、4 无法读取截图/视频帧中的系统时间，降级为跳过图片/视频时间提取，直接进入子步骤 5 飞书询问用户。

**首次运行检查**：执行任何分析前先验证 ffmpeg 可用：
```bash
node -e "const ff=require('@ffmpeg-installer/ffmpeg');const{execSync}=require('child_process');execSync(`\"${ff.path}\" -version`);console.log('ffmpeg OK')"
```
失败 → 飞书私聊通知「ffmpeg 环境依赖缺失，请运行 `cd {workspace} && npm install @ffmpeg-installer/ffmpeg ffprobe-static --no-save` 后重试」，流程终止。

## ⚠️ 执行守则（最高优先级）

> 🔴 分析前必须先读完 `SKILL.checklist.md` 的全部检查项，每条逐项完成。

1. **只用 scripts/ 下的 5 个可执行脚本操作禅道**（不含 `zentao-utils.js` 工具模块），禁止手写临时 Playwright 文件
2. **一个 Bug 只启动一次浏览器**，所有操作复用同一 WS endpoint
3. **脚本报错 = 诊断脚本的输入条件**（WS 是否有效？参数是否正确？），不是另起炉灶的理由
4. **分析完成后保持仓库不动**：`git checkout <commit-id>` 分析完后不切回原分支（非 worktree 场景）。worktree 场景按步骤 6 清理。
5. **分析完输出报告**：步骤 4d 产出分析报告后，根据 `auto_comment` 配置决定是否评论禅道：
   - `auto_comment === true` 或未配置（默认视为 `true`）：运行 `zentao-post-comment.js` 评论 + 飞书摘要
   - `auto_comment === false`：仅飞书摘要，不评论禅道
6. **环境依赖缺失立即停止**：ffmpeg / Node.js zlib / Playwright 任一不可用 → 飞书通知用户安装，禁止用替代品硬撑（详见「环境依赖」章节）
7. **Windows 读取中文文件必须用 Node.js，禁止 PowerShell `Get-Content` / `Select-String`**：
   - Windows PowerShell 控制台默认 GBK（CP936）编码，读取 UTF-8 中文文件直接显示乱码
   - ❌ 禁止：`Get-Content xxx.txt -First 5`、`Select-String -Path xxx.txt -Pattern "中文"`、`Get-ChildItem | Where-Object Name -like '*.中文.txt'`
   - ✅ 必须：`node -e "console.log(require('fs').readFileSync('xxx.txt','utf8').slice(0,500))"`
   - 涉及场景：读取日志中的中文 TAG、中文注释、报告 review 时的中文文件名/路径、PowerShell 调用 `node script.js --video=中文.mp4` 时加 `--` 分隔符规避 argv 解析 bug
   - 例外：`Get-Content` 加上 `-Encoding UTF8` 参数可以读 UTF-8（输出仍可能乱码，但不会被识别为 ANSI）；推荐一律走 Node.js

## 触发方式

### 方式一：邮件转发触发
飞书 Bot 收到包含禅道 Bug 链接的消息时自动触发。

正则模式：`zentao\.gxatek\.com:20080/bug-view-(\d+)\.html`

### 方式二：自然语言触发
用户直接在飞书对话中：
- 发送禅道 Bug 链接
- 「帮我分析我名下所有未解决的缺陷」
- 「分析最近 3 天指派给我的严重缺陷」

**批量分析**：批量触发时，先通过 Playwright 会话查询 Bug 列表，每个 Bug 独立走完整流水线。不同 Bug 按第三章并发规则处理。

**无有效链接时**：飞书私聊回复「未识别到有效的禅道缺陷链接，请确认消息内容」。

---

## 配置文件

依赖 `{workspace}/bug-analyzer-config.json`。

```jsonc
{
  "zentao": {
    "url": "http://zentao.gxatek.com:20080",
    "account": "wyhe",
    "password": "你的禅道登录密码"
  },
  "notify": {
    "feishu_open_id": "飞书私聊通知目标用户 Open ID，步骤 3/4b 等所有飞书通知场景使用"
  },
  "auto_comment": true,
  "modules": [
    {
      "name": "车机设置",
      "aliases": ["桌面卡片", "设置", "systemui", "SystemUI"],
      "code_dir": "D:/code/car-settings",
      "commit_extract": "日志中以 'Build commit:' 开头的那一行，取后面的 8 位 hash",
      "analyzer": "default",
      "analyze_hint": "重点关注桌面卡片相关代码，常见问题是侧滑返回时的 Activity 生命周期处理"
    },
    {
      "name": "蓝牙模块",
      "aliases": ["蓝牙", "BT", "bluetooth", "bt-stack"],
      "code_dir": "D:/code/bt-stack",
      "commit_extract": "日志里搜索 'git_hash='，取等号后面的完整 hash",
      "analyzer": "default",
      "analyze_hint": "蓝牙相关缺陷通常与连接状态机有关，优先检查 BluetoothManager 的状态流转"
    }
  ]
}
```

字段说明：
- `name`：模块名称
- `aliases`：模块别名列表（字符串数组），用于精确匹配。**匹配规则**：将 Bug 的 title、module.name、product.name 与所有模块的 name + aliases 做**子串匹配**（忽略大小写），任一命中即判定为该模块。此规则为硬规则，优先于 AI 主观判断
- `code_dir`：模块本地代码仓库绝对路径
- `commit_extract`：自然语言，告诉 AI 如何从日志提取 commit id
- `analyzer`：`"default"` | `"skill:技能名"`。default 走通用 AI 分析流程；skill:xxx 委派给对应 Skill
- `analyze_hint`：模块专属分析提示词（可选），无论哪种分析器都会传给分析器

> ⚠️ `auto_comment` 是**根级别**字段（与 `zentao`、`notify`、`modules` 平级），控制全局行为。非 module 级别字段。

### 首次配置引导

配置文件不存在时启动对话式引导。流程：

1. 「请提供禅道的登录账号和密码（用于 Playwright 登录禅道。密码会存储在本地配置文件中，不会泄露）」
2. 「你负责哪些模块？请列出模块名称（用逗号分隔，如：车机设置, 蓝牙模块, 语音助手）」
3. 对每个模块依次询问：
   - 「对于"{模块名}"模块，有哪些别名/关键词可以用来识别？（用逗号分隔，如：桌面卡片, systemui, 设置）」
   - 「对于"{模块名}"模块，本地代码目录路径是什么？（请使用绝对路径）」
   - 「对于"{模块名}"模块，日志中如何提取 commit id？请用自然语言描述提取规则」
   - 「对于"{模块名}"模块，是否需要使用专用分析 Skill？（目前可用的 Skill：[列出]。输入 Skill 名或留空走默认分析）」
   - 「对于"{模块名}"模块，有什么分析提示或重点关注方向？（可选，留空则用默认分析策略）」
4. 「分析完成后，是否需要自动将分析报告评论到禅道 Bug 下？（回复"是"=自动评论，"否"=仅飞书通知，不评论禅道）」
5. 「配置完成！请确认你已创建邮件收信规则：当发件人为 `zentao@syncore.space` 时，自动将邮件转发/分享到本 Bot 的对话中。」

---

## 分析流水线

### 步骤 1：消息解析

从消息内容提取禅道 Bug 链接，正则：`zentao\.gxatek\.com:20080/bug-view-(\d+)\.html`

### 步骤 2：重复分析检查

> ⚠️ 此步骤是强制检查点，无论通过哪种触发方式（邮件转发或自然语言）进入分析流水线，必须先走步骤 2。已评论过的 Bug 绝对不允许直接进入后续步骤。

1. 运行 `scripts/zentao-login.js` 登录禅道，获取 WS endpoint（后续所有脚本复用此 endpoint）
2. 运行 `scripts/zentao-get-bug.js` 获取 Bug 详情（含评论列表 `comments` 字段，后续步骤复用）
3. 检查 Bug API 返回的 `comments` 数组中是否已有 `zentao.account` 配置账号的评论（`comments[].author` 字段，不是 `historyChanges` 操作历史）

**已有我的评论**：飞书私聊询问「该 Bug 你已评论过，是否需要重新分析？（回复"是"或"分析"继续，回复"否"或"取消"跳过）」
- 确认「是」→ 继续步骤 3
- 确认「否」或 5 分钟内未回复 → 流程终止

**没有我的评论**：直接继续步骤 3。

### 步骤 3：模块分类

**匹配规则（优先级从高到低）**：

1. **硬别名匹配（优先）**：遍历配置中每个 module 的 `aliases` 数组，将每个别名与 Bug 的 `title`、`module.name`、`product.name` 做**子串匹配**（忽略大小写）。只要任一副本字段包含任一个别名（或 `name` 本身），即判定命中该模块。
   - 例如：Bug标题含"桌面卡片"，配置别名中有"桌面卡片" → 直接命中
   - ⚠️ 此规则是机械规则，不依赖 AI 判断，直接执行
2. **AI 语义判断（兜底）**：硬别名未命中时，AI 综合判断 Bug 归属模块，对照配置文件 `modules` 列表

**结果处理**：
- **在范围**：继续步骤 4
- **不在范围**：飞书私聊通知（Bug 标题、链接、AI 判断的模块归属），提醒模块确认和手动流转。流程结束
- **置信度低**：飞书私聊通知（Bug 链接 + 关键信息），告知无法确定模块，请手动确认。流程结束

### 步骤 4：深度分析

#### 4a. 下载附件和日志
运行 `scripts/zentao-download-files.js` 下载 Bug 所有附件到 `bugs/{bug_id}/`。（script 自动处理大文件分块传输，支持 160MB+ 附件）

> ⚠️ 步骤 4a 完成后必须先执行 4b（确定 Bug 发生时间），再进入 4c。

#### 4b. 确定 Bug 发生时间

> ⚠️ 硬约束：Bug 发生时间必须从可靠来源直接获取，禁止猜测或间接推断。
> 此步骤是 4c 分支定位的前置条件，时间不准会导致日志定位、Git blame 全部偏移。
> **经过 3 个真实 Bug 视频（1443538/1443544/1443665）验证**：Android 车机录屏状态下状态栏只显示 HH:MM（无秒），且相机外拍场景下状态栏经常被遮挡；这些坑必须显式处理。

**时间来源优先级（一旦确定后不要再换）**：
1. **Bug 描述文本中明确记录的时间**（steps / description 字段中出现的 `HH:MM[:SS]` 或 `YYYY-MM-DD HH:MM[:SS]` 格式）
2. **设备系统状态栏**（手机/车机屏幕顶部实时时间）
3. **录屏工具水印**（仅参考，水印时钟与设备时钟不同步是常见 bug）
4. **相机水印 / 文件名时间戳**（仅参考）
5. **飞书询问用户**（兜底）

**禁止行为**：
- ❌ 使用**附件文件名中的时间戳**作为时间来源（仅可辅助佐证）
- ❌ 使用 **Bug 创建时间 / 最后修改时间**作为时间来源
- ❌ 使用**聊天消息转发时间 / 邮件接收时间**作为时间来源
- ❌ 使用**附件上传时间、附件最后修改时间**作为时间来源
- ❌ 在多个来源冲突时擅自挑一个，必须飞书通知用户选择
- ❌ 在状态栏只读到 HH:MM 时强行猜测秒数
- ❌ 在视频、描述、用户三处都拿不到时间时，用以上任何间接来源凑数

**子步骤 1：从 Bug 描述文本提取**
- 解析 Bug `steps` 和 `description` 字段，匹配 `HH:MM[:SS]` 或 `YYYY-MM-DD HH:MM[:SS]` 格式
- 命中即记录为「描述时间」，进入子步骤 5 的交叉校验
- 没命中 → 进入子步骤 2

**子步骤 2：枚举附件并按类型分流**

读取步骤 4a 下载到 `bugs/{bug_id}/` 的附件列表，按 MIME/扩展名分流：
- **图片类**（`.jpg/.jpeg/.png/.webp/.bmp`）→ 子步骤 3
- **视频类**（`.mp4/.mov/.mkv/.avi/.webm/.3gp`）→ 子步骤 4
- **其它** → 跳过，进入子步骤 5

**子步骤 3：图片附件直接读取时间**

对每张图片文件，使用视觉能力读取画面中的系统时间（将图片文件路径作为输入，视觉模型自动解析画面内容），**按优先级寻找以下区域**：
1. **状态栏右上角**（Android 系统时间显示区，最常见）
2. **状态栏左上角**（部分 ROM 习惯）
3. **录屏水印**（很多测试工具会在画面角落叠加时间戳）
4. **锁屏/通知面板**（如截图包含）

读取规则：
- 接受 **HH:MM 精度**（不强求秒，Android 车机录屏**通常只显示到分钟**）
- 必须输出**时间所在画面区域**（例如「右上角状态栏」「左下角水印」），便于人工复核
- 同一 Bug 多张图片时，记录**每张图片独立读出的时间**，不要直接合并
- 读不出 → 标记「图片无可见时间」，继续下一张
- ⚠️ **水印与状态栏冲突时，以状态栏为准**（实测验证：水印时钟经常和设备时钟不同步，例如 1443665 视频水印年份显示 `2026`，状态栏为正确日期）

**子步骤 4：视频附件抽帧 + 视觉读取**

> ⚠️ 视频不能直接送视觉模型（容量大、模型处理不了连续帧），必须先抽帧。
> ⚠️ 工具依赖：本 Skill **强制依赖 ffmpeg**（详见 SKILL.md 开头「环境依赖」章节）。必须使用 `npm install @ffmpeg-installer/ffmpeg ffprobe-static` 提供的 ffmpeg（动态路径通过 `node -e "console.log(require('@ffmpeg-installer/ffmpeg').path)"` 获取），**禁止用 PowerShell/.NET 替代品处理视频**（参考 4c 关于 .NET 解压 bug 的教训），禁止用 winget 装系统级 ffmpeg（实测 winget 装 Gyan.FFmpeg 超时不可靠）。

**▸ 粗扫：确认视频里有没有可见 BUG**

> 🆕 此步是前置门槛（验证坑 #4：部分 Bug 视频里根本看不到 BUG 现象）。

1. 用 2 秒 1 帧抽帧（约视频时长一半的张数，80 秒视频约 40 张）：
   ```bash
   node scripts/zentao-extract-frames.js --video=<视频路径> --dir=bugs/{bug_id}/frames --mode=coarse
   ```
   > 💡 PowerShell 调用时建议加 `--` 分隔符以规避 argv 解析 bug：`node scripts/zentao-extract-frames.js -- --video=xxx.mp4 --mode=coarse`。脚本同时支持 `--key=val` 和 `--key val` 两种参数形式。
2. 视觉模型扫一遍所有粗帧（将 `coarse_*.png` 文件逐个传入，每次不超过 20 张），判断**画面里有没有 BUG 现象**（错误提示、卡死、空白、花屏、异常弹窗等）
3. **看得到 BUG** → 进入 4b 精抽
4. **看不到 BUG** → 视频是「正常录屏，BUG 由其它渠道复现」（日志/用户描述），**跳过视频读时间，直接进入「交叉校验 + 落盘」步骤飞书询问用户**
   - 在报告里记录「视频未观察到 BUG 现象，跳过视频时间提取」

**▸ 精抽：1 秒 1 帧抽全片**

确认有 BUG 后，抽出全片每秒 1 帧：
```bash
node scripts/zentao-extract-frames.js --video=<视频路径> --dir=bugs/{bug_id}/frames --mode=fine
```
> 💡 PowerShell 调用同样推荐加 `--` 分隔符（详见上面粗抽步踩说明）。

> 🔴 不要一次送视觉模型超过 20 张（实测 OpenClaw `image` 工具多张时延不可控）。建议**关键区间（BUG 前后 ±10 秒）1 秒 1 帧抽满后才送视觉模型**，不要全片无脑送。

**▸ 读时：状态栏时间 + 处理遮挡**

视觉模型读取每帧，**优先级**：
1. **设备状态栏**（最高优先，记录 HH:MM）
2. **录屏水印**（仅参考，与状态栏冲突时以状态栏为准）
3. 两者都不可见 → 标记「该帧状态栏不可见」，读前后相邻帧推断大致时间窗

> 🆕 验证坑 #1：状态栏只显示 HH:MM，无秒。**接受 HH:MM 精度**，秒数由日志/描述交叉校验得到，不要强行猜测。
> 🆕 验证坑 #2：相机外拍场景下，状态栏经常被遮挡（实测 1443544 前 3 秒、1443538 BUG 关键帧都被遮挡）。**被遮挡的帧跳过状态栏，只读水印或前后帧推断**。

**▸ 输出：候选时间 + 证据**

视频起始帧、BUG 首次出现帧、BUG 消失帧各读一次时间，记录到：
- 候选时间（HH:MM）
- 对应的帧文件名（例如 `sec_0060.png`）
- 时间所在画面区域（「右上角状态栏」「左下角水印」「被遮挡」）

**子步骤 5：交叉校验 + 落盘**

把子步骤 1~4 得到的所有候选时间汇总：
1. **至少 2 个独立来源时间吻合**（例如描述 + 视频起始帧；或视频起始帧 + 结束帧差值符合视频时长）→ 采纳为「Bug 发生时间」
2. **只有一个来源** → 采纳，但报告里标注「单一来源，建议人工复核」
3. **多个来源冲突** → 飞书通知列出所有候选时间让用户选，**不要自己挑一个**
4. **全部子步骤都没拿到时间** → 飞书私聊询问「该 Bug 发生的精确时间是什么？」

**最终落盘**：
- 在 `bugs/{bug_id}/.time-metadata.json` 写入结构化元数据（供步骤 4d 读取并输出到报告）：
  - 采纳的时间（含时区，默认 `Asia/Shanghai`）
  - 时间来源（例如「视频 sec_0060.png 右上角状态栏」）
  - 证据文件路径（相对 `bugs/{bug_id}/`）
  - 置信度（高/中/低）
- 步骤 4d 的日志分析窗口**直接以这个时间为中心 ±5 分钟**，不再二次推断
- ⚠️ 此步骤不直接写 `report.md`——`### Bug 发生时间` 章节由步骤 4d 统一下读取 `.time-metadata.json` 后输出

#### 4c. 分支定位
1. 解压并读取日志文件：
   - Android logcat 的 `.gz` 文件**必须使用 Node.js zlib 解压**。⚠️ 禁止使用 PowerShell `tar` / `System.IO.Compression.GZipStream` 等 .NET 解压工具（兼容性 bug 详见「环境依赖」章节）。推荐命令：
     ```bash
     node -e "const zlib=require('zlib');const fs=require('fs');const buf=fs.readFileSync('<log.gz>');zlib.gunzip(buf,(e,r)=>{if(e){console.error(e);return}const s=r.toString('utf8');/* 搜索 s */})"
     ```
2. 按配置中 `commit_extract` 从日志提取 commit id
3. `cd {code_dir}` → `git branch --contains <commit-id>` 确认 commit 在哪些分支上。结果写入分析报告的「分支信息」字段（格式：`分支名 | commit-id`）
4. 分支检出（根据仓库占用情况二选一）：
   - **仓库空闲**（无其他 Bug 分析占用）：`git checkout <commit-id>`（进入 detached HEAD 是正常行为，分析完成后保持不动即可）+ `git submodule update --init --recursive`
   - **同模块已有其他分析任务占用**：`git worktree add .claude/worktrees/bug-{bug_id}/ <commit-id>` 创建隔离工作区，在 worktree 内执行 `git submodule update --init --recursive`

**commit id 提取失败**：飞书私聊通知（附带日志片段），流程终止。

> ⚠️ 硬约束：只使用配置中 commit_extract 指定的提取规则，禁止 AI 自行更换搜索关键词（如换 TAG、换正则）。搜不到就是搜不到，不允许"近似匹配"或"换成类似的 TAG 试试"。
> Self-Check：若在分析过程中进行了 commit_extract 规则以外的额外搜索，应立即停止、丢弃中间产物，回到步骤 4c 标准路径并报告提取失败。

**commit id 不在任何分支**：飞书私聊通知（附带 commit id），流程终止

> ⚠️ 硬约束：`git checkout <commit-id>` 后必须执行 `git submodule update --init --recursive`，确保所有 submodule 都已 checkout 到对应版本。未 checkout submodule 可能导致分析时缺少依赖代码、漏掉跨仓库 API 不一致问题。

#### 4d. AI 综合深度分析

历史评论已在步骤 2 获取（Bug API 的 `comments` 字段），操作历史（`historyChanges`，包含状态流转、指派人变更、优先级调整等记录）同样已在步骤 2 由 `zentao-get-bug.js` 提取，此处直接使用。

根据 `analyzer` 字段：
- `"default"`：AI 综合 Bug 详情 + 附件/日志 + 历史评论 + 本地代码分析
- `"skill:xxx"`：委派给指定 Skill，传入分析上下文

无论哪种方式，`analyze_hint` 都作为上下文传入。

分析时读取 `bugs/{bug_id}/.time-metadata.json` 中步骤 4b 确定的 Bug 发生时间，以该时间为中心 ±5 分钟缩小日志分析范围，聚焦根因定位。

输出格式（Markdown，AI 直接产出此结构）：

```markdown
### Bug 发生时间
- **采纳时间**：yyyy-MM-dd HH:mm (Asia/Shanghai)
- **时间来源**：视频 sec_0060.png 右上角状态栏
- **证据文件**：frames/sec_0060.png
- **置信度**：高/中/低

### 分支信息
- **commit**: `abc12345`
- **分支**: `branch/name`

### 操作历史（如有）
- **状态流转**：active → resolved → closed
- **关键变更**：指派人 / 优先级 / 严重程度的变更记录

### 根因定位
- **文件**：`path/to/file.ext:行号`
- **代码片段**：
  ```lang
  // 关键代码
  ```
- **判断依据**：（结合日志/历史评论/代码逻辑的推理过程）

### 修复建议
1. 具体修复方向（可操作步骤，非抽象建议）

### 风险评估
- **影响范围**：（哪些功能/模块受影响）
- **严重程度**：（低/中/高/严重 + 理由）
```

### 步骤 5：结果输出

> ⚠️ **auto_comment 开关**：步骤 4d 已产出 `bugs/{bug_id}/report.md`（无论 `auto_comment` 取值，分析报告始终生成到本地）。步骤 5 仅决定是否将报告发布到禅道：
> - `auto_comment === false`：跳过禅道评论（步骤 5.1），仅生成 `report.md` + 执行飞书私聊通知（步骤 5.2）
> - `auto_comment === true` 或未配置：执行完整双通道（禅道评论 + 飞书通知）

1. **禅道评论**（仅在 `auto_comment !== false` 时执行）：
   a. 确认 `bugs/{bug_id}/report.md` 已生成（步骤 4d 产出），按步骤 4d 输出格式
   b. 运行 `node scripts/zentao-build-comment.js bugs/{bug_id}/report.md --out bugs/{bug_id}/comment.html` 生成 HTML
   c. 运行 `node scripts/zentao-post-comment.js --ws=<wsEndpoint> --bug-id=<id> --comment-file=bugs/{bug_id}/comment.html` 发布（**必须用 `--comment-file`，禁止用 `--comment` 传 HTML 内容**）
   d. ⚠️ `--comment` 参数仅用于极简手动测试（单行纯文本），生产环境严禁使用——shell 转义和 HTML 特殊字符会导致内容截断或损坏
   e. ⚠️ 禁止手写临时 Playwright 脚本发布评论
2. **飞书私聊**：简要摘要 + 禅道 Bug 链接

### 步骤 6：清理

分析完成后必须清理残留进程，避免占用系统资源：

1. **杀掉 login 常驻进程（连带 Chrome）**：
   - Windows: `taskkill /PID <login-PID> /F /T`
   - macOS/Linux: `kill -9 <login-PID> && pkill -P <login-PID>`（精准终结子进程树，避免误杀用户其他 Chrome 实例）
   - PID 来自 `zentao-login.js` 输出行 `PID=<value>`（Node.js 进程 PID，`/T` 或 `pkill -P` 会连带终结 Chrome 子进程树）
2. **清理 git worktree**：`git worktree list` 检查是否有 `.claude/worktrees/bug-{bug_id}/` 残留，有则 `git worktree remove --force .claude/worktrees/bug-{bug_id}/`
3. **检查残留脚本进程**：
   - Windows: `Get-Process node` 检查是否还有 `zentao-*.js` 相关进程
   - macOS/Linux: `ps aux | grep 'zentao-' | grep -v grep`
   - 有则 `taskkill /F /PID <pid>`（Windows）或 `kill -9 <pid>`（macOS/Linux）
4. **确认清理完毕**：最终应只剩 OpenClaw 自身的 node 进程（gateway/worker），不应有其他 `zentao-*.js` 残留

> ⚠️ 注意：不要杀掉 OpenClaw 自身的 node 进程（gateway/worker），只清理 `zentao-*.js` 和 Chrome headless 相关进程。

---

## 并发处理

- **不同模块**：代码目录不同，全部并行处理
  - ⚠️ 并行时每个 Bug 需要独立的 CDP 端口，通过 `zentao-login.js --port=<不同端口>` 避免冲突（如 `--port=9224`、`--port=9225`、`--port=9226`）
- **同一模块同时分析多个 Bug 时**：用 `git worktree` 为每个 Bug 创建隔离工作区，分析完成后 `git worktree remove` 清理
- **并发清理**：每个 Bug 分析完成后各自执行步骤 6 清理自己的 login 进程和 worktree，最后确认所有端口对应的 `zentao-*.js` 进程均已终止

---

## 禅道交互方式

> ⚠️ 企业版 12.1 不支持 Bearer Token 认证（`POST /api.php/v1/tokens` 不可用），所有读写操作统一走 Playwright。

### 🔴 铁律：单次 Playwright 会话

**一个 Bug 的分析全程只允许启动一次 Playwright 浏览器**。登录后所有操作（读详情、下载附件、写评论）复用同一会话，禁止：

- ❌ 分多个脚本文件各启动一次 Playwright
- ❌ 中途关闭浏览器再重新登录
- ❌ 写评论时用新的浏览器实例

### 🔴 铁律：脚本优先，禁止手写临时 Playwright 脚本

脚本列表、参数和用法详见 [TOOLS.md](TOOLS.md)。核心铁律：

**禁止行为**：
- ❌ 手写临时 `post_comment.js`、`check_bug.js`、`debug_login.js` 等任何 Playwright 脚本
- ❌ 在 `bugs/{bug_id}/` 目录下创建任何 `.js` 文件
- ❌ 用 `page.evaluate`、`page.fill`、`page.click` 等 Playwright API 绕过已有脚本
- ❌ 禁止用 `--comment` 参数传 HTML 内容发布评论（shell 转义风险），必须用 `--comment-file`

**遇到脚本报错时的正确处理方式**：
1. 先读脚本源码，理解它依赖的输入（WS endpoint、参数格式等）
2. 修复输入条件（如重新登录获取有效 WS endpoint），而不是绕过脚本
3. 如果脚本本身有 bug，修复脚本源码（`scripts/` 目录下），让修复对所有后续分析生效

---

## 边界情况处理

| 场景 | 处理 |
|------|------|
| 不含禅道链接 | 「未识别到有效的禅道缺陷链接，请确认消息内容」 |
| 链接解析失败 | 「无法解析该链接，请确认是否正确转发」 |
| 禅道 API 请求失败（登录失效/会话过期） | 「无法访问禅道，请检查连接和登录状态」 |
| 模块分类置信度低 | 飞书通知：Bug 链接+关键信息，请手动确认 |
| 模块不在负责范围 | 飞书通知：Bug 归属 + 提醒手动流转 |
| commit id 提取失败 | 飞书通知：日志片段，请手动确认分支 |
| commit id 不在任何分支 | 飞书通知：commit id，请手动确认 |
| Bug 发生时间所有来源提取失败 | 飞书私聊询问用户精确时间（见步骤 4b 子步骤 5） |
| 附件/日志下载失败 | 降级：仅基于 Bug 描述+历史评论+代码分析，评论注明「未能获取附件」，飞书通知 |
| 本地代码目录不存在 | 降级：跳过代码分析，仅日志+附件+评论，飞书通知检查配置 |
| 分析过程中断或超时 | 飞书通知进度和失败原因，不留半截评论 |
| 用户 5 分钟内未回复重新分析确认 | 默认不重新分析，流程终止 |
| 分析过程中 git worktree 冲突 | 清理残留 worktree 后重试；仍失败则飞书通知 |

---

## 范围约束

- 不自动填写指派人或流转状态
- 不自动生成修复代码
- 不做缺陷趋势统计或报表
- 当前只服务单一用户

---

## 飞书通知模板

所有飞书私聊通知遵循以下统一格式（参考附录模板），各场景按表填充：

```
【Bug 分析】{状态标签}

Bug：#{bug_id} {title}
链接：{zentao_url}/bug-view-{bug_id}.html

{核心信息}

{操作引导}
```

| 场景 | 状态标签 | 核心信息 | 操作引导 |
|------|----------|----------|----------|
| 环境依赖缺失 | ❌ 环境异常 | 缺失的工具名称 + 安装命令（参考环境依赖章节） | 「安装后重试」 |
| 未识别有效链接 | ⚠️ 解析失败 | 「未识别到有效的禅道缺陷链接」 | 「请确认消息内容」 |
| 模块不在范围 | ↩️ 不在范围 | AI 判断的模块归属 | 「请确认模块并手动流转」 |
| 置信度低 | ❓ 无法确定 | Bug 关键信息（标题、描述摘要） | 「请手动确认模块归属」 |
| commit 提取失败 | ❌ 分析中断 | 日志片段（前 200 字符） | 「请手动确认分支」 |
| commit 不在任何分支 | ❌ 分析中断 | commit id | 「请手动确认分支」 |
| 时间提取失败 | ❓ 需补充信息 | 已尝试的来源汇总 | 「该 Bug 发生的精确时间是什么？」 |
| 分析完成 | ✅ 分析完成 | 根因摘要（1-2 句）+ report.md 路径 | 「详见禅道评论 / 本地 report.md」 |
