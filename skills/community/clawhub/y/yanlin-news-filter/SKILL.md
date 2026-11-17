---
name: yanlin-news-filter
description: 研林Skill — 财经新闻采集+关键事件筛选过滤，只保留有实质影响的事件
---

# 研林 · 新闻过滤 (yanlin-news-filter)

## 功能
1. **财经新闻采集** — 从公开财经资讯源获取当日新闻
2. **关键事件筛选** — 过滤无效/低影响力新闻，只保留有实质影响的事件
3. **事件重要性分级** — 对每事件标注影响等级（⭐⭐⭐⭐⭐）
4. **关联行业映射** — 将事件自动映射到对应行业/赛道

## 筛选规则
- ✅ **保留（高优先级）：** 货币政策/监管政策/重磅产业政策/龙头公司重大公告/地缘政治事件/经济数据发布
- ✅ **保留（中优先级）：** 行业供需数据/技术突破/涨价信息/大额订单
- ❌ **过滤（低优先级）：** 日常人事变动/例行股东大会/常规分红/个股日常波动/娱乐八卦

## 调用方式
```bash
python3 {baseDir}/scripts/filter_news.py [--date YYYY-MM-DD] [--output json|text]
```

## 输出示例
```json
{
  "date": "2026-07-03",
  "events": [
    {
      "title": "存储芯片'供应严重短缺'，PC及内存硬盘价格持续高位",
      "source": "新浪财经",
      "importance": 5,
      "category": "行业供需",
      "related_sectors": ["存储芯片", "消费电子", "半导体"],
      "is_marginal": true,
      "market_expectation": "此前市场预期Q3备货偏保守",
      "expectation_gap": "涨价幅度+拉货动能超预期"
    },
    {
      "title": "特朗普扬言卸任前拿走台湾六成晶片产能",
      "source": "新浪财经",
      "importance": 5,
      "category": "地缘政治",
      "related_sectors": ["半导体", "军工"],
      "is_marginal": true,
      "market_expectation": "此前地缘风险定价不充分",
      "expectation_gap": "避险溢价上行"
    }
  ]
}
```
