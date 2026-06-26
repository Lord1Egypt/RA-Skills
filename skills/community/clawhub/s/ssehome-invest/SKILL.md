---
name: ssehome-invest
displayName: 投资研究报告助手
description: 基于 baostock 金融数据库和 tavily-search 智能搜索的股票投资分析技能，提供完整的多时间框架技术分析、市场热点资讯追踪和投资报告生成功能。
category: business_tools
tags:
  - 投资
  - 研究
  - 技术指标
  - 强弱
  - 资讯
tools:
  - tavily-search
---

# ssehome-invest Skill - 投资研究报告技能

## 📋 技能描述

基于 baostock 金融数据库和 tavily-search 智能搜索的股票投资分析技能，提供完整的多时间框架技术分析、市场热点资讯追踪和投资报告生成功能。

**版本**: 1.0.4
**更新日期**: 2026-04-07
**作者**: OpenClaw Assistant & haojl@ssehome.com
**核心特性**: baostock K 线数据 + Tavily AI 新闻搜索 + 技术分析

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/ssehome-invest
pip install -r requirements.txt
```

### 2. 配置 Tavily API (可选)

访问 [https://app.tavily.com/](https://app.tavily.com/) 获取免费 API Key，然后编辑配置文件：

```bash
# 编辑 ~/.openclaw/.env 文件
TAVILY_API_KEY=tvly-你的 API_Key
```

保存后重启 OpenClaw 即可生效。

### 3. 运行分析

```python
from analyze_stock import analyze_stock
analyze_stock("002328", "新朋股份")
```

---

## 📁 文件结构

```
skills/ssehome-invest/
├── SKILL.md              # 本技能文档
├── README.md             # 使用指南
├── analyze_stock.py      # 主分析脚本 (含 Tavily 集成)
├── demo_tavily.py        # Tavily 搜索演示
├── TAVILY_README.md      # Tavily 详细配置指南
└── requirements.txt      # Python 依赖包列表

输出目录 data/:
└── {股票代码}_investment_report.md # Markdown 报告
```

---

## 🔄 更新日志

### v1.0.4 (2026-04-07)
- 🐛 **修复资讯搜索时行业条件** - 根据代码获取的行业类型(原来固定了行业)


### v1.0.3 (2026-04-02)
- 🐛 **修复收益率计算** - 涨跌幅 clip(-10, 10) 过滤异常数据
- 🐛 **修复月涨跌幅** - 使用涨跌幅累乘方式，非首尾价格
- 📰 **Tavily 新闻集成** - 自动搜索公司/产品/行业动态
- 📝 **完善文档** - README.md / SKILL.md / TAVILY_README.md 同步更新

### v1.0.2 (2026-04-01) 🔥
- ✨ **Tavily Search 集成** - 自动搜索公司相关新闻热点
- ✨ **AI 情感分析** - 正负面判断和股价影响评估
- ✨ **三维度搜索** - 公司动态/产品业务/行业热点
- 📝 **配置简化** - 使用 ~/.openclaw/.env 统一管理 API Key
- 🗑️ **移除配置文件** - 删除 tavily_config.py
- 🛠️ **代码优化** - 简化 baostock 调用逻辑

### v1.0.1 (2026-03-31)
- ✅ 仅使用 baostock 作为数据源
- ✅ 移除 AKShare 依赖
- ✅ 强化错误处理机制

### v1.0.0 (2026-03-31)
- ✅ 完整实现所有技术分析功能
- ✅ 支持 Markdown/PDF 报告导出
- ✅ 均线系统评分机制

---

## 💡 Tavily 搜索功能详解

### 自动搜索内容

每次分析时自动执行三次智能搜索：

1. **公司动态** 
   - 查询：`{股票名} {代码} 股价 投资 最新`
   - 深度：advanced
   - 返回：前 5 条

2. **产品业务**
   - 查询：`{股票名} 产品 技术 主营业务`
   - 深度：basic
   - 返回：前 3 条

3. **行业热点**
   - 查询：`{行业关键词} 行业 政策 市场`
   - 深度：basic
   - 返回：前 3 条

### 输出示例

```markdown
### 六、市场热点资讯分析

**整体情绪**: 🟢 偏正面

**公司动态** (4 条):
1. 中科曙光发布新一代 AI 服务器
2. 液冷技术获重大突破
...

**股价影响评估**:
- 短期：利好支撑可能推动股价上行
- 中长期：关注订单落地情况
```

---

## ⚙️ 技术指标说明

完整的 5+1 项技术分析：

1. **MACD** - 趋势方向和强度判断
2. **RSI(14)** - 超买 (>70)/超卖 (<30) 检测  
3. **DMI/ADX** - 动向指标和趋势强度
4. **BOLL** - 布林带位置分析
5. **均线系统** - 5/14/21/89/250 日 MA 排列
6. **成交量** - 放量/缩量对比

**均线评分标准**:
- 5/5: 强势多头（黄金交叉）
- 3-4/5: 部分多头
- 0-2/5: 弱势或空头

---

## 📊 投资建议生成

基于多维度的综合分析结果，自动生成：

| 周期 | 决策依据 | 建议类型 |
|------|---------|---------|
| **短期** | 技术指标信号 + 最新消息 | 买入/持有/卖出 |
| **中期** | 均线排列趋势 + 基本面 | 增持/观望/减仓 |
| **长期** | 行业前景 + 公司竞争力 | 深入研究 |

---

## ⚠️ 注意事项

### 数据获取
- baostock 需要稳定的网络连接
- 如遇网络问题可稍后重试
- 建议使用代理优化连接

### Tavily 使用
- 免费版每天 1000 次搜索额度充足
- API Key 配置在 ~/.openclaw/.env 中
- 未配置 API Key 不影响其他功能
- 搜索结果仅供参考

### 免责声明
本报告基于量化分析和公开信息生成，不构成投资建议。股市有风险，入市需谨慎。

---

## 📞 技术支持

- **baostock 文档**: https://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5
- **Tavily 文档**: https://docs.tavily.com/
- **OpenClaw 社区**: 欢迎反馈问题和分享经验

---

## 📜 许可证

MIT License - Open Source

*最后更新：2026-04-02*
