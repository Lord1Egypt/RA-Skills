# 字帖生成器与练字助手｜字帖库

想给孩子做可打印的姓名字帖、拼音田字格，或不知道今天练什么？用字帖生成器与练字助手，从自然问题开始安排练习。

| 你可以这样问 | 可以安排的字帖 |
|---|---|
| “给孩子做一张林小禾的姓名字帖” | 姓名描红或独立书写 |
| “春夏秋冬做成带拼音的田字格” | 拼音田字格 |
| “把这几个字做成描红，格子用米字格” | 汉字描红、田字格或米字格 |
| “帮我把《静夜思》做成字帖” | 古诗字帖 |
| “孩子最近练什么比较合适？” | 基础笔画、控笔线条或适合的汉字练习 |

AI 会帮你选练习、安排练法，并生成可在[字帖库官网](https://zitieku.com/ai-zitie.html)预览、调整、下载 PDF 和 A4 打印的字帖。

支持姓名练字、汉字描红、拼音、笔顺、基础笔画、控笔线条和古诗字帖。日常安装使用 main 分支；版本标签（如 `v0.5.2`）用于固定和复现某个快照。

## 开始使用

在[平台使用指南](https://zitieku.com/ai-zitie/start/)选择你常用的 AI，复制对应指令发到对话里。例如：

```text
请从 https://github.com/bryancat/zitieku-print（main 分支）添加“字帖生成器与练字助手｜字帖库”技能，按仓库 README 中「给 AI 的安装说明」完成安装和验证。装好后直接帮我安排这次练字；如果装不上，请如实告诉我，并先帮我把练习内容和练法定下来。
```

装好后可以直接问：“给孩子做一张可打印的姓名字帖，叫林小禾”，或“把春夏秋冬做成带拼音的田字格”。

## 给 AI 的安装说明

以下步骤写给执行安装的 Agent。用户已经在指令中授权安装本技能，安装细节无需向用户复述。

1. **确认环境**：当前宿主支持技能安装、能联网获取文件、能运行 Python 3。任何一项不满足，直接按第 5 步处理。
2. **获取完整文件**：按宿主的技能安装机制获取 main 分支内容，保留 `SKILL.md`、`scripts`、`references` 和 `agents`。遵循宿主的目录与权限规则，不猜测目录，不覆盖已有同名技能。
3. **确认已启用**：确认宿主能发现并启用技能。只读取说明、没有真正添加，不算安装成功。
4. **运行验证**：在技能目录运行 `python3 scripts/create_link.py --list-templates`，应返回 13 种方案；再把 `{"template_id":"basic-strokes"}` 通过 JSON 文件或标准输入传给脚本，输出应为 `configuration_ready` 并包含完整网站链接。不要把用户内容拼进 shell 命令。
5. **无法安装或运行脚本时**：如实告诉用户哪一步不可用。仍按 `SKILL.md` 的思路给出练习文字、格型、练法和停止建议，并提供 https://zitieku.com/zitie-shengchengqi.html 让用户手动制作。不编造预填链接，不声称已生成字帖。
6. **验证通过后**：直接进入练字流程。结合已有对话只问还缺少的必要信息，推荐内容和练法，最后提供“查看并打印字帖”链接。

各平台的入口差异：ChatGPT 使用已开通 Skills 的工作区；Claude 区分 Claude Code 与网页端 Customize → Skills（网页端需开启代码执行）；Grok 使用 Grok Build；Kimi Work 可用 Plugin Builder；千问办公与扣子编程按各自技能机制添加。账号、权限与额度以实际客户端为准。

## 各平台使用方法

- [WorkBuddy 练字教程](https://zitieku.com/ai-zitie/start/#platform-workbuddy)：在对话中添加，接着就能练字。
- [豆包 练字教程](https://zitieku.com/ai-zitie/start/#platform-doubao)：聊聊孩子的情况，让豆包帮你选内容和练法。
- [Kimi 练字教程](https://zitieku.com/ai-zitie/start/#platform-kimi)：在 Kimi 对话中安排练习，用 Kimi Work 获取技能。
- [腾讯元宝 练字教程](https://zitieku.com/ai-zitie/start/#platform-yuanbao)：从名字、生字或练字困惑出发，整理一份练习方案。
- [通义千问 练字教程](https://zitieku.com/ai-zitie/start/#platform-qwen)：用千问规划练习，也可在千问办公中添加技能。
- [DeepSeek 练字教程](https://zitieku.com/ai-zitie/start/#platform-deepseek)：把练字目标说清楚，得到具体的练习内容与建议。
- [扣子 练字教程](https://zitieku.com/ai-zitie/start/#platform-coze)：在扣子编程中准备技能，再进入对话使用。
- [ChatGPT 练字教程](https://zitieku.com/ai-zitie/start/#platform-chatgpt)：在已开通 Skills 的工作区中，通过对话添加练字技能。
- [Claude 练字教程](https://zitieku.com/ai-zitie/start/#platform-claude)：用 Claude Code 获取技能，或在 Claude 的 Skills 中添加。
- [Grok 练字教程](https://zitieku.com/ai-zitie/start/#platform-grok)：在 Grok Build 中添加技能，用对话准备练习。

## 适用环境

需要宿主支持 Agent Skills、联网获取仓库、文件操作和 Python 3 执行。生成链接只使用 Python 标准库，不需要字帖库 API Key。仓库地址让具备相应能力的 AI 自行获取文件，不能让普通聊天窗口自动获得技能安装能力。

常用命令（从技能目录执行）：

```sh
python3 scripts/create_link.py --list-templates
python3 scripts/create_link.py --describe-template name-blank
python3 scripts/create_link.py --input request.json
```

配置生成成功不代表网页渲染或 PDF 已导出。请打开链接确认字形、拼音、笔顺及分页，再下载或打印。

## 文件结构

- SKILL.md：技能入口与顾问工作流程。
- scripts/create_link.py：确定性配置链接生成脚本。
- references/：能力契约、输入说明和练习建议。
- agents/：宿主展示配置。

## 官网与备用下载

只有 Agent 无法访问 GitHub，或环境仅支持手动导入时，才需要下载备用 ZIP。

- [产品介绍](https://zitieku.com/ai-zitie.html)
- [安装帮助](https://zitieku.com/ai-zitie/start/)
- [可直接上传的扁平 ZIP](https://zitieku.com/downloads/zitieku-print-0.5.2.zip)
- [问题反馈](https://github.com/bryancat/zitieku-print/issues)

GitHub 自动生成的源码 ZIP 带仓库外层目录；若平台要求 ZIP 根目录直接包含 SKILL.md，请使用官网提供的扁平 ZIP。

## 开源许可

本仓库的 Skill 发布包（说明、脚本、参考文件及宿主配置）采用 [MIT-0](LICENSE)，允许使用、修改和再分发，无需署名。该许可仅覆盖本仓库提供的 Skill 文件，不覆盖字帖库网站代码、在线服务、字体、字形、笔顺及其他未随包提供的资源；在线服务仍适用其自身条款。

## 内容与隐私

本地脚本不发起网络请求。用户输入会由所用 AI 平台处理；生成链接包含可还原的练习文字，压缩不等于加密，请只分享给信任的人。链接的查询参数只含来源、技能版本和可选的平台标识，不含姓名或正文。不要在公开问题中提交孩子的真实姓名或个人字帖链接。

## 质量检查

覆盖链接长度校验、方案能力查询、无汉字拒绝与杂字符提示、一次返回全部错误、无效字段拒绝和实际设置回执。对话验收场景见 [tests/evals/conversations.md](tests/evals/conversations.md)，需在目标 Agent 宿主执行。

## 版本维护

更新时按宿主机制操作，保留用户自行修改的版本。本仓库为独立分发版本，维护源为字帖库项目中的 `integrations/zitieku/skills/zitieku-print`（含本 README）；更新源后需同步发布，当前未配置自动同步。
