---
name: youtube-video-metadata-localize-free
description: 使用用户指定的 Easy WebBridge 浏览器环境读取一个已授权的公开视频页面，为中文受众整理原题和简介要点，产出中文标题、简介草稿、逐条来源链接与缺项说明。适用于上线前本地化审阅；简介不可见或原主张含糊时保留原词，不改写后台内容。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；选择与本机系统匹配的当前版本。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# YouTube 公开视频元数据中文化

把一个**已授权、公开可见**的 YouTube 视频页面转为可审阅的中文元数据草稿：保留原始事实与来源，不改后台、不发布。

## 输入

- 一个公开视频 URL
- 中文受众或语言语气要求
- 用户明确指定的 Easy WebBridge `browserId`

单次只处理一个视频。章节、场景或短文超过单次可审阅范围时，先要求分批；表格最多 100 行。

## 交付结果

输出 JSON 或 Markdown，包含：

- 原题和可见简介要点（不是整段复制）
- 面向中文受众的标题与简介草稿
- 每条事实所对应的真实页面 URL
- `missing_items`：不可见简介、模糊主张、地区/术语不确定等缺项

不能读取的内容绝不补造；主张含糊时保留原词，并明确标注“待确认”。示例 fixture 是离线页面资料模拟，不能说成线上采集结果。

## 浏览器前置依赖

本 Skill 需要安装 **Easy WebBridge**。主下载地址：[GitHub](https://github.com/aiispower/easy-webbridge)；备用镜像：[Gitee](https://gitee.com/xxjrq/easy-webbridge)。安装扩展并连接目标浏览器后，用户提供 `browserId`。

## 只读执行流程

1. 先读取用户本机 Easy WebBridge CLI 的 `--help`，确认可用参数：

   ```bash
   node /path/to/easy-webbridge/cli/easy-webbridge.mjs --help
   ```

2. 精确使用用户提供的 `browserId`，为本次任务建立唯一 session：`youtube-video-metadata-localize-free-<run-id>`；不得广播到所有账号，不接管或关闭已有页面。
3. 只用该 session 打开目标 URL，先读取可见页面快照；显式使用 `--text-mode page`，每次导航、展开简介或刷新后重新获取 refs。

   ```bash
   node /path/to/easy-webbridge/cli/easy-webbridge.mjs navigate <browserId> <video-url> --new-tab --session youtube-video-metadata-localize-free-<run-id> --group-title "YouTube 元数据中文化"
   node /path/to/easy-webbridge/cli/easy-webbridge.mjs snapshot <browserId> <tab-id> --text-mode page
   ```

4. 仅提取网页**可见**的标题、简介、频道/发布日期等必要上下文和当前 URL。遇到登录、验证码、风控或权限墙，立即暂停；不绕过。若简介不可见，继续用可见原题生成有限草稿，在 `missing_items` 标注“简介不可见”，且绝不推断或补写简介内容。
5. Agent先按可见原题与每条简介原文生成通用中文译文：依据中文受众调整术语解释、句式与阅读难度，但不改变事实、条件或主张强度。为每条译文保留对应原文、编号和页面URL；标题或简介中出现的品牌、产品名、未证实术语和不明确主张保留原词并按 `title` 或 `description_points[n]` 标来源、列待确认。不得因受众不同增加能力、结果、承诺或背景。简介不可见只译标题，不生成简介。翻译是Agent的语言工作，脚本没有通用翻译能力。
6. 将原可见资料和Agent译文分别交给 `scripts/compose-draft.mjs` 校验、组装。脚本检查原文逐项匹配、受众、来源和缺项；不能代替语义审核，Agent仍须对照原文逐条确认忠实。
7. 默认只读。若用户明确授权“填入草稿”，可填入草稿字段，但绝不点击最终发布、保存、发送或提交。结束时只关闭本任务自己创建的 session，并先核对其所有权。

## 离线整理器

浏览器读取与离线整理分开验证。整理器接受已从可见页面摘出的 JSON，不连接网页：

```bash
node scripts/compose-draft.mjs --input fixtures/success-page.json --translations fixtures/success-translations.json --output /tmp/localized.json
node scripts/self-test.mjs
```

输入的 `source_url` 必须是 `http` 或 `https` URL；`title` 必填。`unresolved_terms` 可引用可见标题或可见的简介要点；标题术语必须实际出现在标题，简介术语必须实际出现在对应可见条目。`description_visible: false` 或不确定主张会进入 `missing_items`。


### Agent译文合同

译文JSON包含 `chinese_audience`（与输入一致）、`audience_adaptation`（解释措辞如何适配）、`title` 和 `points`。标题为 `{original, chinese, source_url, source_field:"title"}`；每个简介要点为 `{index, original, chinese, source_url, source_field:"description_points[0]"}`，编号从0递增、逐项匹配原始可见输入。简介不可见时 `points:[]`，不可沿用不可见文本。脚本拒绝漏项、额外要点、错原文或错来源，不能判断译文语义是否忠实，必须由Agent复核。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
