---
name: writing-pipeline
description: |
  内容再创作管线：输入参考资料 → AI 生成中文初稿 → 人工改稿 →
  系统对比学习写作偏好 → 多平台格式输出。
  支持自动路由——根据输入材料特征自动匹配最合适的写作风格。
---

# Writing Pipeline

内容再创作管线。三个阶段：**Draft → Review → Publish**。

---

## Stage 1: Draft（生成初稿）

### 步骤

1. **创建文章目录**
   ```
   projects/writing/articles/YYYY-MM-DD-{slug}/
   ```

2. **保存参考材料（含 comment/highlight）**
   将用户提供的参考资料保存到 `references/` 子目录。

   **comment 机制（新增，必做）：**
   - 若参考资料存在行内评论 sidecar（如 `references/*.comments.json`），必须一并保存，不可丢失。
   - 评论中带有 highlight 的片段视为“强信号素材”，在 Stage 1 写初稿时必须优先吸收。
   - 先生成一份素材提炼清单 `references/reference-notes.md`，按如下结构整理：
     - `must-include`：被 highlight 的原句/要点（后文必须落入初稿）
     - `angle`：评论给出的写作角度、争议点、可展开问题
     - `evidence`：可直接引用的数据、案例、事实
     - `avoid`：评论中明确标注不建议采用的表达

   **X/Twitter 链接处理：** 如果参考材料中包含 `x.com` 或 `twitter.com` 链接，使用 `deepreader` skill 抓取推文内容（FxTwitter API，无需 API key），保存为 `references/tweet-{id}.md`。用法：
   ```python
   from deepreader_skill import run
   result = run("https://x.com/user/status/123456")
   ```

3. **X 搜索：查询相关事实与事件**
   用 `x_search` 搜索与参考材料相关的关键词、人物、事件，获取最新信息：
   - 从参考材料中提取 2-3 个核心关键词
   - 调用 `x_search` 查询，收集近期相关讨论、事实、数据
   - 将搜索结果摘要保存到 `references/x-search-results.md`
   - 生成初稿时将搜索结果作为补充上下文，确保内容基于最新事实

4. **自动路由：匹配写作风格**
   分析输入材料的特征，匹配最合适的 writing-style skill：

   ```
   输入材料 → 提取特征(domain, content_type, tone) → 匹配 style skill → 确认
   ```

   **路由规则（按优先级）：**
   1. 用户明确指定 style → 直接使用
   2. 未指定 → AI 分析材料特征，与每个 style skill 的 `routing` metadata 匹配
   3. 选择匹配度最高的 skill，向用户确认后加载

   **匹配矩阵：**

   | 输入特征 | → 推荐风格 |
   |----------|-----------|
   | 技术论文、产品发布、AI 模型 | `writing-style-huasheng` |
   | 创业故事、人物传记 | `writing-style-huasheng` |
   | 方法论、工具教程、how-to | `writing-style-baoyu` |
   | AI 工具评测、写作技巧 | `writing-style-baoyu` |
   | 哲学思辨、人生设计、意义探讨 | `writing-style-dankoe` |
   | 跨领域框架、自我提升、身份探讨 | `writing-style-dankoe` |
   | 长文摘要、知识提取、结构化转述 | `writing-style-zhengliu` |
   | 表达欲过强的文章、信息提取困难 | `writing-style-zhengliu` |

   **路由分析流程：**
   ```
   1. 识别材料的主题领域(domain)
      → tech/AI/product → huasheng 候选
      → writing/productivity/tools → baoyu 候选
      → psychology/identity/meaning → dankoe 候选

   2. 识别内容类型(content_type)
      → explainer/biography → huasheng 候选
      → methodology/how-to/opinion → baoyu 候选
      → essay/thought-piece/philosophical → dankoe 候选

   3. 识别语气倾向(tone)
      → narrative/data-driven → huasheng
      → teaching/metaphor-driven → baoyu
      → philosophical/provocative → dankoe
      → structured/fact-driven/extractive → zhengliu

   4. 检查蒸馏触发条件（优先级高于风格匹配）
      → 用户明确要求"蒸馏/提取/结构化转述" → zhengliu
      → 原文篇幅长 + 信息密度低 + 表达欲强 → zhengliu 候选

   5. 综合三个维度，选择匹配度最高的 skill
   6. 如果两个 skill 匹配度接近，列出两个选项让用户选择
   ```

5. **选题讨论**（必做，不可跳过）

   提供 3-4 个选题方向，每个包含：

   ```
   选题 N：标题
   - 核心角度：一句话说清楚文章讲什么
   - 核心比喻：（如使用宝玉风格）贯穿全文的比喻
   - 结构预览：3-5 个章节标题 + 预计字数分配
   - 优势：为什么这个角度好
   - 风险：可能的问题或难点
   ```

   **标题原则——共鸣式标题：**
   标题的目标不是概括内容，而是说出读者心里那句没说出口的话。
   找到目标读者普遍存在但很少被说清楚的困惑/痛点/感受，用一句话替他们问出来。
   读者看到标题的反应应该是"对！我也是这样！"→ 然后点进来。

   **其他规则：**
   - 每个选题的角度必须明显不同，不能是同一个思路换个说法
   - 等用户选择后再进入下一步，不要自行决定
   - 用户可以选某个选题、混合多个选题、或提出全新方向

6. **生成初稿（reference + comment 联合驱动）**
   用户确认选题后，加载匹配的 writing-style skill，基于 `references/` 与 `references/reference-notes.md` 联合生成初稿，保存为 `draft-v1.md`。
   - **硬约束：所有 `must-include`（highlight 片段）必须在初稿中被明确吸收**（可改写措辞，但核心信息不能丢）
   - 若某个 highlight 与其他证据冲突，必须在文中给出说明，且在草稿末尾加“冲突说明”小节
   - 如有多轮风格迭代，按 `draft-v0.md`、`draft-v1.md`、`draft-v2.md` 递增保留各版本
   - **初稿完成后，必须立刻复制最新 draft 为 `final.md`**，供用户直接在终稿编辑器中改稿（`cp draft-vN.md final.md`）
   - 若 `final.md` 已存在且非空，不覆盖；仅在缺失或空文件时执行复制

7. **提取观点与生成信息图**（可选，也可在 Stage 2 后执行）
   a. 加载 `viewpoint-extractor` skill，从初稿中提取 3-5 个核心观点
   b. 保存 `viewpoints.yaml` 到文章目录
   c. 加载 `infographic-gen` skill，为每个观点生成信息图
   d. 输出到 `output/infographics/{slug}.jpg`

   > 此步骤可推迟到 `final.md` 完成后再执行，用终稿提取的观点更准确。

8. **写入元数据**
   创建 `README.md`：
   ```yaml
   ---
   title: 文章标题
   date: YYYY-MM-DD
   style_skill: writing-style-xxx
   sub_template: 子模板名（如适用）
   source_materials:
     - references/xxx.md
   status: draft
   ---
   ```

   **状态字段约束（必须遵守）**
   - 仅允许：`draft` / `reviewed` / `ready` / `published` / `deprecated`
   - 禁止写自定义状态（例如 `draft-generated`），前端状态徽章不会识别

### 参考资料 comment 文件约定（新增）

- `references/*.comments.json` 视为参考资料的 sidecar 评论文件，存储高亮与讨论线程。
- 执行 Stage 1/2/3 时，**不要删除或覆盖**这些 sidecar 文件。
- 写初稿时必须优先读取 sidecar 中的 highlight 与 comment，再结合原文 reference 生成内容。
- 若缺失 sidecar 但用户明确说“我做了高亮/评论”，先在 `references/reference-notes.md` 记录该缺口并提示补充。

### 文章目录结构

```
articles/YYYY-MM-DD-{slug}/
  README.md              # 元数据
  references/            # 参考材料
    *.comments.json      # 参考资料行内评论 sidecar（含 highlight）
    reference-notes.md   # 从 reference+comment 提炼出的素材清单
  draft-v1.md            # AI 初稿
  final.md               # 人工终稿（Stage 2）
  final.comments.json    # 终稿行内评论（前端编辑器 sidecar 数据）
  diff-analysis.md       # 差异分析（Stage 2）
  viewpoints.yaml        # 观点提取结果（viewpoint-extractor skill 生成）
  output/                # 多平台输出（Stage 3）
    infographics/        # 信息图（infographic-gen skill 生成）
      {slug-1}.jpg
      {slug-2}.jpg
    blog/
      article.md
    wechat/
      article.md
      cover.jpg           # 微信封面（wechat-cover skill 生成）
    xiaohongshu/
      text.md             # 发帖文本（编辑推荐语）
      cards/              # 文转图卡片（xiaohongshu-cards skill 生成）
        01.jpg, 02.jpg, ...
    jike/
      article.md
    twitter/
      article.md
```

---

## Stage 2: Review（人工改稿 + 学习）

### 前置条件
用户已将改稿保存为 `final.md`

如果改稿在前端完成，目录中可能存在 `final.comments.json`（终稿行内评论数据）。该文件用于编辑协作，不参与平台分发。

### 步骤

1. **执行 Diff-and-Learn**
   详见 `references/diff-learn.md`

2. **生成差异分析**
   将分析结果保存为 `diff-analysis.md`

3. **提议 Skill 更新**
   根据差异分析，提出对应 writing-style skill 的更新建议：
   - 新增的禁止项
   - 需要调整的风格要点
   - 新发现的偏好规则

   **必须先向用户确认后再执行更新**

4. **更新元数据**
   将 `README.md` 中 `status` 改为 `reviewed`

### 文件约定（重要）

- `final.comments.json` 是 `final.md` 的 sidecar 文件，存储 inline comment 线程。
- 执行 Stage 2 / Stage 3 时，**不要删除或覆盖** `final.comments.json`。
- 多平台输出只读取正文（`final.md`），**不要把评论内容写入平台文案**。
- 复制/迁移文章目录时，建议连同 `final.comments.json` 一并保留，避免评论线程丢失。

---

## Stage 3: Publish（多平台输出）

### 步骤

1. **读取终稿**
   加载 `final.md`（如无则用最新 draft）

2. **原文图片统一上传 R2 并回写终稿**（必做）
   - 扫描文章目录下图片资产（至少包含 `images/`，可扩展到其他本地图片目录）
   - 用 `r2-upload` skill 批量上传，生成 `output/r2-image-mapping.json`（相对路径 → R2 URL）
   - 将 `final.md` 里的本地图片路径统一替换为 R2 URL
   - 若原文图片较多（例如案例集），在 `final.md` 里补充“原文图集”章节，确保可直接复用

3. **选择目标平台**
   让用户选择输出平台（可多选）：
   - 微信公众号 (`wechat`)
   - 小红书 (`xiaohongshu`)
   - 即刻 (`jike`)
   - 推特 (`twitter`)
   - 博客 (`blog`)

4. **加载 Formatter 并生成**
   对每个目标平台，加载 `projects/writing/formatters/{platform}.md`，按规则生成格式化内容。
   - 小红书：额外加载 `xiaohongshu-editor-pick` skill 生成编辑推荐语风格的发帖文本，**并必须运行 `xiaohongshu-cards` skill 生成文转图卡片**（小红书是图文平台，卡片是必做输出）

5. **保存输出**
   按平台分目录保存到 `output/{platform}/`：
   - `blog/article.md`
   - `wechat/article.md`
   - `xiaohongshu/text.md`（发帖文本）
   - `jike/article.md`
   - `twitter/article.md`

6. **插入信息图到全平台文章**（如 `output/infographics/` 存在且非空，必做）

   信息图必须插入到每个平台文章的**对应内容段落位置**（不是堆在末尾）。
   根据信息图的 slug 和 viewpoints.yaml 中的 title，找到文章中对应的章节，在该章节标题前插入。

   **上传：**
   - 用 `r2-upload` skill 批量上传 `output/infographics/` 到 R2，获取 R2 URL
   - 用 `wechat-upload` skill 批量上传到微信素材库，获取 `mmbiz.qpic.cn` URL
   - 按文件名顺序记录 R2 URL 和微信 URL 的对应关系

   **插入（全平台，每个都要做）：**
   - **blog**：`![alt](R2 URL)` 插入到对应段落前
   - **wechat**：`![alt](mmbiz URL)` 插入到对应段落前。微信不支持外链图片，必须用微信素材库 URL
   - **jike**：`📊 R2 URL` 纯文本行，插入到对应段落前（即刻是纯文本平台）
   - **twitter**：`📊 R2 URL` 纯文本行，插入到对应段落前
   - **xiaohongshu**：见步骤 8 的小红书卡片生成流程（信息图嵌入卡片图片中）

7. **微信图片链接替换**（当目标平台包含 wechat 时，必做）
   - 用 `wechat-upload` skill 批量上传文章图片（至少包含 `images/` 与 `output/infographics/`）
   - 保存映射到 `output/wechat/image-mapping.json`（相对路径/R2 URL → `{media_id, url}`）
   - 将 `output/wechat/article.md` 中所有图片链接替换为微信素材库 URL（`mmbiz.qpic.cn`）
   - 校验：`output/wechat/article.md` 不得残留 R2/GitHub 等外链图片 URL

8. **生成图片资产**（必做）
   - **微信封面**（必做）：用 `wechat-cover` skill → `output/wechat/cover.jpg`
     - 默认风格：Claymation 3D mascot + flat UI mockup（详见 wechat-cover SKILL.md）
     - prompt = 默认风格前缀 + 文章主题描述 + `no text`
     - `flash` 模型优先，失败换 `pro`
     - 生成后**必须**用 `wechat-upload` skill 上传到微信素材库，记录 media_id 和微信 URL 到 `output/wechat/image-mapping.json`（key 为 `cover.jpg`）。微信公众号封面图必须使用微信素材库中的图片
   - **小红书卡片**（必做）：用 `xiaohongshu-cards` skill → `output/xiaohongshu/cards/*.jpg`
     - **如果 `output/infographics/` 存在且非空，必须将信息图嵌入卡片：**
       1. `cp final.md final.md.bak`（备份原文）
       2. 在 `final.md` 对应段落位置插入信息图的 markdown 图片引用（`![alt](R2 URL)`）
       3. 运行 `xiaohongshu-cards` 生成脚本（脚本会渲染 markdown 中的图片到卡片中）
       4. `mv final.md.bak final.md`（还原原文）
     - 卡片生成脚本的 HTML 模板已有 `.card-flow img` 样式，会自动渲染内嵌图片

9. **更新元数据**
   将 `README.md` 中 `status` 改为 `ready`（中文：已就绪），记录发布平台

   **状态约束（强制）**：
   - 完成全平台内容产出后，**只能标记为 `ready`**，禁止自动改为 `published`
   - `published` 仅在用户明确要求“已发布/已实际发布”时才可使用

---

## 自动路由详解

### Style Skill 的 Routing Metadata

每个 writing-style skill 的 YAML frontmatter 包含 `routing` 字段：

```yaml
routing:
  content_types: [...]     # 擅长的内容类型
  domains: [...]           # 擅长的领域
  tone: [...]              # 语气特征
  best_for: "..."          # 一句话描述最佳场景
```

### 路由算法

```
输入：参考材料文本
输出：推荐的 style skill 名称

1. 分析材料特征
   - domain: 从关键词、主题、术语判断领域
   - content_type: 从结构、目的判断内容类型
   - tone: 从语气、目标读者判断期望语调

2. 计算匹配度
   对每个 style skill:
     domain_match = 材料 domain ∩ skill routing.domains
     type_match = 材料 content_type ∩ skill routing.content_types
     tone_match = 材料期望 tone ∩ skill routing.tone
     score = domain_match * 2 + type_match * 2 + tone_match * 1

3. 选择 score 最高的 skill
   - 如果最高分 skill 唯一 → 推荐该 skill
   - 如果两个 skill 分数接近（差距 < 20%）→ 列出两个让用户选
   - 如果所有 skill 分数都很低 → 提示用户手动选择
```

### 当前可用 Style Skills

| Skill | 擅长 | 关键词 |
|-------|------|--------|
| `writing-style-huasheng` | 技术解读、人物叙事、产品评测 | AI, 深度学习, 创业, 数据驱动 |
| `writing-style-baoyu` | 方法论、教程、观点输出 | 写作, 工具, 生产力, 比喻驱动 |
| `writing-style-dankoe` | 思辨文章、框架构建、身份探讨 | 心理学, 控制论, 意义, 跨领域 |
| `writing-style-zhengliu` | 知识蒸馏、结构化转述、长文摘要 | 任意领域, 四层结构, 数据优先, 信息提取 |

---

## 快速命令

- **开始新文章**：提供参考材料，管线自动进入 Stage 1
- **提交改稿**：告知 `final.md` 已就绪，管线进入 Stage 2
- **发布**：指定目标平台，管线进入 Stage 3
