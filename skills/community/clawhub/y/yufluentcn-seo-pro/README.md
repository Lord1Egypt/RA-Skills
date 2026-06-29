# yufluentcn-seo-pro

跨境电商 **Amazon / Shopify / TikTok Shop** 关键词扩展与 SEO 投放建议（JSON 报告），经 Harness `seo_keywords` 云端执行。本机仅需 `requests`。

## 安装

```powershell
cd skills\yufluentcn-seo-pro
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts\run.py `
  --product "无线耳机" `
  --keywords "降噪,蓝牙,运动" `
  --competitor-keywords "anc earbuds" `
  --platform amazon `
  --market "美国" `
  -o seo-report.json
```

## 文档

- **Agent / OpenClaw**：[SKILL.md](./SKILL.md)（方法论 + 关键词策略 + 工作流）
- **卖家**：[docs/技能-SEO关键词客户指南.md](../../docs/技能-SEO关键词客户指南.md)

Harness scene：`seo_keywords` · API：`POST /v1/skills/seo-pro/run`
