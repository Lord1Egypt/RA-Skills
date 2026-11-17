---
name: wenqu-translate
description: >-
  将 README、论文、源码注释、文档和英文文章等材料翻译成自然中文，供中文内容创作与阅读
  使用。当用户要求“翻译一下”“把这段英文翻译成中文”或“译成中文”，或使用 "translate to
  Chinese", "translate this README", "translate this paper" 等英文表达时使用。
slug: wenqu-translate
displayName: 文曲·翻译
version: 0.1.19
summary: 英文材料（README、论文、源码注释、文档）翻译成自然中文，用于内容创作与阅读。
license: MIT
homepage: https://github.com/gogoingai/wenqu-skills
metadata:
  openclaw:
    homepage: https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-translate
---

# 英文材料翻译 Skill

> 📦 项目仓库与源码：<https://github.com/gogoingai/wenqu-skills>

## 用户输入工具

当本技能需要用户确认选择、补充必要信息或授权有副作用的操作时：

1. 优先用运行时自带的用户输入工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或等价能力。
2. 若没有此类工具，使用带编号或字母选项的文本问答。
3. 同一决策阶段中彼此独立的问题可合并提问；后一个问题依赖前一回答时，按依赖顺序逐个问。
4. 已由用户当前指令、调用方或文章偏好提供的信息，不重复询问。
5. 文中出现的具体工具名均为示例；应替换为当前运行时的等价能力。

## 工具等价说明（非 Claude Code 环境）

`Skill`（调用 wenqu-review 做 R2 审查）是 Claude Code 工具名。其他 agent 没有该工具时，直接 Read `~/.agents/skills/wenqu-review/references/r2-translation.md` 内联执行。

## 触发识别

| 场景 | 入口 |
|------|------|
| 用户直接说"翻译一下"、给一段英文要求译成中文（单篇文章量级） | 独立触发，走下方"翻译流程" |
| wenqu-write Step 2 获取素材时源材料是英文 | 被调用，读者画像已由调用方提供，跳过下方"确认读者背景"这一步 |
| 源文档很长（约 4000 词以上）、要翻译多篇与整本书、需要 quick/normal/refined 多模式切换或分块并行翻译 | **超出本技能范围**，如实告知用户另寻专门的长文档翻译工具，不要硬凑 |

---

## 超出范围的情况

源文档词数明显超过 4000、需要 quick/normal/refined 多模式切换、分块并行翻译，或要翻译整本书/多篇文档时，**超出本技能范围**：如实告知用户“这个量级超出本技能范围，建议寻找专门的长文档翻译工具”，不要硬凑一份打折扣的翻译。本技能不依赖、也不主动推荐任何第三方技能。
---

## 翻译流程

→ 查 `references/translation-guide.md`（完整方法论：分析→翻译→自查，核心原则，注解密度规则，常见误译信号）

**独立触发时，先确认读者背景**（决定注解密度）：没有调用方提供读者画像，用 `AskUserQuestion` 询问"目标读者的技术背景是？"（无背景、初级工程师、中级工程师、高级工程师），再进入翻译。

**翻译完成后，强制当场执行一次 R2，不等到全文写完**：用 `Skill` 工具调用 **wenqu-review**，指定只跑 R2（翻译腔审查）；没有跨技能调用机制时直接 Read `~/.agents/skills/wenqu-review/references/r2-translation.md` 内联执行。这一步不可省略——Claude 系模型生成中文时容易出现翻译腔，尤其是刚读完英文源码、文档之后，译者很难察觉自己写出的翻译腔。

---

## 依赖

- `references/translation-guide.md` 完整自包含，覆盖单篇文章量级的翻译，不需任何外部依赖
- R2 审查依赖 **wenqu-review**（同仓库技能，随套件一起安装）

---

## 用户反馈与偏好持久化

本技能不修改自身仓库的 `references/translation-guide.md`，遇到新的误译模式或用户给出的持久化翻译偏好（专有名词是否保留英文、注解密度、直译信号判定……），改为写入**被翻译文章自身的**存储目录：`{项目根目录}/wenqu-skills/{文件名}/references/preferences.md`「翻译偏好」表（表结构见 wenqu-write 的 `references/planning/questionnaire.md`「写入 preferences.md」一节）。

**判定标准**：这条反馈下次译同一篇文章时还用得上吗？
- 是（"agent 不要翻译成智能体，保留英文"这类持续适用的取舍）→ 当场往 `references/preferences.md`「翻译偏好」表里追加一行
- 否（这次这段话的临时改法）→ 不持久化

**每次翻译前先查这份文件**（被 wenqu-write 调用时通常已加载；独立触发时自己检查该文章的 `wenqu-skills/{文件名}/references/preferences.md` 是否存在），有已记录的偏好就照着做，不重复问用户。
