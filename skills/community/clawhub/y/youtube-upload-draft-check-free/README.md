# YouTube 上传草稿检查

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；选择与本机系统匹配的当前版本。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

在发布前，用一份可追溯的问题单看清本人 YouTube Studio 草稿是否缺标题、简介、缩略图、受众、可见性或字幕。输入是用户指定的浏览器、本人草稿页或发布目标与 browserId；结果是逐字段的可见值、缺项状态和来源。登录、所有权或稿件选择不明确时会停止，不发布也不修改内容。

![YouTube 上传草稿检查推广图](assets/promo-1600x900.png)

## 安装

```bash
npx skills add xxjrq/youtube-upload-draft-check-free
```

## 使用

macOS（Apple 芯片）和 Windows 可按官网指南使用内置 Easy WebBridge 的 EasyBR；普通浏览器请按[官网 AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)配置独立 Bridge，源码见 [GitHub](https://github.com/aiispower/easy-webbridge) 或 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。提供唯一目标及明确 browserId；Skill 只在该环境创建自己的 session 分组，默认只读，不操作其他账号或已有页面。

离线资料可独立验证：

```bash
python3 scripts/check_draft.py fixtures/success-page.json
python3 scripts/self_test.py
```

fixtures 是离线页面资料模拟，验证本地清单逻辑，不代表在线采集。完整行为边界见 [SKILL.md](SKILL.md)。

## 许可与来源

MIT，见 [LICENSE](LICENSE)。业务主题参考与原创说明见 [SOURCES.md](SOURCES.md)。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
