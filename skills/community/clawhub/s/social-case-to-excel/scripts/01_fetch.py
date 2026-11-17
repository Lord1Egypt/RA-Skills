# -*- coding: utf-8 -*-
"""社媒案例库 Round1：Reddit 种子轮（六条线 × 主要社区）。

数据源：Reddit MCP（`cb_mcp.py`）。检索是**社区内**搜索 —— 每个组合 =
一个 subreddit + 一句关键词 + 一个相对天数窗，没有全站搜索（`subreddit:"all"` 恒空），
所以"铺开覆盖面"靠**加 subreddit × 加词**，不是靠一句大 OR 检索式。

检索式口径与旧版一致：**动作词**（case study / what worked / we scaled / results / tested）
比**热度词**重要 —— 只按热度抓会抓到大量观点帖和引流帖。

落盘：`/tmp/cbx1_all.json`，标准形状 `{label: {keyword, subreddit, days, tweets:[规范字段]}}`
（`harvest_round()` 内部已调 `norm_post()` 归一化）。
"""
import cb_mcp

LIMIT = 300      # 服务端上限；oldest-first 排序下命中触顶会丢最新的，见 cb_mcp.py 头部
DAYS = 730
OUT = '/tmp/cbx1_all.json'

# (label, subreddit, query, days)
SPECS = [
    # ---- 选品 ----
    ('e1_research_fba',      'AmazonFBA',          '"product research" OR "winning product" OR "my first product"', DAYS),
    ('e2_research_fba2',     'FulfillmentByAmazon', '"product research" OR sourcing OR supplier', DAYS),
    ('e3_research_ec',       'ecommerce',          'found a product OR winning product OR niche research', DAYS),
    ('e4_research_dropship', 'dropship',           '"product research" OR "winning product" OR tested', DAYS),
    # ---- 黑五营销 ----
    ('e5_bfcm_ec',           'ecommerce',          '"black friday" OR BFCM OR "cyber monday"', DAYS),
    ('e6_bfcm_shopify',      'shopify',            '"black friday" OR BFCM results', DAYS),
    ('e7_bfcm_marketing',    'marketing',          'BFCM OR "black friday" email OR SMS campaign', DAYS),
    # ---- 关键词 ----
    ('e8_kw_fba',            'AmazonFBA',          '"keyword research" OR "search terms" OR indexing', DAYS),
    ('e9_kw_seo',            'SEO',                '"keyword research" case study OR "we ranked"', DAYS),
    ('e10_kw_bigseo',        'bigseo',             '"keyword research" OR "content gap" OR "we ranked"', DAYS),
    # ---- Listing 运营 ----
    ('e11_listing_fba',      'AmazonFBA',          '"main image" OR "listing optimization" OR "A+ content"', DAYS),
    ('e12_listing_seller',   'AmazonSeller',       'listing optimization OR "conversion rate" OR PPC', DAYS),
    ('e13_listing_etsy',     'EtsySellers',        'listing optimization OR "conversion rate" OR photos', DAYS),
    # ---- 站外运营 ----
    ('e14_offsite_ec',       'ecommerce',          'influencer OR UGC OR affiliate OR "creator"', DAYS),
    ('e15_offsite_ppc',      'PPC',                'case study OR "we tested" OR results ROAS', DAYS),
    ('e16_offsite_email',    'EmailMarketing',     'flow OR "revenue" OR "we made" OR results', DAYS),
    # ---- Reddit 营销 ----
    ('e17_reddit_marketing', 'marketing',          '"reddit ads" OR "reddit marketing" OR "advertise on reddit"', DAYS),
    ('e18_reddit_ent',       'Entrepreneur',       '"reddit ads" OR "reddit marketing" OR "we got customers"', DAYS),
]

if __name__ == '__main__':
    cb_mcp.harvest_round([dict(zip(("label", "subreddit", "query", "days"), spec)) for spec in SPECS], OUT, limit=LIMIT, per_label_files='/tmp/cbx1_%s.json')
