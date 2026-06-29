# yufluentcn-ad-optimize

跨境 **Meta / TikTok / Google** 广告投放五维优化教练（定向 → 素材 → 出价 → 落地页 → 数据分析）。经 Yufluent 云端 Harness 执行，本机仅需 `requests`。

## 安装

```powershell
cd skills\yufluentcn-ad-optimize
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts\run.py --dimension bidding --platform meta -m "ROAS 下降，请给预算重组建议" --market Vietnam
```

## 五维

| dimension | 说明 |
|-----------|------|
| targeting | 定向优化 — 找对人 |
| creatives | 素材与文案 — 说对话 |
| bidding | 出价与预算 — 出对价 |
| landing | 落地页与 UX — 接住人 |
| analytics | 数据分析与 A/B — 做对决策 |

完整说明见 [docs/技能-广告投放客户指南.md](../../docs/技能-广告投放客户指南.md)。
