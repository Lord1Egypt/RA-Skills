---
name: trade-dashboard
version: 1.0.0
description: B2B外贸全链路数据看板技能 - 转化漏斗 + ROI追踪 + 自进化分析
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: 📈
---

# Trade Dashboard - B2B外贸全链路数据看板

## 功能
- 全链路转化漏斗可视化（发现→筛选→触达→成交）
- ROI追踪与趋势分析
- 邮件触达效果监控
- 多维度雷达图评分展示
- 地理分布地图可视化
- 自进化数据回流机制

## 触发条件

当用户需要：
- 查看获客数据总览
- 分析转化漏斗
- 追踪ROI效果
- 监控邮件触达
- 生成数据报告

## 核心指标

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| 发现客户 | 新增潜在客户数 | Hunter产出 |
| 高价值目标 | A级客户数量 | Qualifier产出 |
| 邮件回复 | 收到回复数 | Closer产出 |
| 转化率 | 成交/发现 | 漏斗转化 |
| ROI | 收益/成本 | 财务数据 |

## 图表类型

- **漏斗图**: 转化路径可视化
- **折线图**: 月度趋势对比
- **柱状图**: 成本收益分析
- **饼图**: 模型路由分布
- **雷达图**: 多维度评分

## 技术栈

- ECharts 5 - 图表渲染
- Leaflet - 地图可视化
- CDN加载 - 无需本地依赖

## 闭环生态

Trade Dashboard 是外贸获客4技能闭环的第四环，也是数据回流起点：
- **trade-hunter** 🔍 → 客户发现
- **trade-qualifier** 📊 → 客户筛选
- **trade-closer** ✉️ → 开发信生成
- **trade-dashboard** 📈 → 数据看板 → 数据回流至Hunter

数据回流实现自进化：Dashboard分析结果自动优化Hunter的搜索策略和Qualifier的评分权重。
