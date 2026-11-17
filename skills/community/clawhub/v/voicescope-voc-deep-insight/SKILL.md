---
name: voicescope-voc-insight
description: >
  VoiceScope VOC 客户反馈分析：自动登录 VoiceScope，上传反馈数据（CSV/Excel/TXT），
  观点提取与聚类，生成/校验标签体系，批量打标签，逐行通用分析（情感判断/关键词提取/
  摘要/场景/行动），取回结果并生成洞察摘要。
  当用户要分析客户反馈、用户评论、投诉、问卷开放题，或提到“打标签”“标签体系”“VOC”
  “反馈分类”“观点提取”“观点聚类”“高频观点”“情感判断”“关键词提取”“自定义分析列”时使用。
---

# VoiceScope VOC Insight Skill

本 Skill 只做入口、编排和展示。所有鉴权、额度、长任务、LLM 调用和结果持久化都在 VoiceScope 后端完成，正式结果写入用户自己的 VoiceScope 项目。

## 功能总览（用户问“能干什么/怎么用”时按此回答）

| 能力 | 说明 | 工作流 |
|---|---|---|
| 观点提取 + 聚类 | 从每条反馈抽取观点片段（带情感极性），再语义聚类出正/负/中三桶高频观点簇 | 工作流 A |
| 批量打标签 | 用标签体系给每条反馈分类，结果写回表格可导出 | 工作流 B |
| 生成标签体系 | 没有标签体系时，从反馈样本自动生成草案，用户确认后可直接入库（或到控制台精修入库） | 工作流 C |
| 校验标签体系 | 默认检查结构/规则问题；加 `--llm` 进一步做语义检查 | `validate` |
| 通用分析列 | 对某列逐行做单一类型分析：情感判断 / 关键词提取 / 摘要 / 场景识别 / 行动建议，结果写回表列 | 工作流 D |

支持的数据格式：CSV、Excel（.xlsx/.xlsm）、TXT（每行一条）。Excel 旧格式 .xls 不支持，提示用户另存为 .xlsx。

> 工作流 D 与控制台「添加自定义分析列」同源（复用后端 `ai_analysis` 引擎），按月度 U 额度计量。注意：聚类链路里那个内部 bigram 指纹 `signature_keywords` 不是关键词产物、不对外——工作流 D 的 `keyword` 是独立的 per-row 关键词分析，两者不要混为一谈。

## 意图分流（先判断用户要什么，再选工作流）

| 用户说法 | 走哪条 |
|---|---|
| “提取观点”“聚类”“大家都在说什么”“高频观点/痛点” | 工作流 A：观点提取 → 聚类 |
| “打标签”“分类”“按标签统计” | 工作流 B：打标签（先确认标签体系，见下） |
| “帮我建标签体系”“没有标签体系” | 工作流 C：生成标签草案 |
| 既要观点又要标签 | 先 A 后 B，同一张表复用 |
| “判断情感/情绪”“正负面”“逐行打情感” | 工作流 D：`analyze --type sentiment` |
| “提关键词”“每条抽关键词” | 工作流 D：`analyze --type keyword`（注意：不是观点聚类的内部指纹） |
| “逐行摘要/总结”“识别使用场景”“给行动建议” | 工作流 D：`--type summary` / `scenario` / `action` |

工作流 D 与工作流 A 的区分：A 是「全表观点提取＋跨行聚类」，产出三桶高频观点簇；D 是「对某列逐行做单一类型分析」，每行一个结果写回表列。用户说“高频/大家都在说什么/痛点排行”走 A；说“给每条/逐行/这一列都判断一下”走 D。

用户想打标签但没说用哪个标签库时，**必须先停下来问，不要替用户默认选择，更不要直接抓一个预置体系就开打**：

- **预置/已有体系不一定贴合用户数据**。先 `taxonomies` 列出项目里现成的（含预置行业模板）给用户看，并明确告知：“这些是通用/预置模板，不一定完全契合你的反馈，先确认是否够用。”
- 给用户两条路二选一：① **用已有/预置体系**——挑一个 `taxonomy_id`；② **从你的数据现生成一套**——走工作流 C，生成草案后在控制台改完入库（更贴合）。
- 用户没明确选定之前，不要进入打标。

## 通用前置步骤（所有工作流共用）

1. **登录检查**：`auth-status`，未登录先 `login`（见下方“登录”）。
2. **预览数据并确认列**：用户给的是 CSV/Excel 时，先本地预览列名：

   ```bash
   python scripts/vs_api.py preview --file 用户的文件.xlsx
   ```

   把列名和样例展示给用户，**必须停下来等用户确认对哪一列做分析，拿到确认前不要上传、不要进入任何工作流**。这是硬性闸门：分析按行扣额度，选错列＝白扣额度，所以即使某列"明显"是反馈原文、即使全表只有一列文本、即使用户在开头已经提过列名，也仍要把"我准备用『X』列，对吗？"明确问出来、得到肯定答复后再继续。绝不替用户默认、绝不猜列直接开跑。
3. **上传**（仅在用户确认列之后执行）：

   ```bash
   python scripts/vs_api.py upload --file 用户的文件.xlsx --text-column 用户原声
   ```

   记下输出的 `table_id`、`text_column_id`（和打标用的 `result_column_id`）。

## 工作流 A：观点提取 → 聚类

这是两步流水线：先逐行提取观点片段（按行扣额度），再对观点列做语义聚类（不按行扣额度）。

```bash
# 第一步：提取（--column 传 text_column_id；输出会给出观点列 result_column_id）
python scripts/vs_api.py extract-viewpoints --table <table_id> --column <text_column_id>
python scripts/vs_api.py wait <extract_task_id>

# 第二步：聚类（--column 传上一步返回的 result_column_id，不是原文列！）
python scripts/vs_api.py cluster --table <table_id> --column <viewpoint_column_id>
python scripts/vs_api.py wait <cluster_task_id>

# 取结果（控制台摘要；--out 导出。.xlsx=官方观点洞察 Excel，推荐；也支持 .csv/.json）
python scripts/vs_api.py cluster-results <cluster_task_id> --out clusters.xlsx
```

结果是 pos/neg/neu 三桶 Top-K 簇，每簇含 LLM 命名（簇名）、片段数、桶内占比和原声样例。向用户汇报时按“正面亮点 / 负面痛点 / 中性观察”组织，引用簇名 + 片段数 + 一两条原声。

`--out *.xlsx` 直接下载**官方观点洞察 Excel**：与控制台 Studio「保存到报告 → 导出 Excel」走同一套序列化（观点 / 数量 / 占比 / 对应原声，按正负向分 sheet），skill 与控制台导出格式一致。注意观点洞察链路**没有“关键词”这个产物**——聚类内部的 bigram 指纹只用作 LLM 命名缓存 key，不对外、不要当关键词汇报。

注意：
- `extract-viewpoints` 可加 `--background "产品背景"` 提升提取质量。
- 聚类报 `viewpoints_not_extracted`：说明传错列（传成原文列）或提取还没完成。
- 同列重复聚类会命中快照缓存秒回；数据变了想强制重算加 `--force-refresh`。

## 工作流 B：批量打标签

前置：确认 `taxonomy_id`（`taxonomies` 列出让用户选；没有合适的走工作流 C）。

```bash
python scripts/vs_api.py taxonomies
python scripts/vs_api.py tag-batch --table <table_id> --column <text_column_id> --taxonomy <taxonomy_id> --result-column <result_column_id>
python scripts/vs_api.py wait <task_id>
python scripts/vs_api.py results <task_id> --out tagged.csv
```

## 工作流 C：生成标签体系

```bash
# CSV/Excel 用 --text-column 指定取哪一列做样本；TXT 整文件按行
python scripts/vs_api.py generate --file 用户的文件.xlsx --text-column 用户原声
python scripts/vs_api.py wait <task_id>
python scripts/vs_api.py draft <task_id>
# 展示草案给用户、得到确认后再入库（下面二选一）
python scripts/vs_api.py confirm-draft <task_id> --name "标签体系名"
```

**必须先把草案展示给用户、拿到明确确认再入库**，不要拿到草案就自动 confirm。确认后两条入库路径二选一：

- **直接入库（agent 闭环）**：`confirm-draft <task_id> --name "…"`，返回正式 `taxonomy_id`，可立刻走工作流 B 打标。需要按用户意见微调草案时，把编辑后的行写成 JSON 数组用 `--items-file edited.json` 传入（后端会重新校验，depth=3 模式下 l3 必填）。
- **控制台精修入库**：需要人工细调（下钻 L3、批量改定义）时，引导用户到控制台改完入库，再用 `taxonomies` 拿 `taxonomy_id`。

用户自带标签体系可先 `validate --file taxonomy.json` 做结构与规则校验；需要进一步检查标签语义重叠、命名等问题时使用 `validate --file taxonomy.json --llm`（会调用 LLM）。

## 工作流 D：通用分析列（情感判断 / 关键词 / 摘要 / 场景 / 行动）

对某一列逐行做**单一类型**分析，结果写回表列（按月度 U 额度计量，与打标 / 观点提取同口径）。`--type` 取值：

| type | 含义 | 每行产出 |
|---|---|---|
| `sentiment` | 情感判断 | 正面 / 负面 / 中性 |
| `keyword` | 关键词提取 | 该行关键词列表 |
| `summary` | 摘要 | 一句话总结 |
| `scenario` | 场景识别 | 使用/反馈场景 |
| `action` | 行动建议 | 可执行建议 |

```bash
# --column 传源文本列 id（text_column_id）；result_column_id 缺省后端自动建列
python scripts/vs_api.py analyze --table <table_id> --column <text_column_id> --type sentiment
python scripts/vs_api.py wait <task_id>
python scripts/vs_api.py analysis-results <task_id> --out analysis.csv   # 不加 --out 只预览前 5 行
```

- 可加 `--background "产品背景"` 提升质量（同观点提取）。
- 一次只跑一种 `--type`；要多种就分别提交、各自一个结果列。
- 汇报口径：行数、有结果/空行数、`sentiment` 额外给情感分布；`keyword` 不要和工作流 A 聚类里的内部 `signature_keywords` 指纹混淆，那个不对外。

## 登录

先检查登录状态：

```bash
python scripts/vs_api.py auth-status
```

如果返回 `auth_required` 或提示未登录，执行：

```bash
python scripts/vs_api.py login
```

登录会自动打开浏览器。用户在 VoiceScope 网页登录并确认授权后，脚本会把 token 保存到 `~/.voicescope/auth.json`。无浏览器环境使用：

```bash
python scripts/vs_api.py login --no-browser
```

开发者 fallback：如果环境变量里有 `VOICESCOPE_API_KEY=vs_xxx`，脚本会优先使用 API Key，不读取本地登录 token。

本地联调后端时可设置：

```bash
VOICESCOPE_API_BASE=http://127.0.0.1:8000
```

退出：

```bash
python scripts/vs_api.py logout
```

## 错误处理

按 `error.code` 决定下一步：

| code | 处理 |
|---|---|
| `auth_required` | 执行 `login`。 |
| `authorization_pending` | 用户还没在浏览器确认，继续等待。 |
| `authorization_expired` | 设备码过期，重新执行 `login`。 |
| `token_expired` | 脚本会自动 refresh；失败则重新 `login`。 |
| `token_revoked` | 本地登录已撤销，重新 `login`。 |
| `quota_exceeded` | 告诉用户本月 U 额度不足，引导到控制台查看用量或升级套餐。 |
| `task_not_ready` | 继续 `wait`，不要重复提交任务。 |
| `viewpoints_not_extracted` | 聚类的 `--column` 传错（应传观点列）或提取未完成，先完成工作流 A 第一步。 |
| `missing_dependency` | 本地缺 openpyxl：`pip install openpyxl` 后重试。 |
| `validation_failed` | 按 message 修正参数后重试。 |

## 交付口径

任务完成后只汇报关键数字：行数、命中数/未命中数、簇数与各桶片段数、issue 数、task_id、导出文件路径或控制台链接。大结果不要塞进对话上下文，除非用户明确要求抽样展示。观点聚类汇报模板：总片段数 → 负面 Top 痛点（簇名+数量+原声例）→ 正面 Top 亮点 → 值得注意的中性观察。

**务必讲清楚结果在哪看**，给用户两个明确出口，不要让用户猜（`results` / `cluster-results` 命令末尾已自动打印这两条，转述即可）：

- **在线（需登录）**：优先转述脚本给出的**直达链接**（`links.open_url`，形如 `https://voiceaiscope.com/workbench?openTaskId=<task_id>`），点开即定位到本次任务结果，未登录会先提示登录再跳回，可分享。后端没回 `open_url` 时才回落到工作台首页 `project_url`。正式结果都写在用户自己的项目里，刷新即见。
- **下载到本地**：`cluster-results` 加 `--out 文件名.xlsx`（官方观点洞察 Excel，与控制台导出一致，推荐）导出到本地，把**绝对路径**告诉用户；也支持 `.csv` / `.json`。`results`（打标）用 `--out 文件名.csv`。

打标完成时，除了命中数，也要把**未命中**讲明白：未命中＝该行没匹配到任何标签，常见原因是标签体系不够贴合，可建议换体系或走工作流 C 重新生成。

### 引导用户去平台做更强的后续（强后续类型才提示）

skill 是上车点，平台 Studio 才是深度分析的地方（词云、标签洞察、情感看板、报告这些可视化终端做不了）。所以**只在「平台确有更强后续」的分析类型**完成后，顺带引导用户去平台继续——不是每次都弹，避免噪音。`results` / `cluster-results` / `analysis-results` 命令已在结果末尾自动打印这句引导，转述即可：

- `keyword`（工作流 D）→ 平台可一键生成**词云**
- 打标 / `tag`（工作流 B）→ 标签 **Studio** 的洞察 / 趋势 / 下钻 / 交叉透视
- `sentiment`（工作流 D）→ **情感分布看板**
- 观点聚类（工作流 A）→ 保存为**观点洞察报告**、与标签交叉分析

`summary` / `scenario` / `action` 无强后续，不提示。链接优先用后端回传的 **`open_url` 直达深链**（`?openTaskId=<task_id>`，点开即定位到本次结果），skill 透传即可；后端未回时回落到 `project_url` 工作台首页。
