# 写作工作室技能库

> AI Agent Skills for Writing —— 文案、技术文章、长文内容、SEO 检查

## 定位

为独立开发者和创作者提供一套可安装的 AI Agent 写作技能，覆盖从短文案到长文章的完整创作链。

## 核心理念

> 好内容自带流量。让 AI 帮你完成 80% 的写作流程，你只负责创意和判断。

- **短文案驱动转化** — PAS/AIDA/BAB 框架写出让人点击和购买的文案
- **技术文章建立权威** — 7 阶段全流程，从选题到标题终审
- **长文内容增长** — Information Gain 策略，不做 AI 共识内容的搬运工
- **发布前验收** — 11 项 SEO 检查，发布前发现问题

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 📢 短文案 | `copywriter` | 短文案写作：标题、广告语、CTA、着陆页、邮件文案 | [衍生](https://skills.sh/kostja94/marketing-skills/copywriting) |
| 📝 技术文章 | `technical-writer` | 技术文章全流程：选题、标题、结构、起草、编辑 | [衍生](https://skills.sh/samber/cc-skills/technical-article-writer) |
| 📄 长文内容 | `content-writer` | 长文创作：博客正文、操作指南、信息增益策略 | [衍生](https://skills.sh/kostja94/marketing-skills/article-content) |
| 🔍 SEO 检查 | `seo-checker` | 博客发布前 SEO 检查：11 项 Pass/Fail 报告 | [衍生](https://skills.sh/agricidaniel/claude-blog/blog-seo-check) |

## 快速开始

```bash
# 安装全部写作技能
npx skills add skills-repo/writer-studio -g -y

# 或按需安装单个技能
npx skills add skills-repo/writer-studio@copywriter -g -y
npx skills add skills-repo/writer-studio@technical-writer -g -y
npx skills add skills-repo/writer-studio@content-writer -g -y
npx skills add skills-repo/writer-studio@seo-checker -g -y
```

## 推荐工作流

```
选题打磨 → 长文起草 → SEO 优化 → 短文案推广
technical-   content-    seo-        copywriter
writer       writer      checker
```

## 深层 Playbook（按需加载）

`SKILL.md` 只做路由，深层方法论放在 `references/`，按需读取：

| Playbook | 内容 | 何时读 |
|----------|------|--------|
| [references/writing-process.md](references/writing-process.md) | 通用写作流程、流程选择决策树、可运行的写作体检命令（注水词/被动句/句长/段落/篇幅 + 判读阈值表 + 命令盲区表）、量化编辑清单 | 起草/编辑阶段、不确定走哪条流程时、发布前量化体检 |
| [references/seo-content-strategy.md](references/seo-content-strategy.md) | 关键词对齐、信息增益、内容结构、发布前 SEO 策略层自检命令 | 发布前的 SEO 策略层自查（技术层验收交给 `seo-checker`） |

## 许可

MIT
