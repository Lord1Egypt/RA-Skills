# 看板与数据接口参考

## RedBI 看板

- **看板 URL：** `https://redbi.devops.xiaohongshu.com/dashboard/list?dashboardId=45500&pageId=page_pWvbwhxFPz&projectId=4`
- **看板名称：** 家清人群宇宙看板
- **数据更新：** 每日自动更新

## 关键 analysisId

| analysisId | 图表名称 | 说明 |
|-----------|---------|------|
| 42623804 | 广告主人群宇宙投放分析 | 人群宇宙各广告主消耗、CTR、I+TI、进店率、进店成本 |
| 42626327 | 整体种草投放情况 | 整体种草各广告主同上指标 |
| 42703713 | 整体种草消耗走势 | 整体种草近10周走势 |
| 42626064 | 广告主x人群包x笔记分析new | 人群宇宙笔记+人群包效果明细 |
| 42701238 | 宇宙人群包投放分析 | 人群包维度消耗、CTR、I+TI 等 |
| 42704593 | YTD人群宇宙整体投放效果 | YTD汇总数据 |
| 42705927 | YTD整体种草投放效果 | YTD整体种草汇总 |

## 下载任务流程

1. 在看板页面点击图表右上角 `...` → 导出
2. 查询任务状态：`POST /api/download/task/list`（返回 downloadTasks 列表）
3. 从 `fileUrl` 下载 CSV：`https://datatools.xhscdn.com/exporter/...`

```bash
# 查询最新下载任务
COOKIE=$(bash /app/skills/data-fe-common-sso/script/run-sso.sh "$WORKSPACE")
curl -s -X POST "https://redbi.devops.xiaohongshu.com/api/download/task/list" \
  -H "Cookie: $COOKIE" \
  -H "Content-Type: application/json" \
  -d '{"pageNo":1,"pageSize":10}' | python3 -c "
import json,sys
d=json.load(sys.stdin)
for t in d['data']['downloadTasks']:
    print(t['taskName'],'|',t['status'],'|',t.get('fileUrl','')[:80])
"
```

## CSV 正确读取方式

CSV 下载后必须用 `csv.DictReader` 读取，不能直接用 `pd.read_csv`（会导致列名识别错误）：

```python
import csv, pandas as pd

def read_csv_safe(path):
    rows = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return pd.DataFrame(rows)
```

## 关键字段说明

| 字段名 | 说明 |
|--------|------|
| 策略消耗（复记） | YTD 消耗金额（元），需 /10000 转换为万元 |
| CTR | 点击率（小数形式，如 0.1 = 10%） |
| I+TI转化率 | 互动+品牌兴趣转化率 |
| 淘宝进店率 | 淘宝进店率（小数形式） |
| 淘宝进店成本 | 元/人 |
