# arXiv 每日论文控制面板

## 配置文件

- [[arxiv-daily/config.yaml]]
- 脚本：[[arxiv-daily/scripts/arxiv_daily.py]]
- 日志目录：[[arxiv-daily/logs]]

## 手动运行

在 PowerShell 中从 Vault 根目录运行：

```powershell
.\arxiv-daily\scripts\arxiv_daily.ps1
```

只测试不写入：

```powershell
.\arxiv-daily\scripts\arxiv_daily.ps1 -DryRun
```

## 最近 30 天新增论文

```dataview
TABLE field, published, updated, status, summary_status
FROM "arxiv-daily/papers"
WHERE type = "arxiv-paper" AND archived = false AND created >= date(today) - dur(30 days)
SORT updated DESC
LIMIT 100
```

## 待读论文

```dataview
TABLE field, published, summary_status
FROM "arxiv-daily/papers"
WHERE type = "arxiv-paper" AND status = "new" AND archived = false
SORT published DESC
```

## 已归档论文

```dataview
TABLE field, published, updated, archived
FROM "arxiv-daily/archive/papers"
WHERE type = "arxiv-paper"
SORT updated DESC
LIMIT 30
```
