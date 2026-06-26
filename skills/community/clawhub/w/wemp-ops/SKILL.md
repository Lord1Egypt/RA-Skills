---
name: wemp-ops
version: 1.0.0
description: >
  微信公众号全流程运营：选题→采集→写作→排版→发布→数据分析→评论管理。
  Use when: (1) 用户要写公众号文章或提供了选题方向,
  (2) 用户说"写一篇关于XXX的文章"/"帮我写篇推文"/"出一篇稿子",
  (3) 用户要求采集热点/素材/竞品分析,
  (4) 用户提到公众号日报/周报/数据分析/阅读量/粉丝,
  (5) 用户要求检查评论/回复评论/评论管理,
  (6) 用户说"发布"/"推送"/"推到公众号"/"发到草稿箱",
  (7) 用户讨论文章排版/封面图/标题优化。
  即使用户没有明确说"公众号"，只要涉及微信文章写作、内容发布、
  公众号后台操作、文章数据查看、或读者互动管理，都应使用此技能。
  当用户给出选题方向时，自动完成素材采集→内容写作→封面生图→排版美化→推送草稿箱全流程。
  NOT for: 小红书运营（用 xiaohongshu-ops）、纯内部文档写作（用 internal-comms）、
  通用 Word 文档（用 docx）。
---

# wemp-ops — 微信公众号运营技能

## 环境检查

首次使用前执行：
```bash
node scripts/setup.mjs
```

检查 Node.js 版本、Python3、微信公众号 API 配置。

## 工作流路由

根据用户意图选择对应流程：

| 意图 | 流程 |
|------|------|
| "写一篇关于 X 的文章" | → **全流程**（下方详述） |
| "采集 X 热点" | → 仅采集 |
| "公众号日报/周报" | → 数据分析 |
| "检查/回复评论" | → 互动管理 |
| "发布文章" | → 仅发布 |
| "选题/有什么可以写的" | → 选题管理（检查 topic-pool.md） |

## 全流程：选题到草稿箱

当用户给出选题方向时，执行以下完整流程。先读 `persona.md` 确定写作人设。

### Step 0: 选题准备

**如果老板没有指定具体选题**，先检查选题池：
1. 读取 `<WORKSPACE>/collections/topics/topic-pool.md`
2. 列出当前高优选题，每个附带角度和素材情况
3. 让老板选择，或老板提出新选题
4. 选定后进入 Step 1

**如果老板已有明确选题**，直接进入 Step 1。

### Step 1: 理解选题

读 `references/article-templates.md` 判断内容类型：

- **AI 产品拆解** — 具体产品名 + 分析/拆解
- **场景解决方案** — "怎么用 AI 做 XXX"
- **效率提升实战** — 工具 + 技巧/心得
- **产品方法论** — 抽象话题 + 思考
- **行业观察** — 新闻/趋势 + 观点

选题模糊时给 2-3 个具体方向让用户选（最多 1 轮澄清）。

### Step 2: 素材采集

**2pre. 交接文件检查**
先检查 `<WORKSPACE>/temp/handoffs/collector-to-writing.md` 是否存在：
- 有 → 读取，筛选与当前选题相关的素材条目，纳入写作参考
- 消费后删除已使用的条目（如果文件清空则删除文件）
- 没有 → 跳过，正常流程

**2a. 收藏库检索（优先）**
先从个人收藏库中检索相关素材——这是让文章有"人味"的关键（详见 writing-techniques.md §五）：
1. 标签匹配：`grep -i "关键词" <WORKSPACE>/collections/tags.md`
2. 全文搜索：`grep -ril "关键词" <WORKSPACE>/collections/`
3. 有匹配时，读取对应文件的核心观点、要点摘录、个人笔记
4. 标记可用素材的使用场景：开头引入？观点支撑？案例展示？反面论据？
5. 收藏素材用自己的话重新表述，自然融入文章，不是学术式引用

**2b. 外部采集（补充）**
收藏库素材不足时，从外部补充：
1. 根据选题扩展 3-5 个搜索关键词
2. `web_search` 搜索 2-3 轮（官方信息→深度分析→对比评测）
3. `web_fetch` 抓取 2-4 篇高质量参考文章
4. 可选：`node scripts/smart_collect.mjs` 从 20+ 数据源采集相关热点
5. 提取关键事实、数据、观点备用

**⚠️ 中间存盘规则**：每 2-3 轮 web_search/web_fetch 后，立刻把已获得的关键发现写到 `<WORKSPACE>/temp/wemp-findings-{slug}.md`（选题 slug），防止连续采集时前面的信息在 context 中被挤掉。采集完成后此文件可删除。

**2c. 素材整理**
合并收藏库 + 外部素材，按相关度排序，标注来源

**2d. 对标账号分析（可选，首次写某领域时推荐）**

找 2-3 个同领域做得好的公众号，填写对标颗粒度检查表：

| 维度 | 对标账号 | 我们 | 差异说明 |
|------|---------|------|---------|
| 文章长度 | | | |
| 标题风格 | | | |
| 开头结构（故事/数据/问题/金句） | | | |
| 配图风格和数量 | | | |
| 排版密度（段落长度/留白） | | | |
| 结尾 CTA（关注/转发/留言） | | | |
| 发布频率 | | | |

**每个不一致都要有理由，否则改成一致。** 0 到 1 阶段模仿是正确答案。

**2e. 素材丰富度门禁（写作前必检）**

写作前过一遍素材储备，5 维中至少 3 个有料才开始写。不够就回 Step 2 补采集，不要硬写。

| 维度 | 有没有 | 具体内容 |
|------|--------|---------|
| 冲击力数据（大数字/百分比/对比） | ✅/❌ | |
| 转变故事（之前 vs 之后，反差越大越好） | ✅/❌ | |
| 金句（能独立传播的一句话观点） | ✅/❌ | |
| 权威背书（人物/机构/论文/官方数据） | ✅/❌ | |
| 痛点共鸣（目标读者的焦虑/常见错误） | ✅/❌ | |

- **0-2/5** → ⛔ 停止，回 Step 2 补充。素材不够硬写 = 进入「内容差→没流量→以量取胜→内容更差」的死亡螺旋
- **3-4/5** → ⚠️ 可以写，但开头冲击力受限。标注薄弱维度，写作中刻意补强
- **5/5** → ✅ 素材充足，放心写

### Step 3: 写作

读 `references/writing-sop.md`、`references/style-guide.md` 和 `references/writing-techniques.md`，按以下流程写作：

**3a. 创意排水（正式动笔前必做）**
花 2-3 分钟快速列出这个选题的"废水"——套路想法、陈词滥调、第一反应。标记为禁用列表，正式写作中刻意避开。（详见 writing-techniques.md §一）

**3b. 正式写作**
- 遵循 `persona.md` 人设（AI 产品经理第一人称）
- 按 `references/article-templates.md` 对应类型的结构模板
- 2000-3000 字，短句为主
- 链接用纯文本格式
- 输出为 Markdown 文件，保存到工作目录（文件名格式：`draft-v1.md`，放在当前文章的工作目录下，如 `wemp-article-NN/draft-v1.md`）
- **不要在文中出现 H1 标题**（公众号自带标题，正文从 H2 开始）
- 融入收藏库素材（Step 2 中检索到的真实经历/观点/案例）

写作中运用五大技巧（详见 writing-techniques.md §二）：
- **微幽默**：每 200 字至少 1 个嘴角上扬的小细节
- **强开头**：禁止"在当今时代…"等套话。开头公式 = **话题（讲什么）+ Hook（为什么看）+ 可信度（为什么信你）**，三要素缺一不可。Hook 优先级：晒结果+反转⭐⭐⭐⭐⭐ > 数据冲击⭐⭐⭐⭐ > 反差/转变⭐⭐⭐⭐ > 金句⭐⭐⭐ > 权威+观点⭐⭐⭐ > 痛点+悬念⭐⭐⭐
- **概念把手**：为复杂概念创造 3-6 字记忆短语，每篇至少 1-2 个
- **句子节奏**：短/中/长句交替，不允许连续 3 句同长度
- **多巴胺密度**：每段至少 1 个"有意思"的点，连续 3 段没有 = 危险区域

**3c. 标题生成（双轨制）**
按 writing-techniques.md §四 生成标题候选：
1. 爆款标题 3-5 个（金钱数字/暴力隐喻/悬念等要素）
2. 自然风格标题 3-5 个（经验分享/观点输出/对比评测等）
3. 可选：组合优化（自然标题 + 注入 1-2 个爆款要素）
4. 推荐 Top 3 给老板选择

**悬念制造铁律**：标题和开头制造悬念，不给答案。用「为什么」不用「证明」。
- ❌ 「Computer Use 效率低，证明 API 才是正路」（给了答案，读者不想看了）
- ✅ 「Claude 能操控微信了，为什么我说这不是未来？」（留悬念，想知道为什么）
- ❌ 「Agent 的 3 个核心能力」（平铺直叙，无冲突）
- ✅ 「为什么 90% 的 Agent 产品会在 6 个月内死掉？」（制造好奇）

**3d. 三遍审校**
按 writing-techniques.md §三 结构化审校：
- 第一遍：内容审校（事实/逻辑/结构）+ 段落迷你论点串联测试
- 第二遍：风格审校（对照 24 条 AI 味特征清单降 AI 味 + 灵魂注入 + 5 维质量评分 ≥ 35 分才过）
- 第三遍：细节打磨（句子节奏 + 多巴胺密度 + 微幽默 + 概念把手检查）

#### ⚠️ 写作红线

- **不暴露 AI 参与写作**：不说"这篇文章是 AI 写的"、"让 AI 帮我写"等 — 读者对 AI 生成内容有抵触心理，暴露会显著降低阅读量和信任感
- **讲故事，不讲论点**：用时间线、场景、情绪推进，不用"总结"、"核心观点"、编号式论点堆砌
- **自然过渡**：不用中括号小标题、不用"以下是 N 条心得"式结构
- **让读者感受到力量**：分享经历，不是教学。有踩坑有收获，有真实细节
- **禁止废水开头**：不用"在当今 XX 的时代…"、"随着 XX 的不断发展…"等陈词滥调

### Step 4: 封面图

设计指南见 `references/cover-image-guide.md`（六维度体系：Type/Palette/Rendering/Text/Mood/Font + 12 个预设 + 兼容矩阵 + 构图核心原则）。三种方案按优先级：

**方案 A（优先）：idealab Chat API**
- `<WORKSPACE>/scripts/generate-image.sh --prompt "prompt" --filename output.jpg`
- 默认模型 `gemini-3.1-flash-image-preview`，团队 AK 免费，走 /chat/completions 接口
- 2.35:1 裁剪：生成后 `sips -c 1090 2560 output.jpg`
- 超时/报错时脚本自动降级到 Gemini Key 轮换
- ⚠️ 不用 emoji（浏览器截图会变色块），用纯文字 + 几何图形

**方案 B（降级）：Seedream 5.0 Lite**
- `<WORKSPACE>/scripts/seedream-generate.sh "prompt" output.jpg "2560x1440" 1`
- 0.22 元/张，idealab 不稳定时使用
- 裁剪同方案 A：`sips -c 1090 2560 output.jpg`

**方案 C（兜底）：HTML 渲染 + 浏览器截图**
- 写一个 HTML 页面（渐变背景 + 标题文字 + SVG 图形）
- 用 `python3 -m http.server` 本地启动
- 用 browser 工具 navigate + screenshot 截图
- 适用于需要精确控制布局时

### Step 4.5: 配图规划与生成

完整指南见 `references/illustration-prompts.md`（Type×Style 矩阵、Prompt 规范、风格锚点）。

**4.5a 配图规划（先规划再生图）**

1. **扫描文章结构**，按以下规则标注潜在配图位置：
   - `##` 标题后的第一段 → 潜在配图点
   - 概念首次出现 → 用插图辅助解释
   - 转折/对比处（"但是"、"然而"、"相比之下"）→ 适合对比图
   - 连续超 800 字无任何视觉元素 → 需要打断

2. **内容信号自动匹配**，根据段落关键词推荐 Type：
   - 架构/分层/系统 → `framework` | 步骤/流程 → `flowchart` | vs/对比 → `comparison`
   - 数据/百分比 → `infographic` | 叙事/经历 → `scene` | 代码/界面 → `screenshot`

3. **锁定全文 Style**（一篇文章只用一种 AI 生图风格，从 `cover-image-guide.md` 预设中选）：
   - 技术/产品文 → `ai-product`（默认）| 数据/架构文 → `dashboard` | 故事/教育文 → `pm-growth` | 观点文 → `bold-opinion`

4. **输出配图计划表**（保存到 `illustration-plan.md`），让老板确认后再生图。
   密度参考：2000 字 3 张、3000 字 4-5 张，正文配图硬上限 5 张。

**4.5b 生图执行**

配图有两条渲染路径，在配图计划表中按每张图标注：

**路径 A：AI 生图**（视觉美感优先，适合大部分场景）
- **优先级**：idealab Image API → Seedream 5.0 Lite → Gemini 生图 → ComfyUI
  - idealab（首选）: `<WORKSPACE>/scripts/generate-image.sh --prompt "prompt" --filename output.jpg --size 2560x1440`
    - 默认模型 `gemini-3.1-flash-image-preview`，团队AK免费；超时/报错自动降级到 Gemini
  - Seedream（降级）: `<WORKSPACE>/scripts/seedream-generate.sh "prompt" output.jpg "2560x1440"`
  - 正文插图 16:9 `2560x1440`
- **Prompt 按 LDSCS-R 六层结构构造**：Layout → Data → Semantics → Characters → Style → Ratio
- **风格锚点**：第一张图成功后，记录风格特征到 `prompts/style-anchor.md`，后续图片引用保持一致
- **Prompt 持久化**：每张图的 prompt 保存到 `prompts/NN-{type}-{slug}.md`，便于回溯修改

**路径 B：Mermaid 渲染截图**（信息精确性优先，技术文章的流程/架构/对比图）
- **适用条件**：配图计划中 Style 标注为 `mermaid-render` 的插图
- **工作流**：
  1. 生成 Mermaid 代码（遵守 `references/illustration-prompts.md` 中的 Mermaid 规范）
  2. 写入 `<WORKSPACE>/scripts/mermaid-render.html`（临时 HTML 模板）
  3. 浏览器打开 → resize 2560x1440 → screenshot
  4. 裁剪白边（如需要）→ 存入 `images/`
- **Mermaid prompt 也持久化**：保存到 `prompts/NN-{type}-{slug}.md`，记录 Mermaid 源码

**通用规则**：
- 截图美化：`<WORKSPACE>/scripts/beautify-screenshot.sh <input> [output] --shadow --bg "#f5f5f5"`
- 水印去除：`<WORKSPACE>/scripts/remove-watermark.sh <input> [output]`（Gemini 生图 需去水印）
- 配图数量：宁缺毋滥。不确定要不要配图 → 不配。
- 同一篇文章中路径 A 和路径 B 可以混用，但渲染方式不超过 2 种。

### Step 4.6: 产品截图获取

文章涉及线上产品（AI 工具、SaaS 产品等）时，截取真实产品界面作为配图。

**公开页面（无需登录）：**
```bash
# 1. 打开产品页面
browser action:open url:"https://example.com/product"

# 2. 等待加载完成后截图
browser action:screenshot fullPage:false type:png

# 3. 裁剪/缩放（macOS sips 工具）
sips -z <高度> <宽度> screenshot.png                    # 缩放
sips -c <高度> <宽度> screenshot.png                    # 裁剪居中
sips --resampleWidth 800 screenshot.png                  # 按宽度等比缩放

# 4. 上传到微信素材库
node scripts/publisher.mjs  # 通过 --markdown 自动上传
# 或手动：在 utils.mjs 中调用 uploadArticleImage()
```

**需登录页面（付费产品/内部系统）：**
1. 让用户在 Chrome 打开目标页面
2. 用户点击 OpenClaw Browser Relay 工具栏图标 attach 该 tab
3. `browser action:screenshot profile:chrome` 截图
4. 截图后同上流程裁剪上传

**截图规范：**
- 宽度 600-900px，避免过大（微信有尺寸限制）
- 隐藏/打码敏感信息（用户名、私有数据等）
- 浏览器地址栏按需保留（能说明产品来源时保留）
- 优先截取核心功能区域，不截全屏
- 深色/浅色主题根据文章风格选择

### Step 5: 排版美化

```bash
# 基础排版
python3 scripts/markdown_to_html.py --input article.md --theme tech --output article.html

# 带图片自动上传（本地图片自动上传到微信素材库并替换 URL）
python3 scripts/markdown_to_html.py --input article.md --theme tech --output article.html --upload
```

主题选择：tech（科技风，默认）、minimal（简约风）、business（商务风）。
排版约束详见 `references/weixin-constraints.md`。

#### Step 5.5: 外链转底部引用（微信外链不可点击问题）

微信公众号不支持外链点击跳转，文章中的外链对读者没有交互价值。排版时自动处理：

**处理规则**：
1. 普通外链 `[text](https://example.com)` → 文中显示为 `text¹`（上标序号），链接收集到文末「引用链接」章节
2. `https://mp.weixin.qq.com/...` 链接保留为直接链接（微信内部链接可点击）
3. 裸链接（链接文本 = URL 本身）保留不动（已是展示型，读者可复制）
4. 没有外链的文章跳过此步

**文末引用格式**：
```markdown
---
## 引用链接

1. example.com: https://example.com/article
2. GitHub: https://github.com/user/repo
```

**执行时机**：Markdown 转 HTML 之前处理（在 Markdown 层面替换，不是 HTML 层面）。可在 `markdown_to_html.py` 中集成，或作为单独的预处理步骤。

如果有额外配图需要手动插入（非 Markdown 内嵌图片），先上传再手动插入 HTML。

### Step 6: 推送草稿箱

```bash
# 一键从 Markdown 到草稿（推荐，自动转 HTML + 上传图片 + 清理旧同名草稿）
node scripts/publisher.mjs --markdown article.md --title "文章标题" --cover cover.png

# 或手动分步：先转 HTML 再推送
python3 scripts/markdown_to_html.py --input article.md --theme tech --output article.html --upload
node scripts/publisher.mjs --title "文章标题" --content article.html --cover cover.png

# 跳过自动清理旧草稿
node scripts/publisher.mjs --markdown article.md --title "标题" --cover cover.png --no-cleanup

# 列出草稿
node scripts/publisher.mjs --list

# 删除草稿
node scripts/publisher.mjs --delete --media-id <id>

# 发布草稿（用户确认后）
node scripts/publisher.mjs --publish --media-id <草稿media_id>
```

**默认停在草稿箱，不自动发布。** 告知用户草稿已创建，确认后再发布。
推送新版本时自动清理同标题旧草稿（`--no-cleanup` 跳过）。

### Step 6+: 发布数据回流（推送草稿箱后自动执行）

推送草稿箱成功后，顺便采集历史文章数据，用于选题评分校准。

```
1. browser(action=tabs, profile="user") 检查是否有 mp.weixin.qq.com tab
2. 有 → browser(action=snapshot, targetId=<tab_id>) 读取发表记录页
3. 从 snapshot 提取每篇文章的：标题、阅读量、点赞、分享、留言
4. 自动更新 collections/topics/publish-feedback.md
5. 没有 tab 或 snapshot 失败 → 跳过，不影响主流程
```

注意：此步不影响主流程，失败就跳过。数据用于选题评分校准（见 eval-criteria.md + publish-feedback.md）。

### Step 6.5: 五维内容自检（交付前必做）

排版完成后、交付前，逐维度自检。任何一项 ❌ 必须修改后再进入下一步。

| 维度 | 检查问题 | 合格标准 | 判断 |
|------|---------|---------|------|
| **文字洁癖** | 有没有 AI 味？（空洞排比句、Emoji 堆叠、"让我们来看看"） | 每句话都有信息量，没有填充语 | ✅/❌ |
| **标题/封面** | 平铺直叙能不能吸引人？不看封面只看标题想不想点？ | 有立场/反差/数据之一，不靠震惊体 | ✅/❌ |
| **表达效率** | 能不能一句话说清核心观点？有没有 99% 时间包装 1% 内容？ | 删掉任何一段，整篇不完整 = 没有冗余 | ✅/❌ |
| **认知落差** | 读完后读者会不会觉得「这个我知道」？和同行比有增量吗？ | 至少有 1 个「我之前没想到」的点 | ✅/❌ |
| **数据支撑** | 核心判断有没有数据/事实/一手经验支撑？ | 每个核心判断都有来源（数据/案例/亲身经历） | ✅/❌ |

> 借鉴 dbs-content 五维诊断框架。第五维从「AI 辅助」改为「数据支撑」，更适合公众号写作场景。

### Step 7: 读者测试（可选但推荐）

交付前，用一个无上下文的子 Agent 阅读文章全文，检查：
- 标题是否让人想点开？（不知道背景的人能否被吸引）
- 开头两段是否抓住注意力？（3 秒法则）
- 是否有行业黑话/未解释的概念？（非目标读者能否理解）
- 结尾是否有力？（读完后想做什么）
如果子 Agent 发现盲点，修改后再交付。

### Step 8: 风格学习采集

**写作完成时自动执行，不需要老板操作。**

在 Step 3 写作完成（draft-v1.md 定稿）后，自动记录 AI 原稿：
```bash
python3 <WORKSPACE>/scripts/style-observe.py record-original <工作目录>/draft-v1.md --skill wemp-ops --topic "选题关键词"
```

当老板确认最终版（可能经过多轮修改）后，记录最终版：
```bash
python3 <WORKSPACE>/scripts/style-observe.py record-final <最终版文件> --skill wemp-ops
```

**触发 record-final 的信号**：
- 老板说"可以了"/"发吧"/"推到草稿箱"
- 老板手动修改后把最终版发回来
- 文章已发布（从草稿箱发布 = 确认最终版）

**如果老板没有修改直接发布**，也要 record-final（no_change = 正反馈，说明这次写得好）。

积累 5+ 对 diff 后，可执行风格规则提取：
```bash
python3 <WORKSPACE>/scripts/style-observe.py pairs --skill wemp-ops --days 30
```

### Step 9: 交付

向用户汇报：文章标题、字数、草稿状态、封面预览、建议发布时间。

## 仅采集

```bash
node scripts/smart_collect.mjs --query "用户需求" --keywords "AI扩展的关键词" --sources "hackernews,v2ex,36kr" [--deep]
```

数据源分类：
- `tech`: hackernews, github, v2ex, sspai, juejin, ithome, producthunt
- `china`: weibo, zhihu, baidu, douyin, bilibili, toutiao, tencent, thepaper, hupu
- `finance`: 36kr, wallstreetcn, cls

采集后整理为选题候选清单，每条含：标题、来源、热度、链接、与用户需求的相关度。

## 数据分析

```bash
# 日报（默认昨天）
node scripts/daily_report.mjs [--date YYYY-MM-DD]

# 周报
node scripts/weekly_report.mjs
```

输出包含：用户增长、阅读数据、热门文章、互动数据、AI 洞察。

## 互动管理

```bash
# 检查新评论
node scripts/check_comments.mjs

# 回复评论
node scripts/reply_comment.mjs --comment-id <id> --content "回复内容"
```

AI 生成回复建议时遵循 `persona.md` 的语气规范，用户确认后再执行回复。

## 配置

公众号凭证配置在 **skill 自己的** `config/default.json`：

```json
{
  "weixin": {
    "appId": "你的AppID",
    "appSecret": "你的AppSecret"
  }
}
```

⚠️ **不要写到 `openclaw.json` 的 `channels` 里！** `channels` 只接受 OpenClaw 内置渠道类型（dingtalk/telegram/discord 等），写入未知类型会导致 gateway 校验失败并不断重启。

其他配置（数据源偏好、报告时间等）同样在 `config/default.json` 中调整。

---

## 多版本分发（一篇→多平台）

公众号文章完成后，可一键生成其他平台版本。

### 触发词
- "把这篇文章分发到小红书/X"
- "生成多平台版本"
- "同步到其他平台"

### 分发流程

#### Step 1: 读取源文章
从公众号草稿箱/已发布文章中提取：标题、正文、核心观点、配图

#### Step 2: 生成小红书版本
自动调用 `xiaohongshu-ops` 技能：
1. **标题**：从公众号标题中提炼，加 emoji，≤20 字
2. **正文**：缩写到 300-600 字，口语化改写，去掉长段落
3. **配图**：从公众号文章中选 1-3 个核心观点，制作信息卡（Seedream 优先，备选 Gemini 生图 / HTML截图）
4. **标签**：5-10 个小红书话题标签
5. 通过 openclaw browser 发布到创作中心

#### Step 3: 生成 X/Twitter 版本
1. **单条推文**（≤280 字符）：提炼文章最核心的一个观点，英文或中文
2. **Thread 版本**（可选）：3-5 条推文，适合深度内容
3. 通过 openclaw browser 发布（参考 TOOLS.md 中的 X 发帖 SOP）
4. 发帖前**先让老板确认内容** — 外部发布是不可撤回的操作，确认能避免事后删帖的尴尬

#### Step 4: 记录分发状态
在公众号文章对应的 memory 记录中标注已分发平台和链接

### 改写原则
- 每个平台版本**重新改写** — 直接复制粘贴会被平台算法降权，且不同平台的受众期待和内容格式差异很大
- 小红书：口语化、短句、emoji 多用、互动提问结尾
- X/Twitter：精炼、有冲击力、适合英文受众（如有）
- 保持核心观点一致，但表达方式适配平台调性

---

## 下一步建议（条件触发）

文章完成后，根据结果判断是否推荐下一步。

| 触发条件 | 推荐 |
|---------|------|
| 文章已发布成功 | 「文章已发布。要分发到小红书/X 吗？或者用 content-collector 存档素材方便下次复用。」 |
| 写作过程中发现素材不足 | 「素材不够，建议先用 content-collector 搜索已有收藏，或 web_search 补充。」 |
| 文章涉及会议纪要/内部沟通 | 「这篇更像内部文档，建议用 internal-comms 的格式。」 |
| 需要配图但 Seedream/Gemini 生图效果不佳 | 「配图可以试试 drawio 画流程图/架构图替代。」 |

---

## 绝对不要做的事

写作和内容产出中，以下行为直接拉低质量，必须避免：

1. **不要说「每个人的写作风格不同」「见仁见智」** — 这是回避判断。有观点就直接说，标注来源
2. **不要建议「参考同行」而不给具体对标** — 「去看看别人怎么写的」是废话。要给就给具体账号、具体文章、具体写法
3. **不要用「干货满满」「深度好文」「建议收藏」** — 读者自己判断有没有干货，作者说「干货满满」等于自夸
4. **不要写空洞的排比句开头** — 「在这个时代……在这个节点……在这个浪潮中……」是 AI 八股文的标志
5. **不要堆叠修饰词** — 「极其重要的关键性底层核心逻辑」，一个词能说清的事不用四个
6. **不要开头就下结论** — 先给事实/故事/数据制造认知落差，结论放后面。开头下结论 = 读者没动力往下读
7. **不要用「让我们一起来看看」「接下来我们来聊聊」** — 这是视频口播语气硬塞进文章的结果，书面内容不需要这种过渡
8. **不要在没有数据支撑时写「据统计」「研究表明」** — 要么给出具体来源（谁的研究、哪年、样本量），要么不引用

---

## 内联案例库

### 正面案例（老板认可的产出）

**案例 1：公众号 #6「Claude 能操控微信了」V3 定稿**
> 去掉所有比喻，直接用数据说话。1900 字，聚焦 Computer Use vs API 一个视角。新增"Anthropic 自己优先走 MCP 接口"的关键发现。
- 成功要点：一篇文章只讲一件事；数据 > 比喻 > 术语；「50% 成功率」比任何比喻都有说服力
- 老板评价：确认 OK

**案例 2：公众号 #5「Skills 不是低代码，但也不是 App Store」**
> 从第一人称 AI PM 视角，讲自己用 Skills 的真实踩坑经历，有具体场景、有数据、有得失。
- 成功要点：讲故事不讲论点，经历 > 观点，场景 > 总结，有踩坑有收获

**案例 3：封面图 Seedream 生成**
> 2560x1440 生成，裁剪 2.35:1 宽屏比例，简洁主体 + 深色背景 + 大字标题。
- 成功要点：封面不堆元素，一个主体 + 一行标题 + 干净背景

### 反面案例（被打回的产出 + 打回原因）

**反面 1：公众号 #6 V1 初稿（3100 字，被全面打回）**
> 塞了 Computer Use + Agentic Engineering + 冷思考 + 一手实践 + 8 个名人引用，试图一篇文章讲完所有。
- 打回原因：❌ 内容太干太多读不动 ❌ 名人引用堆砌（8 处）❌ 点名反驳其他博主 ❌ 想讲的东西太多
- 教训：一篇文章只讲一件事。名人引用全文不超过 2-3 处。不要点名反驳他人文章，从现象切入。

**反面 2：公众号 #6 V2（1800 字，比喻牵强）**
> 砍掉了多余内容，但用"开车 vs 高铁"比喻贯穿全文。
- 打回原因：❌ 比喻牵强，把事情搞复杂了
- 教训：比喻不是必须的。事实清晰时直接说更好。数据自己会说话。
