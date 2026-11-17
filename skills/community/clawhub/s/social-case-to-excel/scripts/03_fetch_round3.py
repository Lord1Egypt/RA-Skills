# -*- coding: utf-8 -*-
"""社媒案例库 Round3：补齐薄弱主题 + 扩社区（小社区也要收）。

Reddit 案例分布和 X 不同：真正有数字的复盘集中在**垂类运营社区**（r/AmazonFBA、
r/FulfillmentByAmazon、r/Etsy、r/shopify），泛创业社区（r/Entrepreneur）多是观点帖。
这一轮把社区铺到长尾，并用更口语的词去捞"复盘型"帖子（"what worked" / "lessons" / "update"）。
"""
import cb_mcp

LIMIT = 300
DAYS = 1095          # 红人复盘帖稀疏，窗口放宽到 3 年
OUT = '/tmp/cbx3_all.json'

SPECS = [
    # ---- 长尾社区 · 选品/货源 ----
    ('g1_ali',           'Alibaba',            'supplier OR sourcing OR "find a supplier"', DAYS),
    ('g2_aliexpress',    'Aliexpress',         'supplier OR product OR dropship results', DAYS),
    ('g3_ecom_ec',       'ecommerce',          '"what worked" OR lessons OR "update" store', DAYS),
    ('g4_shopify_dev',   'Shopify',            '"what worked" OR "lessons learned" OR results', DAYS),
    ('g5_printondemand', 'printondemand',      'results OR "first sale" OR profit', DAYS),
    # ---- 长尾社区 · 运营/转化 ----
    ('g6_amazon_seller2', 'AmazonSeller',      '"what worked" OR "lessons" OR "after a year"', DAYS),
    ('g7_fba_grind',     'FulfillmentByAmazon', '"lessons learned" OR mistakes OR results', DAYS),
    ('g8_etsy_full',     'Etsy',               '"first sale" OR "my shop" OR results', DAYS),
    ('g9_cro_subs',      'userexperience',     'CRO OR "A/B test" OR "conversion rate" case', DAYS),
    ('g10_analytics',    'analytics',          '"conversion rate" OR "we tested" OR results', DAYS),
    # ---- 广告 / 增长 ----
    ('g11_adwords',      'adwords',            'case study OR results OR performance', DAYS),
    ('g12_ppc2',         'PPC',                '"what worked" OR "after 6 months" OR case', DAYS),
    ('g13_facebookads',  'FacebookAds',        'case study OR results ROAS OR CPA', DAYS),
    ('g14_socialmedia',  'socialmedia',        'campaign OR results OR "grew" case study', DAYS),
    ('g15_growthhack',   'GrowthHacking',      'case study OR experiment OR results', DAYS),
    # ---- 内容 / SEO 长尾 ----
    ('g16_seo2',         'SEO',                '"what worked" OR "lessons from" OR "case study"', DAYS),
    ('g17_bigseo2',      'bigseo',             'client OR "case study" OR results', DAYS),
    ('g18_blogging',     'blogging',           'case study OR traffic OR "earnings" OR results', DAYS),
    # ---- 小红书/中文出海的对应社区（Reddit 上中文内容极少，收得到才有）----
    ('g19_china_ec',     'China_irl',          '跨境电商 OR 亚马逊 卖家 OR 出海 品牌', DAYS),
    ('g20_tiktokshop',   'TikTokshop',         'seller OR results OR GMV OR sales', DAYS),
]

if __name__ == '__main__':
    cb_mcp.harvest_round([dict(zip(("label", "subreddit", "query", "days"), spec)) for spec in SPECS], OUT, limit=LIMIT, per_label_files='/tmp/cbx3_%s.json')
