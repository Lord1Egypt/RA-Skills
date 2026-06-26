# Team Efficiency Daily Report Skill

自动生成 **团队效能数据日报** 的 OpenClaw Skill。

该 Skill 会自动访问团队效能报表系统，通过浏览器修改时间筛选条件，抓取关键效能指标数据，并生成每日效能分析报告。

生成的日报包含：

1. 当天交付的需求情况（产品需求数、最长交付时长、平均交付时长、达成 211 的占比及明细）
2. 目前交付中的主 R 产品需求列表（需求 ID、名称、当前状态、开始开发时间、已耗时、预计剩余时间）
3. 目前交付中创建超过 14 天的产品子任务列表（按创建时间正序排列）

最终输出 **Markdown 格式日报**，可用于：

- 团队每日效能同步
- 需求交付监控
- 管理层交付汇报

---

## 快速开始

### 1. 配置报表

编辑 `config.json`，填入效能报表的 URL 和数据接口：

```json
{
  "reports": [
    {
      "name": "当天交付需求",
      "url": "https://your-dashboard-url",
      "dataAPI": "https://your-data-api-url",
      "needModify": true,
      "column": {
        "teamId": "需求ID",
        "name": "需求名称",
        "totalDays": "总耗时(天)",
        "owner": "负责人"
      }
    }
  ]
}
```

`needModify: true` 表示该报表需要将时间范围修改为昨天。

### 2. 运行

```bash
pnpm start
```

---

## 数据存储

每天采集的数据保存为 `data/YYYY-MM-DD.json`，生成的日报保存为 `report/YYYY-MM-DD.md`。

---

## 目录结构

```
team-efficiency-daily-report/
├── SKILL.md
├── README.md
├── package.json
├── tsconfig.json
├── config.example.json          # 报表配置（需自行填写）
├── src/
│   ├── index.ts         # 主入口
│   └── utils/
│       ├── api.ts       # 数据接口抓取
│       ├── parser.ts    # 数据解析
│       └── report.ts    # 日报生成

```

---

## 定时自动运行（推荐）

通过 cron 每天自动生成日报：

```bash
crontab -e
```

添加：

```
0 9 * * * cd /path/to/skills/team-efficiency-daily-report && pnpm start
```

---

## 技术栈

| 模块 | 技术 |
|------|------|
| 浏览器自动化 | Puppeteer |
| 数据抓取 | XHR 拦截 |
| 数据存储 | JSON |
| 报告生成 | Markdown |
