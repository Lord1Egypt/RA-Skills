---
name: "tech-research"
description: "技术调研智能体：单点/并行调研、每周技术雷达；检索 Dify 知识库与网络资料，输出结构化调研报告"
user-invocable: true
allowed-tools:
  - web_search
  - web_fetch
  - sessions_spawn
  - sessions_yield
  - write
  - read
  - exec
  - memory_search
  - cron
---

# 技术调研智能体

面向云手机研发的技术调研 Skill，支持单点深度调研和多点并行调研，输出结构化 Markdown 报告。

## 触发场景

用户提到以下关键词时触发：
- "调研"、"技术调研"、"技术预研"、"技术选型"
- "查一下XX技术"、"对比一下XX方案"
- "技术雷达"、"技术动态"

## 工作流程

### 模式一：单点深度调研

当用户要求调研**单个技术点**时：

1. **明确调研目标**
   - 提取用户的核心问题（如"WebRTC QoS降档方案"）
   - 拆分为 2-3 个子问题（现状、方案对比、落地建议）

2. **检索知识库（只读）**
   - 定位 dify-rag skill 安装目录（默认 `skills/dify-rag/`，相对 workspace；不确定时先确认实际路径），执行其检索脚本：
     ```bash
     python <dify-rag安装目录>/scripts/search.py --query "<调研关键词>" --top-k 5
     ```
   - 结果解析：内容取 `records[].segment.content`，来源文档名取 `records[].segment.document.name`
   - 提取历史方案、术语规范、架构文档作为调研起点
   - Dify 不可用或未配置时，降级到本地 `memory_search`，并在报告中注明来源

3. **多维度检索**
   - 用 `web_search` 搜索中英文资料（各 3-5 条）
   - 用 `web_fetch` 抓取高质量页面内容
   - 优先选择：官方文档、技术博客、GitHub README、论文

4. **整理报告**
   - 按模板结构输出（见 `scripts/report_template.md`，即 `{baseDir}/scripts/report_template.md`），检索方法论见 `{baseDir}/references/research_guide.md`
   - 包含：背景、技术原理、方案对比、优缺点、落地建议、参考资料

5. **归档（仅本地）**
   - 保存到 `memory/research/`，文件名：`YYYY-MM-DD-<关键词>.md`
   - 更新 `memory/research/INDEX.md` 索引
   - **不自动上传 Dify 知识库**：知识库内容由用户在 Dify 控制台自行管理；如需入库，提醒用户手动上传

### 模式二：多点并行调研

当用户要求调研**多个技术点**时：

1. **拆分任务**：拆为 2-4 个独立子调研，每个明确关键词、检索方向、预期产出
2. **并行启动子 Agent**：用 `sessions_spawn` 为每个子调研启动一个子 Agent，任务描述包含调研关键词、需回答的子问题（2-3 个）、输出格式要求
3. **等待并汇总**：用 `sessions_yield` 等待完成，整合为完整报告，补充跨子调研的关联分析和综合建议
4. **归档**：同模式一

### 模式三：技术雷达（定时触发）

通过 `cron` 定时执行（当前调度为每周一 09:00，配置见 HEARTBEAT.md）：

1. **扫描关注源**：读取 `{baseDir}/assets/radar_sources.json`，对每个源抓取最近一周更新
2. **网络受限降级**：Google 系站点（webrtc.org / blog.chromium.org / android-developers / cloud.google.com）直连可能被阻断（HTTP 000）；失败时改用该源配置的 `fallback`（GitHub API commits/tags 或 web_search），并在报告头部注明降级情况。GitHub API 请求须带 User-Agent 头
3. **筛选与输出**：过滤噪音，保留云手机/音视频/虚拟化相关内容；每条含 [标题] [来源] [一句话摘要] [重要程度⭐]
4. **归档**：保存 `memory/research/tech-radar-YYYY-MM-DD.md` 并更新 INDEX

## 输出规范

所有调研报告必须包含以下结构（详见 `scripts/report_template.md`）：

- **标题**：简洁描述调研主题
- **背景**：为什么需要调研这个技术
- **技术概述**：核心原理和关键概念
- **方案对比**：至少 2 个方案，表格形式对比
- **落地建议**：结合云手机场景给出推荐
- **风险与局限**：潜在问题
- **参考资料**：所有引用的 URL

## 注意事项

- 每次 `web_search` 最多取 5 条结果，避免信息过载
- 优先使用 `web_fetch` 抓取完整内容而非依赖搜索摘要
- 调研报告中的事实性陈述必须标注来源
- 中文搜索 + 英文搜索都要做，覆盖更全面
- 子 Agent 并行调研时，每个子 Agent 最多负责 1 个子问题
- 知识库检索为只读操作（dify-rag skill），不做任何知识库写操作
