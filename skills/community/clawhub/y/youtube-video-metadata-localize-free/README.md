# YouTube 公开视频元数据中文化

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；选择与本机系统匹配的当前版本。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把一个已授权、公开可见的 YouTube 视频页面整理成适合中文受众审阅的标题与简介草稿。输入是**一个公开视频 URL、中文受众要求和指定 browserId**；结果包括原题/简介要点、中文标题/简介草稿、真实来源链接与明确缺项。默认只读，不修改 YouTube 后台。

![推广图](assets/promo.png)

## 适用场景

上线前审阅公开视频的中文元数据；当简介读不到或主张不清晰时，Skill 保留原词并标注待确认，而不是编造内容。

## 安装与使用

```bash
npx skills add xxjrq/youtube-video-metadata-localize-free
```

这是浏览器 Skill。macOS（Apple 芯片）和 Windows 可按官网指南使用内置 Easy WebBridge 的 EasyBR；普通浏览器请按[官网 AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)配置独立 Bridge，源码见 [GitHub](https://github.com/aiispower/easy-webbridge) 或 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。每次运行使用指定的 `browserId`，只管理自己的 session 和标签组。

完整工作流、只读边界和离线整理器见 [SKILL.md](SKILL.md)。可独立验收：

```bash
node scripts/self-test.mjs
```

## 翻译与组装

Agent根据原页面可见文字执行中文翻译，按受众调整术语解释与句式，原文事实保持一致。脚本只校验/组装Agent译文，要求每条保留原文、编号、来源URL与字段，不提供本地自动通用翻译。不可见简介不译，模糊术语保留原词并列待确认。译文语义仍由Agent对照原文复核。

```bash
node scripts/compose-draft.mjs --input fixtures/success-page.json --translations fixtures/success-translations.json --output /tmp/localized.json
```

独立骑行材料示例：[入门受众输入](fixtures/new-input-beginner.json) → [实际中文交付](fixtures/forward-beginner.json)；[熟悉装备的受众输入](fixtures/new-input-experienced.json) → [实际交付](fixtures/forward-experienced.json)。两版事实相同，前者用日常词，后者保留Bikepacking术语。[简介不可见输入](fixtures/new-input-failure.json) → [限制交付](fixtures/forward-failure.json)。实际结果由Agent先写译文，再真实运行组装脚本生成。

fixtures 是离线文字材料，示例视频地址未在线访问，不代表已跑通浏览器工作流。自检校验两受众组装、逐项来源、不可见简介及四种错误合同拒绝；不代替真实翻译语义验收。

## 来源与许可

业务用途参考了 [social-media-skills/skills](https://github.com/social-media-skills/skills) 中的 YouTube 元数据主题；本仓库的说明、流程和代码为原创实现，未复制其文本或源码。见 [LICENSE](LICENSE)。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
