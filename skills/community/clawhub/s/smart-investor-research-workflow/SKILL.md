---
name: smart-investor-research-workflow
description: 智能投资研究工作流 — 多源研报 + 情绪分析 + 风险计算 + PDF报告生成
category: AI
triggers: 投资研究, 行业分析, 投资尽调, 市场调研, 投资报告, portfolio research, investment analysis
---

# Smart Investor Research Workflow
智能投资研究工作流

## 功能概述

将 **zcx-research-assistant**（多源研究）、**zcx-sentiment-analyzer**（市场情绪分析）、**zcx-portfolio-risk-manager**（投资组合风险管理）、**zcx-pdf-report-generator**（PDF报告生成）四个技能串联，形成完整的投资研究闭环工作流。

适用于：投资经理、分析师、基金研究员、个人投资者进行系统化投资研究。

## 工作流程

```
用户输入投资标的/行业主题
        │
        ▼
┌─────────────────────────┐
│  zcx-research-assistant │  多源研究 + 交叉验证 → 结构化研报
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  zcx-sentiment-analyzer │  新闻/社交媒体情绪 → 多空信号 + 情绪评分
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ zcx-portfolio-risk-manager│  VaR/夏普比/最大回撤 → 风险指标 + 仓位建议
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  zcx-pdf-report-generator│  Markdown → 专业格式 PDF 投资报告
└─────────────────────────┘
```

## 核心 Skill 协作说明

### Step 1 — zcx-research-assistant（多源研究）
- 输入：投资标的名称或行业主题
- 输出：SWOT、竞品分析或行业简报，包含完整信息来源引用
- 支持交叉验证，自动标注信息来源可信度

### Step 2 — zcx-sentiment-analyzer（情绪分析）
- 输入：Step 1 研报中提到的相关新闻源、社交媒体关键词
- 输出：看涨/看跌信号、关键词趋势、情绪评分（0-100）
- 辅助判断市场共识与潜在拐点

### Step 3 — zcx-portfolio-risk-manager（风险管理）
- 输入：标的代码/名称 + 模拟仓位权重
- 输出：VaR（风险价值）、夏普比率、最大回撤、相关性矩阵、仓位建议
- 结合情绪分析结果，给出动态调整建议

### Step 4 — zcx-pdf-report-generator（PDF报告生成）
- 输入：前三步输出的完整 Markdown 报告内容
- 输出：A4 专业格式 PDF，支持中文字体，含页眉页脚和页码
- 交付物：可直接分享给客户/上级的正式投资报告

## 使用方法

在 OpenClaw 对话中触发：

```
帮我完成 [标的/行业] 的投资研究，输出完整 PDF 报告
```

系统将依次执行：
1. 联网抓取多源研报信息
2. 分析市场情绪与关键驱动因素
3. 计算风险指标并给出仓位建议
4. 生成并提供 PDF 报告下载链接

## 示例场景

**场景：研究新能源汽车行业发展**
- Step 1：zcx-research-assistant 抓取政策、销量、竞争格局数据
- Step 2：zcx-sentiment-analyzer 分析微博/新闻/研报情绪倾向
- Step 3：zcx-portfolio-risk-manager 给出模拟组合的夏普比和 VaR
- Step 4：zcx-pdf-report-generator 汇总成 10 页专业 PDF 报告

**场景：个股尽调（宁德时代）**
- Step 1：zcx-research-assistant 收集公司财报、竞争对手、行业定位
- Step 2：zcx-sentiment-analyzer 分析机构评级、分析师推荐、社交媒体情绪
- Step 3：zcx-portfolio-risk-manager 计算持仓风险（假设 10% 仓位）
- Step 4：输出 PDF 尽调报告

## 依赖 Skill 列表

| Skill | 版本 | 用途 |
|-------|------|------|
| zcx-research-assistant | ≥1.0.2 | 多源信息收集与结构化 |
| zcx-sentiment-analyzer | ≥1.0.1 | 市场情绪提取与评分 |
| zcx-portfolio-risk-manager | ≥1.0.3 | 风险指标计算 |
| zcx-pdf-report-generator | ≥1.0.0 | PDF 报告渲染与导出 |

## 注意事项

- 本工作流为 **分析辅助工具**，不构成投资建议
- PDF 报告字体渲染依赖系统中文字体支持（pdfkit）
- 情绪分析数据来源于公开新闻源，可能存在滞后性
- 风险计算基于模拟参数，实际交易需自行调整