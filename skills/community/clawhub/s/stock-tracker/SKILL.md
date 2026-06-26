---
name: "stock-tracker"
version: "2.0.0"
description: "东方财富自选股公告追踪。三级过滤 + LLM分类摘要 + Web仪表盘，支持 agent 定时推送。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "python": "3.9+" },
        "install":
          [
            {
              "id": "deps",
              "kind": "shell",
              "command": "cd {{SKILL_DIR}} && pip install requests pdfplumber flask",
              "label": "Install Python dependencies",
            },
          ],
      },
  }
---

# 📊 Stock Tracker - 东方财富自选股公告追踪

**双模式技能** — Agent 定时自动追踪 + 用户 Web 仪表盘查看。

告诉 agent 你想做什么，例如：

> "帮我看看持仓板块这两天有什么重要公告"
> "每天8点提醒我有价值的自选股公告"
> "帮我打开公告仪表盘看看"

## 模式一：Agent Run 模式

Agent 定时运行 `run.sh`，自动抓取公告、生成摘要，输出有价值公告的 digest 转发给用户。

告诉 agent 即可：

> "帮我设置 stock-tracker 定时任务，每天早上8点运行一次，追踪【xx】板块的最新公告，有重要公告通知我"

或者手动运行：

```bash
# 用法: bash run.sh [group] [days] [source]
bash run.sh mygroup 15 eastmoney
```

### 输出示例

**有公告时：**
```
DIGEST_TOTAL:3
1.
【000001平安银行】-【平安银行2026年第一季度报告】
【季度报告】...

2.
【600519贵州茅台】-【贵州茅台关于回购股份的进展公告】
累计回购金额XX亿元...
```

**无公告时：**
```
DIGEST_EMPTY:最近1天test板块无高价值公告
```

---

## 模式二：Dashboard 模式

用户手动运行，抓取公告 + 生成摘要 + 启动 Web 仪表盘，浏览器查看所有公告详情。

告诉 agent 即可：

> "帮我跑 stock-tracker 的 dashboard 模式，抓取 mygroup 板块最近15天的公告并打开仪表盘"

或者手动运行：

```bash
# 用法: bash dashboard.sh [group] [days] [source]
bash dashboard.sh mygroup 15 eastmoney
```

脚本自动执行三步：
1. `stock_tracker.py --fetch-content` — 抓取公告 + 全文 + LLM 分类
2. `daily_summary.py` — 生成摘要
3. `dashboard.py` — 启动 Flask 仪表盘（默认端口 5001）

启动后浏览器访问 `http://localhost:5001`，按 Ctrl+C 停止。

**仪表盘功能：**
- 股票列表表格：7天/15天/30天/全部的有价值公告比例
- 点击展开：懒加载公告详情（标题、日期、摘要、正文、原文链接）
- 类型标签：`大类 / 小类`（如 `股权股本类 / 回购`）
- 搜索过滤，响应式设计

---

## 首次设置

告诉 agent 即可：

> "帮我初始化 stock-tracker，安装依赖、配置 Cookie 和 LLM"

或者按以下步骤手动设置：

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/stock-tracker
pip install requests pdfplumber flask
```

### 2. 配置 Cookie

东方财富网页版登录后的 Cookie，用于获取自选股列表。

1. 浏览器打开 [https://quote.eastmoney.com/zixuan/lite.html](https://quote.eastmoney.com/zixuan/lite.html) 并登录
2. F12 → Console → 输入 `copy(document.cookie)` 回车
3. 粘贴到 `cookie.txt`

**自动续签（可选）：**
```bash
pip install playwright && playwright install chromium
python3 scripts/refresh_cookie.py
```

### 3. 配置 LLM（可选）

LLM 用于标题价值判断、公告分类和摘要生成。未配置时仅使用正则过滤。

```bash
# .env 文件
echo "LLM_API_KEY=sk-your-api-key" > .env
```

```json
// config.json
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

### 4. 验证运行

```bash
python3 scripts/stock_tracker.py --group test --days 15 --fetch-content
python3 scripts/stock_tracker.py --stats
```

### 5. 配置定时任务

告诉 agent 即可，例如：

> "帮我设置 stock-tracker 定时任务，每天早上8点运行一次，追踪【xx】板块的最新公告，有重要公告通知我"

或者手动配置：

```bash
openclaw cron add \
  --name stock-tracker \
  --cron "0 1 * * *" \
  --message "运行股票公告扫描：cd {{SKILL_DIR}} && bash run.sh mygroup 15 eastmoney"
```
---

完整技术文档、公告分类体系、Token 消耗分析等详见 [GitHub](https://github.com/54Lynnn/stock-tracker)

## 开源

- **GitHub**: [github.com/54Lynnn/stock-tracker](https://github.com/54Lynnn/stock-tracker)
