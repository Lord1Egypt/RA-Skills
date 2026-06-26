# PyWenCai-Stock Skill

一个强大的 OpenClaw 技能，无缝集成同花顺问财股票数据查询。

[![ClawHub](https://img.shields.io/badge/ClawHub-📦-orange)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 核心能力

- 📈 实时行情：涨停/跌停、涨幅榜、换手率
- 💰 资金流向：主力净流入、龙虎榜
- 📊 财务筛选：净利润、市盈率、ROE
- 🏷️ 个股查询：基本信息、所属板块
- 🔍 自然语言查询：用中文任意搜索

## 🚀 快速开始

```python
from skills.pywencai_stock import search, top_gainers, dragon_tiger_list

# 查询涨停股
df = search('A股涨停')
print(df[['股票代码', '股票名称', '涨跌幅']])

# 涨幅前10
df = top_gainers(10)

# 龙虎榜
df = dragon_tiger_list()
```

## 📦 安装

```bash
clawhub install pywencai-stock
```

前置：Python 3.8+, `pip install pywencai pandas`

## 💡 商业应用

- ✅ **每日股市简报**：自动生成热门股、龙虎榜报告
- ✅ **量化策略数据源**：低成本替代聚宽/同花顺 API
- ✅ **监控提醒**：设置阈值自动通知
- ✅ **自媒体内容**：公众号/抖音素材自动生成

## 📄 许可证

MIT © QIQ

---

**🔗 发布在 ClawHub**: https://clawhub.ai/skills/pywencai-stock
