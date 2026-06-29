# 库存驾驭（yufluentcn-inventory-pilot）

Harness scene: `inventory_forecast` · API: `POST /v1/skills/inventory-pilot/run`

基于卖家提供的销量/库存数据做预测、补货建议、滞销预警与资金占用分析。本机仅需 `requests`。

## 安装

```bash
cd skills/yufluentcn-inventory-pilot
pip install -r requirements.txt
# 设置 TOKENAPI_KEY、TOKENAPI_BASE_URL
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选，默认 `http://localhost:8080/v1`）

## 调用

```bash
$env:TOKENAPI_KEY = "***"
python scripts/run.py -m "预测下个月销量" --mode forecast --sales-data sales.csv
```

Monorepo 测试：`pip install -r requirements-dev.txt && pytest tests/`
