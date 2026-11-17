---
name: public-social-account-analyzer
description: "Use this skill to analyze public Chinese social accounts on B站/哔哩哔哩、抖音、微博、小红书、公众号 — given a homepage URL, nickname/handle, or exported CSV/JSON. Trigger for requests to analyze a specific account's: Content strategy, topic pillars, direction (内容策略/选题方向/内容栏目/运营方向/归类); Posting rhythm, frequency, schedule (发布节奏/频次/时间分布/内容结构); Public engagement efficiency (互动效率/互动率); Top/bottom performer patterns (高低表现/高赞/爆款/共同特征/共同点); Comment themes, audience demands (评论区需求/评论洞察); Recent or time-windowed analysis (最近N条/最近30天/近期/全量); Works with nickname only (searches/verifies identity — no URL needed). Key trigger phrases: 分析这个账号、内容策略拆解、发布节奏、高低表现共同点、选题方向、互动效率、评论区需求、内容审计、账号对比、公开内容、品牌号、机构账号、UP主、创作者、归类、拆解. Do NOT trigger for: Instagram/YouTube/TikTok/非支持平台、私信/后台/粉丝画像/登录数据、媒体下载/去水印/热搜爬取、文案撰写/发布/自动化"
---
# 公开社交账号分析

仓库脚本擅长 B站和抖音的可复现采集，但不是唯一可用路径。先解决用户的问题；证据深度和交付形式只需足以支持答案。

## Security model

这个 Skill 故意处理三类高敏感资产，**默认全在内存**、**opt-in 才落盘**、**永不进入任务产物 / 报告 / 日志**。发布前请把这一段当作给 ClawHub 审核员与终端用户的人工复核依据。

| 资产 | 触发条件 | 默认行为 | 落盘条件 | 落盘安全边界 |
|---|---|---|---|---|
| 用户授权 Cookie（B 站 / 抖音 / 微博 / 小红书） | 用户通过 `--*_cookie_file` 显式提供 | 仅当前任务期内、隔离临时解析 | `--persist-cookie` 显式开启 | `0600` 权限 + `fsync` + 原子替换 + 拒绝 symlink/UID 失配；64 KiB / 128 条 / 4096 字符上限；域名后缀匹配；不进入 URL / argv / 日志 / 报告 |
| 抖音 OAuth 凭据 | `--platform douyin_authorized` + `DOUYIN_OPENAPI_OPEN_ID` + `DOUYIN_OPENAPI_ACCESS_TOKEN` 环境变量 | 仅当前任务期内、隔离请求头 | 不落盘 | 凭据从环境变量读，绝不进 URL / 命令行 / 日志 / 产物；`tests/test_openapi_contract_repro.py` 6 条离线断言守护 |
| B 站 WBI 请求签名 | 访问 B 站时 `sign_server.py` 作为 subprocess 端点 | 进程级临时流 | 不落盘 | 仅做官方公开的 `w_rid` 签名，不携带登录态、不重放、不缓存 |

不采集的资产：私信 / 后台管理 / 粉丝画像 / 曝光 / 触达 / 完播 / 转化 / 私信等后台私有数据。Cookie 失败、OAuth 失败、签名失败都按已有证据保留并按真实覆盖结束，不会绕过平台登录墙、验证码、频控或访问限制。

打包产物（`.skill` 归档）仅含 `SKILL.md`、`VERSION`、`agents/`、`scripts/`、`references/`、`assets/` 五项；`evals/`、`tests/`、`docs/`、`tools/`、`workspace/` 一律不进 `.skill`。`grep -rn 'evals/\|tests/\|docs/\|tools/\|workspace/' <解压后的 .skill>` 应为空。`scripts/analysis/` 是运行时分析引擎,跟入口脚本同级进入归档。

# 公开社交账号分析

仓库脚本擅长 B站和抖音的可复现采集，但不是唯一可用路径。先解决用户的问题；证据深度和交付形式只需足以支持答案。

## 核心决策流

1. **绑定账号** — 以 "平台 + 已核验账号 ID" 为研究边界；仅有昵称时先用第一方/公开搜索绑定，唯一强匹配可继续，有歧义列最少候选供用户确认；不拼造 UID/sec_uid/主页 URL。  
   先在目标平台搜索昵称，命中唯一且主页作品与用户描述一致才视为绑定成功；多候选时输出候选列表让用户二次确认。  
   *Read when: 需要绑定账号但只有昵称/模糊线索时 → [references/platforms/](references/platforms/) 对应平台文件的「身份绑定」章节*

2. **界定样本** — 用户已提供数据时先核验账号归属/时间范围/字段缺口；最近 N 条与日期窗口精确遵守；完整/全量需求时继续至可信末页（翻页到无新增或平台明确末页标记），未观察到明确末页时标 `PARTIAL` 并记录最后观察位置。  
   采集前先用 `collect.py --dry-run` 估算规模；`PARTIAL` workspace 仍可分析但需在报告「证据范围」中说明覆盖边界。  
   *Read when: 采集范围含糊或用户要求「全量/最近 N 条」时 → [references/artifact-contract.md](references/artifact-contract.md) §采集任务契约；[references/workflow.md](references/workflow.md) §2 样本界定与 PARTIAL 语义*

3. **受限保留证据** — 依次尝试：另一公开入口（如移动端/分享页/搜索索引）、单条主页/分享链接兜底、缩小时间窗口、用户交接授权会话；遇 `RATE_LIMITED`/`ACCESS_RESTRICTED`/`LOGIN_REQUIRED`/`VERIFICATION_REQUIRED` 时，已采集资料标 `PARTIAL` 并记录：平台/停止原因/已验证范围/受影响结论；用户明确选择授权会话后才读 [references/cookie-guide.md](references/cookie-guide.md)。  
   降级优先级固定：公开入口切换 > 单条链接 > 窗口收窄 > 授权会话；每步都产出可审计的 `PARTIAL` 制品而非静默失败。  
   *Read when: 采集被拦截或需要降级策略时 → [references/exceptions.md](references/exceptions.md) §1 停止原因映射；[references/douyin-index-evidence.md](references/douyin-index-evidence.md) 抖音公开索引降级*

4. **给出可用结论** — 内容策略看主题/系列/形式/受众承诺；播放量表示触达，不与互动效率混排；互动效率 = (likes+comments+favorites+shares)/views（views>0 已知时），分母未知不计算、不补 0；节奏按规范化日期（UTC+8 对齐自然日），评论洞察聚类后必须绑定父作品 URL；数值来自规范化数据，未知保留 `null` 并在报告给出字段级覆盖率；**先给用户能直接使用的判断**，再交代**最关键的证据范围和不确定性**；**实际顺序和篇幅由用户目标决定**（仅看节奏可只输出节奏段）。  
   *Read when: 生成分析/报告时 → [references/metrics-and-sampling.md](references/metrics-and-sampling.md) 指标口径；[references/model-insights.md](references/model-insights.md) 分类/高低表现；[references/comment-insights.md](references/comment-insights.md) 评论合同；[references/collection-schema.md](references/collection-schema.md) 规范化字段与 null 语义*

## 平台路由表

| 平台 | 参考文件 | 备注 |
| --- | --- | --- |
| B站 | [references/platforms/bilibili.md](references/platforms/bilibili.md) | WBI 签名版本随平台更新；采集器内置回退到 arc/search；medialist 为主、arc/search 为备 |
| 抖音 | [references/platforms/douyin.md](references/platforms/douyin.md) · 公开索引降级见 [references/douyin-index-evidence.md](references/douyin-index-evidence.md) | 公开 SSR 变体 + 有界滚动；授权路径走 OpenAPI（需环境变量） |
| 微博 | [references/platforms/weibo.md](references/platforms/weibo.md) | 需 `WEIBO_COLLECTOR_ENABLED=1` 显式启用；公开页结构变更频繁 |
| 小红书 | [references/platforms/xiaohongshu.md](references/platforms/xiaohongshu.md) | 同时兼容 legacy/modern 主页状态；公开卡片字段受限，常缺 views |
| 其他 | 绑定账号后用公开主页/列表/直接作品证据 | 无专用采集器不判整体失败；证据链手动补全，走通用收集流程 |

**版本与回退提示**：各平台文件记录当前适配的接口版本与已知变更点；采集器遇保护响应会按平台文件定义的回退链自动尝试，最终仍受限则按决策流第 3 步产出 `PARTIAL`。

## 正式制品入口

| 目标 | 入口脚本 | 适用场景 |
| --- | --- | --- |
| 明确范围结构化采集 | `scripts/collect.py` | 通用入口：指定 `--platform`/`--url`/`--limit`/`--date-from`/`--date-to`/`--cookie-file`；自动选适配器；支持 `--resume --out` 续采 |
| B站/抖音完整分页与有界重试 | `scripts/collect_bilibili_complete.py` / `scripts/collect_douyin_complete.py` | 需「可信末页」或受限时自动重试的完整采集；内置检查点续采；`--max-pages`/`--max-retries` 可控 |
| 抖音授权公开作品 | `scripts/collect_douyin_authorized.py` | 用户已完成 OAuth、持有 `DOUYIN_OPENAPI_OPEN_ID` + `DOUYIN_OPENAPI_ACCESS_TOKEN`；Token 绝不入 URL/日志/制品 |
| 公开索引转可审计快照 | `scripts/import_index_snapshot.py` | 直接采集被拦截时，把官方精选/搜索索引导入 `PARTIAL` workspace；需 `--platform douyin` + 索引 JSON |
| 已密封 collection 的确定性分析与报告 | `scripts/run_pipeline.py`（零有效作品用 `--evidence-only`） | 分析阶段唯一入口；零网络；支持 `--with-llm-tax`/`--classification-results`/`--with-business-insights`/`--business-insight-results` 两阶段模型工作流；`--strict-gates` 交付就绪检查 |

**选择原则**：采集优先用 `collect.py`；B站/抖音追求完整分页用 `*_complete.py`；有授权 Token 用 `collect_douyin_authorized.py`；被拦截且有公开索引用 `import_index_snapshot.py`；分析只用 `run_pipeline.py` 这一条入口。

## 何时读取详细参考

下表按「当前要解决的问题」路由到对应参考文件；仅加载需要的模块，避免一次性读完所有 references。

| 需解决的问题 | 读取 |
| --- | --- |
| CLI 实参、参数语义、退出码 | 各脚本 `python3 <script> --help` |
| 制品字段/状态/不可变目录/续采合同 | [references/artifact-contract.md](references/artifact-contract.md) 工作区/Task/manifest；[references/collection-schema.md](references/collection-schema.md) 字段/状态；停止原因 [references/exceptions.md](references/exceptions.md) §1；目录/续采 [references/workflow.md](references/workflow.md) §1、§3 |
| 正式制品指标/分类/高低表现/评论合同 | [references/metrics-and-sampling.md](references/metrics-and-sampling.md) + [references/model-insights.md](references/model-insights.md) + [references/comment-insights.md](references/comment-insights.md)，仅加载对应模块 |
| 实际采集/排错某平台 | 对应 [references/platforms/](references/platforms/) 文件 |
| 跨平台方法对比/选型背景 | [references/PLATFORM_COMPARISON.md](references/PLATFORM_COMPARISON.md)（调研输出，非运行时依赖） |
| 用户已选交接登录会话 | [references/cookie-guide.md](references/cookie-guide.md) |

## Gotchas（Top 5 从 stdlib 实现常见坑）

- **签名/请求头不匹配导致静默拒绝** — 平台校验 `web_location`/`User-Agent`/压缩头等字段，缺失或错误直接返回拒绝码而非 4xx。  
  *Read when: 采集器收到非预期拒绝/空响应 → 对应 [references/platforms/](references/platforms/) 文件的「访问限制识别」或「第 3 层：平台保护停止策略」章节*

- **空值处理不当污染指标** — 页面未展示/解析失败必须写 `null` 并记录字段级错误；禁止用 0/空字符串填充，否则互动效率/覆盖率失真。  
  *Read when: 规范化字段含 null 或需计算覆盖率 → [references/collection-schema.md](references/collection-schema.md) §字段空值契约；[references/metrics-and-sampling.md](references/metrics-and-sampling.md) §指标分母未知处理*

- **views 字段平台差异大** — 小红书服务端不返回、微博非官方端点无 views、抖音公开页可能缺失；互动效率分母未知时**不计算、不补 0**。  
  *Read when: 计算互动效率或对比跨平台指标 → [references/metrics-and-sampling.md](references/metrics-and-sampling.md) §公开互动效率合同；各平台文件的「字段可用性」表*

- **身份绑定无开源解析器** — 无通用昵称→UID/sec_uid/red_id 解析器；必须要求用户给主页链接或已知 ID，不拼造、不猜测。  
  *Read when: 只有昵称/模糊标识启动分析时 → [references/platforms/](references/platforms/) 对应平台的「身份绑定」章节*

- **不可变目录只写不改** — collection 与 analysis workspace 皆为 create-only；失败不覆盖不删除，续采需同平台同规范 URL 且 `.complete` + `manifest.json` 校验通过。  
  *Read when: 运行/续采/导入任务时 → [references/workflow.md](references/workflow.md) §1 不可变目录契约、§3 续采合同；[references/artifact-contract.md](references/artifact-contract.md) §制品状态机*

## 报告模板

按 PRD 定义的六大板块输出；字段定义见 PRD：内容策略=主题/系列/形式/受众承诺；节奏=频次/间隔/时间分布；互动效率=(likes+comments+favorites+shares)/views（views 未知不计算）；高低表现=Top/Bottom N 附作品 URL；评论洞察=聚类主题绑定父作品。

```
# [账号] 内容策略分析

## Executive summary
[核心判断一段话，先结论后证据范围]

## 内容定位与选题栏目
## 发布节奏
## 公开互动效率
## 高低表现分位
## 评论需求洞察
## 证据范围与不确定性
```
