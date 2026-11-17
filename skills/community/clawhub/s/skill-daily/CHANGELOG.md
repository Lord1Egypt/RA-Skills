# Changelog

All notable changes to **clawhub-daily** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.8] - 2026-07-12

### Fixed (修复)
- **Tp4 MCP Tool Poisoning (High)**：description 未披露 IMA 的 CLI 调用方式（方式 B）和 Obsidian saved/ fallback 路径。description 现已明确披露：① IMA auto 模式可能调用 ima-skill CLI ② Obsidian vault 不可写时 fallback 到 saved/ 目录。
- **Lp3 MCP Least Privilege (Medium)**：SkillHub zip 打包排除了 .claude-plugin/ 目录，SkillSpector 看不到 capabilities 声明。SKILL.md description 新增"🔐 权限声明"区块，覆盖 network/filesystem/env_vars/subprocess 四类权限，与 plugin.json 的 capabilities 保持一致。
- **Scope Creep (Medium)**：push_to_obsidian.py 的 saved/ fallback 目录未在文档中披露。现已写入 description 的数据出口说明和 filesystem 权限声明。
- **Intent-Code Divergence (Medium)**：SKILL.md 声明"不读取 GH_TOKEN"，但 PUBLISHING_GUIDE.md 讨论 GH_TOKEN 使用。PUBLISHING_GUIDE.md 顶部新增"⚠️ 维护者文档说明"，明确 GH_TOKEN 仅用于维护者发布，技能运行时不读取。

### Changed (变更)
- plugin.json capabilities 增强：① 修正 IMA endpoint（ima.tencent.com → ima.qq.com）② filesystem paths 新增 inbox/clawhub-daily/ 和 saved/ ③ env_vars 新增 OBSIDIAN_VAULT_PATH ④ 新增 subprocess 权限声明（ima-skill CLI）
- SKILL.md "不读取 GH_TOKEN" 声明补充上下文："运行时不读取（GH_TOKEN 仅用于维护者发布新版本，见 docs/PUBLISHING_GUIDE.md）"
- Vague Triggers (Medium, 72%) **不修复**：触发词"每日推荐"和"ClawHub 日报"已足够明确（含品牌词或核心功能描述），72% confidence 属于边缘判断。再删触发词会导致技能无法正常触发。

## [2.0.7] - 2026-07-12

### Fixed (修复)
- **Tp4 MCP Tool Poisoning (High)**：description 中 IMA 渠道说明从"默认关闭，需显式启用"修正为"有凭证时自动推送，无凭证时跳过"，准确反映 executor 实际行为（executor 会尝试所有渠道，有凭证则推送，无凭证则跳过）。
- **Vague Triggers (Medium)**：删除宽泛触发词"今天有什么好 Skill"，替换为专用触发词"ClawHub 每日洞察"。从 SKILL.md / plugin.json / setup-wizard.md 三个文件同步清理。
- **Missing User Warnings - 凭证安全 (Medium)**：setup-wizard.md 飞书凭证配置部分新增"⚠️ 凭证安全须知"区块，包含存储/轮换/权限最小化/ClawHub publish 不遵守 .gitignore 等 5 项安全指导。
- **Missing User Warnings - 测试推送 (Medium)**：setup-wizard.md 测试运行步骤前新增"⚠️ 数据推送警告"，明确标注步骤 4-6 是外部传输，步骤 1-3 是本地操作。每个命令标注是否涉及外部传输。
- **Intent-Code Divergence (Low)**：PUBLISHING_GUIDE.md 的 grep 凭证扫描命令新增 GitHub token 全部前缀（gho_/ghs_）和 SkillHub token（skh_），消除"GH_TOKEN 讨论但 grep 不覆盖"的分歧。

### Changed (变更)
- SKILL.md description 新增"推送行为"说明行，明确 executor 的独立 try/except 失败隔离机制。
- setup-wizard.md 测试步骤从 4 步扩展到 6 步（新增 IMA 推送和 Obsidian 推送）。

## [2.0.6] - 2026-07-12

### Added (新增)
- **新增 Obsidian 本地 vault 推送渠道**：参考 web-to-fim 技能的三处存放架构，新增 `scripts/push_to_obsidian.py`，将每日简报推送到 Obsidian vault 的 `inbox/clawhub-daily/` 子目录。
- **三级 fallback 机制**：Obsidian 写入失败时自动降级（重试3次 → ASCII文件名 → 脚本目录 saved/），确保本地存储永不丢失。
- **executor 失败隔离**：推送阶段三个渠道（飞书/IMA/Obsidian）各自独立 try/except，一处失败不阻断其他渠道，参考 web-to-fim 的 `_process_single` 架构。
- **推送汇总报告**：executor 执行结束后输出三渠道推送结果汇总（`飞书=✓ | IMA=✓ | Obsidian=✓`）。

### Changed (变更)
- `clawhub_daily_executor.py` 推送阶段重构：Step 4-6 三处存放独立 try/except + 推送汇总。
- SKILL.md 数据出口说明新增 Obsidian 渠道。
- 凭证来源说明新增 OBSIDIAN_VAULT_PATH 环境变量。

## [2.0.5] - 2026-07-12

### Removed (移除)
- **删除方式 C（自定义 HTTP API）整个函数**：`push_via_api()` 函数将凭证发送到用户配置的 HTTPS 端点，被 SkillSpector 标记为 Critical（Tainted flow: credential → network output）。方式 C 已不再需要，方式 A（官方 OpenAPI）已完全覆盖 IMA 推送需求。
- **删除 fallback 环境变量 `IMA_CLIENT_ID`/`IMA_API_KEY`**：只保留官方变量 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`，消除"未文档化的凭证来源"（Scope Creep finding）。
- **删除 `--api-endpoint` 参数和 `--mode api` 选项**：方式 C 已删除，不再需要。
- **删除触发词 "扫描 ClawHub"**：SkillSpector 标记为 Vague Triggers（语义接近普通扫描请求，易误激活）。触发词从 4 个缩减为 3 个。

### Fixed (修复)
- **触发词残留清理**：`references/setup-wizard.md` 中的 "帮我推荐技能" 和 "扫描 ClawHub" 在 v2.0.3 漏改，本次彻底清理。
- **README summary 行**：删除"自动推送飞书"措辞，新增"⚠️ 数据出口说明"警告区块，明确告知外部传输行为。

### Changed (变更)
- `push_to_ima.py` 重写：删除 `push_via_api()` 函数、`--api-endpoint` 参数、`--mode api` 选项、fallback 环境变量。代码从 308 行精简到 262 行。
- auto 模式优先级简化：官方 OpenAPI > CLI（删除了"自定义 HTTP API"这一级）。
- SKILL.md IMA 推送说明：删除 fallback 变量说明。

## [2.0.4] - 2026-07-12

### Added (新增)
- **IMA 官方 OpenAPI 推送方式（方式 A，推荐）**：`push_to_ima.py` 新增 `push_via_official_api()` 函数，通过两步流程推送简报到 IMA 知识库
  - Step 1: `POST /openapi/note/v1/import_doc` 创建笔记（Markdown 格式，content_format=1）
  - Step 2: `POST /openapi/wiki/v1/add_knowledge` 添加到知识库（media_type=11，knowledge_base_id）
  - 默认推送到 FIM 知识库（ID: `aFEGG-4YH3z_CaCSNVNC5dSJR5cutjlatcEQcNZjtlA=`）
  - API 端点：`https://ima.qq.com`（注意：不是 `ima.tencent.com`）

### Changed (变更)
- **凭证优先级扩展**：CLI 参数 > 环境变量（`IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`，fallback `IMA_CLIENT_ID`/`IMA_API_KEY`）> config.json
- **auto 模式优先级调整**：官方 OpenAPI > CLI > 自定义 HTTP API（之前是 CLI > HTTP API）
- **kb_id 读取逻辑**：过滤 config.json 中的占位符（`<your_ima_kb_id>`），自动回退到 FIM 默认值
- **SKILL.md IMA 推送说明更新**：文档化官方 OpenAPI 两步流程和凭证来源
- **`--mode` 参数新增 `official` 选项**：可指定只用官方 OpenAPI 推送

### Fixed (修复)
- **IMA API 端点错误**：从 `https://ima.tencent.com` 改为 `https://ima.qq.com`（前者返回 401 skill auth failed）
- **import_doc payload 格式错误**：`content_format` 从字符串 `"markdown"` 改为数字 `1`；移除 `title` 字段（IMA 从 content H1 提取标题）
- **add_knowledge payload 字段名错误**：`kb_id` 改为 `knowledge_base_id`；新增 `title` 字段
- **响应解析逻辑**：检查 `code` 字段是否为 0（IMA API 返回 `{"code":0, "data":{...}}`）

## [2.0.3] - 2026-07-12

### Fixed (修复)
- **MCP Least Privilege (Lp3, Medium)**：plugin.json 新增 `capabilities` 字段，声明 network/filesystem/env_vars 三类权限及其用途，消除"未声明权限"的透明度缺口
- **Vague Triggers (Medium)**：删除宽泛触发词 "帮我推荐技能"（可能在普通对话中误激活），保留 4 个含 "ClawHub"/"每日" 限定词的专用触发词

### Added (新增)
- **SKILL.md 新增"🔐 权限声明"区块**：以表格形式列出 network/filesystem/env_vars 三类权限的必需性和说明，并明确声明"不申请 shell 执行、系统信息收集、GH_TOKEN 读取"等权限

### Changed (变更)
- plugin.json `triggers` 数组从 5 项缩减为 4 项
- plugin.json `capabilities` 字段声明所有运行时权限，供宿主平台和用户审查

## [2.0.2] - 2026-07-12

### Fixed (修复)
- **凭证泄露修复（Critical）**：删除 `references/config.local.json`（包含真实飞书凭证，被 ClawHub publish 上传）。该文件虽在 `.gitignore` 中（未进 GitHub），但 ClawHub publish 发布整个目录。已删除文件，用户需在本地重建配置并轮换已泄露的飞书凭证
- **Env Variable Harvesting (High)**：删除临时脚本 `_check_github.py`（包含 `os.environ.get("GH_TOKEN")`，与技能功能无关）
- **MCP Tool Poisoning (Tp4, High)**：删除 `publish_all.ps1`（开发工具，包含 GH_TOKEN 环境变量读取，不属于技能运行时代码）
- **Description-Behavior Mismatch**：description 只说 config.json 读取凭证，但 push_to_feishu.py 还接受 FEISHU_APP_ID 等环境变量。description 现在明确披露凭证来源优先级：CLI 参数 > 环境变量 > config.json

### Changed (变更)
- **description 新增"凭证来源"段落**：披露飞书/IMA 凭证的环境变量名称，并明确声明"不读取 GH_TOKEN、GITHUB_TOKEN 或其他与推荐功能无关的环境变量"
- **SKILL.md 安全约束更新**：添加 config.local.json 在 .gitignore 中的说明，添加不读取 GH_TOKEN 的声明
- **prompt-templates.md 添加数据推送知情说明**：Cron 模板顶部新增"⚠️ 数据推送知情说明"区块，说明数据流向和凭证要求

### Removed (移除)
- `_check_github.py`：临时调试脚本，不属于技能代码
- `publish_all.ps1`：开发工具脚本，不属于技能运行时代码
- `references/config.local.json`：包含真实凭证，不应发布

## [2.0.1] - 2026-07-11

### Fixed (修复)
- **Description-Behavior Mismatch**：description 只披露飞书推送，未说明 IMA 知识库和本地文件两个数据出口。现在 description 明确列出三个推送渠道及其默认状态（SkillSpector findings 修复）
- **Missing User Warnings**：缺少数据推送知情说明。新增"⚠️ 数据推送知情说明"区块，列出所有推送渠道、所需凭证和数据内容，以及安全约束
- **MCP Tool Poisoning (Tp4)**：push_to_ima.py 的 push_via_api 未验证端点协议，可能通过 HTTP 明文传输 client_id/api_key。新增 HTTPS 强制校验，拒绝 HTTP 端点

### Changed (变更)
- **frontmatter description 扩展**：增加"数据出口说明（用户知情同意）"段落，披露飞书/IMA/本地文件三个渠道
- **SKILL.md 结构调整**：新增"⚠️ 数据推送知情说明"区块，含推送渠道表格和安全约束列表
- **飞书/IMA 消息结构标题**：标注"默认推送渠道"和"可选渠道，需显式配置"
- **核心能力描述**：从"飞书推送"改为"多渠道推送"，列出全部 4 个渠道

## [2.0.0] - 2026-07-11

### Changed (变更)
- **抓取范围扩大 200→500**：ClawHub 平台已有 67.9K Skills，200 个仅占 0.3%，扩大到 500 翻倍候选池
- **推荐模式从 4 维度扩展到 6 维度**：新增 actively_maintained 和 verified 两个维度
- **维度配额调整**：trending×3 + quality×1 + newcomers×1 + panorama×2 + actively_maintained×1 + verified×0/1 = 每日 8 个
- **actively_maintained 阈值放宽**：主阈值从 30 天→90 天，新增 fallback 180 天+版本≥2
- **verified 标记为 optional**：候选为 0 时自动跳过，不占配额
- **数据说明文案更新**：Markdown 和飞书 blocks 都反映 6 维度新配置
- **SOLO Schedule 提示词更新**：8 个推荐、6 维度、新阈值、痛点去重、changelog 展示

### Added (新增)
- **适配 ClawHub API 数据结构变更**：`stats.installs`（非 `installsCurrent`）、`categories`（非 `capabilityTags`）、`badges.verified`、`latestVersion.changelog` 等嵌套字段
- **降级策略（fallback_fn）**：每个维度配置降级过滤函数，候选不足时自动放宽阈值
- **optional 维度机制**：候选为 0 的维度自动跳过，不占配额
- **痛点匹配去重展示**：同一 Skill 只在第一个命中场景展示（按权重排序）
- **changelog 展示**：有最近变更摘要的 Skill 在详情中展示"最近变更"字段
- **compute_metrics.py 新增 10+ 字段**：version_count、days_since_update、is_actively_maintained、update_frequency、changelog_summary、supported_os、setup_requirements、is_verified、license
- **safe_get() 函数**：安全获取嵌套字段，适配新旧 API 结构

### Fixed (修复)
- **维度遍历遗漏**：generate_markdown() 和 generate_feishu_blocks() 中硬编码的维度列表未包含 actively_maintained 和 verified，导致推荐生成了但不展示（Critical bug）
- **push_to_feishu.py 同类 bug**：飞书卡片 highlights 遍历也遗漏新维度
- **changelog 换行符破坏格式**：API 返回的 changelog 含 \n，嵌入 Markdown 前替换为空格
- **actively_maintained 推荐理由过时**：从"30天内更新"改为"近期更新（N天前）"

## [1.0.4] - 2026-06-05

### Changed (变更)
- **推荐模式从 4 天轮换改为每日全维度**：每天遍历全部 4 个维度，用户每天都能看到所有维度推荐
- 维度配额调整：trending×2 + quality×1 + newcomers×1 + panorama×2 = 每日 6 个
- 去重窗口从 10 天缩短到 7 天（7×6=42 个去重池）
- 飞书卡片消息扩展到 Top 5 简介 + 底部云文档直达链接
- 飞书卡片按维度分组展示，含维度概况统计

### Fixed (修复)
- 云文档/Markdown 中 Skill 链接改为可点击格式（`[text](url)` 和 `text_element_style.link`）
- 飞书云文档 blocks 中 Skill 标题添加超链接，可直接点击跳转

## [1.0.3] - 2026-06-05

### Fixed (修复)
- D4 全景维度 min_comments 从 50 降为 1，避免候选池过小
- deduplicated 字段语义修正：现在正确统计因去重被跳过的候选数
- 痛点关键词匹配改用词边界正则，避免子串误匹配（如 "ci" 匹配到金融 Skill）

## [1.0.0] - 2026-06-03

### Added (新增)

- 🎯 **首次安装模式选择**（`references/setup-wizard.md`）
  - 模式 A：常规对话模式（手动触发）
  - 模式 B：Cron 定时任务模式（自动推送）
- ⏰ **Cron 提示词模板**（`references/prompt-templates.md`）
  - Trae SOLO / qclaw / WorkBuddy / OpenClaw / Hermes / crontab / Windows Task Scheduler 全平台覆盖
  - 5 个开箱即用模板 + 痛点列表定制指南
- 🌍 **7 大痛点库**：🤖 自动化办公 / 🛠️ 开发工具 / ✍️ 内容创作 / 🕷️ 数据采集 / 🧠 AI 增强 / 🇨🇳 中文支持 / 💰 金融分析
- 📊 **4 维度轮换**：trending / quality / newcomers / panorama（按 `日期 % 4` 自动选）
- 🆔 **本地 JSON 去重**：10 天滚动窗口，0 数据库依赖
- 📥 **200 Skill 大池子抓取**：Convex API，0 token 消耗
- 📝 **简报中文化**：`chinese_one_liner` 自动拼装 + 英文 `<details>` 折叠
- 📤 **多通道推送**：
  - 飞书云文档 + 卡片消息（200-400 字摘要 + Top 3 详细解读）
  - IMA 知识库推送（`scripts/push_to_ima.py`，CLI 优先 + HTTP API 备选）
  - 本地 Markdown 简报（默认开启）
- 🔌 **`.claude-plugin/plugin.json`**：ClawHub 发布支持（**MIT-0 许可证**）
- 📜 **MIT-0 License**（`LICENSE`）— ClawHub 强制要求
- 📚 **`docs/CONTRIBUTING.md`** + **`docs/PUBLISHING_GUIDE.md`**：发布/贡献完整指南
- 🔐 **凭证管理**：`references/config.json` 模板（用户自填，不入库，支持飞书 + IMA 双渠道）

### Security (安全)

- 🔒 **移除硬编码凭证**：所有 `app_id` / `app_secret` / `user_open_id` 改为用户配置
- 🔒 **`.gitignore`**：忽略 `references/config.json`、`data/snapshots/*.json` 等运行时数据

### Documentation (文档)

- 📚 完整的 `README.md`（中英双语）
- 📚 `references/api-contract.md`（Convex API 契约）
- 📚 `references/source-data-schema.md`（数据字段说明）
- 📚 `references/pain-points.md`（痛点库维护指南）
- 📚 `references/briefing-template.md`（简报模板）

## [Unreleased]

### Planned

- 飞书 WebSocket 长连接（替代轮询）
- 多语言支持（英文 / 日文简报）
- 智能体推荐理由（基于 Skill 描述自动生成更精准的中文解读）
- Telegram / Slack / 企微 推送支持
- Skill 评分系统（基于用户安装/卸载行为）

---

## 版本号规则

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向下兼容的新功能
- **PATCH**：向下兼容的 bug 修复

## 链接

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
