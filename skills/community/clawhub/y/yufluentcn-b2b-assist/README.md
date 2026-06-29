# yufluentcn-b2b-assist

B2B 询盘回复与 RFQ 报价（JSON），经 Harness `b2b_inquiry` 云端执行。本机仅需 `requests`。

## 安装

```powershell
cd skills\yufluentcn-b2b-assist
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts/run.py `
  --message "Please quote 500 units FOB Shenzhen" `
  --product "Bluetooth Speaker" `
  --moq 500 `
  --fob-price "USD 12.50" `
  --lead-time "30 days" `
  --lang en
```

Harness scene：`b2b_inquiry` · API：`POST /v1/skills/b2b-assist/run`
