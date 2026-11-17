# zhihu-research-page Skill 更新日志

---

## v22.0.2 — 2026-11-09（重新发布，修正包内版本字段）

### 为什么发
v22.0.1 发布时，`SKILL.md` 的注释头与「当前版本」行已改为 22.0.1，但 frontmatter 的 `version:` 字段漏改，仍是 `22.0.0`。ClawHub 上 `22.0.1` 这个版本号的包内因此写着 22.0.0，而平台不允许同版本覆盖，只能升版本重发。

### 改动
- `SKILL.md`：`version:` → `22.0.2`，注释头、当前版本行、更新日志同步
- `.claude-plugin/marketplace.json`：`version` → `22.0.2`
- 内容与 v22.0.1 完全一致（表述统一为「回答」）

---

## v22.0.1 — 2026-11-09（表述统一：章节 → 回答）

### 为什么改
页面形态是「一个问题 + 10 个不同答主写的回答」，不是「10 个章节」。README 已先行更正为「默认生成含 10 个回答」，其余文档未跟上，造成同一份说明里两种叫法。

### 统一范围（面向用户的介绍性表述）
- `SKILL.md`：frontmatter `examples[].output`（2 处）、概述要点（2 处）、阶段 0 参数表（回答建议 / 回答撰写语言）、N% 裁剪表（每个回答字数 / 回答数 / 字数/回答）、资源文件说明
- `README.md`：核心特性表（10 个回答多答主 / 每个回答独立答主）、剪裁比例表列名、TROUBLESHOOTING 条目数（12 → 15 类）、补齐文件结构（`inline_images.py`、`examples/`、`tests/`、`.claude-plugin/`、`CHANGELOG.md`）
- `examples/basic.md`、`examples/advanced.md`、`tests/test.md`：示例与自检条目描述

### 未改动（有意保留）
- `CHANGELOG.md` 历史记录——日志是事实记录，不倒改
- 内部实现术语 `CHAPTERS` / `_draft_ch_*.html` / 锚点 `ch-01` / 组装步骤——代码与文件名仍以章节为单位，改了会与实现脱节

### 一处产品输出变更
- 生成页侧栏标题 `<h3>📑 本页章节</h3>` → `<h3>📑 本页回答</h3>`（`SKILL.md` 骨架模板与 `scripts/assemble.py` 同步修改）

---

## v22 — 2026-10-29（单文件 HTML 交付 + 可选上传资料库 + 三平台发布）

### 新增文件
- **`scripts/inline_images.py`** — 单文件 HTML 打包脚本
  - 内嵌三类引用：`<img src>`、`<style>`/`style=` 内 `url()`、`<source srcset>`
  - MIME 映射 png/jpeg/svg+xml/gif/webp/ico/bmp/avif
  - 缺失图片保留原路径 + 打印清单，不中断
  - **三重校验**通过才删除 `index.html`：`zh-header` + `</main>`、`<article id="ch-` 计数一致、`data:image/` 计数达标
  - 失败时两个文件都保留，退出码 1

### SKILL.md 改动
- 阶段 7 重组：`7.1 结构校验 → 7.2 链接抽检 → 7.3 打包单文件 → 7.4 交付 → 7.5 可选上传资料库 → 7.6 工作记忆`
- **7.3 打包单文件 HTML**：命名规则 `{工作区文件夹名}_{ASCII 主题名}.html`（中文主题**意译成英文**、去标点、词首大写、≤32 字符）
- **7.5 可选上传资料库**：交付后主动询问一次 → 用户同意才调 `LibraryUpload`（绝对路径）；>100 MiB 直接跳过
- 工作区目录约定：最终产物改为单文件 HTML，`index.html` 降级为中间产物（打包后删除，**不留副本**）
- 阶段 0 输出路径参数同步
- 工作流总览 `[7]` 改为「打包单文件 + 交付 + 可选上传资料库」
- 质量规则新增 3 条（单文件交付 / 删除前校验 / 资料库上传）
- 报错与降级新增 2 条（缺图 / 体积超限）
- 资源文件新增 `scripts/inline_images.py`

### frontmatter 补充（供 SkillHub 发布）
- 新增 `slug: zhihu-research-page`、`displayName`、`summary`、`license: MIT`
- `version` → `22.0.0`

### TROUBLESHOOTING.md
- 12 类 → 15 类：新增「单文件打包缺图」「单文件超 100 MiB」「删除 index.html 后需重生成」

### 已发布平台
- GitHub：`timeRATE-966/zhihu-research-page-skill`
- ClawHub：`@timerate-966/zhihu-research-page-skill`
- SkillHub：`@user_f9803b42/zhihu-research-page`

---

## v21 — 2026-07-21（教程/学习模式 + 自动同步 + 版本头）

- 主题含教程/教学/学习路径/怎么做/入门时启用教程模式：提炼答主背景、必要时提问、搜索偏入门实战、写作按「跟着做就能上手」结构
- 阶段 0 新增「自动同步检查」：对比 `<!-- VERSION -->` 与工作区 `.skill_version`，落后则归档旧脚本到 `./other/_OLD/{时间戳}/` 再复制新版
- SKILL.md 顶部新增版本头 + 逐版本压缩更新日志（带秒级时间戳）

---

## v20 — 2026-07-19（v2_1pct 实战日志 4 项修复）

### 修复 1（阻断性）：assemble.py f-string 转义引号 → SyntaxError
- autocheck 第④项 `f'{prop}:{val.replace(\" \", \"\")}'` → 拆为 `val_compact = val.replace(' ', '')` + `f'{prop}:{val_compact}'`
- 所有 ✓/❌ emoji 替换为 ASCII `[PASS]`/`[FAIL]`（#2 Windows GBK 崩溃）

### 修复 2：Windows GBK emoji 崩溃
- `print("... ✓")` → `print("... [PASS]")`，全部 37 处 emoji 替换为 ASCII

### 修复 3：N% 模式误报"还差 97801 字"
- `assemble.py` 新增 `TARGET_WORDS = 100000`（可配置变量）
- 字数达标判断从硬编码 `100000` 改为 `TARGET_WORDS`
- SKILL.md Phase 6.5 新增 N% 模式提示

### 修复 4：Edit 工具含反引号匹配失败
- SKILL.md Phase 3.2 前新增「追加策略」框：优先 Python `open(path, "a")`，Edit 仅用于文件头计数器

### 其他
- SKILL.md Phase 6.5 新增 Windows 运行 `PYTHONIOENCODING=utf-8` 提示

---

## v19 — 2026-07-18（新增「部分执行模式」—— N% 版本）

### 新增
- **Phase 0「部分执行模式」**：当用户说"仅执行 3%/N%"时，按等比缩放：
  - 搜索次数 `max(15, floor(500 × N%))`、字数 `max(3000, floor(100000 × N%))`
  - 章节数 `min(10, max(3, floor(10 × N%)))`、搜索代理 1 个、跳过头像搜索
  - 工作目录 `v{N}_{percentage}pct/`（与上一版本同级，如 `v3_3pct/`）
  - HTML `<title>` 和问题 `<h1>` 必须包含"N%版本"字样
  - 主题、大纲结构与上一版本保持一致，仅因子量等比压缩

### 同步
- 4 个位置全部同步，`.skill` 34,049 bytes

---

## v18 — 2026-07-18（去硬编码重构 + 异常手册 + 蓝阈值修复）

### 新增文件（5 个）
- **`TROUBLESHOOTING.md`** — 12 类高频异常根因+修复方案（配额/通知/字体/编码/阈值/字数/权限等）
- **`scripts/wordcount_check.py`** — 独立字数核验 + `<code>` 完整性检查脚本（每章写完后强制运行）
- **`templates/writing_agent_prompt.md`** — 章节撰写代理 Prompt 模板（替代 SKILL.md 内嵌 ~90 行）
- **`templates/search_agent_prompt.md`** — 搜索代理 Prompt 模板（替代 SKILL.md 内嵌 ~25 行）
- **`templates/author_block.html`** — 统一作者块 HTML 模板

### 去硬编码
- SKILL.md Phase 3.1：搜索代理 prompt → `templates/search_agent_prompt.md`
- SKILL.md Phase 5.2：章节撰写 prompt + Python 自检脚本 → `templates/writing_agent_prompt.md` + `scripts/wordcount_check.py`
- SKILL.md 字数自检脚本另存为独立可调用文件

### 修复（用户反馈问题 5）
- **蓝阈值收紧**：`b > 0x80 & b > max(r,g)*0.8` → `b > 0xC0 & b > max(r,g)*1.2`，避免 `#f8f8fa` 误替换为 `var(--zhihu-blue)`
- **autocheck 字典兼容**：`padding` 比较改用压缩格式 `cs.replace(' ', '')`，兼容 CSS 压缩后无空格写法

### 新增规则
- **TROUBLESHOOTING 优先**：SKILL.md 顶部新增「异常处理」节，要求遇到异常先读 TROUBLESHOOTING.md
- **资源文件**更新为 8 项（含 3 模板 + TROUBLESHOOTING）

---

## v17 — 2026-07-18（7 项实战教训——配额/验收/去重/前移/编码/头像/引用）

### 1. 搜索代理配额感知（问题 1）
- 7 并行各 72 次 → **3 轮串行**，每轮 `min(3, floor(剩余配额/72))` 个代理
- 官网文档优先 WebFetch（不计入搜索配额），避免"尝试→失败→请提升配额"空转

### 2. 子代理验收标准（问题 2）
- **仅以文件落盘为完成凭证**：`ls` + 文件大小 > 0
- task-notification 元数据声明不可信（"搜索 85 次"可能实际仅 20 次）
- 代理必须写入明确路径文件（如 `./research_result/report_XX.md`）

### 3. 来源池外部化（问题 3）
- 完整来源池写入 `./research_result/source_pool.md`
- 撰写 agent prompt 仅传 **3-5 条专属 URL** + 引用路径，不再全文注入 50+ URL

### 4. `<code>` 自检前移（问题 4）
- **写作 agent 自检脚本增加 `<code>` 完整性检查**（开闭计数 + 块级嵌套），问题消灭在草稿内
- assemble 阶段 scan_html.py 变为兜底验证

### 5. Windows 编码兼容（问题 5）
- `scan_html.py` 新增 `sys.stdout.reconfigure(encoding='utf-8')`（Windows 自动触发）
- SKILL.md Phase 6.2 增加 `python -X utf8` / `PYTHONIOENCODING=utf-8` 说明

### 6. 头像默认 DiceBear（问题 6）
- Phase 4.5 默认策略改为 DiceBear SVG（零搜索成本）
- 仅用户明确要求时才启动子 agent 搜索真实头像

### 7. 报错与降级新增 3 条
- 搜索代理集体触顶、scan_html.py Windows 编码崩溃、`<code>` 自检不通过

---

## v16 — 2026-07-18（三类系统性 CSS 根治：模板规范 + 去硬编码 + 自动自查）

### 一、css-template.css 规范修复
- **`<code>` 样式对齐知乎官方**：color `#191b1f`（正文色，非粉 #d63384）、background `#f8f8fa`、padding `3px 4px`、margin `0 2px`、font-family 知乎专用等宽栈（Menlo/Monaco/Consolas…）、font-size `0.9em`、word-break/line-height 规范
- `.zh-body` → `.zh-page`（v14 已完成，本次确认彻底消除同名类混用）

### 二、SKILL.md Phase 5.2 去硬编码 `<style>` 块
- **写作代理 Prompt 新增铁律**："严禁内嵌 `<style>` 块——骨架已通过 css-template.css 提供全部样式"
- 避免 10 个章节草稿各带一套完整 `<style>` 导致 cascade 冗余和颜色冲突

### 三、assemble.py 新增自动自查步骤（11 步中的第 9 步）
在写回磁盘前运行 5 项检查，**不通过直接 `sys.exit(1)` 终止**：
1. `:root` 中 `--zhihu-blue` 定义数（须为 1）+ `var()` 用法数
2. 检测残留硬编码蓝系 hex（非 `:root` 行）
3. 重复 `<style>` 块报告（"块 X 与块 Y 相同"）
4. `.zh-answer__body code` 样式与模板一致性校验
5. `.zh-body` 类名出现次数（须为 0）

### 修改
- assemble.py 步骤重新编号：…8→侧栏, **9→自查**, 10→写回, 11→统计
- SKILL.md Phase 6.3 步骤列表从 9 步更新为 10 步

---

## v15 — 2026-07-18（assemble.py 新增 `<style>` 去重 + 主题蓝归一）

### 新增（assemble.py 两个后处理步骤）
- **步骤 5 — 去重 `<style>` 块**：10 个章节草稿各带卡片模板，相同模板产生完全重复的 `<style>` 块——遍历所有块，内容相同的只保留首次出现，其余移除。打印 `[去重] 移除了 N 个重复的 <style> 块`
- **步骤 6 — 统一硬编码主题蓝**：扫描去重后的 `<style>` 块，将蓝系 hex（`#0084ff`、`#0066ff`、`#175199` 等，判定规则：蓝通道 >0x80 且 >max(R,G)×0.8）替换为 `var(--zhihu-blue)`。非蓝系（橙 `#ff7a45`、灰 `#333` 等）保留，`:root` 变量定义行不触碰。打印替换数量

### 修改
- `assemble.py` 步骤重新编号：2→2, 3→3, 4→4, **5→去重**, **6→归一**, 7→7, 8→8, 9→9, 10→10
- SKILL.md Phase 6.3 步骤列表从 7 步更新为 9 步（含新增的两个后处理）
- CSS 类名隔离注释精简（去重和归一已内置在 assemble.py 中，不再需要手动建议）

---

## v14 — 2026-07-18（回滚 v13 身份限制 + 修复 CSS 类名冲突 `zh-body`→`zh-page`）

### 修改 1：回滚 v13 身份限制性语言
- 删除 Phase 4.5 的"核心原则（解耦）"块
- 恢复 Tier 1 表格为原始"真实人物公开头像"（去掉"仅作视觉素材、不冒用身份"）
- 铁律中删除"答主名绝不冒用真实人物身份"
- JSON 字段描述从"虚构"恢复为"与章节领域匹配"
- 质量规则从"头像与身份"恢复为"头像真实性"
- **头像三级优先级（真实图源 → DiceBear → 单字符）完全不变**

### 修改 2：CSS 类名冲突修复
- **根因**：页面级包裹层 `<div class="zh-body">` 和卡片模板章节正文容器 `.zh-body` 同名，`<style>` 标签全局生效无作用域隔离，导致模板强调色通过 `.zh-body h2 { border-left: #ff7a45 }` 泄漏到所有章节
- **修复**：`css-template.css` 中 `.zh-body` → `.zh-page`，与卡片容器彻底隔离；SKILL.md 骨架模板同步更新
- **新增 CSS 规范**：
  - Phase 6.3 后追加"CSS 类名隔离与样式合并"注意事项
  - 章节草稿内覆盖样式建议用更具体的选��器链（如 `#ch-01 .zh-body h2`）
  - 多个 `<style>` 块重复选择器的 cascade 覆盖风险提示
- **质量规则新增**：CSS 类名隔离 + `<style>` 块合并去重

---

## v13 — 2026-07-18（解耦头像图源与答主身份——不冒用真人身份）

### 修改
- **Phase 4.5 新增「核心原则」**：头像图源和答主身份必须解耦——头像可借真实人物公开图源（GitHub CDN 等）作视觉素材，但答主名和简介必须虚构
- **铁律新增**："答主名和简介绝不冒用真实人物身份"
- **JSON 映射示例**：`ch-03` 从 `"name":"稚晖君"` 改为 `"name":"开源极客小凯"`，保留 `avatar_remote` 标注头像出处
- **字段调整**：新增 `avatar_source`（头像出处说明），移除 `verified_sources`（不再需要交叉印证真实人物身份，因为答主本来就是虚构的）
- **质量规则**：`头像真实性` → `头像与身份`，增加"答主名必须虚构"规则

### 不变
- 头像三级优先级（真实图源 → DiceBear → 单字符）完全保留
- 头像缓存到 `./images/` 的流程不变
- curl 亲测可达、身份交叉印证等验证规则仍适用于**图源可靠性**（不代表答主身份）

---

## v12 — 2026-07-18（全部图片本地化——`./images/` 适用范围扩大）

### 修改
- **`./images/` 从「仅头像」扩展为「所有图片资源」**：截图、示意图、logo 等全部进 `./images/`
- **目录约定**更新：`images/` 目录描述增加"章节插图/截图/示意图/logo"
- **Phase 5.2 写作规范**新增一行：章节内所有 `<img>` 必须用 `./images/` 本地路径，禁止外链
- **质量规则表**：新增「图片路径」规则——所有 `<img src>` 必须指向 `./images/`

---

## v11 — 2026-07-18（头像本地缓存——`./images/` 子目录）

### 新增
- **头像图片本地缓存**：通过 `curl` 验证的真实头像和 DiceBear SVG 均下载到 `./images/` 子目录
- **新增步骤 2.5「缓存头像到本地」**：Phase 4.5 流程从四步扩展为五步
- **目录约定新增 `./images/`**

### 修改
- **作者块 `img src` 改为本地相对路径**（`./images/ch-01.png`），避免外链失效
- **JSON 映射表**：`avatar` 改为本地路径，真实人物保留 `avatar_remote` 供溯源
- **权限配置**新增 Write/Bash 对 `images/*` 的授权

---

## v10 — 2026-07-18（工作区目录组织——`./other/` + `./research_result/`）

### 新增
- **工作区目录约定**：根目录不再散落大量中间文件，严格按两目录组织：
  - `./other/` — 网页草稿（`_draft_*.html`）、复制脚本（`assemble.py`、`scan_html.py`）、所有中间产物（`.ps1`、`.py`、备份 `index_skeleton.html`）
  - `./research_result/` — 搜索结果累积（`search_result.md`）、来源池清单、搜索报告
- 阶段 0 第一步新增：`mkdir -p ./other ./research_result`
- 最终交付的 `index.html` 仍留在根目录

### 修改
- **SKILL.md 全局路径更新**（65+ 处引用）：
  - `./search_result.md` → `./research_result/search_result.md`
  - `./_draft_*.html` → `./other/_draft_*.html`
  - `./assemble.py` → `./other/assemble.py`
  - `./scan_html.py` → `./other/scan_html.py`
- **权限配置**（`.claude/settings.local.json`）路径同步更新
- **`scan_html.py`**：glob 模式增加 `./other/` 优先查找 + 根目录兜底
- **`assemble.py`**：新增 `DRAFT_DIR = "./other"`，`pick_file()` 优先在 `./other/` 中查找草稿
- Phase 6.4 骨架备份改为 `./other/index_skeleton.html`
- grep 验证命令中的路径同步更新

### 同步
- 4 个位置全部同步（SKILL.md + scan_html.py + assemble.py）
- `.skill` ZIP 重打包（23,497 bytes）

---

## v9 — 2026-07-18（答主身份与头像配置——三级优先级 + 四步流程）

### 新增
- **新增阶段 4.5「答主身份与头像配置」**：夹在章节规划（阶段 4）和并行撰写（阶段 5）之间
- **三级头像优先级**：
  - 1 级：真实人物公开头像直链（GitHub CDN、豆瓣影人、雪球/掘金/丁香园、个人官网），身份须交叉印证
  - 2 级：DiceBear 风格化 SVG（三种风格交替配合不同配色区分答主）
  - 3 级：单字符兜底（前两级均不可用时）
- **四步完整流程**：
  1. **通道探测**：`curl` 测 GitHub CDN / DiceBear API 可达性（含代理 `-x` 支持），不同机器结果不同不预设
  2. **身份搜索与即验**：并行子 agent 搜索真实人物，候选图链一到立刻 `curl` 亲测可达，双重印证
  3. **注入并统一结构**：所有作者块收敛为 `zh-answer__author-avatar > img` 单模板，避免 10 个 agent 4 种变体
  4. **Dump 最终确认**：`grep -o 'author-avatar[^<]*'` 逐行确认，不依赖跨行正则
- **答主映射表**：4.5 产出 JSON（name / bio / avatar / tier / verified_sources），直接传给写作代理 Prompt

### 修改
- **Phase 5.2 作者块模板**：从 `<div class="zh-avatar">` 单字符兜底改为统一的 `<div class="zh-answer__author-avatar"><img src=...>` 结构
- **工作流总览**：8 阶段 → 9 阶段（插入 4.5）
- **Phase 7.1 结构校验**：新增作者块 `author-avatar` 非空 `src` 检查
- **质量规则表**：新增「头像真实性」和「作者块统一」两条
- **报错与降级表**：新增 3 条（头像链不可达、身份无法印证、组装后 avatar 缺失）
- **铁律**：绝不编造图链、身份不明的真实人物宁弃用、不依赖 WebFetch 测可达

### 关键设计决策
- 头像图链 **不用 WebFetch 验证**——企业策略/网络限制下 WebFetch 常不可靠，改用 `curl`
- 跨行 HTML 验证 **不用 `[^>]*` 正则**——换行截断误报，统一用 `grep -o` 或 Python `re.S` 上下文打印
- JSON 映射表驱动：阶段 4.5 一次性确定所有答案主头像，写作代理只填入不编造

---

## v8 — 2026-07-18（组装前预扫描 + 子代理权限 + `<code>` 标签规范）

### 新增
- **`scripts/scan_html.py`**：HTML 章节草稿预扫描脚本，在 `assemble.py` 之前运行，检测 4 类 `<code>` 标签问题：
  - A. `<code>` 开闭数量不匹配
  - B. 块级标签（`<p>`/`<table>`/`<h3>`/`<blockquote>` 等）嵌套在 `<code>` 内
  - C. 含中文字符的异常闭合标签（`</strong文>`、`</code。>`）
  - D. `<code>` 与 `<strong>` 交叉嵌套
- **子代理权限配置**：文档化 `.claude/settings.local.json` 显式授权 Write/Edit/Bash 的方案
- Phase 5 撰写代理 prompt 新增 `<code>` 标签规范 4 条（实战最高频翻车点）

### 修改
- **Phase 6 重组**为 5 步：6.1 准备脚本 → 6.2 预扫描（新增）→ 6.3 运行 assemble.py → 6.4 幂等性说明（新增）→ 6.5 判断达标
- Phase 7.1 结构校验：增加 `<code>` 标签快检项
- 质量规则表新增两条：`<code>` 标签完整性 + 组装前扫描
- 报错与降级表新增 5 条：scan_html.py 报错、字体异常排查、assemble.py 二次运行、权限被拒
- 资源文件列表新增 `scripts/scan_html.py`
- **排查优先级**：字体/结构异常 → 先查 `<code>` 标签完整性，不改 CSS

---

## v7 — 2026-07-17（存疑/争议 + 毫秒时间戳）

### 修改
- **`**存疑/争议**` 模块回归**：作为可选项写在 `**关键数据/事实**` 之后，服务于阶段 4 的「争议焦点」提取
- **区块时间戳精确到毫秒**：从 `更新于 2026-07-17` 改为 `更新于 2026-07-17 17:31:26.123`
  - 代码从 `datetime.date.today().isoformat()` 改为 `datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]`

---

## v6 — 2026-07-17（`search_result.md` 格式对齐真实文件）

### 修改
- **`search_result.md` 格式对齐**：基于 T-WATCH-2020-learn-v2 实际生产的 2609 行文件提炼
- **文件头**新增「目标」和「累计搜索次数」两个实时计数器（断点续跑友好）
- **来源格式简化**：砍掉独立「来源池」区块，来源直接内联在 `**关键数据/事实**` 下
  - 格式：`N. 标题\n   - 来源：URL`
- **区块标题**从 `第 N 批回传 · 方向：XXX` 改为 `[N] 方向 — 更新于 时间戳`
  - 用累计搜索次数做序号（非代理返回顺序）
- **写入代码增加文件头回写**：每次追加后更新「累计搜索次数」和「已覆盖子方向」
- 阶段 1 诊断信息以 `## 学习路径问题诊断` 形式纳入文件
- Phase 3.3 来源提取改用正则 `re.findall(r'- 来源：(https?://[^\s\n]+)', content)`

---

## v5 — 2026-07-16（`assemble.py` 注入机制修复）

### 问题
`assemble.py` 用 `replace('</main>', 内容)` 做章节注入——骨架占位注释若含 `</main>`（如 `<!-- 注入到 </main> -->`），所有章节被塞进 HTML 注释，浏览器不渲染。

### 修改
- **注入点改为独立占位标记** `<!-- ASSEMBLE -->`（不含 `</main>` 字符），脚本做一次 `replace` 替换，不再逐章往 `</main>` 前追加
- **运行前幂等剥离旧章节**：`re.sub(r'<article[^>]*id="ch-\d+"[^>]*>.*?</article>', '', html, flags=re.S)` — 属性顺序无关，重复运行不累积
- **锚点 id 注入改用宽松正则**：`re.sub(r'(<article[^>]*?)(>)', ...)` — 不依赖原草稿 class/id 属性顺序
- **回答数统计改用宽松匹配**：`findall(r'<article[^>]*id="ch-\d+"[^>]*>', html)` — 避免属性顺序导致漏算
- 缺失 `<!-- ASSEMBLE -->` 时脚本报错退出（`sys.exit(1)`），不再静默失败
- SKILL.md Phase 2 骨架模板同步更新，`</main>` 前增加 `<!-- ASSEMBLE -->`

---

## v4 — 2026-07-14（`search_result.md` 协同积累机制）

### 新增
- **`search_result.md` 追加机制**：每收到一个搜索子代理回传，主流程立即将结构化报告追加写入工作区 `./search_result.md`
  - 首次 `w` 模式创建文件头
  - 后续 `a` 模式逐批追加，维护 `global_search_count`
  - 序号格式 `第 N 批回传 · 方向：XXX`
- 并发安全约定：7 代理并行启动，**写入串行执行**（代理只回传，主流程逐一追加）

### 修改
- Phase 3 搜索代理 Prompt 新增「本方向搜索次数」+「回传要求」段落
- 原「汇总来源池」从 3.2 顺延为 3.3

---

## v3 — 2026-07-14（诊断先于搜索 + 去硬编码）

### 修改
- **工作流重排序**：diagnose → search → plan chapters（证据驱动，不搜完不拟标题）
- **阶段 1「诊断问题」成为强制步骤**：拆解核心问题 → 确定 7 个搜索方向 → 拟定临时标题
- **所有路径去掉硬编码**，改用 `os.getcwd()` 和相对描述
- Memory 部分改用相对路径描述：「当前工作区的 `.workbuddy/memory/`」

---

## v2 — 2026-07-14（Skill 目录只读约定）

### 新增
- **Skill 目录只读约定**：用户通过目录路径引用时（如 `{用户目录}/zhihu-research-page`），该目录只读
  - 所有文件创建/编辑在工作区完成
  - `assemble.py` 从 skill 目录**复制**到工作区后再编辑 CHAPTERS
- 增强型工作流说明：CSS 注入方式、脚本复制方式、工作区落点

---

## v1 — 2026-07-13（初始版本）

### 新增
- **8 阶段工作流**：收集输入 → 诊断 → 骨架 → 并行搜索(500+) → 规划章节 → 并行写章 → 组装 → 交付
- **知乎风 CSS 模板** (`references/css-template.css`)：含知乎设计 Token、顶栏、卡片、回答、侧栏、响应式规则
- **通用拼接脚本** (`scripts/assemble.py`)：章节注入、锚点 id、回答数更新、侧栏重建、字数核验
- **字数口径**：有效中文 = 汉字（`\u4e00-\u9fff`）+ 中文标点（`\u3000-\u303f`、`\uff00-\uffef`），去 `<script>`/`<style>`/标签
- 基于 LILYGO T-WATCH-2020 项目实战流程提炼（114,630 有效中文、242 条外链、2000+ 搜索）

> 格式：Markdown 源文件，存放于工作区 `zhihu-research-page-skill/CHANGELOG.md`
