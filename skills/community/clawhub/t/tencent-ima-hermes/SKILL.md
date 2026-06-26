---
name: ima
description: |
  腾讯 IMA OpenAPI 技能（笔记 + 知识库）。当用户提到知识库、资料库、笔记、备忘录、记事，
  或者想上传文件到知识库、添加网页/微信文章到知识库、搜索知识库内容、搜索/浏览/创建/编辑
  笔记时，使用此 skill。即使用户没有明确说"知识库"或"笔记"，只要意图涉及文件上传到
  知识库、网页收藏、知识搜索、个人文档存取（"帮我记一下"、"搜一下知识库里有没有XX"），
  也应触发此 skill。
homepage: https://ima.qq.com
source: https://github.com/MiniMax-AI/cli  (本 skill 不使用此源；本 skill 基于腾讯官方 OpenAPI 包改造)
upstream:
  name: 腾讯官方 IMA OpenAPI 技能
  version: 1.1.7
  url: https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip
  license: 腾讯 IMA OpenAPI 使用条款（沿用原版约束）
  relationship: 基于原版改造（不是 fork；原版 OpenClaw 风格 frontmatter 已替换为 hermes 风格 + 增加 bin/ima CLI 桥接 + 探针发现 5 个未文档化端点）
status: maintained
roadmap:
  - 删除/移动/重命名相关指令**不在 OpenAPI 范围**：官方 ima-skills-1.1.7.zip 文档明确只暴露 16 个端点（全围绕"读+创建/追加"流），50+ 候选变种探针全 RAW=0，3 类 KB 账号 × 6 能力矩阵实测无任何"删/移/改"端点可用。错误码（VERSION_CONFLICT / NOTE_IS_DELETE / NOTE_NOT_OWNER / SHARE_DOC_NOPERM）暗示后端有这些功能但未公开。**唯一例外**：`rename_note` 端点（v8 探针 2026-06-04 新发现，code:0 真生效，字段 `note_id` + `title`）。**用户需到 ima 桌面/移动端 UI 手工操作"删除/移动/改笔记本名"等剩余能力**，或走层次 B 曲线方案（桌面客户端 cookie + Playwright 自动化，需用户明确决策才启动，工作量约半天）
  - 标签管理、知识库分享/成员管理同上：后端错误码承认功能存在但 OpenAPI 路由层不暴露
  - 曲线方案：桌面客户端 cookie + Playwright 自动化（需用户明确决策才启动，工作量约半天）
metadata:
  hermes:
    emoji: 🪶
    category: productivity
    cli: bin/ima
    requires:
      env:
        - IMA_OPENAPI_CLIENTID
        - IMA_OPENAPI_APIKEY
    primaryEnv: IMA_OPENAPI_CLIENTID
  security:
    credentials_usage: |
      This skill requires user-provisioned IMA OpenAPI credentials (Client ID and API Key)
      to authenticate with the official IMA API at https://ima.qq.com.
      Credentials are ONLY sent to the official IMA API endpoint (ima.qq.com) as HTTP headers.
      The file-upload flow also sends requests to COS endpoints (*.myqcloud.com) using
      short-lived, scoped temporary credentials returned by the IMA API (create_media);
      the user's Client ID / API Key are never sent to COS.
      No credentials are logged, stored in files, or transmitted to any other destination.
    allowed_domains:
      - ima.qq.com
      - '*.myqcloud.com'
---

> ⚠️ **基于腾讯官方包改造声明**
> 本 skill **基于腾讯 IMA 官方 OpenAPI 技能 v1.1.7** 改造。
> 原版下载：https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip
> 改造内容（**不**修改原版 API 端点；**不**删改原版字段名）：
>   - OpenClaw 风格 frontmatter → Hermes 风格 frontmatter
>   - 增加 `bin/ima` POSIX 桥接（18 个子命令覆盖全部 16 个原版端点 + 1 个 `upload-file` 便利封装）
>   - 探针发现并补充 5 个未文档化但真实存在的端点（create_folder / create_knowledge_base / move_knowledge / add_notebook / rename_notebook）
>   - 凭证路径对齐 Hermes `.env` 约定（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`）
> 原版约束（写入类工作流 MANDATORY RULES、UTF-8 强制、media_type 拒绝规则）**完全保留**。
>
> 🛠️ **Roadmap**：删除、移动、重命名相关指令**不在 OpenAPI 范围**（官方 ima-skills-1.1.7.zip 文档明确只暴露 16 个端点，全部围绕"读+创建/追加"流）。错误码（VERSION_CONFLICT / NOTE_IS_DELETE / NOTE_NOT_OWNER / SHARE_DOC_NOPERM）暗示后端有这些功能但未在 OpenAPI 公开。用户**需到 ima 桌面/移动端 UI 手工操作**，或走层次 B 曲线方案（桌面客户端 cookie + Playwright 自动化，需明确决策）。完整端点核对、3 类 KB 权限矩阵、副作用清单：见 `references/official-endpoint-coverage.md`。

> ⚠️ **v9 探针新增关键约束**（2026-06-04 实战验证）：
> 1. **跨命名空间 folder_id 不能混用** —— `import_doc` 的 `folder_id` 字段是 **note 命名空间**下的 notebook id（`list-notebook` 拿到的 `folder453087040e892a2d` 这种 32 字符 hash 形式），**不是** wiki/KB 命名空间下的子文件夹（`YOUR_TARGET_FOLDER_ID` 这种数字前缀形式）。错传 wiki folder id 给 `import_doc` 会得到 `code:310001 文件夹不存在`。
> 2. **笔记挂 KB 后无法移到子文件夹** —— `add_knowledge` with `media_type=11`（笔记模式）**没有 `folder_id` 参数**，笔记被挂到 KB 根；`move_knowledge` 端点返回 `code:0` 但 `move_results:{}`，**实际不移动**（3 类 KB 都一样）。**要进 KB 子文件夹只能用文件上传模式 + `check_repeated_names`+ `create_media`+ COS 上传**（upload-file 流程）。
> 3. **CLI 误创的 note 无法删除** —— `import_doc` 误调（参数错、传空等）会创建**空内容笔记**到默认 notebook。**OpenAPI 不暴露 `delete_doc` 端点**。需要手动去 ima 客户端 UI 清理，或保留复用（不浪费 quota）。
> 详见 `references/api-quirks.md` 的 **v9 实战踩坑**段。
>
> ⚠️ **v10 探针新增关键约束**（2026-06-04 修复 `upload-file` bug 时实测）：
> 1. **`add_knowledge` 端点的 `folder_id` 接受带 `folder_` 前缀的 id**（如 `YOUR_TARGET_FOLDER_ID`）。`upload-file` 调 `add_knowledge` 时传纯数字 → `code:222000 文件夹不存在`。修复后传带前缀 → code:0 落到子文件夹。
> 2. **`upload-file` 封装历史上漏 `folder_id`**（2026-06-04 修复）—— CLI 接受 `[folder_id]` 参数但 `add_knowledge` body 始终没有该字段，结果**永远落 KB 根**。已修复（详见 `references/api-quirks.md` v10 段；检查 `bin/ima` 的 `if [[ -n "$fid" ]]` 分支是否还在）。修复后再传 folder_id 才能真进子文件夹。
> 3. **不要只读 `add-knowledge` case 实现就下结论**——`add-knowledge --note`（笔记模式）确实没有 folder_id，但 `add-knowledge`（文件模式，5 参形式）有，是 upload-file 流程在用。看一半 API 列表 = 错一半结论。
> 4. **`bin/ima` 里 v10 修复注释有误导**——注释写"命名空间遵循 create_folder v9 探针结论：纯数字"，**实际错了**（2026-06-05 实测：`create_folder` **也**吃 `folder_` 前缀形式，第 3 参数 `YOUR_PARENT_FOLDER_ID` 返回 code:0 创建成功）。看 `bin/ima` 注释要看实测（带前缀）不要看注释本身。**改注释**前先实测验证一次。**当前统一规则**：`create_folder` / `add_knowledge` / `add-url` 三者**都**接受 `folder_` 前缀形式；纯数字也是 v9 历史经验，但**带前缀更稳**，新代码默认走带前缀。
>
> ⚠️ **v14 实战新增关键约束**（2026-06-05 凭证检测失误被用户当场纠正时实测）：
> 1. **凭证检测必须先看环境变量再看文件** —— SKILL.md 写明优先级"环境变量 → 配置文件"，但 agent 容易写成只检测文件路径的脚本（`test -f ~/.config/ima/client_id && test -f ~/.config/ima/api_key`），漏检 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` 这两个环境变量，得到**假阴性**"⚠️ 凭证缺"。**正确姿势**（按优先级）：
>    1. `env | grep -E '^(IMA_OPENAPI_CLIENTID|IMA_OPENAPI_APIKEY)='` 看 shell 环境
>    2. `grep -E 'IMA_OPENAPI_(CLIENTID|APIKEY)' ~/.hermes/.env` 看 .env 文件
>    3. `ls ~/.config/ima/{client_id,api_key}` 看配置文件（最低优先级）
>    **任一在 = 凭证在**。**不要**只看文件路径就下结论。**真实失误案例**：2026-06-05 用户要求"继续进行 ima 的知识获取与筛选" → agent 只跑文件检测就报"⚠️ 凭证缺，先补才能写操作" → 用户当场纠正"ima凭证是什么？我理解我配置 ima 技能的时候已经加入了。不是吗" → 实际凭证在 `~/.hermes/.env` + shell export 完整在位。
> 2. **不要把"凭证检测失败"扩大成"写操作前必须先补凭证"** —— 这是同一失误的连锁反应。看到 ⚠️ 之前先按上面的 1+2+3 优先级**完整**查一遍再下结论。
>
> ⚠️ **v14 实战新增关键约束**（2026-06-05 50 篇第二批量上传 + 跨 13 个主题相似度匹配时实测）：
>
> 1. **`mmx text chat` 没有 `--output text` 标志**（`mmx text chat --help` 显示的 `--output json` 是 global flag，不是 sub flag）—— stdout **直接**返回 JSON object `{"id","type","role","model","content":[{"type":"thinking"},{"type":"text"}],"usage","stop_reason","base_resp"}`，**不会**带 `--output` 选项。提取文本：遍历 `j["content"]` 找 `c["type"]=="text"` 的 `c["text"]`。**`--output text` 是假选项**（会静默返回 1 字符 stdout，不要浪费时间解析）。
> 2. **"直接当译文" 模式（v14 新增简化路径）** —— 当源仓库**已经是中文**（如 `AlexAnys/awesome-openclaw-usecases-zh`、`xianyu110/awesome-openclaw-tutorial` 等），不需要走 `mmx text chat` 翻译 + 8 校验的完整流水线。简化流程：① 读 H1 ② GATE 3 预检（`check-name` 必跑）③ 复制到沙箱按 H1 命名 ④ `upload-file` 走 4 步门。**省 50%+ 时间**（从 110s/批 → ~20s/批），质量**不**降（源已经是中文，机翻是退化）。
> 3. **8 篇 0 GATE 3 实测**（2026-06-05 验证）：8 篇纯增量中文用例（`A 股每日行情监控.md` / `用 Lark CLI 让 Agent 操作飞书.md` 等），GATE 3 全部 `is_repeated: false`，**没有任何冲突**。`browse-kb` 验证后子文件夹从 42 → 50。**结论**：纯增量内容（slug 命名不同时）GATE 3 命中率极低，`--force` 几乎用不到。
> 4. **subprocess shell=True 中文文件名解析坑**（2026-06-05 实战）—— 用 `subprocess.run(["~/.hermes/skills/ima/bin/ima", "check-name", KB_ID, "A 股每日行情监控.md", ...], shell=True)` 调中文文件名时，**shell 解析会把空格当分隔符**，导致传进去的字段被拆，**JSON 返回成功但解析失败**（`ParseExpecting value: line 1 column 1 (char 0)`）。**正确做法**：直接 `subprocess.run([...], shell=False)` 用 argv 形式传参，或用 `terminal()` 工具调 `~/.hermes/skills/ima/bin/ima check-name ...`。Python 解析 JSON 时**不要** `shell=True` + 中文字符串。
> 5. **frontmatter `source:` 字段按仓库区分**（v14 新增约定）—— 50 篇 vault 笔记的 frontmatter，42 篇用 `source: hesamsheikh/awesome-openclaw-usecases`、8 篇用 `source: AlexAnys/awesome-openclaw-usecases-zh`。**不要统一**写成"OpenClaw 用例"，否则未来想做"按仓库分类"双链聚合时区分不出来。
>
> 详见 `references/api-quirks.md` v14 段（待补）。
>
> ⚠️ **v13 实战新增关键约束**（2026-06-05 42 篇翻译批量上传到 IMA 子文件夹时实测）：
> 9. **`upload-file` GATE 3 不仅查文件名，还查内容指纹**——`check_repeated_names` 触发 `is_repeated=true` 的判定**不是按文件名**。实测：同 KB 子文件夹下，旧项 `ai-video-editing_zh.md`（旧文件名）已存在；上传新名 `通过对话进行 AI 视频剪辑.md`（H1 重命名后）→ **也被 GATE 3 拦**，因为内容相同。**实际错误信息**：`GATE 3: 同名文件已存在。请加 --force 自动加时间戳后缀保留两者，或手动改名。`（**不是**"内容相同"，但实际就是按内容查的）。**含义**：
>    - 想"换文件名不换内容"重传修正错位 = 不可行（除非用 `--force` 加时间戳后缀）
>    - **真正想覆盖修正错位**：用户 IMA App 手工删旧 → 重新 `upload-file`（不要带 `--force`）
>    - 想保留新旧两份 = 传 `--force`，CLI 自动加 `_YYYYMMDDHHmmss` 后缀
> 10. **批量上传时 `check_repeated_names` 的 `folder_id` 参数很重要**——它决定查重范围。同一 KB 下**根目录**的旧 `a.md` 跟**子文件夹**下的新 `b.md`（内容相同）**不会**互相触发 GATE 3，因为查重是按 folder 范围。但**同子文件夹**下会触发。
>
> ⚠️ **v12 实战新增关键约束**（2026-06-05 usecases 批量翻译上传实战）：
> 5. **`upload-file` 是新建不是覆盖**——`create_media` 每次都生成新 `media_id`，重传**同名文件**会得到**第 2 份独立 KB 条目**（不同 `cos_key`、不同 `media_id`），旧条目不会被替换。"重传修正错位"的预期会变成"KB 里 2 份共存"。**修正错位的唯一干净流程**：用户 IMA App 手工删错的 → agent 重新 `upload-file` 传对的。任何"自动覆盖 / 自动清理"都不存在。
> 6. **写操作前先校验 H1 是不是合法文件名**——`upload-file` 的 `file_name` 来源于本地文件路径。H1 含 `/` `\` `:` `*` `?` `"` `<` `>` `|` 时，Linux 文件名非法，会让 `mv`/`cp` 静默失败（如 `head -1` 取到空行后 `cp "$H1.md"` 创建了空名 `.md` 文件，删了原译文）。**修法**：H1 → 文件名时**先把非法字符替换**（`/` → `-`、`?` → 空、`:` → `-` 等），再 `mv` + `upload-file`。
> 7. **`mmx text chat` 的输出默认带外层 ```` ```markdown ... ``` ```` 包裹**——`mmx text chat --message ... --output text` 的输出**首尾**会被 LLM 加 markdown 代码块包裹（如果 LLM 决定"这是 markdown 输出"）。存盘前必须 `strip_outer_markdown_fence`（正则 ``^```\w*\s*\n(.*?)\n```\s*$``），否则 IMA 上传的文件首行会是 ```` ```markdown ````，破坏文件结构。
> 8. **`execute_code` 沙箱对全新中文路径写不进去**——`open(new_path, 'wb')` / `os.rename` 报 `FileNotFoundError: [Errno 2] No such file or directory` 即便父目录存在且权限正常。**绕道**：先 `cp` 到临时英文文件名 → `terminal` 走 `mv "tmp.md" "中文名.md"` 改名。或全程用 `subprocess.run(['cp', ...])` 走 terminal。**这**不是文件系统问题，是 hermes `execute_code` 沙箱的预检限制。
>
> 详见 `references/api-quirks.md` v12 段。
>
> ⚠️ **v11 探针新增关键约束**（2026-06-04 实测 `rename-note` 对 markdown 媒体）：
> 1. **`rename-note` 只对 `note` 媒体（`media_type=11`）生效**，**对 markdown 文件（`media_type=7`）拒绝**——返 `code:210005 RenameNote not author`。**意味着 KB 里上传的 markdown 文件标题一旦定下来就无法修改**（标题 = file_name 由 IMA 端点硬约束）。"修标题"的唯一办法是 **新文件** + 新 file_name + 新 upload-file（产生新 COS 对象 + 新 KB 条目），旧文件必须 IMA App 手工删。
> 2. **跟之前"rename-note 是唯一可用的修复动作"的说法要修正**——它对**误创的 note** 仍可用（例如给真 note 加 `【勿删】` 前缀防手贱），但**对 KB 上传的 markdown 文件无效**。
> 3. **用户的默认规则**：「KB 文件标题 = 文章 H1」。`upload-file` 之前**先把本地文件名改成跟 H1 一致**（中文 / 标点 / 版本号 都要在文件名里），再 upload。否则 KB 里出现的标题是文件名（slug 化）而不是用户期望的标题，违反默认规则。
> 4. **错误码 210005 含义纠正**：不是"作者不匹配"（not author 表面意思），是"该媒体类型不支持 rename-note"。
**Hermes 适配说明**：子模块文档已重命名为 `knowledge-base/GUIDE.md` 和 `notes/GUIDE.md`（原 SKILL.md），避免被 Hermes 当成独立 skill 误识别。

## ⚠️ 写入操作必读（2026-06-04 常总纠正后沉淀）

### 默认规则（default rules，每次写操作前自动走一遍）

1. **做坏了不擅自动手修复，先汇报情况**（常总强纠正 2026-06-04）。本条是常总跨所有写操作的**通用原则**，IMA 是其中一类。**禁止**自创修复路径、禁止回滚、禁止补救——立刻停下走"汇报"分支。
2. **KB 文件标题 = 文章 H1**（常总默认 2026-06-04）。`upload-file` 之前**先把本地文件名 `mv` 成跟 H1 完全一致**（含中文 / 标点 / 版本号），再 upload。**一旦上传，标题不可改**（`rename-note` 对 markdown 返 210005）——只能"新文件 + 重新 upload"补救。
3. **`upload-file` 之前先 `browse-kb` 验证 folder_id 形式**（2026-06-05 实测约束 v12 修正）：**`create_folder` / `add_knowledge` / `add-url` 三者**都**接受 `folder_` 前缀形式**（如 `YOUR_TARGET_FOLDER_ID`）。**纯数字**也是历史上 OK 的形式（v9 探针结论），但**带前缀更稳**，新代码默认走带前缀。`upload-file` 调 `add_knowledge` 时传纯数字 → `code:222000 文件夹不存在`，**不会**默默落根。**验证后**再用 `folder_` 前缀形式调 `upload-file`。
4. **不要凭"我以为"答"能不能做 X"**——`knowledge-base/GUIDE.md` 222 行已经写了"folder_id 始终以 folder_ 前缀开头"这种通用规则。**下结论前先 grep**：`grep -nE 'folder_id|folder_xxx' knowledge-base/GUIDE.md references/api-quirks.md` —— 已经记录了就不重新探针，不重复造轮子。
5. **`bin/ima` 是可改文件，修复不是永久的**（v10 教训）——任何时候做写操作前先 `grep -n 'if \[\[ -n "\$fid" \]\]' bin/ima` 确认 upload-file 修复还在（v10 漏 folder_id 是已修的 bug）。不在了 = 立刻停下修脚本，不要"绕过修复"上传。

### 做写操作前的 5 问

1. **目标位置真的能放吗？** 不要凭印象下手；下表是已验证事实。
2. **要进 KB 子文件夹？** 走 `upload-file`（**唯一**支持 folder_id 的入口）。
3. **如果操作坏了怎么办？** 立刻停下，按"三栏"汇报（正确 / 错位 / 需常总手工处理），**禁止**自我修复。
4. **`bin/ima` 的修复"心跳"还在吗？**（v10 教训）**写操作前先 grep**：`grep -n 'if \[\[ -n "\$fid" \]\]' bin/ima` —— 没匹配 = bug 复现 = 立刻停下不要 upload-file，先修脚本。
5. **本地文件名跟文章 H1 一致吗？**（v11 教训）走默认规则 2：`mv` 本地文件成 H1 文字（保留 `.md` 扩展名），再 upload。

### "做坏了" 的汇报模式（强制 3 栏）

发现做坏时**禁止自我修复**，立刻按以下 3 栏汇报，等常总拍板：

1. **正确**（应该落到哪 + 当前已落到哪 + 错在哪一步）
2. **错误**（agent 自身的错位行为 / 误创 / 误删 / 误改 / 误发 — 列具体 ID/路径/内容片段）
3. **需常总手工处理**（OpenAPI 不支持 / 凭据权限不够 / 客户端 UI 操作 — 列具体步骤）

汇报完**停手**——等常总说"做 X"或"别动"再继续。**禁止**"那我顺手把 X 也修了" / "我先帮你把 Y 准备好" 这种"贴心"动作。

**写入入口选型表**（已实测）：

| 想做的事 | 命令 | 能指定 KB 子文件夹？ | 备注 |
|---|---|---|---|
| 建笔记到「笔记本」 | `new-doc "<content>" [folder_id] [title]` | N/A（note 命名空间） | folder_id 必须是 note notebook id（`list-notebook` 形式），**不是** wiki folder |
| 笔记挂到 KB | `add-knowledge --note <kb_id> <note_id> <title>` | **否**（必进 KB 根） | `add-knowledge` 整个端点不带 folder_id；`kb_id` 从 `list-kb` 查（带 `kb_id` / `kb_name` 字段） |
| 文件到 KB（含子文件夹） | `upload-file <kb_id> <file> [folder_id] [--force]` | **是** | ⚠️ `folder_id` 必须来自 `browse-kb` 查询结果，不接受手填。<br>**完整流程**：<br>1. `browse-kb <kb_id>` 或 `browse-kb <kb_id> <parent_folder_id>` 拿到目标 folder 的带 `folder_` 前缀的 id<br>2. `upload-file <kb_id> <file> <folder_id> [--force]`<br>**内部 4 步流水线**：preflight → check_repeated_names → create_media → cos-upload → add_knowledge<br>**任一步骤失败**：立刻停下，按 3 栏汇报（**禁止**自我修复） |
| 文件到 KB 根 | `upload-file <kb_id> <file>` | N/A | 不传 `folder_id` = 落 KB 根；**传错**（纯数字 / 拼写错）= `code:222000 文件夹不存在`（**不**是落根，**不**是落子文件夹） |
| 移动 KB 内子文件夹 | `move-kb-item` | **空壳端点**（code:0 但 `move_results:{}`） | **不可用**，必须 IMA App 拖 |
| 删笔记 / 删 KB 项 | — | — | OpenAPI 不暴露，必须 IMA App 手工 |
| 改笔记标题 | `rename-note <note_id> <new_title>` | N/A | **仅对真 note 媒体（`media_type=11`）有效**；对 KB 上传的 markdown 文件（`media_type=7`）返 210005 "not author"（实际是媒体类型不支持）。<br>**判断方法**：看 `media_id` 前缀 —— `note_xxx` = note（11）/`markdown_xxx` = md（7）/`weburl_xxx` = 网页（2）/`file_xxx` = 文件；或 `browse-kb` 返回的 `media_type` 字段。详见 v11 探针 |
| 改 KB 上传文件标题 | — | — | **不支持**——`title = file_name` 由 IMA 端点硬约束；`rename-note` 对 markdown 返 210005。**唯一办法**是改本地文件名后重新 upload-file（**会**产生新 COS 对象 + 新 KB 条目，旧对象**不**会**自动**清，需 IMA App 手工删） |

**最容易踩的 4 个坑**（看完整 recipe 见 `references/ima-write-flow.md`）：
- `ima new-doc --help` 会把 `--help` 当 content 误创 1 个空标题笔记（看 help 用 `ima --help`，别带子命令）
- `import_doc` 的 `folder_id` 接 **note 命名空间** id（`folder<32hex>`），**不接** wiki folder（`folder_<digits>`）—— 混用 = `code:310001 文件夹不存在`
- 只看 `add-knowledge` 就下结论说"不能进 KB 子文件夹"——错。`upload-file` 才能
- **只看 `upload-file` 封装就下结论说"已修好"**——**也不行**。该封装历史上漏 `folder_id`（2026-06-04 修复）。**修复后**调用 `upload-file` 时 folder_id **必须带 `folder_` 前缀**，否则 222000。`bin/ima` 里的 `if [[ -n "$fid" ]]` 分支是修复的"心跳"——它不在了就要重新修一次。
- **凭证检查只看 `~/.config/ima/*` 文件**——`ima_api.cjs` 实际是 `options > env > file` 三级优先（行 29-38），用户经常 `~/.hermes/.env` 配凭证由 shell 导出，**只测文件就报"凭证缺"会误导用户**。检查必须先 env 再 file（见 Credential Check 段）

**字段 / 响应结构的实测踩坑**（create_media cos 字段嵌套、search_note 真实字段名、错误码速查、上传四步门、v8 探针发现的 5 个端点 — 详见 `references/api-quirks.md`）：见 `references/api-quirks.md`。
**写盘后必跑验证**（browse-kb 分页拿全 + 14 篇逐一核验 + 重复检查 + 旧残留识别 + 双向链接一致性 + 沉淀工作流教训）：见 `references/post-upload-validation.md`。

**写操作硬闸**（2026-06-04 沉淀）：本节"5 问"是**概念层**——"硬闸"是**命令层**。5 问 = "我应该想什么"，硬闸 = "我必须跑什么命令"。配套文件：`references/ima-write-hard-gates.md`（含 5 个可执行硬闸 + 实施优先级 + 跟本节的关系）。**写 KB 之前**先 cat 一下那个文件——不是参考，是**必跑**。
>
> 🆕 **v8 探针新增端点**（2026-06-04）：
> - `openapi/note/v1/rename_note` — 改单条笔记标题（跟 `rename_notebook` 区别；字段 `note_id` + `title`）
> - `openapi/wiki/v1/create_folder` 支持第 3 参数 `folder_id` — 可在指定父目录下建子目录（默认建在 KB 根）
>
> ⚠️ **批量建子目录的 bash 编码坑**（2026-06-04 踩过）：
> bash 变量名**不能用中文**（`L1_每日快报=folder_xxx` 在 `set -euo pipefail` 下报 `command not found` 被吞，导致 `$L1_每日快报` 解析成空字符串 → `create_folder` 收到的 `folder_id` 字段为空 → 全建到 KB 根）。
> 修复方式：用 **`scripts/build_kb_structure.py`**（python 调 ima_api.cjs，天然支持中文键名）。详见 `references/api-quirks.md` 末尾的"批量建子目录"段。

# ima-skill

Unified IMA OpenAPI skill. Currently supports: **notes**, **knowledge-base**.

> 🆕 **本 skill 的上游（找"该往 KB 里填什么"）由 `ima-kb-curation` skill 负责**。
> `ima-kb-curation` 产出本地候选 markdown + 用户拍板 → 用户说"这篇进 KB" → **本 skill** 用 `add-url` 落地。
> 详见 `ima-kb-curation` SKILL.md。

## ⛔ MANDATORY RULES — read before ANY operation

1. **UTF-8 encoding (notes writes only):** Before calling `import_doc` or `append_doc`, ALL string fields (`content`, `title`) MUST be validated as legal UTF-8. Non-UTF-8 content causes irreversible garbled text. See [Detailed Rules](#detailed-utf-8-encoding-rules) for platform-specific methods.
2. **File upload naming:** `title` MUST equal `file_name` (with extension). Never rename, shorten, translate, or modify the original filename.
3. **Unsupported file types:** Reject immediately with a clear message. Do NOT ask user "do you still want to try?" Video files, Bilibili/YouTube URLs, and `file://` URLs are not supported — tell user to use IMA desktop client.
4. **File upload integrity:** Keep file content as-is during upload. No encoding conversion for binary files (PDF, images, Excel, etc.).
5. **PowerShell 5.1 (all modules):** If running in PowerShell, detect version before first API call. PS 5.1 silently converts request Body to GBK — must use UTF-8 byte array mode. See [Detailed Rules](#powershell-51-environment-detection).

## 模块决策表

| 用户意图                                                                                   | 模块           | 读取                      |
| ------------------------------------------------------------------------------------------ | -------------- | ------------------------- |
| 搜索笔记、浏览笔记本、获取笔记内容、创建笔记、追加内容                                     | notes          | `notes/SKILL.md`          |
| 上传文件、添加网页链接、搜索知识库、浏览知识库内容、获取知识库信息、获取可添加的知识库列表 | knowledge-base | `knowledge-base/SKILL.md` |
| 查看原文、分析原文、导出原文（需要 media_id）                                              | knowledge-base | `knowledge-base/SKILL.md` |

### ⚠️ 易混淆场景

| 用户说的                                                 | 实际意图                 | 正确路由                                                    |
| -------------------------------------------------------- | ------------------------ | ----------------------------------------------------------- |
| "把这段内容添加到知识库XX里的笔记YY"                     | 往已有**笔记**追加内容   | **notes** — 先搜索笔记获取 `note_id`，再用 `append_doc`     |
| "把这个写到XX笔记里"、"记到XX笔记"                       | 往已有**笔记**追加内容   | **notes** — `append_doc`                                    |
| "把这篇笔记添加到知识库"                                 | 将笔记关联到**知识库**   | **knowledge-base** — `add_knowledge` with `media_type=11`   |
| "上传文件到知识库"                                       | 上传**文件**到知识库     | **knowledge-base** — `create_media` → COS → `add_knowledge` |
| "新建一篇笔记记录这些内容"                               | **创建**新笔记           | **notes** — `import_doc`                                    |
| "帮我记一下"、"记录一下"、"保存为笔记"（未指定已有笔记） | 意图不明确，**需要确认** | **notes** — 先询问用户是创建新笔记还是追加到哪篇已有笔记    |
| "添加到笔记里"（未指定具体哪篇）                         | 意图不明确，**需要确认** | **notes** — 先询问用户是创建新笔记还是追加到哪篇已有笔记    |

### ⚠️ 跨模块任务 — 必须读取两个子模块

某些意图跨越 notes 和 knowledge-base 两个模块。**不要只读取一个子模块就开始执行**，必须先读取两个模块的 SKILL.md 再按顺序操作。

| 用户说的                             | 实际流程                                      | 读取顺序                                               |
| ------------------------------------ | --------------------------------------------- | ------------------------------------------------------ |
| "把知识库里的XX内容记到笔记"         | KB 搜索/读取 → Notes 创建/追加                | 先读 `knowledge-base/SKILL.md` → 再读 `notes/SKILL.md` |
| "查看原文"（知识库中的笔记类型媒体） | KB `get_media_info` → Notes `get_doc_content` | 先读 `knowledge-base/SKILL.md` → 再读 `notes/SKILL.md` |
| "把这篇笔记添加到知识库"             | Notes 搜索获取 note_id → KB `add_knowledge`   | 先读 `notes/SKILL.md` → 再读 `knowledge-base/SKILL.md` |
| "把这份 md 写到 KB 某个子文件夹"     | ⚠️ **OpenAPI 不支持"笔记直入子文件夹"**（见上 v9 探针约束）→ 走 `upload-file` 流程让文件进入子文件夹 | 先读 `knowledge-base/SKILL.md`（upload-file 4 步门）|

**规则**：如果用户意图同时涉及「笔记」和「知识库」，或者 API 响应揭示需要另一个模块（如 `media_type=11` 表示笔记类型），必须读取两个子模块再继续。

**核心判断规则**：

- 目标是**笔记的内容**（读、写、追加）→ notes 模块
- 目标是**知识库的条目**（上传文件、添加链接、关联笔记到知识库）→ knowledge-base 模块
- 目标是**获取知识库条目的原始内容**（查看原文、分析原文、导出原文）→ knowledge-base 模块（若原文是笔记，会跨模块到 notes `get_doc_content`）
- 用户提到"知识库"只是在**描述笔记的位置**（如"知识库里的那篇笔记"），真正操作对象仍是笔记 → notes 模块

## Credential Check

!`if [ -n "$IMA_OPENAPI_CLIENTID" ] && [ -n "$IMA_OPENAPI_APIKEY" ]; then echo "✅ Credentials configured (env vars)"; elif test -f ~/.config/ima/client_id && test -f ~/.config/ima/api_key; then echo "✅ Credentials configured (files)"; else echo "⚠️ NO CREDENTIALS — setup required before any API call"; fi`
> `options.clientId` → `process.env.IMA_OPENAPI_CLIENTID` → `~/.config/ima/client_id` 文件。
> **环境变量优先于文件**。**只测文件 = 大概率假阴性**（2026-06-05 踩过：
> 用户已 `~/.hermes/.env` 配好并由 shell export，agent 只看 `~/.config/ima/*` 文件
> 误报"凭证缺"，用户当场质疑"我配置 ima 技能的时候已经加入了。不是吗"）。

!`if [ -n "$IMA_OPENAPI_CLIENTID" ] && [ -n "$IMA_OPENAPI_APIKEY" ]; then echo "✅ Credentials configured (env vars)"; elif [ -f ~/.config/ima/client_id ] && [ -f ~/.config/ima/api_key ]; then echo "✅ Credentials configured (files)"; else echo "⚠️ NO CREDENTIALS — setup required before any API call"; fi`

**If ⚠️ NO CREDENTIALS:** Guide the user through setup BEFORE attempting any API call:

```bash
# 1. 当前 shell 是否已 export
env | grep -E '^IMA_OPENAPI_(CLIENTID|APIKEY)=' >/dev/null && echo "✅ env 在" || echo "  env 缺"

# 2. 配置文件是否在
test -f ~/.config/ima/client_id && test -f ~/.config/ima/api_key && echo "✅ file 在" || echo "  file 缺"

# 3. 真用 ima_api.cjs 实测一次（最权威，模拟真实调用链）
SKILL_DIR=~/.hermes/skills/ima
if echo '{"limit":1}' | node "$SKILL_DIR/ima_api.cjs" openapi/list_docs '{}' \
  "$(printf '{"clientId":"%s","apiKey":"%s"}' "${IMA_OPENAPI_CLIENTID:-$(cat ~/.config/ima/client_id 2>/dev/null)}" "${IMA_OPENAPI_APIKEY:-$(cat ~/.config/ima/api_key 2>/dev/null)}")" \
  >/tmp/ima_credtest.json 2>/tmp/ima_credtest.err; then
  grep -q '"code":0' /tmp/ima_credtest.json && echo "✅ 真调用 code:0 — 凭证可用"
else
  cat /tmp/ima_credtest.err
fi
# IMA OpenAPI 实战踩坑库

按探针版本倒序排列。每个段都是一次"端点 + 实测请求 + 真响应"的复盘。

---

## v14 实战（2026-06-05 14 篇 usecases-zh 增量上传 + 6 篇部分覆盖）

### 发现 1：`browse-kb` 默认 `limit=50`，验证子文件夹总数必须分页拿全

**症状**：传 6 篇部分覆盖到子文件夹 `YOUR_FOLDER_ID` 后，agent 调 `browse-kb <kb_id> <folder_id>`（不传 limit），**返回 50 篇**。agent 拿"50"跟上传前子文件夹的"50"对比，下结论"没增加、可能上传失败"——**差点误报数据丢失**。

**实际**：6 篇**已经全部在第 1 页 50 篇里**（按字母序 / 上传时间排），但子文件夹**实际总数从 50 涨到 57**。`browse-kb` 第 1 页只给前 50，**剩下的在第 2 页**。

**根因**：端点 `Limit` 字段范围 `(0, 50]`，**最大 50**。`is_end=False` 时必有 `next_cursor`，必须 cursor 翻页拿全。

**心跳/验证代码**（验证子文件夹总条数时**必须**跑）：

```python
import json, subprocess
KB_ID = "..."
SUBFOLDER = "folder_xxx"

def get_all_titles(kb_id, sub):
    r = subprocess.run(["/home/jerome/.hermes/skills/ima/bin/ima",
                       "browse-kb", kb_id, sub], capture_output=True, text=True)
    j = json.loads([l for l in r.stdout.split("\n") if l.startswith("{")][-1])
    titles = [it["title"] for it in j["data"]["knowledge_list"]]
    cursor = j["data"].get("next_cursor", "")
    if cursor and not j["data"].get("is_end"):
        r2 = subprocess.run(["/home/jerome/.hermes/skills/ima/bin/ima",
                            "browse-kb", kb_id, sub, cursor, "50"],
                           capture_output=True, text=True)
        j2 = json.loads([l for l in r2.stdout.split("\n") if l.startswith("{")][-1])
        titles += [it["title"] for it in j2["data"].get("knowledge_list", [])]
    return titles
```

**绝对不要做的**：单跑 `browse-kb` 一次、用 `len(items)` 当子文件夹总数。**必须**分页拿全。

**含义 / 实战教训**：
- 写"操作前/后"对比的核验脚本，**必须**循环 cursor 拿完
- "操作前 50 + 操作 6 = 应该 56"这种估算错得很常见——分页上限 + 旧残留 + 重复会让估算失真
- IMA App 显示的子文件夹数（用户视角）跟 `browse-kb` 单次返回的 `len(items)` **不等价**

### 发现 2：SKILL.md `Credential Check` 块有 env var 检测盲区

**症状**：agent 跑 SKILL.md 顶部 `Credential Check` 块（测 `~/.config/ima/client_id` + `api_key` 文件存在），报"⚠️ NO CREDENTIALS"——**误报**。

**实际**：用户凭证在 `~/.hermes/.env` 里以环境变量形式存在（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`），**没有**写成 `~/.config/ima/` 文件。`ima_api.cjs` 实际**两个都支持**（env var 优先，回退文件）。

**用户纠正原话**："ima 凭证是什么？我理解我配置 ima 技能的时候已经加入了。不是吗"。

**修法 / 心跳检查升级**（下次进入 ima skill 时**先跑**这段）：

```bash
# 完整凭证检测（先 env var，后文件）
if [ -n "$IMA_OPENAPI_CLIENTID" ] && [ -n "$IMA_OPENAPI_APIKEY" ]; then
  echo "✅ 凭证在环境变量（.env 已加载）"
elif [ -f ~/.config/ima/client_id ] && [ -f ~/.config/ima/api_key ]; then
  echo "✅ 凭证在 ~/.config/ima/ 文件"
else
  echo "⚠️ 凭证缺（env var + 文件都没有）"
fi
```

**含义**：
- "看起来缺 vs 实际在"是高频陷阱——**永远跑实测命令**验证配置状态
- 用户环境跟 SKILL.md 默认假设（"凭证在文件里"）不一致是常态
- 看到"凭证缺"信号 → **先**用 `env | grep IMA` + `cat ~/.hermes/.env | grep -i ima` 跑实测，**再**下结论

### 发现 3：批量传 KB 后的"实际落点"核验模式

**症状**：传 14 篇到子文件夹后，agent 只看 `upload-file` 的 `code:0 + media_id` 就报"成功"——但**没核验**这 14 篇**真的在子文件夹里**、**没**被静默丢弃、**没**导致旧数据被覆盖。

**正确收工核验模式**（跟发现 1 配对）：

```bash
# 1. 拿全子文件夹（分页 + cursor）—— 复用发现 1 的 get_all_titles
# 2. 跟上传清单逐一对比：for title in NEW; do grep -q "$title" || echo "❌ 缺失"; done
# 3. 重复项检查：python3 -c "from collections import Counter; ..."
```

**含义**：
- `code:0 + media_id` = "后端接收成功"，**不**等于"用户视角能查到"
- IMA GATE 3、folder_id 错传、subfolder ID 不存在等原因可能让 `code:0` 但**实际**入错位置
- "操作前/后"对比比"操作返回码"更可靠

---

## v13 实战（2026-06-05 42 篇 usecases 翻译批量上传）

1. 打开 https://ima.qq.com/agent-interface 获取 **Client ID** 和 **API Key**
2. 存储凭证（二选一）：

**方式 A — 配置文件：**

```bash
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```

**方式 B — 环境变量（推荐，~./hermes/.env 已留行）：**

```bash
# 编辑 ~/.hermes/.env，找到这两行（开头的 # 已注释），替换占位值
IMA_OPENAPI_CLIENTID="your_client_id"
IMA_OPENAPI_APIKEY="your_api_key"
# 新开 shell 后 env | grep IMA 应能看到
```

**方式 A + B 共存时优先级**（`ima_api.cjs:29-38`）：`options 传入` > `env` > `file`。**`bin/ima` CLI 调用时传 options**（在 OPTS 字符串里带 clientId/apiKey），实际从 env / file 读是 fallback。

缺凭证时 `node ima_api.cjs ...` 会以程序错误退出（`code: -100`），stderr 输出对应 `msg`。

> **Security note:** Credentials are only sent as HTTP headers to `ima.qq.com` and never to any other domain, file, or log.
> **Runtime dependencies:** Check `meta.json` → `required_binaries`

## API 调用模板

所有请求统一为 **HTTP POST + JSON Body**，仅发往官方 Base URL `https://ima.qq.com`。

`ima_api` 已抽离到脚本：`./ima_api.cjs`

```bash
# Example usage (cross-platform, pass credentials via options JSON)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
OPTS=$(printf '{"clientId":"%s","apiKey":"%s"}' "$IMA_OPENAPI_CLIENTID" "$IMA_OPENAPI_APIKEY")

# stdout 返回正常响应；stderr 返回结构化错误 {"code":-100|-200,"msg":"..."}
if ! resp=$(node "$SKILL_DIR/ima_api.cjs" "openapi/list_docs" '{"limit":10}' "$OPTS" 2>/tmp/ima_err); then
  err_json=$(cat /tmp/ima_err)
  err_code=$(echo "$err_json" | jq -r '.code // empty' 2>/dev/null)
  err_msg=$(echo "$err_json" | jq -r '.msg // empty' 2>/dev/null)

  if [ "$err_code" = "-200" ]; then
    # 有新版本，原请求未发送；stdout 中带有更新上下文 JSON（含 instruction）
    echo "[update] $err_msg" >&2
  else
    # -100 或其他程序错误：msg 已包含可直接展示给用户的说明
    echo "[error] $err_msg" >&2
  fi
  exit 1
fi

echo "$resp"
```

> **错误处理有两层，必须都检查：**
>
> **第一层 — 脚本执行错误**（进程非 0 退出，错误在 **stderr**）：
>
> - `-100`：程序错误（缺少凭证、参数非法、网络错误等），`msg` 可直接展示给用户
> - `-200`：skill 需要更新，原请求未发送，stdout 中有更新上下文 JSON
>
> **第二层 — 后端业务错误**（进程正常退出，响应在 **stdout**）：
>
> - stdout 返回 JSON `{"code": 0, "msg": "...", "data": {...}}`
> - `code=0` 表示成功，从 `data` 提取业务字段
> - `code≠0` 表示后端业务错误（如参数不合法、权限不足、资源不存在等），**直接将 `msg` 展示给用户**
> - 常见后端错误码见各子模块的「错误处理」章节

## SKILL Update

`ima_api` 已内置更新检查：默认**每天首次 API 调用自动检查一次**，同一天内不会重复检查。

- `latest_version`：最新版本号，格式为 `MAJOR.MINOR.PATCH`
- `release_desc`：最新版本发布说明
- `instruction`：更新指引（prompt 文本）

### 错误返回与后续处理

> 出错时进程以非 0 退出，并在 **stderr** 输出结构化 JSON：`{"code":-100|-200,"msg":"具体错误描述"}`。

- `-200`（skill 需要更新）
  - 含义：检测到可用更新，原请求**未发送**
  - 后续处理：从 `ima_api.cjs` 的 stdout 读取更新上下文 JSON，根据其中 `instruction`（prompt）引导用户完成更新，然后重试原请求
- `-100`（程序错误，兜底）
  - 含义：其他所有错误（缺少凭证、参数非法、缺少 apiPath、网络错误等）
  - 后续处理：直接读取 `msg` 向用户展示；`msg` 已指出具体原因与修复建议

> 更新检查调用本身失败时，会**直接跳过本次检查并继续原请求**，不会抛错。

如需主动触发（忽略"每天一次"限制），可在调用前设置：

```bash
export IMA_FORCE_UPDATE_CHECK=1
```

---

## Detailed Rules Reference

> The sections below contain full platform-specific examples for the mandatory rules above. Refer to these when you need implementation details.

### Detailed UTF-8 Encoding Rules

> **此规则为强制性要求，不可跳过。** 非法编码会导致内容在 IMA 中显示为乱码，且无法修复，必须重新写入。
>
> **适用范围：notes 模块**（`import_doc`、`append_doc` 等文本写入 API）。
>
> **不适用于 knowledge-base 模块的文件上传**：上传文件时必须保持文件原始内容，不得转码。文件以二进制方式上传，服务端自行处理。

**每次调用 notes 写入类 API（`import_doc`/`append_doc`）之前，必须对 `content`、`title` 等所有字符串字段执行 UTF-8 编码校验/转换。** 无论内容来源如何——用户直接输入、从文件读取、WebFetch 抓取、剪贴板粘贴、外部 API 返回——都不能假设已经是合法 UTF-8，必须显式确认。

#### 强制检查清单（notes 模块写入前）

在构造 notes 写入请求的 body **之前**，完成以下步骤：

1. **来自文件的内容**：先检测文件编码，转为 UTF-8 后再读入变量（注意：这是指读取文件内容作为笔记正文写入，不是上传文件到知识库）
2. **来自 WebFetch / HTTP 请求的内容**：响应可能为 GBK/Latin-1 等，必须转码
3. **来自用户输入或变量拼接的内容**：清洗非法 UTF-8 字节（`\xff\xfe` 等）
4. **标题字段同理**：`title` 也必须为合法 UTF-8

#### 各环境转码方法

**Python（推荐，几乎所有环境都有）：**

```bash
# 读取文件，自动检测编码并转为 UTF-8
content=$(python3 -c "
import sys
data = open('tmpfile', 'rb').read()
for enc in ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']:
    try:
        sys.stdout.write(data.decode(enc))
        break
    except (UnicodeDecodeError, LookupError):
        continue
" 2>/dev/null)

# 如果内容已在变量中，清洗非法 UTF-8 字节
content=$(printf '%s' "$content" | python3 -c "import sys; sys.stdout.write(sys.stdin.buffer.read().decode('utf-8','ignore'))")
```

**Node.js：**

```bash
content=$(node -e "const fs=require('fs');const buf=fs.readFileSync('tmpfile');process.stdout.write(buf.toString('utf8'))")
# 已知编码（如 GBK）：
content=$(node -e "const fs=require('fs');process.stdout.write(new TextDecoder('gbk').decode(fs.readFileSync('tmpfile')))")
```

**Unix (macOS/Linux)：**

```bash
content=$(iconv -f "$(file -b --mime-encoding tmpfile)" -t UTF-8 tmpfile 2>/dev/null || cat tmpfile)
```

**Windows PowerShell：**

```powershell
# 读取非 UTF-8 文件并转码
$content = [System.IO.File]::ReadAllText('tmpfile', [System.Text.Encoding]::Default)
[System.IO.File]::WriteAllText('tmpfile.utf8', $content, [System.Text.Encoding]::UTF8)
```

### PowerShell 5.1 Environment Detection

> **此问题影响所有 API 调用（notes、knowledge-base 等）**
>
> **此问题极其隐蔽：PowerShell 5.1 下 `Invoke-RestMethod` 会静默将请求 Body 从 UTF-8 转为系统 ANSI 编码（中文 Windows 为 GBK），即使设置了 `Content-Type: charset=utf-8` 也无效。结果是请求看起来发送成功，但服务端收到的内容已经是乱码，且无任何错误提示。**

**当 agent 运行在 PowerShell 环境时，必须在首次 API 调用前检测版本：**

```powershell
# 检测 PowerShell 版本 — 在任何 API 调用之前执行（notes 和 knowledge-base 都需要）
if ($PSVersionTable.PSVersion.Major -le 5) {
    Write-Host "⚠️ 检测到 PowerShell 5.1，将使用 UTF-8 字节数组模式发送请求"
    $useUtf8Bytes = $true
} else {
    Write-Host "✅ PowerShell 7+，默认 UTF-8，无需额外处理"
    $useUtf8Bytes = $false
}
```

**PowerShell 5.1 下必须使用以下方式发送请求**（用 `ConvertTo-Json` 构建 JSON 以避免手动拼接的转义风险，再显式转为 UTF-8 字节数组）：

```powershell
# PowerShell 5.1 安全请求模板（适用于所有模块的所有 API 调用）
$body = @{ title = "标题"; content = $content; content_format = 1 } | ConvertTo-Json -Depth 10
if ($useUtf8Bytes) {
    # CRITICAL: 必须转为字节数组，否则中文/非ASCII内容会变成乱码
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    Invoke-RestMethod -Uri $url -Method Post -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -Headers $headers
} else {
    # PowerShell 7+ 可直接传字符串
    Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json; charset=utf-8" -Headers $headers
}
```

> **总结：** 在 PowerShell 5.1 环境中，**所有** API 调用（无论 notes 还是 knowledge-base）都必须将 Body 显式转为 UTF-8 字节数组。不检测版本直接发请求 = 中文内容必乱码。这是 PowerShell 5.1 的已知设计缺陷，不是 bug 可以被修复。
