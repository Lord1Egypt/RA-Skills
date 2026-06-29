# yufluentcn-product-pick

选品分析（Amazon / TikTok Shop / 速卖通）：BSR、价格、评论、利润与竞争度 AI 打分，筛选蓝海、规避备货风险。经 Harness `product_pick` 云端执行。

**推荐流程**：Browser Service 提取 Listing/SERP → 本技能打分 → 老板决策 go/watch/no-go。

## 安装

```powershell
cd skills\yufluentcn-product-pick
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts/run.py --niche "便携榨汁杯" --product-candidates .\market_data.txt --lang zh
```

Harness scene：`product_pick` · API：`POST /v1/skills/product-pick/run`
