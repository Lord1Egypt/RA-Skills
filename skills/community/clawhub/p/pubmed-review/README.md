# PubMed Review Skill

飞书自然语言触发的 PubMed 文献检索与 AI 综述生成系统。

## 功能概览

- 飞书消息触发：`帮我查瘢痕激光 最近5年 综述` → 自动完成检索+摘要+综述+通知
- 检索词专业化：OR/AND 布尔扩展，支持时间/文献类型/人群/研究类型限定词
- AI 综述生成：brief（飞书推送）+ full（完整文件）
- 追问能力：基于 PMID 的相关文献推荐，支持上下文绑定

## 目录结构

```
pubmed-review-skill/
├── README.md
├── SKILL.md
├── .env.example
├── config.example.json
└── scripts/
    ├── pubmed_intent_handler.py    # 自然语言入口
    ├── pubmed_intent_prompt.md     # LLM prompt
    ├── pubmed_followup_handler.py  # 追问处理器
    ├── pubmed_llm_summarize.py     # AI 摘要生成
    ├── run_pubmed_summary.sh       # 综述生成执行脚本
    ├── run_pubmed_review.py         # PubMed 检索+摘要抓取
    ├── add_pubmed_task.py          # 任务创建
    ├── task_dispatcher.py          # 任务调度器
    └── run_processor.sh            # Processor 路由
```

## 安装步骤

### 1. 克隆或解压到目标目录

```bash
git clone <repo_url> pubmed-review-skill
cd pubmed-review-skill
```

### 2. 配置环境变量

```bash
cp .env.example .env.minimax
# 编辑 .env.minimax，填入你的 API Key
```

`.env.example` 内容：
```bash
MINIMAX_API_URL=https://api.minimax.chat/v1/text/chatcompletion_v2
MINIMAX_API_KEY=your_api_key_here
MINIMAX_MODEL=MiniMax-M2.7-highspeed
```

### 3. 配置 cron 任务

```bash
# 每30分钟运行一次调度器
*/30 * * * * cd /path/to/pubmed-review-skill && python3 scripts/task_dispatcher.py >> logs/dispatcher.log 2>&1
```

### 4. 配置飞书通知

系统依赖飞书通知脚本 `notify`，确保它在 PATH 中：

```bash
# 或通过环境变量指定路径
export NOTIFY_PATH=/usr/local/bin/notify
```

## 使用方法

### 自然语言触发

在飞书向 OpenClaw 发送消息：

```
帮我查瘢痕激光 最近5年 综述
婴儿血管瘤 普萘洛尔 临床研究
帮我搜索增生性瘢痕 激光治疗
```

### 支持的限定词

| 类型 | 关键词 | PubMed 格式 |
|------|--------|------------|
| 时间 | 最近5年 / 最近10年 | `last 5 years[dp]` |
| 文献类型 | 综述 / 系统评价 / meta分析 | `review[pt]` 等 |
| 人群 | 儿童 / 成人 | `(child OR infant)` |
| 研究类型 | 临床研究 / 随机对照 | `clinical study` 等 |

### 追问

```
# 带 task_id 追问（精确）
帮我深入讲讲这篇 PMID:12345678

# 不带 task_id（自动使用上次综述的上下文）
帮我推荐更多相关文献
```

## 输出说明

### 飞书推送（brief）

约 200 字结构化摘要，3 条核心结论：

```
· 异维A酸是唯一能实现中重度痤疮治愈或长期缓解的系统治疗药物
· 抑制皮脂分泌、抗炎、免疫调节三重机制协同作用
· 需规范剂量方案、加强监测，以平衡疗效与安全性
```

### 本地文件（full）

`results/pubmed/{task_id}_summary.md`：完整 Markdown 综述，含：
- 研究背景、作用机制、临床应用、疗效与安全性
- 参考文献列表（PubMed 格式 DOI）

## 配置说明

`config.example.json` 中的关键配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `tasks_file` | 任务队列文件 | `./tasks/pubmed_tasks.json` |
| `results_dir` | 结果输出目录 | `./results/pubmed` |
| `max_articles` | 单次检索最大文献数 | `10` |
| `default_max_retries` | 默认最大重试次数 | `5` |

## 依赖项

| 依赖 | 说明 |
|------|------|
| Python 3.8+ | 运行时 |
| PubMed E-utilities | 文献检索（免费，无需 API Key） |
| MiniMax API | AI 综述生成（需 API Key） |
| notify（飞书通知脚本） | 结果推送 |

## 与 OpenClaw 集成

本 skill 可通过 OpenClaw 的 `pubmed_intent_handler` 接收飞书消息，实现自然语言触发。具体集成方式参考 `SKILL.md`。
