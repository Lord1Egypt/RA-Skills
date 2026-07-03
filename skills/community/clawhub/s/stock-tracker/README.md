# Stock Tracker - 东方财富自选股公告追踪

自动追踪东方财富自选股公告，三级过滤 + LLM 分类摘要 + Web 仪表盘。支持 Agent 定时推送和手动查看。

> 通过 ClawHub 安装：`clawhub install stock-tracker`

---

## 快速开始

### 1. 安装依赖

```bash
cd /path/to/stock-tracker
pip install requests pdfplumber flask
```

### 2. 配置 Cookie

浏览器登录 [东方财富自选股](https://quote.eastmoney.com/zixuan/lite.html)，F12 → Console → `copy(document.cookie)`，粘贴到 `cookie.txt`。

自动续签：`pip install playwright && playwright install chromium && python3 scripts/refresh_cookie.py`

### 3. 配置 LLM（可选）

```bash
echo "LLM_API_KEY=sk-your-api-key" > .env
```

`config.json` 中配置模型地址等参数（默认使用 DeepSeek V4 Flash）。未配置时自动禁用 LLM，仅使用正则过滤。

### 4. 验证运行

```bash
python3 scripts/stock_tracker.py --group test --days 15 --fetch-content
python3 scripts/stock_tracker.py --stats
```

---

## 两种模式

### Agent Run 模式

告诉 agent：`"每天8点提醒我有价值的自选股公告"`

或手动运行：

```bash
bash run.sh mygroup 15 eastmoney
```

输出 digest 到 stdout（agent 读取转发），无公告时输出 `DIGEST_EMPTY:...`。

### Dashboard 模式

告诉 agent：`"帮我打开公告仪表盘，看看 mygroup 板块最近15天的情况"`

或手动运行：

```bash
bash dashboard.sh mygroup 15 eastmoney
```

自动执行：抓取 → 摘要 → 启动 Web 仪表盘（`http://localhost:5001`），支持 CSV 导出，Ctrl+C 停止。

---

## 常用命令

```bash
python3 scripts/stock_tracker.py --stats                 # 数据库统计
python3 scripts/stock_tracker.py --list                  # 最近公告
python3 scripts/stock_tracker.py --list --stock 600519   # 指定股票
python3 scripts/stock_tracker.py --list-groups           # 可用分组
python3 scripts/stock_tracker.py --clean                 # 清洗正文
```

---

## 文件结构

```
stock-tracker/
  SKILL.md              # Agent 入口文档
  README.md             # 本文档
  config.json           # LLM 配置
  cookie.txt            # 东方财富 Cookie
  .env                  # LLM API Key
  run.sh                # Agent Run 模式
  dashboard.sh          # Dashboard 模式
  scripts/              # Python 脚本
    stock_tracker.py    # 主入口
    eastmoney_api.py    # 东方财富 API
    cninfo_api.py       # 巨潮资讯 API
    ann_detail.py       # 公告详情获取
    llm_judge.py        # LLM 标题判断
    text_cleaner.py     # 正文清洗
    daily_summary.py    # 摘要生成
    db.py               # 数据库操作
    dashboard.py        # Flask 仪表盘
    refresh_cookie.py   # Cookie 自动续签
    dependencies.py     # 依赖管理
    error_handler.py    # 错误处理
    config_manager.py   # 配置管理
  tests/                # 单元测试
  logs/                 # 运行日志
  .stock-tracker-state/ # SQLite 数据库
  references/           # 技术参考文档
```

---

## 配置

### config.json

```json
{
  "llm": {
    "enabled": true,
    "base_url": "https://opencode.ai/zen/go/v1",
    "model": "deepseek-v4-flash",
    "timeout": 60,
    "retries": 2
  }
}
```

### .env

```
LLM_API_KEY=sk-your-api-key-here
```

### 数据源

默认全部走东方财富 API（A股+港股）。指定 `--source cninfo` 时 A 股走巨潮资讯网（PDF 更稳定），港股仍走东方财富。

## 数据库字段

| 字段 | 说明 |
|------|------|
| `ann_id` | 公告唯一标识 |
| `stock_code` | 股票代码 |
| `stock_name` | 股票名称 |
| `title` | 公告标题 |
| `ann_date` | 公告日期 |
| `ann_type` | 公告类型 |
| `url` | 公告链接 |
| `art_code` | 文章编码 |
| `full_text` | 原始正文 |
| `clean_text` | 清洗后正文 |
| `status` | 状态（valuable/filtered） |
| `ann_type_tag` | 小类标签 |
| `ann_type_category` | 大类标签 |
| `display_time_dfcf` | 东方财富显示时间 |
| `summary` | LLM 摘要 |
| `first_seen_at` | 首次抓取时间 |

## 单元测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行特定模块测试
python3 -m pytest tests/test_text_cleaner.py -v
python3 -m pytest tests/test_llm_judge.py -v
python3 -m pytest tests/test_db.py -v
```

当前共 107 个单元测试，覆盖所有核心模块。

---

## 依赖

- Python 3.9+ / requests / pdfplumber / flask / sqlite3
- playwright（可选，Cookie 自动续签）

---

## 公告过滤规则

三级过滤体系自动跳过低价值公告：

**第一级：正则过滤**（标题匹配，全文采集前）
- 公司章程、信用评级、募集说明书
- 债券程序性公告（付息、上市、摘牌、发行结果等）
- 董事会报告、法律意见书
- 股东会决议公告、投票表决结果
- 薪酬制度、周年会通告
- 担保类公告（提供担保、为xx担保、合计xx担保等）
- 公司内部制度文件（管理制度、议事规则、工作细则等）
- 回购注销+股权激励/限制性股票
- 业绩说明会/业绩发布会
- 限制性股票/股票期权预留授予、完成登记
- 限制性股票作废（量小无市场影响）

**第二级：LLM 价值判断**（全文采集后）
- AI 判断公告是否包含实质经营信息
- 按8大类64小类自动分类

**第三级：LLM 摘要生成**（仅保留的公告）
- 自动生成结构化摘要

用户可随时指定新的过滤类型，自动添加到正则规则中。

---

## 技术参考

详细文档见 `references/` 目录：

- [系统架构](references/architecture.md) — 数据流、模块详解、过滤策略
- [公告分类体系](references/classification.md) — A股8大类64小类 + 港股7大类41小类
- [Token消耗分析](references/token-cost.md) — LLM 调用成本优化
- [正文清洗规则](references/text-cleaning.md) — 14类清洗规则详解
