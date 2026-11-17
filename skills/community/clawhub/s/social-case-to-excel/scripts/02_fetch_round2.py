# -*- coding: utf-8 -*-
"""社媒案例库 Round2：更贴「证据口径」的检索式（数字 / 金额 / 复盘）。

与 Round1 的区别：Round1 铺社区，Round2 压**可量化结果**的词（revenue / profit / per month /
"$" / ACOS / ROAS / 复盘）。Reddit 上的案例帖往往是长篇复盘，社区选得对（r/AmazonFBA 这类）
比词写得花更重要。
"""
import cb_mcp

LIMIT = 300
DAYS = 730
OUT = '/tmp/cbx2_all.json'

SPECS = [
    # ---- 金额/月度复盘（选品 + 运营）----
    ('f1_amz_num',       'AmazonFBA',          '"this month" OR "per month" revenue OR profit', DAYS),
    ('f2_amz_mystore',   'AmazonFBA',          '"my store" OR "our brand" revenue OR sales', DAYS),
    ('f3_pl_review',     'FulfillmentByAmazon', 'private label review OR results OR "a year"', DAYS),
    ('f4_ec_review',     'ecommerce',          '"case study" OR "we did" OR "after 12 months" revenue', DAYS),
    # ---- 黑五复盘 ----
    ('f5_bfcm_review',   'shopify',            '"black friday" OR BFCM "we made" OR record', DAYS),
    ('f6_bfcm_email',    'EmailMarketing',     'BFCM OR "black friday" flow OR campaign results', DAYS),
    # ---- 关键词 / SEO ----
    ('f7_kw_amz',        'AmazonFBA',          '"search term" OR backend OR "search terms report" rank', DAYS),
    ('f8_kw_tools',      'SEO',                '"keyword research" workflow OR process OR tool', DAYS),
    ('f9_kw_gap',        'bigseo',             '"keyword gap" OR "ranked" OR "traffic" case study', DAYS),
    # ---- Listing / CRO ----
    ('f10_listing_img',  'AmazonFBA',          '"main image" OR "listing images" conversion', DAYS),
    ('f11_cro_shopify',  'shopify',            'CRO OR "A/B test" OR "conversion rate" increase', DAYS),
    ('f12_etsy_cvr',     'EtsySellers',        'conversion OR views OR sales increase listing', DAYS),
    # ---- 站外 / 广告 ----
    ('f13_ppc_amz',      'AmazonFBA',          '"sponsored products" OR PPC ACOS OR TACOS', DAYS),
    ('f14_ppc_google',   'PPC',                '"google ads" OR "ad spend" ROAS OR CPA', DAYS),
    ('f15_ugc_creator',  'socialmedia',        'UGC OR creator OR influencer ROAS OR revenue', DAYS),
    ('f16_affiliate',    'Affiliatemarketing', 'affiliate OR "affiliate program" revenue OR results', DAYS),
    # ---- Reddit 营销 ----
    ('f17_reddit_ads',   'PPC',                '"reddit ads" OR "advertise on reddit" CPA OR conversions', DAYS),
    ('f18_reddit_ent',   'Entrepreneur',       '"reddit marketing" OR "reddit traffic" sales OR customers', DAYS),
]

if __name__ == '__main__':
    cb_mcp.harvest_round([dict(zip(("label", "subreddit", "query", "days"), spec)) for spec in SPECS], OUT, limit=LIMIT, per_label_files='/tmp/cbx2_%s.json')
