---
name: skill-distributor
description: 一键将 Skill 分发到全平台。读取 SKILL.md → 生成各平台描述文案（GitHub/CocoLoop/SkillHub/SkillsBook/虾技市场/ClawHub）→ 生成社交推广文案（小红书/即刻/知乎/掘金）→ 输出到 distro/ 文件夹 → 可选 GitHub 推送。
version: "1.0.0"
author: GMF515
allowed-tools: Read,Write,Bash
agent_created: true
trigger_words: 分发Skill,全平台发布,帮我发到各平台,一键发布,skill分发
---

# Skill 分发器

将任意 Skill 一键生成全平台分发材料，输出到 `distro/` 文件夹。

## 🎯 我能做什么

将你的 Skill 一键分发到 **10+ 平台**，包括：
- **技能市场**：GitHub / ClawHub / CocoLoop / SkillHub / SkillsBook / 虾技市场
- **社交推广**：小红书 / 即刻 / 知乎 / 掘金

只需告诉我你的 Skill 目录路径，5 分钟内生成所有平台的合规文案。

## 🚀 立即开始

请告诉我：

**1️⃣ Skill 目录路径**（必填）
> 例如：`/Users/mac/WorkBuddy/Claw/ai-usage-collector/`

**2️⃣ GitHub 用户名**（可选）
> 用于自动推送到 GitHub，如不提供则只生成文件

**3️⃣ GitHub Token**（可选）
> 用于自动推送，如不提供我会提示手动推送命令

---

**📌 提示**：也可以直接给我一个 ZIP 包路径，我会解压后处理。

## 参考资料

详细格式规范见 `references/platform-formats.md`，包含：
- WorkBuddy / ClawHub / GitHub 的 SKILL.md 格式差异
- 各平台支持的字段列表
- 常见错误与解决方案

## 支持的平台

| 平台 | 类型 | 生成内容 |
|------|------|---------|
| GitHub | 代码托管 | README.md + Git 推送 |
| ClawHub | 技能市场 | GitHub PR 自动收录 |
| CocoLoop | 国内技能市场 | 上架描述文案 |
| SkillHub（腾讯） | 国内技能市场 | 上架描述文案 |
| SkillsBook.fun | 国内技能市场 | 上架描述文案 |
| 虾技市场 | 国内技能市场 | 上架描述文案 |
| 小红书 | 社交种草 | 标题 + 正文 + 标签 |
| 即刻 | 社交社区 | 短文案 + 评论区引导 |
| 知乎 | 技术内容 | 文章大纲 + 正文 |
| 掘金 | 技术博客 | 文章正文 + 标签 |

## 工作流

### Step 1：接收输入

用户告知要分发的 Skill 路径（目录或 ZIP）。

**输入格式示例**：
```
帮我分发这个 Skill：/Users/mac/WorkBuddy/Claw/ai-usage-collector/
GitHub 用户名：yourusername
```

**如果用户未指定路径**，询问：
> "请告诉我要分发的 Skill 目录路径，以及 GitHub 用户名。"

**如果用户未指定 GitHub Token**，只生成文件，不执行 GitHub 推送。

---

### Step 2：验证 SKILL.md

读取目标目录下的 `SKILL.md`，验证以下必填字段：

| 字段 | 要求 |
|------|------|
| `name` | 必填，Skill 名称（英文或拼音）|
| `description` | 必填，功能描述 |
| `author` | 必填，作者标识 |
| `version` | 可选，默认 1.0.0 |

**验证失败时**：列出缺失字段，要求用户补充后再继续。

---

### Step 3：提取元数据

从 SKILL.md 解析以下字段，缺失时使用默认值：

```yaml
name: <从 SKILL.md name 字段提取>
title: <从 SKILL.md name 翻译为中文名称，或用户提供>
author: <从 author 字段>
version: <从 version 字段，默认 1.0.0>
description: <从 description 字段>
description_zh: <翻译为中文描述，50-150 字>
tags: <从 description 和 name 推断，5-8 个标签>
category: <根据功能推断分类（办公效率/开发工具/数据分析等）>
```

---

### Step 4：生成 GitHub README.md

根据提取的元数据，生成完整的 GitHub README.md，包含：

- Shield Badges（version、license、platforms）
- 中文 + 英文功能介绍
- 安装方法（OpenClaw / WorkBuddy）
- 使用示例（含截图说明文字）
- 适用场景
- 作者信息

**文件路径**：`distro/github/README.md`

---

### Step 5：生成各平台上架文案

为每个平台生成可直接粘贴的内容：

#### 5.1 CocoLoop（hub.cocoloop.cn）

**文件**：`distro/cocoloop.md`

| 字段 | 内容 |
|------|------|
| 标题 | 中文名称（15 字内）|
| 副标题 | 一句话说明 |
| 描述 | 50-100 字，中文 |
| 分类 | category 对应的 CocoLoop 分类 |
| 标签 | 5 个标签 |
| 截图说明 | 建议截图的内容 |

#### 5.2 SkillHub 腾讯（skillhub.tencent.com）

**文件**：`distro/skillhub-tencent.md`

| 字段 | 内容 |
|------|------|
| 技能名称 | 中文名称 |
| 功能描述 | 100 字内 |
| 适用平台 | OpenClaw / WorkBuddy |
| 分类 | category |
| 标签 | 3-5 个 |

#### 5.3 SkillsBook.fun

**文件**：`distro/skillsbook.md`

| 字段 | 内容 |
|------|------|
| 技能名称 | 中文名称 |
| 场景描述 | 50-100 字 |
| 标签 | 5 个 |
| 分类 | category |
| 定价 | 免费 |

#### 5.4 虾技市场（skillcast.cn）

**文件**：`distro/xiajimarket.md`

| 字段 | 内容 |
|------|------|
| 技能名称 | 中文名称 |
| 功能介绍 | 50-100 字 |
| 分类 | category |
| 评分说明 | 1-2 句 |

#### 5.5 ClawHub（clawhub.ai）

使用 `clawhub` CLI 发布到 ClawHub 官方技能注册表。

**前置条件**：安装 clawhub CLI 并登录
```bash
npm install -g clawhub
clawhub login
```

**发布命令**：
```bash
cd <skill-directory>
npx clawhub --workdir . skill publish . \
  --name "<skill-name>" \
  --version "1.0.0" \
  --changelog "Initial release"
```

**文件**：`distro/platforms/clawhub-publish.md`

| 字段 | 内容 |
|------|------|
| 命令 | `clawhub skill publish` 完整示例 |
| 依赖 | Node.js 18+ |
| 注意 | 首次需要 GitHub OAuth 登录 |

**关键参数**：
- `--workdir .` **必须添加**，否则找不到 SKILL.md
- `--version` 必须为字符串格式：`"1.0.0"`

**发布后链接**：`https://clawhub.ai/skills/<skill-name>`

---

### Step 6：生成社交推广文案

#### 6.1 小红书

**文件**：`distro/social/xiaohongshu.md`

```
标题：[场景人群] + [效果] + [工具名]
正文：痛点引入 → 工具介绍 → 使用方法 → 效果展示
标签：#AI工具 #职场提效 #Skill分享 #<category> #<工具名>
配图建议：3 张（痛点/工具/效果对比）
```

#### 6.2 即刻

**文件**：`distro/social/jike.md`

```
正文：1-2 句话场景描述
评论区引导：「Skill 下载地址见评论区」
标签：<name> #AI技能 #效率工具
```

#### 6.3 知乎

**文件**：`distro/social/zhihu.md`

```
标题：<中文名称> 是什么？为什么 AI 原生工作者需要它？
正文结构：
  - 背景痛点（200字）
  - 工具介绍（150字）
  - 使用方法（200字）
  - 效果对比（100字）
  - 总结引导（50字）
标签：AI、效率工具、OpenClaw、职场
```

#### 6.4 掘金

**文件**：`distro/social/juejin.md`

```
标题：<中文名称> 使用指南
正文：精简版使用说明 + 代码示例（如适用）
标签：AI、效率工具、OpenClaw、<category>
```

---

### Step 7：输出 distro/ 文件夹

生成完整的 `distro/` 目录结构：

```
distro/
├── github/
│   └── README.md              ← GitHub 仓库用
├── platforms/
│   ├── cocoloop.md            ← CocoLoop 上架
│   ├── skillhub-tencent.md    ← SkillHub 上架
│   ├── skillsbook.md          ← SkillsBook 上架
│   ├── xiajimarket.md         ← 虾技市场上架
│   └── clawhub-publish.md     ← ClawHub 发布命令
├── social/
│   ├── xiaohongshu.md         ← 小红书
│   ├── jike.md                ← 即刻
│   ├── zhihu.md               ← 知乎
│   └── juejin.md              ← 掘金
└── README.md                   ← 分发说明
```

---

### Step 8：GitHub 推送（如 Token 提供）

**前提**：用户提供 GitHub Token + 用户名

**操作**：
1. **将 distro/github/README.md 复制到仓库根目录**
   ```bash
   cp distro/github/README.md README.md
   ```
   > ⚠️ 这一步很关键！必须把 README 放到根目录，GitHub 仓库才会显示项目说明。
2. 初始化 Git 仓库（如未初始化）
3. 设置 remote：`https://github.com/<username>/<repo>.git`
4. 添加 Token 到 URL：`https://<token>@github.com/<username>/<repo>.git`
5. Git add → commit → push
6. 输出仓库地址

**⚠️ 重要**：README.md 必须覆盖到仓库根目录，否则 GitHub 仓库会显示空白项目页！

**PR 到 ClawHub**：通过 `clawhub skill publish` CLI 命令发布，不是 GitHub PR。发布后输出 ClawHub 链接。

**如未提供 Token**：
- 告知用户：「已生成所有文件，请在 GitHub 手动创建仓库，然后运行以下命令推送」

---

## 输出格式

每次生成完一个平台后，简要汇报：

```
✅ 已生成：
  - distro/github/README.md
  - distro/platforms/cocoloop.md
  - distro/social/xiaohongshu.md
  ...

📋 您的操作（复制粘贴）：
  1. 登录 CocoLoop → 填写 cocoloop.md 内容 → 上传
  2. 登录 SkillHub → 填写 skillhub-tencent.md 内容 → 上传
  ...

🚀 GitHub（如需自动推送）：
  请提供 GitHub Token，我来帮你推
```

## 注意事项

- 生成的内容基于 SKILL.md 元数据，描述要准确，不要夸大
- 各平台文案要有差异化，不要千篇一律
- 截图建议要具体，方便用户快速准备素材
- GitHub Token 安全第一，不要在日志/对话中暴露
