# Team Quality Daily Report Skill

自动生成 **团队质量数据日报** 的 OpenClaw Skill。

该 Skill 会自动访问团队质量报表系统，通过浏览器修改时间筛选条件，抓取关键质量指标数据，并生成每日质量分析报告。

生成的日报包含：

1. 每个质量维度的当日数据
2. 与昨日数据的变化对比
3. 团队质量趋势总结

最终输出 **Markdown 格式日报**，可用于：

- 团队每日质量同步
- 项目质量监控
- 管理层质量汇报

---

## 快速开始

### 1. 配置报表

编辑 `config.json`，填入质量报表的 URL 和数据接口：

```json
{
  "reports": [
    {
      "url": "https://your-dashboard-url",
      "dataAPI": "https://your-data-api-url",
      "column": {
        "qualityScore": "质量分",
        "bugRate": "千行bug率",
        "onlineBugs": "线上缺陷"
      }
    }
  ]
}
```

### 2. 运行

```bash
pnpm start
```

系统会自动打开浏览器、访问报表、抓取数据、生成日报。

---

## 系统流程

```
启动 Skill
   │
   ▼
连接已有 Chrome 浏览器（复用登录态）
   │
   ▼
读取 config.json 中的报表配置
   │
   ▼
访问报表页面，监听数据接口请求
   │
   ▼
修改时间参数，重新请求接口
   │
   ▼
解析数据，保存 JSON
   │
   ▼
与昨日数据对比
   │
   ▼
生成质量日报 Markdown
```

---

## 时间查询规则

所有报表统一使用以下时间范围：

```
开始时间：本月第一天
结束时间：当前日期
```

---

## 数据存储

每天采集的数据保存为 `~/openclaw-skill-data/team-quality-daily-report/YYYY-MM-DD.json`，
生成的日报保存为 `~/openclaw-skill-data/team-quality-daily-report/YYYY-MM-DD.md`。

---

## 目录结构

```
team-quality-daily-report/
├── SKILL.md
├── README.md
├── package.json
├── tsconfig.json
├── config.example.json          # 配置示例json，报表配置（需自行填写）
├── src/
│   ├── index.ts         # 主入口
│   └── utils/
│       ├── api.ts       # 数据接口抓取
│       ├── parser.ts    # 数据解析
│       ├── compare.ts   # 数据对比
└───────└── report.ts    # 日报生成

```

---

## 定时自动运行（推荐）

通过 cron 每天自动生成日报：

```bash
crontab -e
```

添加：

```
0 9 * * * cd /path/to/skills/team-quality-daily-report && pnpm start
```

---

## 技术栈

| 模块 | 技术 |
|------|------|
| 浏览器自动化 | Puppeteer |
| 数据抓取 | XHR 拦截 |
| 数据存储 | JSON |
| 报告生成 | Markdown |
