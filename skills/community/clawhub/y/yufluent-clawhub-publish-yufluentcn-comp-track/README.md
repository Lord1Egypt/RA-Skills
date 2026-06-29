# yufluentcn-comp-track

竞品 Listing 快照对比 — 粘贴竞品文案，AI 从标题/五点/描述/关键词多维度对标，输出差异化建议。

## 安装

```powershell
cd skills\yufluentcn-comp-track
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY、TOKENAPI_BASE_URL
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选，默认 `http://localhost:8080/v1`）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

# 内联竞品文案
python scripts\run.py --our-product "无线蓝牙耳机" --competitor "竞品标题: ... 五点: ..." --platform amazon --lang zh

# 从文件读取竞品文案
python scripts\run.py --our-product "便携式咖啡机" --competitor .\competitor.txt --platform shopify --lang en
```

## 批量对比

多条竞品批量分析 → 请使用 `yufluentcn-comp-scrape`（支持 CSV 导入）。

Harness scene：`comp_alert` · API：`POST /v1/skills/comp-track/run` · 技能名：`yufluentcn-comp-track`
