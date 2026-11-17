---
name: zwjh-skill
description: "统一记忆底座：长期记忆 + 知识图谱 + 自动沉淀 + 检索。让 AI「记得你」，跨会话持久记忆、实体/关系图谱、语义与时间线检索、记忆健康度审计、本地备份（可接百度网盘）。纯本地、零密钥、按硬件自适应，不拖累电脑。并保留 v1.7 的根因分析/预测性维护/进化报告。"
version: 2.6.0
---


# 长期记忆 / 知识图谱 会思考的进化 AI — zwjh-skill v2.6.0

> **安装后说「帮我配置 + 设置定时任务」，AI 自动完成一切。**
>
> 它是一个**统一记忆底座**，而不只是又一个「记忆 skill」：
> - 🧠 **长期记忆**：跨会话持久记住你、项目、客户，减少重复解释背景
> - 🕸️ **知识图谱**：自动抽取「人 / 项目 / 任务 / 事件 / 文档」等实体与关系
> - ⚙️ **自动沉淀**：从对话 / 文件自动提炼知识点（去重 + 冲突消解）
> - 🔎 **检索**：本地语义检索 + 时间线检索（零密钥、零联网、毫秒级）
> - 🩺 **健康度**：审计记忆膨胀、压缩/快照，记忆可观测、可清理
> - 💾 **备份**：导出 / 备份 / 恢复（本地 + 百度网盘可插拔）
> - 🖥️ **不拖累电脑**：自动探测硬件，按 CPU/内存分配并发与批大小
> - 🔔 **更新提醒**：发现新版本主动提示你升级
>
> **v2.0.0**：从「单技能」升级为「可插拔的记忆基础设施」，并完整保留 v1.7 的根因分析 / 预测性维护 / 进化报告能力。

---

## 核心理念

```
传统 AI：每次对话从零开始 → 你反复解释背景 → 记忆散落各处、互不相通
会思考的进化 AI：理解本质 → 沉淀为记忆+图谱 → 跨会话检索 → 举一反三 → 自动进化
```

**为什么做统一底座？** 市面方案碎片化（各 skill 各存各的、跨 skill 不互通）。本技能把「记忆 + 图谱 + 检索 + 健康度」做成一个**其他 skill 可直接调用的基础设施**，而不是又一个孤立的记忆插件。

---

## 30 秒速查表

| 我想做 | 直接说 / 运行 |
|--------|--------|
| **一键启动自动进化** | `帮我配置 + 设置定时任务` |
| 记下一段对话/知识点 | `python scripts/cli.py deposit --text "..."` |
| 从文件沉淀知识 | `python scripts/cli.py deposit --file notes.md` |
| 语义检索记忆 | `python scripts/cli.py query "谁负责机器学习项目"` |
| 让 AI 用记忆回答 | `python scripts/cli.py ask "我最近在做什么项目"` |
| 查某段时间发生的事 | `python scripts/cli.py timeline --from 2026-07-01 --to 2026-07-31` |
| 看知识图谱 | `python scripts/cli.py graph list` / `graph show`（Mermaid） |
| 知识图谱查询 | `python scripts/cli.py graph-query --action search --name 张三` |
| 遗忘指定记忆 | `python scripts/cli.py forget --memory-id 42` |
| 查看归档 | `python scripts/cli.py forget --list-archive` |
| 流式导出 | `python scripts/cli.py export-stream --format markdown` |
| 记忆健康度体检 | `python scripts/cli.py health` |
| 压缩（去重+摘要） | `python scripts/cli.py compact --apply` |
| 备份 / 恢复 | `python scripts/cli.py backup` / `restore <路径>` |
| 写日记 | `python scripts/cli.py diary --text "今天想清楚了一件事"` |
| 看是否有新版本 | `python scripts/cli.py update-check` |
| 查看/消解冲突 | `python scripts/cli.py conflicts` |
| 一键配置定时任务 | `python scripts/cli.py setup` |
| 总览 | `python scripts/cli.py status` |

> **大部分时候你只需要说第一句，AI 自动完成一切。** 其余命令是给「想精细操控」的高级用户。

---

## 一键启动（2 步）

```
1. 对 AI 说：「帮我配置 + 设置定时任务」
2. AI 自动完成：探测硬件 → 注册每日定时任务（python cli.py autopilot）
```

启动后，每天 23:00 自动执行：

```
补录每日日志 → 沉淀知识点 → 记忆分析(根因) → 预测风险 → 进化报告 → 健康巡检 → 更新提醒
```

**你完全不用管，它自己会跑。** 且定时任务由技能用系统自带能力注册（Windows 用 `schtasks`、macOS/Linux 用 `crontab`），**不生成任何 .ps1 / .sh / .bat 脚本文件**，更干净、更安全。

---

## 功能模块

---

### 模块 1：长期记忆（跨会话 + 每日日志 + 日记）

**做了什么**：把你的对话、文件、每日日志统一沉淀为可检索的长期记忆；另设「日记」自由记录。

- 记忆落库在 `~/.workbuddy/memory/`（与 v1.7 完全兼容，原有每日日志原样保留）
- 索引（图谱 + 向量）存于 `~/.workbuddy/memory/zwjh_store/`
- 每天自动把当日日志补录进底座（幂等，不重复堆积）

**示例**：
```bash
python scripts/cli.py deposit --text "客户张三的对接人是李四，需求是智能客服" --source conversation
python scripts/cli.py diary --text "今天想清楚了一件事：记忆要先去重再沉淀"
```

---

### 模块 2：知识图谱（实体 / 关系）

**做了什么**：自动维护「人 / 项目 / 任务 / 事件 / 文档 / 概念 / 组织」等实体与关系。

- 显式关系模板：`负责 / 参与 / 隶属于 / 创建 / 依赖 / 导致 / 位于 / 关联`
- 已知实体在同一段文本中**共现** → 自动连弱边（图谱随使用自然生长）
- 关系权重累积、可导出 Mermaid 直接可视化
- **可插拔**：其他 skill 可直接 `add-entity` / `relate` 注册自己的实体类型

**示例**：
```bash
python scripts/cli.py graph add-entity --type person --name 张三 --importance 0.9
python scripts/cli.py graph relate --from 张三 --to 智能客服系统 --relation 负责
python scripts/cli.py graph show
```

---

### 模块 3：自动沉淀（去重 + 冲突消解）

**做了什么**：从对话 / 文件自动提炼知识点，并保证质量。

- **去重**：完全重复直接合并；近似重复（Jaccard ≥ 0.82）更新原条目而非新增
- **冲突消解**：同一实体同一谓词出现不同值 → 旧值自动标记 `superseded`，保留历史可追溯
- **事实抽取**：「X 的 Y 是 Z」自动写入图谱事实（如「客户李四 的产品 是 智能客服系统」）

**效果**：
```
沉淀「客户李四对接的产品是智能客服系统」
  → 实体：客户李四(person)
  → 事实：(客户李四, 产品, 智能客服系统)
```

---

### 模块 4：语义检索 + 时间线检索（零密钥）

**做了什么**：两种检索，都不需要任何 API Key、不联网。

- **语义检索**：本地 TF-IDF（中文 char/bigram 向量）余弦相似度。即使表述不同（"学机器" vs "机器学习"）也能召回，毫秒级。
- **时间线检索**：按日期区间 + 关键词过滤，还原「某段时间发生了什么」。

**示例**：
```bash
python scripts/cli.py query "谁负责机器学习项目"
python scripts/cli.py timeline --from 2026-07-01 --to 2026-07-31 --keyword 发布
```

> 其他 skill 也可直接调用 `retrieval.ask(question)` 把长期记忆注入自己的上下文——这就是「可插拔基础设施」。

---

### 模块 5：记忆健康度审计 + 压缩 / 快照

**解决「记忆膨胀」痛点**：记忆越多越慢、重复越多越乱。

- **审计**：产出 0~100 健康度评分，列出陈旧记忆 / 孤儿实体（无关系）/ 冲突事实 / 近似重复 / DB 体积
- **压缩**：对陈旧记忆做抽取式摘要、合并近似重复（先预览 dry-run，再 `--apply`）
- **快照**：导出完整可恢复快照（实体/关系/事实/配置）

```bash
python scripts/cli.py health
python scripts/cli.py compact --apply
python scripts/cli.py snapshot
```

---

### 模块 6：导出 / 备份 / 恢复（接百度网盘）

**做了什么**：记忆可迁移、可恢复。

- **默认本地备份**：快照 + 每日日志原文打包到 `zwjh_store/backups/`，自动保留最近 7 份
- **百度网盘（可插拔）**：仅在用户本地已配置访问凭证时启用（凭证存本地 `config.json`，**不进技能包、不需要密钥**）；未配置时清晰提示，绝不偷偷联网
- **恢复**：从备份写回图谱与每日日志

```bash
python scripts/cli.py backup
python scripts/cli.py backup --target baidunetdisk   # 需先配置凭证
python scripts/cli.py restore <备份目录路径>
```

---

### 模块 7：硬件自适应（不拖累电脑）

**做了什么**：自动探测 CPU 核心数 / 物理内存 / 系统，把机器分 `low / mid / high` 三档，自动给出：

| 档位 | 并发 | 单批 | 向量缓存 | 适用 |
|------|------|------|----------|------|
| low  | 1 | 20 | 关 | ≤2 核或 <4GB |
| mid  | 2 | 60 | 开 | ≤4 核或 <8GB |
| high | ≤8 | 200 | 开 | 更高配 |

- 检索/沉淀按档位**分批**处理，避免一次性占满内存
- 提供 `recommend_subtasks(n)`：按任务量与档位建议拆成几个子任务（给上层调度用）
- 探测失败回退保守 `low` 档，**绝不把电脑跑满**

```bash
python scripts/cli.py hardware
```

---

### 模块 8：技能更新提醒

**做了什么**：本地比较「技能包版本」与「本机已见版本」，发现新版本主动提示你升级（不依赖联网 / 密钥）。

- 运行 `python scripts/cli.py update-check` 立即查看
- 每日 `autopilot` 也会在结尾打印更新提示（若有）
- 已见版本缓存于 `zwjh_store/installed_version.json`，避免重复打扰

```bash
python scripts/cli.py update-check
```

---

### 模块 11：记忆冲突消解

**做了什么**：当新记忆与旧记忆矛盾时，智能检测、分类、消解，避免"记错了还固执"。

- **冲突自动检测**：写入时自动对比同 entity+predicate 的已有事实，计算语义相似度与矛盾度
- **冲突分类**：信息更新（换工作）/ 信息纠错（之前记错）/ 视角变化（同义不同描述）/ 真实冲突（需仲裁）
- **自动消解**：UPDATE / CORRECTION 类型自动处理（新替旧），PERSPECTIVE 自动合并
- **冲突提示**：REAL_CONFLICT 生成对比报告，存入待处理队列，提示用户仲裁
- **处理策略**：覆盖 / 保留两者 / 合并 / 忽略
- **性能保障**：仅在同 entity+predicate 写入时触发，向量缓存，超时保护，不拖累写入

**示例**：
```bash
python scripts/cli.py deposit --text "我之前记错了，张三其实去了字节跳动" --source conversation
# → 自动检测到纠错模式，新值覆盖旧值

python scripts/cli.py conflicts
# → 查看待处理冲突
python scripts/cli.py conflicts --resolve 1 --strategy 1
# → 处理冲突 #1，策略：覆盖
```

---

### 模块 12：记忆导出 / 迁移

**做了什么**：多格式、可选中、跨平台迁移，消除数据锁定担忧。

- **多格式导出**：Markdown（可读性）/ JSON（结构化）/ Neo4j Cypher（图数据库）/ CSV（Excel）/ Obsidian / Logseq
- **选择性导出**：按实体类型 / 时间范围 / 重要度阈值筛选
- **批量导入**：支持从 Markdown、JSON、Obsidian vault 批量导入
- **零依赖**：所有格式纯标准库生成，无需额外工具

**示例**：
```bash
python scripts/cli.py export --format markdown --output D:\backup
python scripts/cli.py export --format obsidian --from-day 2026-01-01 --to-day 2026-07-31
python scripts/cli.py export --format cypher --types person,project
python scripts/cli.py export --format csv --output D:\export
```

---

### 模块 13：时间线叙事生成

**做了什么**：把分散的记忆组织成连贯的叙事，从"数据库"变成"有温度的回忆"。

- **项目进展时间线**：输入项目名称，自动生成从立项到当前的所有关键节点
- **人脉交互历史**：输入人名，生成与 TA 的所有互动时间线
- **知识成长轨迹**：输入主题，展示认知变化（入门→深入）
- **周期性回顾**：每周/每月自动生成回顾报告
- **可插拔 LLM**：支持配置外部 LLM API，未配置时使用模板降级

**示例**：
```bash
python scripts/cli.py narrative project --name "机器学习项目"
python scripts/cli.py narrative person --name "张三"
python scripts/cli.py narrative knowledge --name "Python"
python scripts/cli.py narrative weekly
python scripts/cli.py narrative monthly
```

---

### 模块 14：多模态记忆

**做了什么**：记忆从文字扩展到图片、音频、文件，全媒体覆盖。

- **图片记忆**：AI 理解图片内容、拍摄时间、关联事件
- **音频记忆**：会议录音摘要、关键决策关联到项目
- **文件记忆**：文档摘要、存在路径、关联实体
- **媒体理解适配器**：可插拔（本地模型 / LLM API / 手动描述）
- **实体关联**：媒体文件自动链接到知识图谱实体

**示例**：
```bash
python scripts/cli.py multimodal index-image --path D:\photo.jpg --entity "张三" --text "项目启动会合影"
python scripts/cli.py multimodal index-audio --path D:\meeting.mp3 --project "智能客服"
python scripts/cli.py multimodal index-file --path D:\contract.pdf --entity "李四" --project "合同审核"
python scripts/cli.py multimodal list --type image
```

---

### 模块 15：跨 skill 记忆总线（MCP 服务器）

**做了什么**：把 zwjh-skill 的核心能力暴露为 MCP Tool，让其他 skill / Agent 直接调用，「可插拔基础设施」定位落地。

- **3 个 MCP Tool**：`zwjh_query`（语义检索）/ `zwjh_deposit`（沉淀知识点）/ `zwjh_health`（健康度报告）
- **零依赖**：纯标准库实现 MCP 协议（JSON-RPC 2.0 over stdio），不引入 `mcp` 包
- **协议标准**：兼容 MCP 2024-11-05 规范，可与任何支持 MCP 的 Agent 集成

**启动方式**：
```bash
python scripts/mcp_server.py
# 或
python scripts/cli.py mcp
```

**MCP 配置示例**（`~/.workbuddy/mcp.json`）：
```json
{
  "mcpServers": {
    "zwjh-memory": {
      "command": "python",
      "args": ["D:/skill/zwjh-skill/scripts/mcp_server.py"]
    }
  }
}
```

---

### 模块 16：自动归档策略（冷热分层）

**做了什么**：按访问频率 + 时间衰减自动控制记忆膨胀，「热记忆保持、温记忆摘要、冷记忆高压缩归档」。

- **热度算法**：`0.6 × ln(access_count + 1) + 0.4 × exp(-days_since_access / 30)`
- **三层策略**：热（保持原样）/ 温（抽取式摘要，30~50% 压缩）/ 冷（仅保留事实，70~90% 压缩）
- **自动触发**：`autopilot` 末尾自动调用，无需手动干预
- **硬件感知**：批处理大小按 `hardware.tier` 分配

**示例**：
```bash
python scripts/cli.py archive --dry-run    # 查看归档计划
python scripts/cli.py archive              # 执行归档
python scripts/cli.py archive --stats      # 查看归档统计
```

---

### 模块 17：任务状态面板（Web 可视化增强）

**做了什么**：在原有图谱可视化基础上，新增底部任务状态面板，autopilot 运行可观测。

- **定时任务状态**：显示是否注册、频率、输出
- **健康度评分**：实时显示当前健康度（绿/黄/红三色标识）
- **归档统计**：热/温/冷记忆数量 + 压缩节省百分比
- **可折叠设计**：不占用图谱空间，需要时展开

**启动方式**：
```bash
python scripts/web_server.py
# 浏览器打开 http://127.0.0.1:8080 → 底部任务状态面板
```

---

### 模块 18：本地 Embedding 层（ONNX BGE）

**做了什么**：接入 bge-small-zh v1.5 ONNX 量化模型，实现真正的语义向量检索。

- **模型外部放置**：模型文件不打包，包内只带 SHA256 校验与下载指引
- **零密钥**：用户下载 .onnx 放置 `models/` 即启用语义检索
- **自动回退**：无模型时自动回退 TF-IDF（行为同旧版）
- **向量存储**：SQLite BLOB 表，万条级暴力余弦检索
- **扩展预留**：接口预留 HNSW 索引扩展点

**模型信息**：
- 模型：BAAI/bge-small-zh-v1.5 (ONNX INT8 量化)
- 维度：512
- 大小：约 30MB
- 下载：放置 `models/bge-small-zh-v1.5-q.onnx`

---

### 模块 19：混合检索（三路召回 + RRF 融合）

**做了什么**：检索升级为语义/关键词/时间三路召回 RRF 融合排序，返回结果附命中理由。

- **三路召回**：语义（ONNX BGE）/ 关键词（TF-IDF）/ 时间衰减
- **RRF 融合**：Reciprocal Rank Fusion 平滑融合多路结果
- **可解释输出**：返回语义分/关键词分/时间分，让 Agent 知道为何召回
- **向后兼容**：无 ONNX 模型时自动回退纯 TF-IDF

**示例**：
```bash
python scripts/cli.py query "张三去哪了"
# 返回: [{day, source, score, snippet, explanation: {semantic, keyword, time, summary}}]
```

---

### 模块 20：存量记忆重建索引

**做了什么**：后台分批重建存量记忆的向量索引，不阻塞使用。

- **后台分批**：按硬件档位分配批次大小
- **断点续传**：已处理的跳过，支持中断后继续
- **进度输出**：实时显示处理进度
- **让出 CPU**：每批处理后让出线程，不卡顿

**示例**：
```bash
python scripts/cli.py rebuild-index           # 重建全部
python scripts/cli.py rebuild-index --batch 100  # 大批次
python scripts/cli.py embedder-info           # 查看模型状态
```

---

### 模块 21：MCP 工具扩建（记忆即服务）

**做了什么**：MCP 服务器从 3 个工具扩建至 7 个，覆盖图谱查询、时间线检索、遗忘归档、流式导出，并附赠 mcp_version 协商机制。

- **7 个 MCP Tool**：query / deposit / health / **graph_query** / **timeline** / **forget** / **export_stream**
- **graph_query**：知识图谱查询（实体搜索/详情/事实/最短路径）
- **timeline**：时间线检索（按日期区间+关键词过滤记忆）
- **forget**：遗忘（软删除）指定记忆，移入归档表可恢复
- **export_stream**：流式导出（分批返回，避免大内存占用，支持 json/markdown/csv）
- **mcp_version 协商**：initialize 时返回服务端版本，兼容不同客户端

**启动方式**：
```bash
python scripts/mcp_server.py
# 或
python scripts/cli.py mcp
```

---

### 模块 22：记忆访问权限分级

**做了什么**：调用方提交 manifest（HMAC-SHA256 签名），服务端校验签名、有效期和权限，实现命名空间隔离。

- **命名空间**：`public`（公共）/ `private/<skill-id>`（技能私有）/ `shared/<name>`（共享）
- **权限等级**：read（读）/ write（写）/ admin（删除/管理）
- **向后兼容**：未传 manifest 默认 public 只读（旧调用方零改造）
- **签名算法**：HMAC-SHA256（namespace + permissions + timestamp + nonce）
- **有效期**：manifest 5 分钟过期，防重放
- **密钥管理**：首次运行自动生成，CLI `access-key --rotate` 轮换

**示例**：
```python
from scripts.memory_access import create_manifest
manifest = create_manifest("private/my-skill", ["read", "write"])
# 将 manifest 作为 MCP tool 参数传递
```

---

### 模块 23：多进程并发写入门禁

**做了什么**：通过 SQLite 事务 + version 字段乐观锁，防止多进程/多线程并发写入时的数据不一致。

- **乐观锁**：memories 表新增 `version` 字段，UPDATE 时校验版本号，冲突返回 `WRITE_CONFLICT` 错误码
- **原子操作**：所有写入走 `threading.Lock` + SQLite 事务
- **错误码**：WRITE_CONFLICT（版本冲突）/ NOT_FOUND（记忆不存在）/ ALREADY_EXISTS（已存在）
- **归档隔离**：forget 操作移入独立归档表，不阻塞主表写入
- **命名空间隔离**：不同命名空间的记忆可独立管理

**示例**：
```python
from scripts.store import update_memory_with_lock
result = update_memory_with_lock(memory_id, {"version": 1, "raw_text": "修正内容"})
if not result["ok"] and result["error"] == "WRITE_CONFLICT":
    # 冲突处理：重新读取最新版本再写入
    ...
```

---

### 模块 10：知识图谱可视化（Web 界面）

**做了什么**：在浏览器中直观探索实体关系网络，从"黑盒存储"变为"可视化探索"。

- **交互式关系网络图**：力导向图，可缩放/拖拽/搜索，按类型着色
- **实体详情面板**：点击节点弹出，显示属性、关联关系
- **路径探索**：选择两个实体，BFS 自动展示最短关系路径
- **时间线视图**：按时间轴展示实体历史变迁
- **子图过滤**：按类型/关系/重要度过滤，聚焦关心的部分
- **大规模优化**：1000+ 节点时分层加载（核心节点优先 + 邻居按需加载）+ 聚合显示
- **零依赖**：内置 Python HTTP 服务器，前端 ECharts，开箱即用

**启动方式**：
```bash
python scripts/web_server.py [--port 8080]
# 浏览器打开 http://127.0.0.1:8080
```

---

### 模块 9（保留 v1.7）：记忆分析 / 预测性维护 / 进化报告

原有「会思考的进化 AI」核心能力完整保留：

- `analyze`：智能记忆分析（理解本质 / 根因 / 隐含需求 / 自动修复建议）
- `predict`：预测性维护（从历史推断明日风险）
- `report`：进化报告（成长趋势统计）
- `demo`：无数据时看效果

```bash
python scripts/cli.py analyze
python scripts/cli.py predict
python scripts/cli.py report
python scripts/cli.py demo
```

---

## 典型应用场景

- **让 Agent「记得你」**：减少重复解释背景，新对话自动带入历史上下文
- **项目知识沉淀**：新人接手时一句 `ask "这个项目的关键人物和坑是什么"` 快速上手
- **个人 / 客户 CRM（轻量）**：客户、对接人、需求自动成图谱，随问随答

---

## 差异化 / 竞争力

- **中文优化**：char/bigram 向量对中文语义召回友好
- **与其他 skill 打通**：作为可插拔记忆底座，任何 skill 都能 `import` 复用
- **接企业微信 / 百度网盘做备份**：备份通道可插拔扩展
- **可观测、可清理**：健康度评分 + 压缩/快照，正面解决「记忆膨胀」
- **纯本地、零密钥**：无模型下载、无 API 费用、无隐私外泄

---

## 技术实现要点

- **存储**：`sqlite3`（WAL 模式，写入不阻塞）+ 每日日志原文（append-only）
- **向量**：本地 TF-IDF 稀疏向量（中文 char/bigram），**零模型、零密钥**
- **图谱**：实体 / 关系表 + 共现 + 模板关系抽取 + 事实冲突消解
- **调度**：硬件自适应并发 / 批大小；定时任务用系统原生能力注册（无脚本文件）
- **可插拔**：嵌入适配器、百度网盘适配器、实体类型均可扩展

---

## 更新日志

| v2.6.0 | 2026-09-19 | 新增：MCP 工具扩建至 7 个（graph_query / timeline / forget / export_stream + mcp_version 协商）；新增记忆访问权限分级（HMAC-SHA256 manifest + 命名空间隔离，未声明默认 public 只读）；新增多进程并发写入门禁（SQLite 事务 + version 字段乐观锁 + WRITE_CONFLICT 错误码）；新增 forget / export-stream / graph-query / access-key CLI 子命令；新增 graph.py BFS 最短路径；新增 memory_access.py 权限模块；新增 memories 表 version/namespace 字段 + memories_archive 表 |
| v2.5.0 | 2026-08-24 | 新增：本地 embedding 层（ONNX BGE 语义向量 + TF-IDF 回退，模型外部放置 + SHA256 校验）；新增混合检索（语义/关键词/时间三路召回 RRF 融合排序）；新增检索解释（返回结果附命中理由分项）；新增存量记忆一键重建索引（后台分批不阻塞）；新增 embedder.py / rebuild_index.py；优化 retrieval.py 升级为 hybrid_search |
| v2.4.0 | 2026-08-17 | 新增：跨 skill 记忆总线（MCP 服务器，暴露 query/deposit/health 为 MCP Tool，零依赖）；新增自动归档策略（冷热分层 + 时间衰减热度分，autopilot 自动触发）；新增任务状态 Web 面板（定时任务/健康度/归档统计可视化）；新增 mcp_server.py / archive.py；新增 CLI archive / mcp 命令 |
| v2.3.0 | 2026-08-07 | 新增：多格式导出（Markdown/JSON/Cypher/CSV/Obsidian/Logseq）与选择性筛选；新增时间线叙事生成（项目/人脉/知识成长/周期回顾）；新增多模态记忆（图片/音频/文件索引）；新增 export.py / narrative.py / multimodal.py |
| v2.2.0 | 2026-07-29 | 新增：记忆冲突消解（冲突自动检测 + 四类分类 + 自动/手动消解策略）；新增 conflict_resolver.py；新增 CLI conflicts 命令 |
| v2.1.0 | 2026-07-17 | 新增：知识图谱 Web 可视化（力导向图/详情面板/路径探索/时间线/子图过滤）；增加 web_server.py 零依赖内置 HTTP 服务器；增加大规模图谱分层加载与聚合；新增 REST API |
| v2.0.0 | 2026-07-08 | 新增：统一记忆底座（长期记忆 + 知识图谱 + 自动沉淀 + 检索 + 健康度 + 备份）；新增硬件自适应调度与技能更新提醒；保留 v1.7 能力；零密钥纯本地 |
| v1.7.0 | 2026-06 | 优化：大幅简化操作（一键启动）、增强自愈能力（极少人工介入） |
| v1.6.0 | 2026-05 | 新增：思维进化引擎、根因分析、一键定时任务 |
| v1.5.0 | 2026-04 | 优化：友好错误处理、预测冷启动优化 |
| v1.0.0 | 2026-03 | 初始版本发布 |

---

## ❌ 边界说明

| 不支持 | 替代方案 |
|--------|---------|
| 修改 SKILL.md 本身 | 手动更新版本 |
| 删除 MEMORY.md | 只追加不删除 |
| 100% 自动修复 | 复杂情况给精确命令 |
| 完美概率预测 | 数据越多越准，冷启动也给建议 |
| 联网语义（默认） | 默认本地向量；如需更强语义可自行挂接嵌入适配器 |
| 百度网盘无凭证自动备份 | 先在 `config.json` 配置访问凭证，或用本地备份 |

---

## ❓ 常见问题（FAQ）

### Q1: 第一次使用怎么做？
说 **「帮我配置 + 设置定时任务」**，AI 自动探测硬件、注册定时任务。

### Q2: 没有记忆文件怎么办？
说 **「模拟演示」**，用假数据看效果。之后再聊几天话就有了。

### Q3: 定时任务设置了没反应？
```bash
python scripts/cli.py task-status      # 查看状态
python scripts/cli.py autopilot        # 手动跑一次
```

### Q4: 如何暂停自动进化？
```bash
python scripts/cli.py remove           # 删除定时任务
```

### Q5: 数据存在哪？安全吗？
记忆原文在 `~/.workbuddy/memory/`，索引在 `~/.workbuddy/memory/zwjh_store/`。
全部本地、**不上传任何外部服务器**、不要求任何密钥。

### Q6: 会拖慢电脑吗？
不会。技能自动探测硬件并限流：低配机单线程小批量，高配机才多并发；检索/沉淀分批处理。

### Q7: 记忆太多太乱怎么办？
`python scripts/cli.py health` 看健康度，`compact --apply` 压缩去重，`snapshot` 留底。

### Q8: 怎么把记忆给别人 / 换电脑？
`python scripts/cli.py backup` 导出到本地备份目录，拷贝即可；到新机器 `restore <路径>`。

### Q9: 支持 Mac / Linux 吗？
支持。定时任务用 `crontab`（由 `setup` 命令自动写入，不生成 .sh 文件）。

### Q10: 怎么知道有新版本？
`python scripts/cli.py update-check`；每日自动进化也会提示。

### Q11: 其他 skill 怎么复用这个底座？
直接 `from scripts import retrieval, store, graph, deposit` 调用；或用 CLI 的 `ask` / `deposit` 子命令。

### Q12: Python 版本要求？
Python 3.8+，标准库即可，无需安装任何第三方包。

---

## 安全声明

- 所有分析在本地完成，不上传任何外部服务器
- 不要求、不读取任何 API Key；联网功能均为可插拔且默认关闭
- 只读写你指定的记忆目录，不碰其他文件
- 自动修复有白名单，危险操作需确认
- 所有文件操作都有异常捕获，不会崩溃
- 定时任务由系统原生能力注册，**不生成任何 .ps1 / .sh / .bat 等可执行脚本**

---

## 支持

- 平台：WorkBuddy 等使用 `~/.workbuddy/memory/` 的 Agent；Windows / macOS / Linux
- 中文界面、零密钥、本地优先
- 有更好建议：**njskills@agent.qq.com**

---

## 发布信息

- **作者**: Admin
- **许可证**: MIT
- **最低引擎版本**: 1.0.0
- **更新历史**:
  - v2.0.0: 升级为统一记忆底座（长期记忆+知识图谱+自动沉淀+检索+健康度+备份+硬件自适应+更新提醒），保留 v1.7 能力，零密钥纯本地
  - v1.7.0: 大幅简化操作（一键启动）、增强自愈能力（极少人工介入）、功能开箱即用
  - v1.6.0: 思维进化引擎、根本原因分析、一键定时任务
  - v1.5.0: 友好错误处理、预测冷启动优化
  - v1.4.0: 升级为进化 AI
  - v1.3.0: 首次使用向导
  - v1.2.0: 代码折叠优化
  - v1.1.0: 智能经验提取
  - v1.0.0: 初始版本