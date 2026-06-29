# yufluentcn-shopify-operator

Shopify **全店运营** 教练 — 六阶段指导型 Harness 技能（选品 → 寻源 → 上架 → 装修 → 社媒 → 监控）。覆盖新店启动与已开业店铺的扩品、优化与复盘。

## 安装

```powershell
cd skills\yufluentcn-shopify-operator
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY、TOKENAPI_BASE_URL
```

## 调用

```powershell
# 老店复盘
python scripts\run.py --stage monitoring -m "转化率偏低，请给优化检查表" --store-url "https://xxx.myshopify.com"

# 新店选品
python scripts\run.py --stage sourcing -m "宠物用品店，请给调研表结构" --niche "pet accessories"
```

## 与其他技能配合

| 阶段 | 可联动技能 |
|------|------------|
| listing | `yufluentcn-ecommerce-listing` — 生成 Shopify JSON 产品文案 |
| monitoring | `yufluentcn-comp-track`、`yufluentcn-review-intel` — 竞品与评论洞察 |
| listing / monitoring | `yufluentcn-seo-pro` — 关键词布局 |
