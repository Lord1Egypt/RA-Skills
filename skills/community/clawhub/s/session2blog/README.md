# Session2Blog 📝

> ⚠️ **敏感数据提醒**：本工具会把 OpenClaw 会话历史提取并写入本地文件。对话中可能包含 API Key、Token、私人路径、邮箱或用户名等敏感信息。工具会做**最佳努力脱敏**（非 100% 保证），**发布前请人工复核**是否仍有遗漏。不要在含机密信息的会话上直接运行。

把 OpenClaw **你与 AI 真正协作解决问题的过程**，沉淀成带真人决策链的结构化博文（技术复盘 / 学习笔记 / 排障记录）。

## 为什么是它，而不是又一个 AI 写作工具

各大平台抵制的，从来不是「AI 参与创作」，而是**无脑 AIGC 的注水低质货**——没有观点、没有判断、没有真人在 loop 里拍板。

Session2Blog 解决的正是这个问题：它生成的不是 AI 替你写的文章，而是**你和 AI 对话协作的痕迹**。每一个关键决策、每一次纠错、每一句「我觉得应该这样」都来自真人。AI 只负责把这段协作过程整理、润色成可读的博文。

> 平台反感的是「没有人的内容」。**你的内容里，每一个观点都站着一个人。**

**协作溯源**是核心差异点：文章的可信度不靠一句「这是人写的」空话，而来自可见的对话轨迹与决策节点。

## 一句话

你在 OpenClaw 里跟 AI 干完活、把问题聊透了，输一句 `/s2b`，它就把**这段真实协作过程**整理成一篇结构化博文，直接保存为 Markdown 文件。

**零配置（免费版）**：不需要 API Key，不需要装 PATH，不需要开终端。模型用 OpenClaw 会话自带的，对话读本地的——**免费版 100% 本地处理，不出本机**。

> 📌 **信任边界**：免费版完全本地。Pro 版的一键发布为**可选功能**，需你主动配置平台凭证（如掘金 Cookie）才会发生远程调用，非默认行为，且默认只发到草稿箱、由你复核后再公开。

## 适用场景

| 场景 | 模板 | 效果 |
|------|------|------|
| 刚修好一个 bug | `troubleshooting` | 排障记录，下次踩坑直接翻 |
| 刚学会一个新工具 | `learning-notes` | 学习笔记，内化成自己的 |
| 刚做完一个技术决策 | `tech-review` | 技术复盘，沉淀团队经验 |

## 安装

把 `session2blog/` 目录复制到 OpenClaw 的 skills 目录下即可：

```bash
# 方式一：直接复制（推荐）
cp -r session2blog ~/.openclaw/skills/

# 方式二：用安装脚本
bash install.sh
```

安装后重启 OpenClaw 会话（或新开一个），`/s2b` 命令即可用。

## 使用

在 OpenClaw 会话中直接输入：

```
/s2b                          # 处理当前会话，自动选模板，通用风格
/s2b -n 3                     # 处理列表里第 3 个会话
/s2b --session <id>           # 用完整 session ID 指定
/s2b --template tech-review   # 指定模板：tech-review | learning-notes | troubleshooting | auto(默认)
/s2b --platform wechat        # 微信公众号风格（故事感、情绪、代入感）
/s2b --platform juejin        # 掘金风格（硬核、代码密集、体系化）
/s2b --platform csdn          # CSDN 风格（问题导向、步骤化、实用）
/s2b --platform zhihu         # 知乎风格（观点感、深度、辩证）
/s2b --platform all           # 中文: 一次生成 4 个平台版本（wechat/juejin/csdn/zhihu 各一）
/s2b --lang en --platform devto  # 生成英文 Dev.to 风格博文
/s2b --lang en --platform all    # 英文: 一次生成 Dev.to/Hashnode/Medium/HN 4 版
/s2b --list                   # 列出所有可用会话（带序号、Agent、日期）
```

### 示例

```
你: /s2b

→ AI 提取当前会话对话
→ 自动匹配「技术复盘」模板
→ 生成博文并保存到 ~/.openclaw/session2blog/articles/
→ 告诉你文件路径
```

## 平台风格适配

同一段对话，可以输出不同平台的爆款文风格。指定 `--platform` 后，AI 会按对应平台的读者预期重写标题和正文结构。

| 平台 | 风格特征 | 标题示例 |
|------|----------|----------|
| `wechat` 微信公众号 | 故事感、情绪、场景代入、口语化 | 「我做了3个月数字产品，0销量之后终于想通了一件事」 |
| `juejin` 掘金 | 硬核、体系化、代码密集、带目录 | 「万字长文讲透 OpenClaw Skill 开发」 |
| `csdn` CSDN | 问题导向、步骤化、搜索友好 | 「OpenClaw 会话导出失败？【已解决】」 |
| `zhihu` 知乎 | 观点感、深度、辩证、分层论证 | 「如何评价用 AI 把对话变成博客这件事？」 |
| `none` 通用（默认） | 平衡调性，[模板] 标题结构 | 「[复盘] 从0到1做数字产品的踩坑」 |
| `all` 全平台(中文) | 一次生成上述 4 个平台版本 | — |
| **英文平台** | | |
| `devto` Dev.to | 实用、友好、代码导向 | "How I cut build time by 60% with X" |
| `hashnode` Hashnode | 精致、个人品牌向、结构化 | "The Complete Guide to X for Beginners" |
| `medium` Medium | 叙事、思辨、长文 | "Stop Using X — Here is What I Do Instead" |
| `hn` Hacker News | 极简、重实质、无营销 | "Show HN: X does Y in 10 lines" |
| `all` 全平台(英文) | 一次生成 Dev.to/Hashnode/Medium/HN 4 版 | — |

文件命名规则：`YYYY-MM-DD-<模板>-<平台>-<slug>.md`

例如：`2026-07-11-tech-review-wechat-openclaw-product.md`

生成的博文**自动脱敏**，不会泄露：
- API Key / Access Token / Secret（自动替换为 `<REDACTED>`）
- 真实用户名、邮箱、手机号（替换为占位符）
- 绝对文件路径（如 `/Users/jasonlee/...` 替换为 `<USER_HOME>/...`）

发布前可自查：`grep -rn "sk-\|eyJ\|/Users/" ~/.openclaw/session2blog/articles/`

## 模板说明

### 技术复盘 (tech-review)
```
标题: [复盘] <核心问题描述>

1. 背景 — 当时在做什么
2. 踩坑过程 — 遇到了什么
3. 关键决策 — 怎么分析的
4. 最终方案 — 怎么解决的
5. 总结与教训 — 学到了什么
```

### 学习笔记 (learning-notes)
```
标题: [笔记] <主题>

1. 学习动机 — 为什么学
2. 核心概念 — 用自己的话解释
3. 实践过程 — 踩过的坑、跑过的代码
4. 心得体会 — 真正理解了什么
```

### 排障记录 (troubleshooting)
```
标题: [排障] <问题现象>

1. 问题现象 — 具体表现
2. 排查过程 — 怎么查的，用了什么工具
3. 根因分析 — 根本原因
4. 解决方案 — 具体怎么修的
5. 预防措施 — 下次怎么避免
```

## 配置

配置文件：`~/.openclaw/session2blog/config.yaml`（安装时自动生成，权限 600）

```yaml
default_template: auto      # auto | tech-review | learning-notes | troubleshooting
default_platform: none      # none | wechat | juejin | csdn | zhihu | devto | hashnode | medium | hn | generic | all
language: zh-CN
author: ""
articles_dir: ~/.openclaw/session2blog/articles

# 协作溯源：是否在博文末尾追加「协作过程与关键决策点」区块（默认 false 不加）
# 也可临时用 /s2b --with-collab 开启，无需改配置
include_collab_trace: false

> 📌 **发布为 Pro 版功能**：免费版仅生成本地 Markdown。一键发布（掘金/微信/CSDN/知乎）的配置与用法见文末「升级到 Pro 版」及 Pro 版文档。

## 目录结构

```
session2blog/
├── SKILL.md          # Skill 定义（/s2b 命令行为）
├── s2b.sh            # 内部实现：读 session JSONL → 脱敏 → 提取对话 → 输出
├── install.sh        # 安装脚本（复制到 ~/.openclaw/skills/）
├── README.md         # 本文件
└── gumroad-product-copy.md  # 产品页文案

~/.openclaw/session2blog/   # 运行时目录（自动创建）
├── config.yaml        # 本地可选配置（免费版仅需 articles_dir）
├── articles/          # 生成的博文
└── logs/
```

## 产品信息

- 定价: $5 一次购买，终身更新
- 许可证: MIT
- 平台: OpenClaw Skill（需要 OpenClaw 环境）

## 生成质量说明

- **博文生成质量与您使用的大模型直接相关。** 本工具负责把对话整理成结构化的平台风格草稿，但文风、准确性、深度取决于实际写文的模型（OpenClaw 会话模型或本地 ollama）。
- **建议人工复核后再发布。** 尤其是技术细节、代码片段、数据准确性，以及自动脱敏是否遗漏了敏感信息。
- 工具已内置「去 AI 味·仿人写作」指令，但不同模型遵循程度不一，最终可读性以人工检查为准。

## 支持这个项目

如果这个工具帮到了你，欢迎到 GitHub 点个 ⭐，让更多人发现：

👉 https://github.com/jasonleezy/session2blog

你的 star 是对开源创作者最好的鼓励。
