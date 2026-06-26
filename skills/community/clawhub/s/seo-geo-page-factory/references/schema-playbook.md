# Schema Playbook

本文件定义不同页面类型适合使用的结构化数据类型、适用条件与禁止事项。

---

## 1. 总原则

### 1.1 schema 的目的
结构化数据的目的不是“作弊”，而是帮助搜索系统更稳定地理解页面内容与实体关系。

### 1.2 schema 必须与正文一致
凡是 schema 中出现的信息，页面正文应有对应可见内容。

### 1.3 不为炫技乱加
如果页面本身不适合某种 schema，不应为了“显得专业”而强行添加。

### 1.4 不得伪造
绝对禁止伪造以下字段：
- aggregateRating
- review
- offers
- price
- availability
- author
- datePublished
- dateModified
- brand
- softwareVersion

除非页面可见内容中真实存在且能对应。

---

## 2. 通用可选 schema

### 2.1 WebPage
适用：
- 几乎所有可索引网页

适合场景：
- 无更具体类型可用时的基础兜底
- 首页、功能页、落地页、说明页均可考虑

### 2.2 BreadcrumbList
适用：
- 站内层级明确
- 页面存在可见面包屑路径

适合场景：
- 分类页
- 详情页
- 文档页
- 文章页

### 2.3 Organization
适用：
- 首页
- 品牌介绍页
- 关于页

要求：
- 页面中有品牌实体信息
- 品牌名称与网站主体明确

### 2.4 WebSite
适用：
- 首页
- 网站级语义说明

可用于表达：
- 网站名称
- 网站 URL
- 搜索入口（仅在站内搜索真实存在时）

---

## 3. 页面类型对应建议

## 3.1 首页

### 优先推荐
- WebPage
- WebSite
- Organization
- BreadcrumbList（仅当页面真的有可见面包屑时，首页通常不必强加）

### 适用理由
首页主要承担站点级、品牌级、导航级语义。

### 不建议
- FAQPage（除非首页确实有一组真实 FAQ 且适合展示）
- Product（除非首页本身就是单一产品详情页，一般不适用）

---

## 3.2 分类页 / 聚合页 / 市场页

### 优先推荐
- CollectionPage
- WebPage
- BreadcrumbList
- FAQPage（仅当页面有真实 FAQ）

### 适用理由
这类页面本质上是“集合 / 聚合 / 目录”页面，适合用 CollectionPage 表达集合属性。

### 不建议
- Product（整页不是单一产品）
- Article（除非页面本质是文章，而不是目录）

---

## 3.3 功能页 / 落地页

### 优先推荐
- WebPage
- FAQPage（若确有 FAQ）
- BreadcrumbList

### 适用理由
功能页主要是能力说明和转化承接，通常不一定满足 Product 的完整条件。

### 谨慎使用
- SoftwareApplication / Product  
只有当页面明确对应某个具体软件 / 工具 / 产品实体，且正文中已有对应字段时，才考虑。

---

## 3.4 产品页 / 工具详情页 / Skill 详情页

### 优先推荐
- Product（条件满足时）
- WebPage
- BreadcrumbList
- FAQPage（若有）

### 使用 Product 的条件
至少满足以下大部分条件：
- 页面明确介绍一个单一工具 / 单一 Skill / 单一产品
- 页面中有产品名
- 页面中有功能说明
- 页面中有品牌 / 提供方信息
- 页面中有 URL 归属明确
- 页面内容像一个真正详情页，而不是泛泛介绍

### 不建议
- 若页面只是“这个类目是什么”，不要用 Product

---

## 3.5 文章页 / 博客页

### 优先推荐
- Article
- BreadcrumbList
- FAQPage（若有 FAQ）
- WebPage

### 使用条件
- 页面是完整文章
- 页面中有清晰标题
- 页面中有正文
- 若提供作者 / 发布时间，则必须真实

### 不建议
- Product
- CollectionPage（除非本质是专题集合）

---

## 3.6 文档页 / 教程页

### 优先推荐
- TechArticle（若明显偏技术说明）
- Article
- FAQPage（若有）
- BreadcrumbList
- WebPage

### 适用理由
文档 / 教程页更接近知识型页面，适合文章类 schema。

---

## 3.7 FAQ 页

### 优先推荐
- FAQPage
- WebPage
- BreadcrumbList

### 使用条件
- 页面主体确实由问题与回答组成
- 问题真实、清晰
- 回答可见

### 不建议
- 若只是页面末尾 1-2 个简单问答，未必需要单独上 FAQPage

---

## 4. CollectionPage 使用模板

适用于：
- Skills 页面
- Tools 页面
- MCP 聚合页
- 资源目录页

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "AI Skills - AI STORE",
  "url": "https://www.example.com/skills",
  "description": "AI STORE 聚合优质 AI Skills，帮助用户按场景发现适合写作、搜索、办公、编程和自动化的 AI 能力。",
  "isPartOf": {
    "@type": "WebSite",
    "name": "AI STORE",
    "url": "https://www.example.com/"
  }
}
</script>