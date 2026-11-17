# 新闻流事件驱动选股系统 (wq-news-event-driven-stock-pick)

接收财经新闻输入，通过百度千帆 API 进行事件 NLP 分析，关联受益 A 股标的，输出事件驱动选股信号。

## 功能

- **AI 新闻分析引擎**：对接百度千帆 LLM（默认 ernie-4.5-turbo-128k），将财经新闻转换为结构化投资信号
- **事件分类体系**：政策 / 财报 / 行业 / 公司 / 宏观五类事件识别
- **信号强度评级**：强（直接受益，主营占比>30%）/ 中（间接受益，供应链关联）/ 弱（情绪面受益，概念相关）
- **受益标关联**：输出股票代码、名称、受益逻辑、信号强度
- **风险提示 + 综合研判**：始终标注数据来源与分析置信度
- **降级机制**：千帆 API 不可用时自动切换当前模型内联分析

## 分析流程

```bash
# 传入新闻文本分析（推荐）
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py -t "新闻内容..."

# 或通过 stdin 传入
echo '新闻内容...' | python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py
```

脚本返回结构化 JSON（事件类型/摘要/受影响板块/受益标的/风险/综合信号），格式化为 Markdown 报告输出。

## 事件分类体系

| 类型 | 代号 | 示例 |
|------|------|------|
| 政策类 | policy | 降准降息、产业政策、监管新规 |
| 财报类 | earnings | 业绩超预期/不及预期、预告修正 |
| 行业类 | industry | 供需变化、价格异动、技术突破 |
| 公司类 | company | 并购重组、股权变动、高管变更 |
| 宏观类 | macro | GDP/CPI/PMI 数据、国际经贸 |

详见 `references/event_taxonomy.md`。

## Web Dashboard（事件驱动交易台）

系统包含可视化 Web 前端，已部署于 `racingai.top/event-driven`（ECS + systemd + nginx）。

```
浏览器 (HTML+JS) → Python http.server (:5566) → news_analyzer.py → 千帆API
```

- 前端：事件驱动交易台 HTML（七层全链路分析面板）
- 后端：`server.py` 纯标准库 HTTP 服务（ECS 为 Python 3.6.8，零外部依赖）
- 分析引擎：`scripts/news_analyzer.py`

详细架构与部署见 `references/web-dashboard-setup.md`。

## 目录结构

```
clawhub/
├── SKILL.md                        # 技能主文件（分析流程/事件体系/部署/陷阱）
├── references/
│   ├── event_taxonomy.md           # 事件分类体系详解
│   └── web-dashboard-setup.md      # Web Dashboard 架构与部署
├── scripts/
│   └── news_analyzer.py            # 千帆 API 新闻分析引擎（读环境变量，无硬编码密钥）
├── templates/
│   └── output_template.md          # 分析报告输出模板
├── README.md                       # 本文件（中文说明）
└── README.en.md                    # 英文说明
```

## 安全说明

- `scripts/news_analyzer.py` 通过环境变量读取千帆 API Key（`QIANFAN_API_KEY`），**未设置时脚本报错退出**，不内置任何密钥
- 服务器 IP 已脱敏为 `<SERVER_IP>` 占位符

## 安装

1. 将本技能目录放入 `~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/`
2. 配置环境变量 `QIANFAN_API_KEY`（千帆 API Key）
3. Hermes Agent 自动发现技能，用户在"新闻流事件驱动选股"群发送财经新闻即自动触发
