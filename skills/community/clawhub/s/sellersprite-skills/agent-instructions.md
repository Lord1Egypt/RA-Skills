# SellerSprite Skills - 卖家精灵 Skills

## 项目概述

基于卖家精灵 MCP Server 提供的 Amazon 数据工具，为跨境电商卖家定制的 AI Skills 集合。

## 两层 Skills 体系

### 战术选品 Skills (`skills/`)

17个精准选品策略卡片，每个对应一个具体选品打法：
- 新品爆发型 (01-02): 新品快速爆发、隐形爆款
- 关键词趋势型 (03-05): ABA增长词、流量分散词、标题密度漏洞
- 产品缺陷型 (06-07): 热销低评分、评论语义分析
- 类目结构型 (08-10): 低品牌垄断、高新品占比、高毛利轻小
- 流量防伪型 (11-12): 自然流量反查、变体拆解
- 边缘捡漏型 (13-17): 本土溢价、FBM拦截、极差Listing、高客单长尾、季节前置

用法：对话中引用 skill 卡片，让 AI 按卡片参数执行。

### 综合分析 Skills (`skills/comprehensive/`)

10个场景化分析命令，通过 `/命令` 调用：
- `/product-research` - 智能选品助手
- `/market-analysis` - 市场全景分析
- `/competitor-analysis` - 竞品深度拆解
- `/keyword-research` - 关键词选品研究
- `/listing-optimizer` - Listing优化诊断
- `/traffic-analysis` - 流量结构分析
- `/opportunity-finder` - 蓝海机会挖掘
- `/review-insights` - 买家评论洞察
- `/pricing-strategy` - 定价策略分析
- `/ad-optimizer` - 广告投放优化

## Python MCP 客户端

```bash
pip install sellersprite-cli
```

```bash
# 设置密钥
sellersprite config --key 你的密钥
```

```python
from sellersprite_cli import SellerSprite
ss = SellerSprite()
result = ss.product_node(keyword="earbuds")
```

## MCP 工具清单 (38个)

ASIN分析: asin_detail, asin_prediction, asin_coupon_trend, asin_detail_with_coupon_trend, keepa_info
商品竞品: product_research, competitor_lookup, product_node
关键词: keyword_miner, keyword_research, keyword_research_trends, keyword_order, bsr_prediction
流量: traffic_keyword, traffic_keyword_stat, traffic_source, traffic_listing_stat, traffic_listing, traffic_extend
市场: market_research, market_research_statistics, market_price_distribution, market_brand_concentration, market_product_concentration, market_seller_concentration, market_rating_distribution, market_ratings_count_distribution, market_listing_date_distribution, market_listing_trend_distribution, market_seller_country_distribution, market_seller_type_concentration, market_ebc_distribution, market_product_demand_trend
ABA/趋势: aba_research_weekly, aba_research_monthly, aba_research_trend, google_trend, review

支持站点(共9个): US(美国), JP(日本), UK(英国), DE(德国), FR(法国), IT(意大利), ES(西班牙), CA(加拿大), IN(印度)