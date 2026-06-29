# yufluentcn-comp-scrape

竞品批量对比（v1：CSV 或已授权 API 导出），经 Harness `comp_scrape` 云端执行。本机仅需 `requests`。

**非未授权爬虫** — 仅分析用户上传的 CSV/导出或已授权 API 快照。

## 安装

```powershell
cd skills\yufluentcn-comp-scrape
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

# CSV 内联
python scripts/run.py --our-product "蓝牙耳机" --competitor-data "title,price`nComp A,29.99" --platform amazon --lang zh

# 从 CSV 文件
python scripts/run.py --our-product "USB-C Hub" --competitor-data .\competitors.csv --source-type csv_export
```

单条竞品快照对比请用 `yufluentcn-comp-track`。

Harness scene：`comp_scrape` · API：`POST /v1/skills/comp-scrape/run`
