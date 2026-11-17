---
name: wenqu-image
description: >-
  为内容设计并生成、质检、上传、嵌入架构图、流程图、信息图和示意图，覆盖提示词设计到
  最终出图。当用户要求“画个架构图”“画流程图”“生成配图”“生成图片”“把图画出来”
  “渲染一下”或“帮我生图”，或使用 "draw an architecture diagram", "generate an image",
  "create a flowchart" 等英文表达时使用。
slug: wenqu-image
displayName: 文曲·配图
version: 0.1.19
summary: 为内容生成 AI 配图（架构图/流程图/信息图/示意图）：提示词、生图、质检、上传全流程。
license: MIT
homepage: https://github.com/gogoingai/wenqu-skills
metadata:
  openclaw:
    homepage: https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-image
---

# 内容配图与生图 Skill

> 📦 项目仓库与源码：<https://github.com/gogoingai/wenqu-skills>

## 与调用方的接口约定

其他写作技能（如 wenqu-write）在正文里为图片预留位置时，用两种标记之一：

| 标记 | 含义 | 谁来写 |
| --- | --- | --- |
| `> 🖼️ 待配图：[一句话描述这张图要表达的核心内容]` | 占位标记，只知道这里需要一张图，还没想好具体画法 | 调用方（写作阶段） |
| \`\`\`（代码块）第一行 `# 画图提示：[描述]` | 完整画图提示，规范已写全，可以直接生成 | 本技能，或调用方已自行写好 |

本技能被调用时，**先把占位标记转换成完整画图提示，再进入生成流程**——两步不能合并，写法未确认前不要直接生成。

**完整画图提示必须带风格 YAML frontmatter**，格式是 `# 画图提示` 代码块内、提示正文之前加一段 YAML，风格、参考图路径、版本记录都写进提示本身，不能只存在对话记忆里——不然下次改图或复现时，所用风格、参考图与版本记录都无从解析：

```
```
---
style: 单色马克笔   # 对应风格库表里的风格名；无风格关键词时写"默认极简PPT"
ref: mono-marker/mono-marker-02-branch-decision.png   # 实际用过的参考图：styles/ 下的相对路径（不含域名），由 wenqu image fetch-ref 解析为受管缓存路径；临时本地路径不得写入；本轮没用 --ref 时保持原值不动；该字段从未用过时才省略
versions:   # 历次生成的版本记录；每项必须是 HTTPS CDN URL，含质检不通过/用户否决版本，编号递增，不删除、不覆盖
  v1: https://cdn.example.com/article-img-1111aaaa2222bbbb.png   # 简要说明
generation: # 与 versions 同编号，记录实际渲染后端；不存密钥或 API 地址
  v1:
    provider: codex
    model: codex-image-gen
---
# 画图提示：[图片标题]
# ...（提示正文，四条核心原则见下方）
```
```

转换占位标记、或用户直接给风格关键词时，都按这个格式写；`references/styles/*.md` 里该风格追加的专属描述句，直接拼进提示正文，不要另起一段脱离 YAML 之外的"风格说明"，避免以后只读提示正文时丢失风格信息。**每次实际传入 `--ref` 后**，把这次真正生效的参考来源回填进 `ref` 字段：风格资产用 GitHub raw URL，已采用图片用 HTTPS CDN URL；命令中临时使用的 `/tmp` 文件不得回填。`ref` 记的是“这次生成实际参考了什么”，不是“这个风格理论上可以参考什么”；**没用 `--ref` 的这一轮，不要动 `ref:` 字段**，保留上一次的记录。**只有上传成功、拿到 HTTPS CDN URL 的版本才可写入 `versions`**，同时把本次实际 provider/model 写入同编号 `generation`；正文的 `![]()` 只指向当前采用的那一版，其余版本仅留存在 `versions` 里供回看对比，具体写入规则见 `references/gen-workflow.md` 第四步。

## 用户输入工具

当本技能需要用户确认选择、补充必要信息或授权有副作用的操作时：

1. 优先使用当前运行时提供的原生用户输入工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或等价能力。
2. 若没有此类工具，使用带编号或字母选项的文本问答。
3. 同一决策阶段中彼此独立的问题可合并提问；后一个问题依赖前一回答时，按优先级逐个问。
4. 已由用户当前指令、调用方或文章偏好提供的信息，不重复询问。
5. 文中出现的具体工具名均为示例；应替换为当前运行时的等价能力。

### 模型配置提问规则

先检查全局配置 `~/.gogoingai/wenqu-skills/image/config.json`，再检查本篇
`{项目根目录}/wenqu-skills/{文件名}/config/image.json`：

1. 两者都没有时，用原生输入工具一次询问默认 provider、模型与画幅；**不要索要密钥**，仅告知用户运行 `wenqu image doctor` 查看本机凭证文件路径，然后创建全局非敏感配置。
2. 有全局配置、本篇没有配置时，在首次为本篇实际生成前询问是否沿用全局选择；拒绝后询问本篇选择并写入文章级配置。
3. 有本篇配置、或用户已在当前指令/命令中指定 provider/model 时，不重复询问。
4. 直接生图（非文章场景）只读取全局配置；运行时命令由 `wenqu image` 提供。

## 工具等价说明（非 Claude Code 环境）

文中 `Skill` 工具是 Claude Code 的跨技能调用机制名。其他 agent 没有对应机制时，调用方直接读取本技能的 `SKILL.md` 和 `references/` 文件就地执行。

---

## 触发识别

**讨论不触发生图：** 用户说“看看图”“讨论怎么画”“评价图片”“先给画图方案”或“这张图哪里不对”时，只分析现图或给出增量修改方案，不生成、上传或写入文章。只有用户明确说“生成”、“画”、“重画”、“插入”、“上传并替换”时，才进入实际流程；增量调整只改用户点名的内容，需要整体重画时先说明原因。

| 场景 | 入口 |
|------|------|
| 用户直接说"画个XX图"、"生成配图"，给出内容描述 | 直接进入「写画图提示」 |
| 文章里已有 `> 🖼️ 待配图` 占位标记 | 先转换成完整画图提示，见 `references/gen-workflow.md` 第二步 |
| 用户说"生成图片"、"渲染一下"、"把图画出来" | → 查 `references/gen-workflow.md`，完整生成流程 |
| 用户提到"手绘风格""Excalidraw""马克笔风格""水彩涂鸦""奶油描边""思维导图风""彩色铅笔""排线阴影""技术PPT风格"等风格关键词 | → 直接跳对应的 `references/styles/*.md`（见下方风格库表） |

---

## 写画图提示

核心原则（4 条，展开说明见 `references/core-principles.md`）：
1. 描述视觉物体，不指定显示文字——prompt 触发元素，不指定渲染细节
2. 不写 px/尺寸/颜色值/字号——生图模型自行决定渲染细节
3. 图类型、节点标签、箭头语义、关键数据、视觉层次是该写的内容
4. 禁止任何画图 DSL（Mermaid、draw.io、Graphviz、PlantUML）——只输出 `# 画图提示` 代码块

**动笔前先查本篇偏好库**（`references/preferences.md`「配图偏好」表，路径与读取方式见下方「用户反馈与偏好持久化」）——有没有已记录的默认风格、配色规则等，有则直接应用，不重复问用户。

先判断该画哪类图 → `references/diagram-type-selector.md`（图类型快速选表与该画哪类架构图），再去对应的图型模板文件取 prompt 骨架：

| 图型模板文件 | 覆盖的图类型 |
| --- | --- |
| `references/templates/architecture.md` | 横向多层架构图、树形层次检索路径图 |
| `references/templates/flow.md` | 竖向三阶段流程、竖向分支流程、横向阶段列流程、两层流程（主流程+展开细节） |
| `references/templates/comparison.md` | 并排方案对比、并行双路流程、左右结果对比 |
| `references/templates/data-viz.md` | 横向条形图、公式+分级卡片、时间演化折线图、金字塔分层图 |

风格库（见下表，不混用）：

| 风格 | 文档 | 参考图目录 |
| --- | --- | --- |
| 手绘插画 | `references/styles/handdrawn.md` | `wenqu-image-assets/styles/handdrawn/` |
| Excalidraw（白板斜线填充） | `references/styles/excalidraw.md` | `wenqu-image-assets/styles/excalidraw/` |
| 单色马克笔（波浪线注释） | `references/styles/mono-marker.md` | `wenqu-image-assets/styles/mono-marker/` |
| 水彩涂鸦（星星火花装饰） | `references/styles/doodle-watercolor.md` | `wenqu-image-assets/styles/doodle-watercolor/` |
| 奶油描边（黑色粗描边思维导图） | `references/styles/cream-outline.md` | `wenqu-image-assets/styles/cream-outline/` |
| 彩色铅笔质感（编号徽章与排线阴影） | `references/styles/pencil-sketch.md` | `wenqu-image-assets/styles/pencil-sketch/` |
| 技术PPT（机器人吉祥物） | `references/styles/techppt.md` | `wenqu-image-assets/styles/techppt/` |
| （无风格关键词/默认） | 默认极简 PPT，直接在图型模板结尾加「风格：白色背景，高级技术 PPT 配图，极简专业，文字标注全部用中文。」 | — |

其他参考文档：

| 文档 | 内容 |
| --- | --- |
| `references/pitfalls.md` | 常见踩坑教训（跨风格通用） |
| `references/design-principles.md` | 设计四大原则与配色审美 |
| `references/diagram-examples.md` | 完整示例 |

---

## 生成图片

→ 查 `references/gen-workflow.md`（环境检测 → 列出画图点并补全占位标记 → 逐张生成/质检/确认 → 写入文章 → 联动提醒）。

逐张生成、逐张确认，不批量、不跳过用户；Codex 路径受 session 输出提取限制，必须串行，其他后端也按同一确认节奏逐张处理。

**单图采用标准：** 一张图只承担 1～2 个关键关系；图中文字、节点、箭头与正文术语一致，最终采用的 URL 是 `versions` 中的 HTTPS 版本。满足这些条件后才可标记为“已采用”；若调用方文章存在 `references/status.md`，同步图片状态与待复查原因。

---

## 运行时要求

- 运行器：`wenqu image` CLI（`doctor`、`config-init`、`generate`、`fetch-ref`）。该 CLI 独立于 skill 安装；每次调用前先获授权更新 `wenqu-cli`，再运行 `wenqu image doctor --json` 确认。它会随包安装所需 Python 依赖；Crawl4AI 与浏览器只属于 `wenqu library`，不是 image 的前置条件。
- 后端：`codex`（复用已登录订阅）、OpenAI GPT Image（`OPENAI_API_KEY`）、OpenRouter（`OPENROUTER_API_KEY`）、通义万相（`DASHSCOPE_API_KEY`）或豆包 Seedream（`ARK_API_KEY`）；密钥由 `wenqu image` CLI 从本机凭证文件读取（运行 `wenqu image doctor` 查看路径）；不要在技能里硬编码密钥值。
- 图床：`picgo`（可选，上传时需已配置 uploader）。
- 风格参考图库：`styles/` 下分目录（`handdrawn/` 手绘插画、`excalidraw/` 白板斜线填充、`mono-marker/` 单色马克笔、`doodle-watercolor/` 水彩涂鸦、`cream-outline/` 奶油描边思维导图、`pencil-sketch/` 彩色铅笔质感、`techppt/` 技术PPT风格，配合 `--ref` 使用，对应文档见 `references/styles/`）。图片不随技能分发，托管地址由 `wenqu image fetch-ref`（环境变量 `WENQU_IMAGE_ASSETS_BASE`）解析，首次使用下载到受管缓存，需要联网。

---

## 用户反馈与偏好持久化

不再向用户提议修改本技能仓库的文档（`references/pitfalls.md`、`references/styles/*.md`、`references/templates/*.md` 等），遇到新画图踩坑或用户给出的持久化偏好，改为记进**调用方文章自己的**存储目录：`{项目根目录}/wenqu-skills/{文件名}/references/preferences.md`「配图偏好」表（表结构见 wenqu-write 的 `references/planning/questionnaire.md`「写入 preferences.md」一节）。provider、模型和画幅例外：它们只写入同级的 `config/image.json`，避免和写作偏好混在一起。

**判定标准**：这条反馈下次给这篇文章画图还用得上吗？
- 是（默认风格、配色规则、某类结构反复踩坑的修法、用户明确要求"以后都这样画"）→ 当场追加一行进 `references/preferences.md`「配图偏好」表，格式：`| ID | 内容 | 来源 | 状态 |`
- 否（这次改这张图的临时要求，比如"这条箭头改成红色"）→ 不持久化，正常执行即可

**每次画图前先查这份文件**：有已记录的默认风格/配色/常见修法，直接应用，不重复问用户；生成结果反复触发同一个踩坑时，把修复策略当场写成一条偏好记录，而不是只在当次会话里口头记住。

被独立文章调用（无 wenqu-write 提供的存储路径）时，若找不到调用方上下文，询问用户"这次的画图偏好要记到哪篇文章的存储目录"，或按当前工作目录和输出文件名推断。
