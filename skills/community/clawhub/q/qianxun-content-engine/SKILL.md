---
name: content-engine
description: "内容引擎（小红书）。两种 mode：①拆解（v1）— 输入 XHS 爆款链接，输出 18 维结构化拆解卡；②生成（v2）— 在拆解卡基础上结合品牌信息，用 Ofox（LLM + Nano Banana）生成我方版本的脚本/文案/素材图/封面/标签全套产出。视频生成（Seedance 2.0）规划在 v2.1。同时维护 graph/ 知识图谱（品牌声音、平台 playbook、钩子库、风格词典），mode 之间共享，越用越聪明。架构受 Ronin Skill Graph 启发。后续阶段陆续接入抖音 / 视频号等平台 + evaluate 评估 mode。"
---

# 内容引擎

跨平台内容拆解 + 生成 + 知识图谱。底层是一个**会成长的图谱**，上层挂多种 mode + 多个平台。

> 英文版 / English: see `~/.agents/skills/content-engine-en/`

## Mode 路线图

| Mode | 状态 | 说明 |
|---|---|---|
| **deconstruct（拆解）** | ✅ v1 | 参考链接 → 18 维拆解卡，过程中喂养图谱 |
| **generate（生成）** | ✅ v2.2 | 拆解卡 + 图谱 + 我方品牌 → 脚本 / 字幕 / 封面 / desc / 标签 / 参考素材图。**v0.3.0**：接火山方舟 Seedance 2.0 真生视频（N 个 shot 顺序生成 + ffmpeg 自动拼成片，partial-video.md 记录失败 shot 便于手补）。**v0.2.1**：内置 validator 质检 + 自动 fallback v1。 |
| evaluate（评估） | 🔜 v3 | 成片 → 8 维加权评分 |

## 平台路线图

| 平台 | 状态 | 当前覆盖 / 计划 |
|---|---|---|
| **小红书** | ✅ v1 | 视频笔记 + 图文笔记 |
| 抖音 | 🔜 v1.1 | 短视频拆解（计划接 TikHub Douyin API） |
| 视频号 | 🔜 v1.2 | 短视频拆解 |
| B 站 | 🔜 v2 | 短视频 + 长视频 |
| TikTok / Instagram | 🔜 探索中 | 国际平台 |

> **当前阶段**：本文档完整描述了**小红书 deconstruct + generate** 的 v1+v2.0 实现。其他平台计划复用同一架构（`extract_{platform}.py` / `generate_{platform}.py` + `content_engine/{platform}/` 子模块），graph 知识图谱跨平台共享。

本文档覆盖**小红书 deconstruct mode（v1）+ generate mode（v2.0 文本+图）**。视频真生成（Seedance）在 v2.1。

> **平台兼容**：本 skill 在 OpenClaw（personal agent skill）和 Claude Code 都能直接跑。脚本用 Python 3.10+ stdlib（无外部依赖），系统命令只需要 ffmpeg。文件读写假定你的 agent 有 `Read` / `Write` 工具（OpenClaw 中是 `apply_patch`/`Exec`/`Web browser`）。

---

## 架构核心：graph/ 是大脑

```
content-engine/
├── SKILL.md           ← 你正在读的这个，agent 入口
├── graph/             ← 知识图谱（mode 之间共享的"记忆 / 灵魂 / 上下文"）
│   ├── index.md             品牌总 briefing，agent 进来先读
│   ├── brand/{brand-voice,brand-story}.md
│   ├── platforms/xiaohongshu.md     XHS 平台 playbook（v1 唯一支持）
│   │                                 (v1.1+ 会补 douyin.md / shipinhao.md / ...)
│   ├── audience/segments.md          客群分层
│   └── engine/{hooks,style-tags,taboo}.md
├── references/{output-template,example-video,example-image}.md
└── scripts/
    ├── extract_xhs.py                ← v1 拆解 CLI：链接 → 工作区
    ├── generate_xhs.py               ← v2 生成 CLI：链接 → 我方脚本/图/文案套件
    │                                  (v1.1+ 会加 extract_douyin.py / generate_douyin.py 等)
    └── content_engine/               Python 包（zero deps）
        ├── client.py                  TikhubClient（v1）
        ├── parsers.py                 NoteData / Comment 解析（v1）
        ├── linkresolve.py             短链 → note_id（v1+v2 共享）
        ├── video.py                   下载 + ffmpeg 抽帧（v1）
        ├── images.py                  图文笔记图片下载（v1）
        ├── llm.py                     Ofox LLM 客户端（v2）
        ├── nano_banana.py             Ofox 图片生成（v2，Nano Banana Pro）
        ├── lookup.py                  链接 → 拆解卡映射 + freshness（v2）
        ├── prompts.py                 5 类文本 prompt 模板（v2）
        ├── generate.py                generate mode 主编排（v2）
        ├── preflight.py               环境自检（v1+v2）
        └── models.py                  dataclass 定义
```

**两条铁律**：
1. graph 文件**可以是空模板**——拆解仍能跑，退化为「客观拆解」模式
2. 拆解过程中发现的新钩子/新风格词**自动回写**到 `graph/engine/`，图谱越用越大

---

## 何时触发

- 用户给 XHS 链接说「拆一下」「研究一下」「分析一下这条为什么火」
- 内容策划阶段对标分析
- 生成新内容前的「先研究」

## 输入

| 必填 | 项 | 说明 |
|---|---|---|
| ✅ | 参考链接 | XHS 短链/长链/24 位 hex/分享口令文本均可 |
|  | 任务编号 | 默认 `AIC-{YYMMDD}-{序号}` |
|  | 内容目标 | 例如「门店引流」「私域加微」，影响"可学习要点"字段 |

## 输出

Markdown 文件 → `docs/deconstructions/{编号}-{slug}.md`。

完整字段定义见 `references/output-template.md`，范例见 `references/example-video.md` / `example-image.md`。

---

## 工作流

### Step 0：检测 graph 状态 → 选模式

用 agent 自带工具直接检查（**不依赖 shell**，避免 bash globstar / realpath 兼容问题）：

1. 找到 skill 根目录（`SKILL.md` 所在目录）
2. 用 `Read` 或 `Grep` 工具扫 `graph/**/*.md` 中是否有 `# TODO:` 标记

最简单：用 Grep 工具一次搜索：
```
Grep pattern: "^# TODO:"  path: <skill_root>/graph/  output_mode: files_with_matches
```

| 命中文件数 | 模式 | 行为 |
|---|---|---|
| 0 | **品牌视角** | Step 5 的"目标客群""可学习要点"基于 graph 内容生成；字段填充时**强制读** graph 相应节点 |
| ≥1 | **客观拆解** | 跳过品牌视角字段；输出末尾追加提示「⚠️ graph/ 未填充，建议先补 {未填文件列表}」 |

**两种模式的"可学习要点"差异**：见 `references/example-video.md` 末尾的双版本对比。

> graph 文件之间的引用约定 `[[brand/brand-voice]]`：这是 Obsidian 风格的 wikilink，指向 `graph/brand/brand-voice.md`（不带 `.md` 后缀）。agent 看到 `[[X]]` 时应该 Read 对应文件加载上下文。

### Step 1-3：一键拉数据 → 工作区

**全部用一个命令完成**：解析链接 / 拉元数据 / 拉评论 + 提取关键词 / 下载视频 + 抽帧 / 下载图文图片。

> ⚠️ **v1 仅支持小红书**。抖音 / 视频号 / B 站等其他平台规划中（v1.1+），届时会有对应的 `extract_douyin.py` / `extract_shipinhao.py` 脚本。

```bash
python3 scripts/extract_xhs.py "<XHS 链接 / note_id / 分享口令>"
# 默认工作区：{tempdir}/content-engine/{note_id}/
# 自定义： --out /your/path
```

首次运行先环境检查：
```bash
python3 scripts/extract_xhs.py --check
```
（检查 Python 版本 / ffmpeg / TIKHUB_API_TOKEN / 网络 / 工作区可写。详见下方"## 安装与依赖"）

**工作区产物**（默认 `{tempdir}/content-engine/{note_id}/`，跨平台）：

| 文件 | 内容 | 后续怎么用 |
|---|---|---|
| `note.json` | 解析后的 `NoteData` dataclass（已抽好所有字段） | 直接 Read，对应 SKILL.md Step 5 字段表 |
| `comments.json` | 解析后的 `Comment` 列表（含 `is_pinned` 启发式标记） | 你（agent）在 Step 5c 自己读原文做语义分类——比 regex 准 |
| `{note_id}.mp4` | 视频笔记的原视频（CDN 直链下载） | Step 4 抽帧用 |
| `frames/frame_NNN.png` | 视频抽帧（按时长自动选 fps：短片 1.0、中片 0.5、长片 0.25） | Step 4 逐帧 Read |
| `images/image_NNN.jpg` | 图文笔记的所有图片（按顺序编号） | Step 4 逐图 Read |

**异常处理**：
- API 401/403 → 返回非 0 退出码，告诉用户并停止
- 评论 API 失败 → `comments.json` 写 `{"_error": "..."}`，"评论关键词" 字段填「⚠️ 未获取」
- 非 XHS 链接 → 告知「v1 仅支持小红书」并停止

**常用 flags**：
- `--no-video` 跳过视频下载（只看元数据时）
- `--no-comments` 跳过评论
- `--fps 1.0` 强制抽帧频率（默认按时长自适应）

### Step 4：多模态拆解

#### Step 4a · 拆解前必读（graph 硬卡点）

**一律先 Read 一次**：
- `graph/platforms/xiaohongshu.md` 的「拆解时重点看」+「平台爆款公式」+「禁忌」三章
- `graph/engine/style-tags.md` 完整词典（Step 5 风格标签字段会用）
- `graph/engine/hooks.md` 完整钩子库（Step 5 情绪钩子字段会用）

如果是品牌视角模式，再读 `graph/brand/brand-voice.md` + `graph/brand/brand-story.md` + `graph/audience/segments.md`。

#### Step 4b · 视频分支（type == "video"）

1. **逐帧 Read** `frames/frame_NNN.png`，按文件名顺序。每帧 mental-note：景别 / 主体 / 动作 / 背景 / 道具 / 镜头方向。**不是输出 N 行流水**，是为下一步聚合积累素材。
2. **按时间段聚合**写入"参考内容拆解"。**核心规则**：

   | ✅ 好（聚合 + 信息密度） | ❌ 差（流水账或空话） |
   |---|---|
   | 第 7-12 秒｜镜头：固定 → 缓推｜景别：特写 → 极特写<br>画面：祖母绿马甲领口和门襟，绿色玉石盘扣 + 白色钉珠勾勒的几何纹样，挂着白色玉牌作为搭配示范 | 第 7 秒｜特写｜画面：领口<br>第 8 秒｜特写｜画面：领口<br>第 9 秒｜特写｜画面：盘扣<br>... |
   |  | 第 7-12 秒｜画面：很美的衣服细节，工艺精致 |

   **合并规则**：
   - 连续 2+ 帧主体/景别相同 → 合并成一个时间段
   - 主体/景别切换 → 另起一段
   - 单帧停留 < 2 秒一般不单独成段
   - 描述用**具体名词**（祖母绿、钉珠、玉石盘扣），禁用**形容词堆砌**（高级、精致、唯美）

3. **旁白文案**：
   - 视频字幕条原文 + `note.json` 的 `desc` 拼合
   - 纯画面无字幕 → 写「无旁白/字幕，纯画面表达」+ 列出底部固定 watermark 信息

4. **旁白逻辑分析**：分层填，每层标时间段 + 一句话功能：
   - 例：「第一层 · 建立反差与好奇（0-12 秒）：用 75 后 + 2000 平的数字反差激发好奇」
   - 常见结构：钩子开场 → 场景代入 → 产品/卖点 → 身份感升华 → CTA / 反差开场 → 故事铺垫 → 价值观 → CTA / 工艺特写 → 文化寓意 → 情感共鸣 → 标签升华

#### Step 4c · 图片分支（type == "normal"）

1. **逐图 Read** `images/image_NNN.jpg`，按顺序
2. 每张描述：构图 / 元素 / 风格 / 作用（在整组里的角色）
3. **聚合**写入"参考内容拆解"，按图序：「图 1（封面）：... / 图 2：... 」

### Step 5：抽取剩余字段

#### Step 5a · 字段填充表（graph 影响）

| 字段 | 来源 | graph 必读 |
|---|---|---|
| 平台 | 链接来源 | — |
| 目标客群 | `note.json.desc` + `hashtags` + 评论行为推断 | **品牌视角下**：必须对照 `graph/audience/segments.md` 已有分层填，命中哪一层显式标注 |
| 爆款主题 | `note.json.desc` + `title` + 拆解 | — |
| 风格标签 | 画面 + 文案 | **必须**对照 `graph/engine/style-tags.md`，命中标"已有"，没命中标"新增"并准备 Step 6 回写 |
| 场景标签 | 画面 | — |
| 情绪钩子 | 开头 + 钩子句 | **必须**对照 `graph/engine/hooks.md` 已分类的钩子模式，命中哪一类显式标注 |
| 评论关键词 | `comments.json`（agent 自己分类） | 见 Step 5c — agent 直接读评论原文做语义分类，比 regex 准 |
| 旁白逻辑分析 | 文案结构 | — |
| 参考热门标签 | `note.json.hashtags`（已清理 `[话题]`） | parser 已抽好，直接拼 `#xxx`；**不要再 grep desc** |
| 可学习要点 | 全局总结 | **强依赖**：品牌视角下写"我方做同主题怎么用"；客观模式写客观要点 |

#### Step 5b · 主观字段质量标尺

详见 `references/output-template.md` 的"字段定义详解 + Anti-Pattern"小节。**核心原则**：

- **爆款主题**写"为什么火"（机制），不写"是什么"（描述）
- **情绪钩子**写"用什么手法激发什么情绪"（双层），不写一个孤词
- **风格 vs 场景 vs 情绪钩子**：风格="看起来感觉"，场景="发生在哪"，情绪钩子="让用户内心起什么波澜"——三者不混淆

#### Step 5c · 评论关键词的语义分类（你自己做，不依赖 regex）

**为什么不用 regex**：语言无穷变体（`怎么卖` / `啥价` / `贵不贵` / `多少米`），regex 永远漏抓；regex 也分不清语义（`价格不是问题` 不是询价；`不是真丝吗` 不是异议）。**你（agent）有完整的语言理解能力，直接做这件事，比 regex 强 100 倍。**

**数据源**：`comments.json` 已经过 parser 过滤——`is_pinned=True` 的商家置顶 / 反诈骗自动标了，可以跳过；其余都是用户真实评论。

**分类四类**（按"用户在干什么"分）：

| 类别 | 抓什么 | 例 |
|---|---|---|
| **ask** 问 | 问购买路径 / 价格 / 地址 / 时间 / 渠道（转化前置信息） | "怎么买" / "多少钱" / "啥价" / "怎么卖" / "店在哪" / "几点关门" / "线上有吗" |
| **request** 求 | 主动提需求（强意向） | "求微信" / "还有吗" / "断码了吗" / "求联系" |
| **praise** 夸 | 共鸣 / 喜欢的具体表达 | "好美" / "想要" / "高级感" / "显气质" / "心动" |
| **objection** 异议 | 纠正 / 反对（**不是中性疑问**） | "请不要叫它X" / "这是 A 不是 B" / "不应该这么贵" |

**输出格式**（强制带证据）：

```
- {关键词}（{N} 条原评：「原文1」「原文2」「原文3」）— {一句解读 / 转化信号判断}
```

**防伪约束**（硬性）：
1. 每个关键词必须附 1–3 条**原始评论原文**（直接从 comments.json 复制，不许改写）
2. 找不到原文证据的关键词**不允许出现**——禁止凭空生成
3. **疑问句不算异议**——「不是真丝吗？」是中性询问，归 ask；「请别叫它新中式」才归 objection
4. 同一原评可以同时归到多类——比如「怎么买啊好喜欢绿色」既是 ask 又是 praise，分别引用
5. comments.json 是 `[]` 或带 `_error` → 写「⚠️ 评论数据未获取」，**不允许从 desc 推测**

**好坏对照**：

```
✅ 好（带证据 + 解读）：
- 怎么买（5 条原评：「绿色裤子怎么买」「怎么购买？线上」「怎么买呢 好喜欢绿色」）—
  最高频转化信号
- 怎么卖 / 啥价（2 条原评：「怎么卖啊」「这套啥价」）— 询价的另一种说法
- 异议·满族服饰（1 条原评：「这是新宾满族服饰，请不要叫它新中式！」👍 1）—
  虽只 1 条但获赞，提示标签使用边界

❌ 差（无证据 / 编造）：
- 怎么买、多少钱、求链接（光列词，没原文，禁止）

❌ 差（误判疑问为异议）：
- 异议（评论：「这是真丝吗」）  ← 这是疑问不是异议
```

### Step 6：回写图谱（让系统越用越聪明）

**回写位置规范（严格）**：

| 类型 | 文件 | 插入位置 | 格式 |
|---|---|---|---|
| 新钩子 | `graph/engine/hooks.md` | `## 待分类（拆解新发现，先扔这里再人工归类）` 章节末尾 | `### {情绪类型｜模式名}` 三级标题 + bullet (模式/适用/例/来源) |
| 新风格词 | `graph/engine/style-tags.md` | `## 待归类（拆解新发现）` 章节的表格末尾追加行 | `| 标签 | 适用 | 首次来源 |` |
| 平台观察 | `graph/platforms/xiaohongshu.md` | `## 观察日志` 章节**头部**插入（倒序，新的在最上） | `### {YYYY-MM-DD} · {一句话主题}` + bullet (来源/观察/数据/推论) |

**回写原则**：
1. 只追加，不删旧
2. 每条带「来源 = 拆解编号」+「日期 / 数据」
3. 与现有图谱有矛盾 → 不写入，输出末尾打 ⚠️ 给人工裁决
4. 命中已有钩子/标签 → **不要重复添加**，只在拆解卡里标"复用 graph 现有"即可

### Step 6.5：输出前自检（强制清单）

每条必须 ✓，不通过不能进 Step 7：

```
□ 18 个 Excel 字段都填了，没有跳过
□ 元数据 5 项（作者/时间/互动/note_id/类型）都从 API 实拉，没编造
□ "风格" vs "场景" vs "情绪钩子" 没混淆（区分见 output-template.md）
□ 参考发布文案是 desc 原文（含 emoji 和换行），没改写没精简
□ 评论关键词每条都从 comments.json 找原文佐证；comments.json 含 `_error` 时统一写"⚠️ 未获取"
□ 旁白逻辑分析按"分层（钩子/铺垫/升华/CTA）"写了，不是一段流水
□ 风格标签命中 graph 已有词标了"已有"；新词标了"新增"
□ 情绪钩子命中 graph 已有模式显式标注；新模式准备 Step 6 回写
□ 参考热门标签直接用 note.json.hashtags（parser 已清理 [话题]）
□ Step 6 回写：明确说"N 项"或"无"，每项标了来源/日期
□ 客观拆解模式下：输出末尾追加 graph 未填充提示
```

### Step 7：发布拆解卡

#### Step 7a · 生成 slug
从 title 生成文件/文档名 slug：
```python
import re
slug = re.sub(r"[^\w一-龥\-_·]+", "-", title)[:30].strip("-") or "untitled"
# 例：「深圳新中式｜把江南春色穿在身上」→ "深圳新中式-把江南春色穿在身上"
```

最终命名：`{编号}-{slug}`（如 `AIC-260426-001-深圳新中式-把江南春色穿在身上`）。

#### Step 7b · 输出（按 agent 环境分支）

**优先：飞书 Docx**（OpenClaw 装了 [飞书官方插件](https://www.feishu.cn/content/article/7613711414611463386) 时）

OpenClaw + 飞书插件给 agent 暴露的工具能直接创建云文档。在 OpenClaw 环境下：
1. 用 **飞书插件的「创建云文档 / create cloud doc」工具**（具体工具名以你装的插件版本为准），把完整 markdown 内容传进去
2. 标题用 `{编号}-{slug}`
3. 拿到飞书文档 URL，记下来用于 Step 7c

**Fallback：本地 markdown**（Claude Code / 没有飞书插件 / 飞书工具失败）

```bash
# Agent 用 Write 工具写到：
docs/deconstructions/{编号}-{slug}.md
```

**判断逻辑**：
- agent 自检：当前会话有「create cloud doc」「飞书文档」类工具吗？
- 有 → 飞书优先，本地不写第二份
- 无 → 直接本地

**注意**：本 skill 不再封装飞书 API 调用。OpenClaw 飞书插件已经处理认证 / 上传 / 转换；agent 只需要调插件工具。Claude Code 用户如果想发布到飞书，需要自己手动复制 markdown 到飞书文档。

#### Step 7c · 给用户的总结（固定 4 行）

```
1. 拆解对象：{标题 / 作者 / 时长 / 互动数} ——一句话
2. 最强洞察：{1 个核心钩子或反常识发现}（{数据佐证，如"藏赞比 70%"}）
3. 发布到：{飞书 URL 或本地绝对路径}
4. 图谱回写：{N 项；列前 3 个，余略；如果 0 项明示"无"}
```

---

# v2 Generate Mode（v0.2.0+）

把 v1 拆解卡当对标参考 + 我方品牌信息 → 生成我方版本的脚本 / 文案 / 素材图 / 封面 / 标签全套产出。

## 何时触发

用户说类似的话：
- 「基于 https://xhslink.com/o/xxx 给我家品牌生成同主题的视频」
- 「学这条结构出我家的 8 张图文笔记」
- 「这条爆款的钩子可以学，给我家做一套」

## 输入

| 必填 | 项 | 说明 |
|---|---|---|
| ✅ | XHS 链接 | 用户**只传链接**，agent 不让用户记拆解卡文件名 |
| ✅ | --type | `video` / `image` / `script` 三选一 |
| ✅ | --count | 1-N（图片张数 / 视频条数） |
|  | --product-imgs | 我方产品图路径（目录或单图）— v2.0 仅文本辅助生图，v2.1 改 image-to-image |
|  | --product-usp | 我方产品卖点文字描述 |
|  | --fresh | 强制重拆 v1（绕开缓存）|

## 输出工作区

```
docs/deconstructions/AIC-260426-001-xxx-generated/    ← v1 拆解卡同名目录加 -generated
└── GEN-260427-001-image/                            ← 一次 generate 一个 GEN-N
    ├── script.md                                    ← 完整脚本（图组规划 / 视频分镜 / 拍摄指引）
    ├── caption.txt                                  ← (video 类型) 屏幕字幕层
    ├── cover.png + cover.txt                        ← 封面图（含大字）+ 文案备份
    ├── frames/frame_NNN.png                         ← N 张参考素材图（Nano Banana 出，竖版 9:16）
    ├── desc.txt                                     ← XHS 发布正文
    ├── tags.txt                                     ← 标签（10-15 个）
    ├── seedance-prompt.md                           ← (video 类型) Seedance cinema-style prompt
    ├── shots/shot_NN.mp4                            ← (video, v0.3.0) Seedance 出的每个分镜真视频
    ├── final-video.mp4                              ← (video, v0.3.0) ffmpeg 拼接好的成片
    └── partial-video.md                             ← (video, v0.3.0) 各 shot 状态 + 失败 shot 的 prompt
```

## 工作流（10 step）

### Step 0：preflight + 选模式
- 检查 OFOX_API_KEY（必需）+ TIKHUB_API_TOKEN（fallback 拆解用）
- 检查 graph 状态（决定品牌视角 vs 客观模式）

### Step 1：链接 → 拆解卡
1. 解析 link → note_id（复用 v1 linkresolve）
2. 在 `docs/deconstructions/` grep note_id
3. 找到（≤7 天）→ 直接 Read
4. 找到（>7 天）→ 提示用户「复用 / 重拆」
5. 没找到 → **自动 fallback**（v0.2.1 起）：透明触发 `extract_xhs.py` 抽取 note.json + comments.json + frames，写入 stub 拆解卡（文本字段填好；视觉字段标 ⚠️ AUTO-STUB 待 agent 后续读 frames/ 完善）

### Step 2：读 graph 必读节点
- brand-voice / brand-story / segments / taboo / hooks / style-tags / xiaohongshu

### Step 3：收集我方输入
- type / count / product-imgs / product-usp（前面 args 已拿）

### Step 4：生成「脚本」（核心）
- prompt 模板：拆解卡 + brand-voice + 钩子库 + 我方卖点
- 输出：`script.md`
- 重要约束：image 类型时强制每张图必须 single isolated subject（避免下游生图拼图）

### Step 5：并行生成 4 类辅助文本
- caption.txt（video 类型）
- cover.txt
- desc.txt
- (依赖 desc 之后) tags.txt

### Step 6：素材成片生成（image / video 类型）
- N 张 frame（image 类型按 --count）+ 1 张 cover
- Nano Banana 三路约束 prompt：
  1. **Layout reference** ← 来自 script.md 单图描述
  2. **Brand style anchors** ← 来自 graph/brand/brand-voice
  3. **Product description** ← 来自 --product-usp + --product-imgs
- 关键约束（`build_prompt` 里硬编码）：
  - STRICTLY VERTICAL 9:16 portrait
  - SINGLE IMAGE only, NO collage / grid / multi-panel
  - frame: ABSOLUTELY NO text；cover: 允许文字层

### Step 7：seedance-prompt.md（仅 video 类型）
- LLM 把脚本翻译成 Seedance cinema-style prompt（5-6 个 shot，每个 4-7s）
- v0.3.0 起这个文件不仅给人看，还会被自动喂给 Seedance API（除非 --no-real-video）

### Step 7.5：Seedance 真生视频（v0.3.0 起，video 类型默认）
- 解析 seedance-prompt.md 切出 N 个 shot
- **打印成本估算 + 3 秒 Ctrl+C 倒数**（默认 1 shot 5s ≈ $0.20，5 shots ≈ $1）
- 顺序提交到火山方舟 Seedance 2.0（异步任务 + 轮询，单 shot 通常 1-3 分钟）
- 失败的 shot 不阻断其他 shot，只在 `partial-video.md` 里写明哪几个失败 + 失败 shot 的 prompt 方便手补
- 成功的 shot 用 ffmpeg concat 拼成 `final-video.mp4`
- 开关：`--no-real-video`（仅出 prompt 不调 API）/ `--async`（仅提交不等结果）/ `--no-confirm`（跳过 3 秒倒数）

### Step 8：质检 validator（v0.2.1 起内置）
- **硬错** → 自动重跑相应步骤（最多 1 次）：禁忌词命中 / 文件为空 / tags < 5 / 图片过小（疑似生成失败）
- **软错** → 出 `quality_report.md` 让用户决定：desc 长度异常 / emoji 过多 / cover 多行
- 禁忌词词典从 `graph/engine/taboo.md` 自动提取，叠加默认极限词 / 营销过度词

### Step 9：发布拆解卡
- 沿用 v1 Step 7：飞书优先 + 本地 fallback
- 输出 GEN-xxx 目录路径作为"产物"给用户

### Step 10：4 行总结
```
1. 生成对象：基于 {拆解卡} + {我方品牌} 的 {类型}（{count} 张/条）
2. 产出：script.md + cover + N 张 frame + desc + tags + (seedance-prompt)
3. 工作区：{绝对路径}
4. 耗时 / 调用：{秒} / {LLM 次} + {图片次}
```

## 命令行用法

```bash
# 8 张图文笔记
python3 scripts/generate_xhs.py "<XHS link>" --type image --count 8 \
  --product-usp "新中式女装：真丝马甲 + 立体绣衬衫" \
  --product-imgs ~/photos/spring-2026/

# 1 条视频（v0.3.0 起默认真生视频，~$1，Ctrl+C 可中断）
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1

# 1 条视频但只出 prompt + 封面 + 1 帧关键图（节省成本）
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1 --no-real-video

# 异步：仅提交 Seedance 任务立即返回 task_id，自己后续手动拉
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1 --async

# 仅出脚本（拍摄指引型）
python3 scripts/generate_xhs.py "<XHS link>" --type script --count 1

# 强制重拆 v1（绕开缓存）
python3 scripts/generate_xhs.py "<XHS link>" --type image --count 8 --fresh

# 仅环境检查（含 OFOX_API_KEY）
python3 scripts/generate_xhs.py --check
```

## 已知限制 / 路线图

| 限制 | 解决方向 | 计划 |
|---|---|---|
| ~~视频不真生成（仅出 prompt）~~ | ~~接火山 Seedance 2.0 API~~ | ✅ v0.3.0 |
| 不出钩子变体（一次只 1 套） | LLM 多 round 出 N 套不同钩子 | v0.4.x |
| 人物一致性弱（每张图脸不同） | 引入 IP-Adapter / InstantID | v0.5.x |
| ~~没自动质检~~ | ~~validator.py 硬+软错检测~~ | ✅ v0.2.1 |
| ~~Fallback 拆解需手动跑~~ | ~~内置自动调用 v1~~ | ✅ v0.2.1 |
| Stub 卡视觉字段 agent 手补 | vision LLM 自动补全 | v0.4.0 |

## 边界与原则（generate mode）

1. **不伪造产品信息**：用户没传产品图 / 卖点 → prompt 里说明"用户未提供视觉参考"，让 LLM 不虚构具体颜色/材质细节
2. **不抄对标**：脚本里禁止出现对标视频里的具体专有名词（品牌 / 主理人 / 地点）
3. **图片质量是参考非成品**：v2.0 生图定位是 mood board / 给摄影师看的视觉参考，不是直发素材（决策见 spec §1）
4. **品牌一致性走三路约束**：参考图 + brand-voice prompt + 拆解卡 layout，缺任意一路都退化但不阻断
5. **Ofox 调用按次计费**：每次 generate 约 4-7 LLM + N+1 image calls，建议先 `--count 1` 验证再上量

---

## v1 边界与原则（deconstruct mode）

1. **不伪造**：API 失败、视频下载失败、字幕识别不到 → 直接标「未获取」
2. **拆解是观察不是评论**：客观字段写"画面是 X"，主观判断只在「情绪钩子 / 爆款主题 / 可学习要点」三格允许
3. **graph 只追加**：回写不改写历史；矛盾打 ⚠️ 给用户
4. **Token 控制**：视频帧 >30 张时，先按时间段聚合（每 5 秒选 1 帧代表）再细描
5. **不做内容生成**：本 mode 只输出拆解卡 + 图谱回写（v2 generate 干生成的事）

---

## 安装与依赖

### 系统要求

| 依赖 | 用途 | 安装 |
|---|---|---|
| **Python ≥ 3.10** | 运行所有脚本 | macOS: `brew install python@3.12`<br>Linux: `apt install python3.12` 或 pyenv<br>Windows: [python.org](https://python.org) |
| **ffmpeg** | 视频抽帧（图文笔记可省） | macOS: `brew install ffmpeg`<br>Linux: `apt install ffmpeg`（或 dnf / pacman）<br>Windows: `choco install ffmpeg` |

> 没有 pip 依赖——脚本只用 Python stdlib。

### API tokens

**v1 拆解需要 `TIKHUB_API_TOKEN`**（必需 for deconstruct）
**v2 生成需要 `OFOX_API_KEY`**（必需 for generate；管 LLM + Nano Banana 出图）
**v0.3.0+ 真生视频需要 `ARK_API_KEY`**（必需 for video 类型默认行为；可用 `--no-real-video` 绕开）

```bash
# v1 拆解：TikHub
mkdir -p ~/.config/content-engine
echo 'TIKHUB_API_TOKEN=你的_tikhub_token' >> ~/.config/content-engine/.env

# v2 生成：Ofox（管 LLM 文本 + Nano Banana 图片）
echo 'OFOX_API_KEY=ofox-你的_key' >> ~/.config/content-engine/.env

# v0.3.0+ 视频生成：火山方舟 Ark（Seedance 2.0）
echo 'ARK_API_KEY=你的_ark_key' >> ~/.config/content-engine/.env
```

| Token | 注册 | 用途 | 必需吗？ |
|---|---|---|---|
| `TIKHUB_API_TOKEN` | [tikhub.io](https://tikhub.io) | XHS API（拆解原始数据） | v1 拆解必需 |
| `OFOX_API_KEY` | [ofox.ai](https://ofox.ai) | LLM + Nano Banana 图片 | v2 生成必需 |
| `ARK_API_KEY` | [火山方舟](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) | Seedance 2.0 视频生成 | v0.3.0+ 真生视频时必需；`--no-real-video` 可绕开 |
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) | （备选）替代 Ofox 提供 LLM | 可选兼容 |

> ⚠️ ARK API Key 不要用 IAM AK/SK（两者格式都是 UUID 但不通用）。在火山方舟控制台「API Key 管理」单独创建，并在「开通管理 → 视觉模型」下开通 `Doubao-Seedance-2.0-fast`（默认有 500 万 tokens 免费额度）。
>
> 切换 model：`export ARK_VIDEO_MODEL=doubao-seedance-1-5-pro-251215`（或其他版本）。

Token 查找顺序（第一个找到即用）：
1. 对应环境变量（`TIKHUB_API_TOKEN` / `OFOX_API_KEY` / `ARK_API_KEY` / `OPENROUTER_API_KEY`）
2. 当前工作目录的 `.env`
3. `~/.config/content-engine/.env`（XDG 标准）
4. Skill 根目录的 `.env`

### 验证安装

```bash
python3 scripts/extract_xhs.py --check
```

输出每项检查 ✅/❌/⚠️ 状态 + 失败的修复指引。

### 国内用户注意

- TikHub 主域名 `api.tikhub.io` 在中国大陆需要代理
- 替代镜像：`api.tikhub.dev`（无需代理）— 在 `.env` 设 `TIKHUB_BASE_URL=https://api.tikhub.dev` 启用

### 飞书发布（仅 OpenClaw 用户）

本 skill **不内置**飞书 API 调用。如果你想拆解卡自动发布到飞书 Docx，安装 OpenClaw 飞书官方插件：

```bash
npx -y @larksuite/openclaw-lark install
```

详见 [OpenClaw 飞书官方插件文档](https://www.feishu.cn/content/article/7613711414611463386)。

装好后：
- agent 在 OpenClaw 里有「创建云文档 / 读取云文档 / 更新云文档」等原生工具
- SKILL.md Step 7 会让 agent 调插件工具发布
- 凭据由插件管理，本 skill 无需任何飞书相关配置

**Claude Code 或其他环境**：拆解卡保存到本地 `docs/deconstructions/`，需手动复制到飞书。

---

## 相关 / 参考

- `analyze-xhs` skill：拆账号（不是拆单条）
- 架构灵感：[Ronin · How To Build Own Content Engine](https://x.com/DeRonin_/status/2042604279077237170)（Skill Graph：用 .md + wikilink 当 agent 的"记忆 / 灵魂"）
