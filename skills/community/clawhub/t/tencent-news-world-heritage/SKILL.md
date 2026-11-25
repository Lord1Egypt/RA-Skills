---
name: tencent-news-world-heritage
display_name: 文遗云图·知识库
display_name_en: Tencent News World Heritage
description: 读懂世界遗产的随身顾问，覆盖世界文化遗产、自然遗产、文化与自然双重遗产的遗产地、名录申报、历史背景、价值特色、保护修缮与最新动态。当用户询问某个世界遗产地是什么、在哪里、何时列入名录、有什么价值、近期有什么保护或修缮动态时使用。
description_zh: 读懂世界遗产的随身顾问，覆盖世界文化遗产、自然遗产、文化与自然双重遗产的遗产地、名录申报、历史背景、价值特色、保护修缮与最新动态。当用户询问某个世界遗产地是什么、在哪里、何时列入名录、有什么价值、近期有什么保护或修缮动态时使用。
description_en: World Heritage knowledge base Q&A covering heritage sites, inscription, history, values, conservation and recent updates.
version: 1.0.7
examples_zh: ["中国世界遗产中哪些是自然遗产？", "世界遗产的申报需要哪些材料？", "世界遗产的申报流程是怎样的？"]
examples_en: []
shared_resources: ["tencent-news-cli"]
author: shasha
tags: [tencent, news, world heritage, cultural heritage, wiyun, knowledge base]
---

# 文遗云图·知识库 / Tencent News World Heritage

通过 `tencent-news-cli` 的 `wiyun` 能力，调用星辰后台「文遗云图·知识库」智能体（`UTR2026063018255100`）完成世界遗产知识库问答：

1. 先检查当前 CLI 与 API Key 状态；环境未就绪时完成诊断与恢复指引。
2. 环境就绪后，通过 `run-cli` 执行 `wiyun`，把用户的问题传入。
3. 成功时**原样展示 CLI 返回的正文**；失败或空结果时保留明确失败状态，不编造内容。

> **核心原则**：基础设施交给脚本处理；智能体只负责判断意图、构造查询和展示结果。**除 `cli-state` 外，所有 CLI 调用都通过 `run-cli` 执行；不要手动传 `--caller`；答案内容以 CLI 返回为准，不用模型记忆补充或改写。**

## 平台约定

| 平台 | 脚本运行方式 | 示例 |
|------|------------|------|
| macOS / Linux | `sh scripts/<name>.sh` | `sh scripts/cli-state.sh status` |
| Windows | `powershell scripts/<name>.ps1` | `powershell scripts/cli-state.ps1 status` |

以下所有脚本调用均以 macOS / Linux 为例，Windows 将 `.sh` 替换为 `.ps1`，`sh` 替换为 `powershell`。

除 `cli-state` 外，所有 CLI 命令都通过 `run-cli` 脚本执行：

| 平台 | CLI 调用模板 |
|------|-------------|
| macOS / Linux | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/run-cli.ps1 <command> [args]` |

## Phase 1：环境就绪与失败处理

**执行业务前必须读取并遵守 [CLI 环境与失败处理](references/cli-environment.md)**，完成状态检查、安装/更新、shell 配置核实与脱敏恢复。它是环境处理的统一入口；不要重新实现 Key 检测或读取明文 Key。环境失败优先于下文业务输出格式及通用错误话术；本轮无法恢复时返回其中的结构化「环境失败结果」，不得用其他数据源补结果。

本 Skill 的失败结果 `capability` 填 `world-heritage`；`query` 使用脱敏后的实际问题。环境就绪后继续下方业务流程。

## Phase 2：意图识别与查询构造

1. **判断是否属于本 Skill**：世界遗产地（文化遗产 / 自然遗产 / 文化与自然双重遗产）的介绍、位置、列入名录时间、历史沿革、建筑与艺术价值、保护修缮与近期动态，以及「XX 是不是世界遗产」「我国有哪些世界遗产」这类问题。**明显与遗产无关的通用问答不走本 Skill**，不调用 `wiyun`。
2. **构造查询**：优先保留用户的自然问法，直接作为 `--query` 传入；补充遗产地的标准名称或常用别名（如「布达拉宫」/「Potala Palace」）以避免歧义。
3. **拆分与预算**：复合问题拆成多个子问题分别查询，同一次提问合计调用不超过 3 次。预算不足时说明未覆盖的子问题，不声称全部查过。
4. **不做的事**：不自行改写、摘要或补充 CLI 未返回的内容；不用模型记忆回答遗产事实。

## Phase 3：执行查询

> `wiyun` 的参数和输出可能随 CLI 版本变化。**以当前 `help wiyun` 输出为准，不凭记忆组装命令。**

1. 每个会话首次查询前执行 `sh scripts/run-cli.sh help wiyun`，确认参数名、必填项与输出格式；确认后不再重复读帮助。
2. 组装并执行查询：

   ```sh
   sh scripts/run-cli.sh wiyun --query "<用户问题或改写后的检索问句>"
   ```

   - 默认 `text` 输出包含回答正文，末尾可能附带独立的 `traceid` 诊断行；按 Phase 4 剥离该尾行后展示正文。
   - 需要结构化字段（如 `session_id`、`model`）时用 `--format json`，正文取 `choices[0].delta.content`。
3. 若当前 CLI 帮助中没有 `wiyun`，按 Phase 1 的共享环境流程更新后重新检查；更新后仍不支持时，直接说明「当前 CLI 构建未提供本 skill 所需的文遗云图能力」并停止，**不得改用其他命令、WebSearch 或模型记忆作答**。

## Phase 4：输出结果

- 最终回复中不得出现任何与「新闻妹」有关的招呼、自我介绍、身份宣传、引导、落款或其他文案，也不得自行添加。展示前清理 CLI 正文中的相关文案，不限于开头：包括「您好！我是新闻妹~」「你好呀！我是新闻妹～」「我是新闻妹」、带「【】」的包装，以及空白、换行、中英文标点和半角/全角波浪号变体；移除完整的相关短句或独立段落及其专属包装。若相关文案与实质回答在同一行，仅移除相关短句，保留同一行其后的遗产知识、列表、表格和来源链接；不因一句招呼而删除整行答案。清理后再次检查全文，若仍有「新闻妹」相关文字，继续移除相关片段，直至不再出现。此规则同时适用于 text 输出和 JSON 中提取的正文。
- 除上述角色相关文案外，展示前只剥离 CLI 输出末尾独立的 `traceid` 诊断行（字段名为 `traceid`，后接 `:` 或 `：` 与追踪标识，可有行首尾空白；定位末行时忽略尾部空白行）。该行属于 CLI 诊断信息，不是回答正文，不向用户展示。没有符合条件的尾行时保留原文；不得删除正文中提及 traceid 的句子、代码块中的内容或非末尾行。JSON 模式只取 `choices[0].delta.content`，不展示响应元数据；若正文含同样的末尾诊断行，按同一规则处理。
- 将移除角色相关文案与末尾诊断行后的正文**原样作为最终答复主体**直接展示，不重新组织、摘要、改写或转述成另一版答案。
- 不自行补充外部信息、不伪造来源链接；确实需要补充一句说明时，只能放在正文之后，且不能替代正文。
- 清理角色相关文案与末尾诊断行后正文为空，或执行失败时，按下方「CLI 执行失败处理」处理，不生成兜底答案。

## CLI 执行失败处理

1. CLI 返回非零退出码、超时或权限/安全错误时，立即停止，不重试、不换命令、不使用 WebSearch 或其他数据源。
2. 按错误信息区分处理：
   - 缺少 `--query`（帮助中明确提示「缺少必填参数」）：补齐查询内容后，**仅在用户重新发起提问时**再调用，不当场猜测用户意图反复调用。
   - 环境问题（未安装、Key 缺失/无效、鉴权失败）：按 Phase 1 返回结构化「环境失败结果」与恢复步骤。
   - 其他未知错误：用自然语言说明本次查询未能完成，请用户稍后重试；只保留脱敏后的错误类别，不展示原始报错或 traceid。
3. 智能体成功返回但内容与问题无关时，如实说明未查到对应内容，不推断「不存在」或「未收录」。

## 能力边界

- 只做世界遗产知识库问答；**不做真假判定 / 谣言识别**（属于较真查证），**不做通用新闻搜索**（属于腾讯新闻搜索）。
- 回答由智能体基于知识库生成，不等同于联合国教科文组织或遗产地管理机构的官方口径；用户需要权威依据时，建议以官方渠道核实。
- 不提供订阅、定时检查或主动推送。

## References

- CLI 接入与调用契约：[`references/cli-integration.md`](references/cli-integration.md)
- 用户手动安装指南：[`references/installation-guide.md`](references/installation-guide.md)
- 用户手动更新指南：[`references/update-guide.md`](references/update-guide.md)
- API Key 获取与手动配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
- 打包自检与沙箱准备：[`references/packaging.md`](references/packaging.md)
