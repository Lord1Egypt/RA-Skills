---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_fad7d732618411f1832e5254006c9bbf
    ReservedCode1: gCVKTc7RFuemETvWGUF7jMbrWZLO2vqnNDblogjRbLPriXJA0MdRQtpDKO359Yh3/n6OCZNWNVlsiXK7JlEZvrReaOWWUBHeqpa843aHPEWh2HObqZlAwDhikof6z0LKlg0hcKv7nSEXzH0lcVV4ZFCCNq0nCEfIvxGzZOfgzWk0DCxC/tfb/6fHtDI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_fad7d732618411f1832e5254006c9bbf
    ReservedCode2: gCVKTc7RFuemETvWGUF7jMbrWZLO2vqnNDblogjRbLPriXJA0MdRQtpDKO359Yh3/n6OCZNWNVlsiXK7JlEZvrReaOWWUBHeqpa843aHPEWh2HObqZlAwDhikof6z0LKlg0hcKv7nSEXzH0lcVV4ZFCCNq0nCEfIvxGzZOfgzWk0DCxC/tfb/6fHtDI=
---



# AI SEO 内容优化 (SEO Optimizer)

## 概述

SEO Optimizer 是一款 AI 驱动的搜索引擎优化技能，基于 Google/Bing/Baidu 排名因子权重体系、LSI 关键词图谱、EEAT 评分标准和结构化数据模板，自动对网页内容进行多维 SEO 分析与优化建议，输出详细优化报告。

## 适用场景

- 网站内容发布前的 SEO 优化检查
- 竞品内容 SEO 对比分析
- 多语言站点的本地化 SEO 策略
- 电商产品页面的搜索可见度提升
- 技术博客 / 文档的结构化数据标记

## 分析维度

| 维度 | 说明 |
|------|------|
| 关键词分析 | 关键词密度、TF-IDF 权重、LSI 语义关联词、长尾关键词覆盖 |
| 标题优化 | Title 标签长度/吸引力、H1-H6 层级结构、关键词前置策略 |
| 元描述 | Meta Description 长度/CTR 预估、关键词自然融入 |
| 内容质量 | EEAT 评分（经验/专业/权威/信任）、可读性指数、原创度 |
| 结构化数据 | JSON-LD Schema 标记完整度、Rich Result 兼容性检查 |
| 技术 SEO | URL 结构、内链/外链分布、图片 Alt 文本、页面速度因子 |
| 移动适配 | 移动端友好度、响应式设计检查、Core Web Vitals 预检 |
| 本地 SEO | Google My Business 要素、NAP 一致性、本地化关键词 |

## 支持的搜索引擎与市场

| 市场 | 搜索引擎 | 语言支持 | 特色优化项 |
|------|---------|---------|-----------|
| 全球 | Google | 多语言 | EEAT、Core Web Vitals、Rich Results |
| 全球 | Bing | 多语言 | Bing Webmaster、IndexNow |
| 中国 | 百度 | 中文 | 百度收录、熊掌号、百家号 |
| 俄罗斯 | Yandex | 俄语 | Yandex Webmaster、Turbo Pages |
| 韩国 | Naver | 韩语 | Naver Blog、Naver Cafe |

## 评分体系

| SEO 分数 | 等级 | 说明 |
|---------|------|------|
| 90-100 | 优秀 | 全面符合 SEO 最佳实践，预期排名前3 |
| 75-89 | 良好 | 大部分优化到位，小幅调整可提升 |
| 60-74 | 一般 | 存在明显优化空间，需要针对性改进 |
| 40-59 | 较差 | 多项关键指标不达标，影响搜索可见度 |
| 0-39 | 严重 | 基础 SEO 要素缺失，需大幅整改 |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/seo-optimizer` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起优化请求  POST /skill/seo-optimizer
2. 服务端返回 402 Payment Required
   Header: X-Payment-Needed: true
   Header: X-Short-Link: alipay_XXXXXXXXXXXXXXXX
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  POST /pay-confirm
   Header: X-Payment-Credential: <支付凭证>
5. 服务端验证通过 → 执行 SEO 分析 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `X-Payment-Needed` | 服务端返回：`true` 表示需要支付 |
| `X-Short-Link` | 服务端返回：支付宝短链 URL 供用户支付 |
| `X-Payment-Credential` | 客户端回传：支付完成后的凭证字符串 |
| `X-Service-Tier` | 可选，`basic`（基础分析）或 `deep`（深度审计） |

## 服务档位

### 基础档（basic = ¥0.50）
- 单页面内容分析（最多 5,000 词）
- SEO 综合评分（0-100）
- 关键词密度与分布分析
- 标题/Meta 优化建议
- 结构化数据检查
- 输出 JSON 格式优化报告

### 深度档（deep = ¥1.00 - 预留）
- 全部基础功能
- 竞争对手 SERP 对比分析
- 完整 LSI 关键词图谱
- 内链结构优化建议
- Core Web Vitals 详细诊断
- EEAT 逐项评分
- 输出 PDF 完整审计报告

## 数据底座

所有排名因子权重、LSI 关键词图谱、EEAT 评分标准、结构化数据模板存储于 `references/seo-optimizer.json`，结构如下：

```json
{
  "ranking_factors": { ... },       // Google/Bing/Baidu 排名因子权重表
  "lsi_keyword_graph": { ... },     // 各行业 LSI 语义关键词图谱
  "eeat_criteria": [ ... ],         // EEAT 评分标准细则
  "structured_data_templates": { ... }, // JSON-LD Schema 模板集
  "title_meta_rules": [ ... ],      // 标题/描述优化规则
  "readability_formulas": [ ... ]   // Flesch/FOG/SMOG 可读性公式
}
```

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/seo-optimizer \
  -H "Content-Type: application/json" \
  -H "X-Service-Tier: basic" \
  -d '{"content": "Best coffee machines for home brewing in 2026. Our top picks include...", "target_keyword": "best coffee machines 2026", "target_market": "global"}'
```

### 响应（支付后）

```json
{
  "service": "AI SEO 内容优化",
  "tier": "basic",
  "target_market": "global",
  "seo_score": 72,
  "rank": "一般",
  "keyword_density": {
    "primary": "best coffee machines 2026",
    "density": 1.8,
    "status": "偏低 (建议 2-3%)",
    "positions": ["title", "h1", "p1"]
  },
  "title_suggestions": [
    "10 Best Coffee Machines 2026: Ultimate Home Brewing Guide",
    "Best Coffee Machines 2026 Review: Top Picks for Every Budget"
  ],
  "structured_data": {
    "type": "Article",
    "status": "缺失",
    "suggestion": "添加 JSON-LD Article Schema，包含 headline/author/datePublished"
  },
  "improvement_checklist": [
    { "priority": "high", "item": "Title 标签长度 52 字符，建议扩展至 55-60 字符" },
    { "priority": "high", "item": "缺少 Meta Description 标签" },
    { "priority": "medium", "item": "H2 子标题中关键词出现次数为 0，建议至少 1-2 次" },
    { "priority": "medium", "item": "图片缺少 Alt 文本，共 3 张图片" },
    { "priority": "low", "item": "内链数量 2 条，建议增加至 5-8 条相关内容链接" }
  ]
}
```

## 许可

MIT License — 详见 LICENSE 文件
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
