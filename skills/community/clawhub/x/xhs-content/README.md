# xhs-content

一个面向 **职场 / 副业 / AI 工具** 赛道的 Xiaohongshu 内容生成 Skill。

A Xiaohongshu content generation skill for **career growth, side hustles, and AI-tool workflows**.

它适合这几类请求：
- 拆解一篇小红书热帖为什么会火
- 按某个主题直接生成小红书文案
- 给一段草稿改成更像平台原生内容的版本
- 批量生成标题、标签、配图建议
- 输出 2-5 个不同风格版本做 A/B 测试

It works well for:
- breaking down why a Xiaohongshu post performs well
- generating a post from a topic or angle
- rewriting rough drafts into more native platform-style content
- producing batches of titles, tags, and image ideas
- creating multiple variants for A/B testing

## 为什么它更适合拿来展示 / Why it presents well
- 聚焦中文小红书语境，不是泛营销文案
- 默认覆盖标题、正文、标签、配图建议
- 偏“真实分享感”，减少生硬广告味
- 对素材不完整的输入也能先给成稿
- 支持热帖拆解、关键词成稿、标题 A/B 测试三类高频需求
- Focused on Chinese Xiaohongshu-native content rather than generic marketing copy
- Covers titles, body copy, hashtags, and image suggestions by default
- Optimized for relatable, human-sounding posts instead of ad-like output
- Can still produce a usable first draft when the input is incomplete

## 目录结构 / Structure

```text
xhs-content-skill/
├── LICENSE
├── SKILL.md
├── README.md
├── assets/
│   ├── README-showcase.md
│   └── social-preview.svg
└── references/
    ├── case-studies.md
    ├── examples.md
    ├── hooks.md
    └── prompt.md
```

## 触发场景 / Triggers

当用户提出下面这类需求时很适合使用：
- “帮我写一篇小红书”
- “分析这篇帖子”
- “给我出几个爆款标题”
- “把这段内容改成小红书风格”
- “围绕 AI 工具 / 副业 / 职场干货生成文案”

Use this skill when the user asks for things like:
- “Write a Xiaohongshu post for me”
- “Analyze why this post works”
- “Give me several high-click titles”
- “Rewrite this into Xiaohongshu style”
- “Generate copy about AI tools / side hustles / workplace efficiency”

## 快速使用 / Quick use

### 输入示例 1：主题成稿
```text
帮我写一篇小红书，主题是：我怎么用 AI 把周报时间从 2 小时压到 20 分钟。
```

### 输入示例 2：热帖拆解
```text
分析这篇帖子为什么火，并按类似结构帮我写一篇适合 AI 副业号的小红书。
```

### What you get
- 3-5 个标题备选 / 3-5 title options
- 1 个可直接发的正文版本 / 1 ready-to-post body draft
- 15 个话题标签 / 15 hashtag suggestions
- 3 张配图建议 / 3 image suggestions
- 必要时补一个爆点简析 / a short virality breakdown when useful

## Showcase

- **热帖拆解**：输入一篇爆款笔记，输出它为什么火，以及一篇结构相似但不照抄的新稿
- **标题 A/B 测试**：围绕同一篇正文，快速产出多组“结果导向 / 共鸣导向 / 反差导向”标题
- **关键词成稿**：只给主题词，也能先产出一个可直接发布的初版
- **案例场景库**：新增 `references/case-studies.md`，方便快速覆盖高频用例


## 输入到输出展示 / Input-to-output demo

- Visual demo: `assets/input-output-demo.svg`
- Output snapshot: `assets/demo-output.md`
- 这类素材适合放在仓库首页、收录页、社媒转发图里

## 仓库展示素材 / Repo assets

- Social preview: `assets/social-preview.svg`
- Input/output demo: `assets/input-output-demo.svg`
- Result card mockup: `assets/mockup-results-card.svg`
- Feed preview mockup: `assets/mockup-feed-preview.svg`
- Showcase notes: `assets/README-showcase.md`
- Asset gallery: `assets/gallery.md`
- Case library: `references/case-studies.md`

## 内容策略 / Content strategy

这个 skill 默认更偏向下面几类内容：
- **热帖拆解型**：学结构，不照抄
- **干货教程型**：强调步骤、工具、结果
- **案例逆袭型**：强调前后反差和可复制性
- **观点共鸣型**：强调打工人痛点和误区

By default, the skill leans toward:
- **hot-post breakdowns**
- **practical tutorial-style posts**
- **before/after transformation stories**
- **pain-point and opinion-driven posts**

## 第四波新增案例 / New case library in wave 4

这次额外补了 4 类更像真实需求的案例：
- AI 周报提效
- AI 副业尝试
- 标题 A/B 测试
- 热帖结构迁移

## 当前亮点 / Current packaging wins

- 双语 README
- 多层展示素材（横版、竖版、结果卡片）
- 高频案例库
- GitHub metadata + topics
- 轻量 repo health workflow

## 后续还能继续冲的方向 / Next upgrades

如果后面还想继续提升展示和转化，可以再补：
- 更细分赛道版本（留学 / 教培 / 电商 / 自媒体）
- 更强的对照式案例库
- ClawHub 专用 metadata（如果平台公开规范）
- 更完整的英文介绍页
- 提交页/收录页专用截图

## License

MIT
