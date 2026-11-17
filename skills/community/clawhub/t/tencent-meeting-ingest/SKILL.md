---
name: tencent-meeting-ingest
description: Ingest Tencent Meeting recordings, minutes, and transcripts into the Research KB by delegating platform fetching to tencent-meeting-skill, then letting OpenClaw generate structured meeting wiki pages and related KB updates.
---

# tencent-meeting-ingest

## 职责边界

本 skill 只负责“腾讯会议资料入库编译”。腾讯会议平台能力不在这里重新实现：会议列表、录制列表、智能纪要、转写全文、录制地址和权限错误都必须通过已安装的 `tencent-meeting-skill` / `tencent-meeting-mcp` 调用。

后端负责创建资料源、触发任务、保存任务状态和传递 payload/resultFile。Python 脚本只负责确定性动作：读取 payload、调用外部腾讯会议 skill、归档源材料到 `source_files/tencent_meeting/`、准备 OpenClaw 上下文和任务专用草稿目录、校验短 manifest 与 Markdown 草稿、读取草稿正文、写入 Gitea、维护 `catalog.json`/`index.md`、写 `resultFile`。OpenClaw 负责智能判断：理解会议内容、把 Wiki 正文写成普通 Markdown 草稿、选择页面、判断是否需要更新项目页/概念页/资源页/其他相关页、组织页面之间的链接。

本 skill 不做会议创建、取消、改期、权限申请提交、邮件通知、issue 草稿、问答沉淀，也不保留“没有 OpenClaw 时自动生成简陋页面”的 fallback。

会议入库不只是生成会议纪要页。写 Markdown 草稿和 manifest 前，OpenClaw 应私下做一次知识图谱规划：每场会议先落到 `meetings/` 实体页，再判断它是否改变项目路线、研究主题、实验计划、资源选择、团队导航或已有概念/资源页。没有证据时不要硬建关系页；但会议明确带来决策、路线变化或跨页面综合价值时，应更新相关 `overview/`、`projects/`、`concepts/`、`resources/` 或其他页面，并保留解释性跳转。

## 依赖环境

必须在 OpenClaw 运行环境中具备：

- 已安装并可调用的 `tencent-meeting-skill` 或 `tencent-meeting-mcp`。
- `TENCENT_MEETING_TOKEN`，供腾讯会议 skill 使用。
- `GITEA_URL`
- `GITEA_BOT_TOKEN`
- `GITEA_BOT_USERNAME` 或 `GITEA_ORG`
- `TEAM_KB_REPO`

可选：

- `TENCENT_MEETING_SKILL_COMMAND`：显式指定腾讯会议 skill CLI，例如 `python3 /path/to/tencent-meeting-skill/scripts/tencent_meeting.py`。未配置时，脚本会查找同级 skill 目录 `tencent-meeting-skill/scripts/tencent_meeting.py` 或 `tencent-meeting-mcp/scripts/tencent_meeting.py`。

## 运行协议

本 skill 使用 `prepare -> Markdown drafts + compact manifest -> validate-manifest -> apply` 流程。长正文不进入 JSON；manifest 只承担短元数据交接。

### 1. prepare

```bash
python3 scripts/run_task.py prepare --input <payload.json> --context-output <context.json>
```

`prepare` 会：

1. 读取后端 payload 中的资料源、配置和 `lastSnapshot`。
2. 初次扫描时默认按最近 `historyLookbackDays` 天扫描历史会议，默认 14 天；默认拆成 31 天窗口以减少 MCP 列表调用次数，`windowDays` 可配置且最大不超过 31 天；默认 `pageSize=10`、`maxRecords=30`，`maxRecords` 强制限制在 1 到 500，并会提前停止列表分页，不是拉完全部记录后才截断。每场会议写入 `context.json` 的 `contentPreview` 默认最多 12000 字符，完整智能纪要/转写仍归档到 `source_files/tencent_meeting/`。若腾讯会议 MCP 对大窗口表现不稳定，可在资料源配置中将 `windowDays` 下调到 7 或 14。
3. 增量扫描时从 `lastSnapshot.scanUntil` 往前重叠 `incrementalOverlapDays` 天，默认 1 天，避免会议纪要延迟生成导致漏扫，同时减少重复 MCP 调用。
4. 调用腾讯会议 skill：
   - 默认优先用 `get_records_list` 按时间窗口查询录制文件，这是最节省额度且最贴近“可入库纪要/转写”的入口；
   - 若某个时间窗口的 `get_records_list` 返回空，且未配置 `fallbackToEndedMeetings=false`，默认仅对最近 `endedMeetingsFallbackRecentDays` 天（默认 14 天）的窗口自动调用 `get_user_ended_meetings` 补充已结束会议，再按会议 ID/会议号查询录制，避免历史空窗口大量消耗 MCP 额度；
   - 若配置 `includeEndedMeetings=true`，则无论录制时间窗口是否返回内容，都额外调用 `get_user_ended_meetings` 补充已结束会议；
   - `get_smart_minutes` 优先获取 AI 智能纪要；
   - `get_transcripts_details(pid=0)` 优先获取转写全文；若返回空或失败，再用 `get_transcripts_paragraphs` 获取段落 ID，并按段落调用 `get_transcripts_details` 补全文。
   - 计数口径：inputItems[] 按逻辑会议发生次数计数，不按腾讯会议原始录制文件计数；`get_records_list` 的单条 `record_meetings` 如果包含多个 `record_files`，先逐文件展开，确保每个录制/转写文件都被读取，再把同一会议 ID/会议号、同一天、标题归一化一致且录制时间区间重叠或 10 分钟内相邻的云录制/转写记录合并；复用会议号但日期或时间明显不同的会议仍分开；合并项保留 recordFileIds、meetingRecordIds 和 mergedRecordCount 以便追踪。
5. 只有智能纪要或转写至少一个可用时才作为 `inputItems[]` 交给 OpenClaw。
6. 把每场可入库会议的源材料归档为 `source_files/tencent_meeting/<sourceId>/<date>-<slug>-<hash>.md`。
7. 基于 record id 和内容 hash 做增量判断；已处理且内容未变的会议写入 `skippedSources[]`。
8. 对缺纪要/缺转写/无权限/未生成内容的会议写入 `incompleteItems[]` 或 `errors[]`，不自动申请权限，也不生成低价值空页面。
9. 输出 `context.json`，并在 `pageOutput` 给出本次 attempt 独立的 `draftDir` 和 `manifestPath`。`prepare` 会先清理同 attempt 的旧草稿，避免失败重试误用上次残留文件；写入 context 前会递归剔除 config 中名称包含 token/secret/password/credential/api_key 的字段。首次 attempt 成功产出可入库 context 后，会按 taskId 缓存这份受限 context；同一后端任务的后续 attempt 在 source/config/lastSnapshot 指纹一致时直接复用，不再次调用腾讯会议 MCP，并为新 attempt 重建空草稿目录。apply 成功写出 resultFile 后删除对应缓存，遗留缓存最多保留 7 天。如果没有新内容，`prepare` 会把 skip 结果写入 `resultFile`。如果某些扫描窗口因为 MCP 额度、网络或平台错误失败，`snapshot.scanComplete=false`，且不会把 `scanUntil` 推进到当前时间；后续扫描会继续覆盖未完整完成的历史窗口，避免漏掉旧会议。

### 2. OpenClaw 生成 Markdown 草稿和短 manifest

OpenClaw 必须阅读 `context.json`，为每个 `inputItems[]` 至少生成或更新一个 `meetings/` 实体页。把正文作为 UTF-8 Markdown 文件写到 `context.pageOutput.draftDir` 下。`draftFile` 使用 KB 根目录相对路径，并同时作为最终 Wiki 页面路径，例如 `meetings/2026-07-11-project-sync.md`。

Markdown 第一行使用 `# 页面标题`。正文可以直接包含中文引号、ASCII 双引号、表格、代码块、JSON 示例和多行文本，不需要做 JSON 转义。不要给草稿添加 frontmatter；Python 会统一补齐来源追踪和 catalog 元数据。正文中的页面关系使用 KB 根路径 wikilink，例如 `[[projects/cloud-native.md|云原生项目]]`、`[[concepts/devops-maturity.md|DevOps 成熟度]]`；Python 会按根目录推导关系字段。

然后使用 JSON serializer 把短 manifest 写到 `context.pageOutput.manifestPath`。manifest 不得嵌入 `content` 或 `body`：

```json
{
  "format": "research-kb-markdown-drafts/v1",
  "pages": [
    {
      "draftFile": "meetings/2026-07-11-project-sync.md",
      "sourceItemKeys": ["<inputItems[].itemKey>"]
    }
  ]
}
```

manifest 的每个页面必须明确列出 `sourceItemKeys`，且只能引用本次 `inputItems[].itemKey`。可选的 `projectIds`、`keywords`、`relatedConcepts`、`relatedResources`、`relatedCodePages`、`relatedPages` 仍受支持，但通常不需要填写：标题从 Markdown H1 提取，类型从路径推导，来源 ID 和 sourceStatus 由 Python 决定，关系从 wikilink 推导。manifest 不控制 snapshot、errors、skippedSources 或 resultFile。

允许写入或更新的目录：`meetings/`、`projects/`、`papers/`、`surveys/`、`code/`、`experiments/`、`tech-notes/`、`notes/`、`concepts/`、`resources/`、必要的 `overview/`。不要写 `qa/`，问答沉淀由 `kb_query` 负责。不要写 `source_files/`，源材料归档由 `prepare` 完成。不要把绝对路径、`..`、草稿目录外文件或与 `draftFile` 不一致的 `path` 放进 manifest。

### 3. validate-manifest

```bash
python3 scripts/run_task.py validate-manifest --input <payload.json> --context <context.json>
```

`validate-manifest` 只读草稿和 manifest，不写 Gitea、不写 `resultFile`。如果失败，修正草稿或 manifest 后重新校验；校验成功不是任务终态，必须继续执行 `apply`。

### 4. apply

```bash
python3 scripts/run_task.py apply --input <payload.json> --context <context.json>
```

`apply` 会再次执行同一套校验，然后：

- 校验 manifest 格式、`pages[]` 非空、每个 `draftFile` 存在且为 UTF-8 Markdown。
- 校验每个可读 `inputItems[]` 至少被一个 `meetings/` 页面覆盖。
- 校验每个页面的 `sourceItemKeys` 引用有效会议 item。
- 拦截绝对路径、路径越界、软链接逃逸、重复目标路径、非 Markdown、写入未允许目录、在 manifest 中重新嵌入正文等问题；manifest 和草稿根目录必须与本次 task/attempt 的 prepare 输出完全一致，不能通过 context 或 CLI 参数改写到其他目录。
- 从 Markdown H1 提取标题，从路径推导页面类型，从正文 wikilink 推导 catalog 关系。
- 为页面补齐 frontmatter、source trace、归档路径、record id、hash、sourceStatus。
- 写入/更新 Markdown 页面、`catalog.json` 和 `index.md`。
- Gitea 写配置不完整时明确失败，不进入假写入 dry-run；现有 `catalog.json` 不是合法对象或 `pages[]` 非法时拒绝覆盖；最终 `resultFile` 先写同目录临时文件再原子替换，避免后端轮询到半截 JSON。
- 合并并写回 snapshot，供后续定时扫描增量判断。
- 把后端需要的统一结果 JSON 写入 `resultFile`。

兼容说明：`apply --pages <legacy-pages.json>` 暂时保留旧格式入口，便于旧任务或手工排查；腾讯会议正常流程和后端提示只使用 Markdown 草稿 + manifest，不再生成大 `pages.json`。

## 会议页面模板

会议实体页沿用本地文件入库 skill 的会议模板，当前判断是合理的：它服务科研团队复用，重点不是流水账，而是决策、行动项、风险和证据。

核心章节：

1. `## 会议信息`：时间、参与者、主题、腾讯会议 ID/会议号/录制 ID、源材料路径；缺失则标注“来源未提及”。
2. `## 议程与背景`：会议围绕什么问题展开，关联哪些项目或资料。
3. `## 关键讨论`：按主题整理观点、证据、分歧和上下文。
4. `## 决议`：已经达成的决定、理由和影响范围。
5. `## 行动项`：任务、负责人、截止时间、依赖、状态；缺失则写“来源未提及”。
6. `## 风险与阻塞`：项目风险、资源缺口、技术难点和待协调事项。
7. `## 开放问题`：未解决问题和需要补充的证据。
8. `## 关联页面`：链接相关项目、实验、论文、技术方案、概念或资源。
9. `## 来源与证据索引`：智能纪要、转写、源材料归档路径、record id、hash。

如果会议明确改变某个项目的路线、任务或开放问题，应同步更新 `projects/`。如果会议反复出现可复用方法、架构、工具、数据集或平台，应视证据更新 `concepts/` 或 `resources/`。不要为普通关键词机械建概念页。

如果会议内容影响团队级导航、阶段性资料包、研究主题地图或项目群总览，应更新 `overview/`；如果只是一次普通同步、没有导航或综合价值，则不需要硬建 overview。普通页面之间的关系用 `relatedPages`，概念、资源、代码页分别用 `relatedConcepts`、`relatedResources`、`relatedCodePages`。

## 输出契约

最终 resultFile 必须是后端可读的顶层 JSON envelope：

```json
{
  "success": true,
  "processedSources": [],
  "createdPages": [],
  "updatedPages": [],
  "archivedFiles": [],
  "skippedSources": [],
  "incompleteItems": [],
  "errors": [],
  "commitId": "",
  "snapshot": {}
}
```

