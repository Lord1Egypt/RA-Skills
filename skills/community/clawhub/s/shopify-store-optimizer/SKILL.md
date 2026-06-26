# Shopify Store Optimizer

## Overview

Shopify Store Optimizer is a descriptive skill that helps Shopify small-to-medium store owners (annual revenue $10k–$500k, moderate technical skill) diagnose store health across three pillars: Conversion Rate, SEO, and User Experience. It delivers actionable optimization suggestions and curated App recommendations — all based on built-in templates, checklists, and best-practice libraries — without requiring real-time API connectivity.

## Trigger

**Primary trigger:** User asks for a Shopify store health check, optimization audit, or improvement recommendations.

**Example prompts:**
- "帮我诊断一下我的Shopify店铺"
- "Shopify店铺健康度检查"
- "How can I improve my Shopify store conversion rate?"
- "我的店SEO做得怎么样？"
- "推荐一些Shopify店铺优化App"

**Activation conditions:** None — this skill is purely descriptive and always available.

## Workflow

```
1. Receive user input (store description, URL, or specific concern)
2. Identify which diagnostic areas are relevant (Conversion / SEO / UX / All)
3. Apply built-in templates and best-practice libraries
4. Generate a structured diagnostic report with:
   - Health scores per area (Low / Medium / High)
   - Specific findings and issues
   - Prioritized optimization suggestions
   - Curated App recommendations
5. Return the report in clear, actionable markdown
```

**Diagnostic Areas:**

| Area | What it covers |
|------|----------------|
| **Conversion Rate** | Product pages, checkout flow, trust signals, pricing psychology, CTA clarity |
| **SEO** | Title/meta, image alt text, URL structure, blog/content strategy, core web vitals guidance |
| **User Experience** | Navigation, mobile-friendliness, page speed, accessibility, search usability |

## I/O

**Input (user provides one or more):**
- Store URL or description
- Specific concern (e.g., "low conversion", "low traffic")
- Annual revenue range (optional, for context)
- Number of products (optional)

**Output:**
A structured markdown report containing:
- Overall health summary
- Per-area health scores and findings
- Prioritized action items
- App recommendations with rationale
- Best-practice tips specific to the concern

## Safety

- **No real API calls:** This skill does not connect to Shopify APIs, Google Analytics, or any external service.
- **No PII collected:** The skill processes only generic store descriptors provided voluntarily by the user.
- **No financial advice:** Recommendations are informational only; actual business decisions remain with the store owner.
- **No installation required:** All content is built-in templates and libraries.

## Examples

### Example 1: Full Diagnostic
**Input:** "我的Shopify店有50个产品，月访问量3000，但转化率只有0.8%，帮我看看哪里有问题"

**Output:**
```
## 🏪 Shopify 店铺健康度报告

### 整体健康度：⚠️ 中等偏低

---

### 1. 转化率分析 — 得分：🟡 中等

**现状：**
- 转化率 0.8%，行业平均 1.4%–2.5%，偏低
- 访问量 3000/月，预期订单 24–75，实际约 24

**发现：**
- 产品页缺少社会证明（评价/销量）
- CTA 按钮不够突出
- 缺少信任标识（安全徽章、退款政策）

**优化建议（优先级排序）：**
1. 添加产品评价插件（如 Shopify Reviews / Judge.me）
2. 在产品页显著位置展示库存数量或"热销"标签
3. 在 Checkout 页面添加安全支付标识
4. A/B 测试不同的 "Add to Cart" 按钮颜色和文案

**推荐 App：**
- Judge.me Product Reviews（免费起步，$9/月）
- Loox Reviews & Photos（$9.9/月）
- Ali Reviews（免费起步）

---

### 2. SEO 分析 — 得分：🟡 中等

**现状：**
- 缺少 SEO 审计数据，建议配合 Google Search Console

**发现：**
- 产品标题可能缺少目标关键词
- 图片缺少 Alt 文本
- URL 结构未做关键词优化

**优化建议：**
1. 为每个产品编写独特、关键词丰富的 Meta Title（50–60字符）
2. 为所有产品图片添加描述性 Alt 文本
3. 在 Shopify BLOG 发布相关产品内容文章
4. 提交 sitemap.xml 到 Google Search Console

**推荐 App：**
- Plug in SEO（免费/付费，$9/月）
- SEO Manager（$9/月）
- Smart SEO（免费起步）

---

### 3. 用户体验分析 — 得分：🟡 中等

**发现：**
- 移动端体验未检测（建议用 Google PageSpeed Insights 自测）
- 导航层级可能过深
- 缺少站点搜索功能

**优化建议：**
1. 确保主题移动端响应式测试通过
2. 简化菜单结构，重要页面 2–3 次点击可达
3. 启用 Shopify 内置搜索并优化搜索结果排序

**推荐 App：**
- Boost Commerce Search & Filter（$9.9/月）
- Raja Theme — Quick View（免费）

---

### 📋 下一步行动清单

| 优先级 | 行动 | 预计时间 |
|--------|------|---------|
| 🔴 高 | 添加产品评价系统 | 1–2 小时 |
| 🔴 高 | 优化产品页 Meta 信息 | 3–4 小时 |
| 🟡 中 | 添加信任标识到结算页 | 30 分钟 |
| 🟡 中 | 启用 SEO App 扫描 | 20 分钟 |
| 🟢 低 | 优化导航和搜索 | 1–2 小时 |

---

*本报告基于 Shopify 最佳实践库生成，不涉及实时 API 调用。建议定期复检。*
```

### Example 2: SEO-Only Query
**Input:** "我的Shopify店SEO做得怎么样？"

**Output:** SEO-focused section only (same structure as above).

### Example 3: App Recommendation Only
**Input:** "推荐一些能提高转化率的App"

**Output:** Conversion Rate App recommendations with pricing and rationale.

## Acceptance Criteria

1. **Skill activates** on any of the trigger phrases listed above.
2. **handler.py runs standalone:** `python3 handler.py` produces valid markdown output without external dependencies.
3. **No network calls:** All content comes from built-in templates; runs fully offline.
4. **Report is actionable:** Output includes specific findings, prioritized suggestions, and App recommendations.
5. **Tests pass:** `python3 tests/test_handler.py` runs ≥ 3 test cases and all pass.
6. **Metadata complete:** `skill.json` and `.claw/identity.json` are present and valid.
7. **Language flexibility:** Handles both Chinese and English inputs.
