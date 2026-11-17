---
slug: seo-audit-master
name: seo-audit-master
version: 1.0.1
displayName: SEO审计大师
summary: "全站SEO体检:技术内容架构链接四维度审计,输出可执行优化清单。SEO审计大师——对网站执行全面SEO审计,覆盖技术SEO+内容SEO+架构验证+链接分析四维度。输出按优先级排序的可执行优化"
summary_zh: "全站SEO体检:技术内容架构链接四维度审计,输出可执行优化清单。SEO审计大师——对网站执行全面SEO审计,覆盖技术SEO+内容SEO+架构验证+链接分析四维度。输出按优先级排序的可执行优化"
license: Proprietary
description: 。Use when 用户需要seo-audit-master相关功能时使用。不适用于超出本技能能力范围的复杂需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。提供结构化输出和错误处理机制。
  SEO
tags:
  - SEO优化
  - 网站审计
  - 搜索引擎优化
  - 技术SEO
  - 流量增长
  - 工具
  - 效率
  - 写作
  - 电商
  - seo
  - google
  - sitemap
  - https
tools:
  - read
  - exec
  - glob
  - grep
category: "Automation"
对网站执行全面 SEO 审计。从技术到内容,从架构到链接,输出可执行的优化清单。支持 Google 与百度双引擎,兼顾海外与国内搜索引擎优化。
---
> **核心功能**: 本技能提供中文交互、化工作流场景等能力。
## 主要能力
1. **技术 SEO 审计**:可抓取性、索引状态、Core Web Vitals、移动适配、HTTPS 安全检查
2. **内容 SEO 审计**:关键词覆盖、标题描述、内容质量、图片优化、重复内容检测
3. **架构与链接审计**:结构化数据(JSON-LD)、内部链接结构、URL 规范化、外链质量分析
4. **双引擎适配**:Google Search Console + 百度站长平台 + 搜狗站长平台
5. **优化清单输出**:按 Critical/Important/Suggested 三级优先级输出可执行修复步骤
## 操作入门
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理
> 详细的输入输出格式请参考下方章节说明。
## 场景示例
| 场景 | 输入 | 输出 |
|---|---|---|
| 全站审计 | 网站域名、sitemap、访问日志 | SEO 审计报告 + 按优先级排序的问题清单 |
| 排名下降诊断 | 域名、下降时间段、目标关键词 | 排名下降原因分析 + 恢复建议 |
| 新站优化 | 新站 URL、目标市场(国内/海外) | SEO 基础配置清单 + 内容策略 |
| 竞品对比 | 自有域名 + 竞品域名列表 | SEO 差距分析 + 赶超路径 |
| 迁移检查 | 迁移前后 URL 映射表 | 301 重定向方案 + 索引完整性验证 |
**不适用于**:
- 黑帽 SEO 与刷排名(仅支持白帽合规优化)
- SEM 竞价广告投放(专注于自然搜索优化)
- APP ASO 应用商店优化(专注于网页 SEO)
- 社交媒体运营(虽有关联,但非核心)
- 实时排名监控(需配合站长平台 API 长期追踪)
## 操作步骤
### Step 1: 确定审计范围
1. 输入目标网站域名(如 https://example.com)
2. 确认目标搜索引擎(国内:百度/搜狗/360;海外:Google/Bing)
3. 确认审计深度(全站/核心页面/特定目录)
4. 收集辅助资料(sitemap.xml、robots.txt、访问日志)
### Step 2: 技术 SEO 审计
1. **可抓取性检查**:robots.txt 配置、爬虫权限、noindex/nofollow 标签
2. **索引状态**:已索引页面数 vs 总页面数、重复页面、canonical 问题
3. **页面速度**:Core Web Vitals(LCP/CLS/INP)、TTFB/FCP、移动端速度
4. **移动适配**:响应式设计、移动友好性、视口配置
5. **HTTPS 安全**:SSL 证书、混合内容检查
### Step 3: 内容 SEO 审计
1. **关键词分析**:目标关键词排名、覆盖缺口、长尾机会
2. **标题与描述**:title 标签、meta description、H1-H6 层级
3. **内容质量**:深度、关键词密度(1-2%)、LSI 语义词、新鲜度
4. **图片优化**:alt 文本、文件大小、WebP 格式
### Step 4: 架构与链接审计
1. **结构化数据**:JSON-LD schema、富媒体资格、错误检查
2. **内部链接**:链接结构、锚文本、孤立页面、点击深度
3. **URL 结构**:规范化、长度、层级、重定向链
4. **外链分析**:反链数量/质量、锚文本分布、有毒链接
### Step 5: 输出优化清单
1. 按 Critical/Important/Suggested 三级优先级排序
2. 每个问题附具体修复步骤与代码示例
3. 标注预期收益与实施难度
4. 生成可跟踪的实施清单
## 双引擎适配说明
| 维度 | Google | 百度 |
|:-----|:-----|:-----|
| 站长平台 | Google Search Console | 百度搜索资源平台 |
| 索引查询 | `site:domain.com` | `site:domain.com` |
| 提交入口 | sitemap 提交 + URL 检查 | 链接提交 + 主动推送 |
| 速度指标 | Core Web Vitals | 百度移动友好度 |
| 结构化数据 | JSON-LD 优先 | JSON-LD + 微数据 |
| 关键词工具 | Google Keyword Planner | 百度指数 + 百度关键词规划师 |
## 审计检查清单(核心)
- [ ] robots.txt 配置正确
- [ ] sitemap.xml 完整并已提交
- [ ] 所有重要页面已索引
- [ ] canonical 标签正确
- [ ] Core Web Vitals 全部达标(LCP<2.5s/CLS<0.1/INP<200ms)
- [ ] 移动友好
- [ ] HTTPS 无混合内容
- [ ] title/meta description 完整
- [ ] H1 唯一且含关键词
- [ ] 结构化数据无错误
- [ ] 内部链接结构合理
- [ ] 无孤立页面
- [ ] 无重复内容
- [ ] 图片有 alt 文本
## 用法示例
### 示例1: 全站 SEO 审计(输入→输出)
**输入**:
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | SEO审计大师处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```
网站: https://shop.example.com
搜索引擎: 百度 + Google
深度: 全站(约 500 页)
关注点: 商品页索引、移动端速度
```
**输出**(seo-audit.md 片段):
```markdown
- 总页面数: 487
- 已索引(百度): 312 (64%)
- 已索引(Google): 401 (82%)
- Core Web Vitals 通过率: 73%
1. [Critical] 商品页缺少 canonical 标签
   - 影响: 175 个商品页存在重复内容
   - 修复: 在 `<head>` 添加 `<link rel="canonical" href="https://shop.example.com/product/{id}" />`
2. [Critical] 移动端 LCP 超标(4.8s,应 <2.5s)
   - 影响: 移动端排名下降
   - 修复: 1) 首屏图片懒加载;2) 关键 CSS 内联;3) 图片转 WebP
3. [Critical] sitemap.xml 缺失
   - 影响: 爬虫无法发现新页面
   - 修复: 生成 sitemap.xml 并提交至百度/Google
4. [Important] 38% 页面 title 重复
5. [Important] 商品图片缺少 alt 文本
6. [Important] 结构化数据错误(JSON-LD 缺少 price 字段)
...
- 修复 Critical 后预计索引覆盖率提升至 90%+
- 移动端排名预计提升 20-30%
```
### 示例2: 新站 SEO 基础配置(输入→输出)
**输入**:
```
新站: https://blog.example.com
目标市场: 国内(百度为主)
CMS: WordPress
```
**输出**(recommendations.md 片段):
```markdown
- [ ] 注册百度搜索资源平台(ziyuan.baidu.com)
- [ ] 添加站点并验证所有权
- [ ] 提交 sitemap.xml
- [ ] 开启主动推送 API
```
User-agent: *
Allow: /
Disallow: /wp-admin/
Disallow: /wp-includes/
Sitemap: https://blog.example.com/sitemap.xml
```
- 安装 Yoast SEO 或 Rank Math
- 启用 XML sitemap 自动生成
- 配置面包屑导航
- 启用结构化数据(Article schema)
- 首月发布 10+ 篇高质量原创文章(>1500字)
- 每篇文章聚焦 1 个主关键词 + 3-5 个长尾词
- 内链密度:每篇 3-5 个内链
- 图片全部添加 alt 文本
```
## 故障恢复
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 网站无法访问 | DNS 解析失败或服务器宕机 | 检查域名状态与服务器健康,待恢复后重试 |
| 站长平台 API 超时 | 国内访问 Google Search Console 较慢 | 切换至百度搜索资源平台 API,或使用代理 |
| sitemap.xml 缺失 | 站点未生成 sitemap | 提供在线生成工具建议(xml-sitemaps.com)或脚本生成 |
| 索引数据为空 | 新站尚未被收录 | 提交至百度/Google 站长平台,等待 1-2 周 |
| 结构化数据校验失败 | JSON-LD 格式错误或字段缺失 | 使用 Schema.org Markup Validator 修正 |
| robots.txt 阻止爬虫 | 配置错误屏蔽了重要目录 | 检查 Disallow 规则,确保 /、/product/ 等允许 |
| Core Web Vitals 数据缺失 | 站点流量过低无 CrUX 数据 | 使用 Lighthouse 本地测试替代 |
## 环境要求
### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要Agent支持exec(命令行执行)能力
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代 |
|:------|------:|:------|:------|------:|
| LLM API | API | 必需 | Agent 内置 LLM 提供分析 | 通义千问/文心一言/智谱 |
| Google Search Console | API | 可选 | 需要 Google 账号验证 | 百度搜索资源平台 |
| Lighthouse | 工具 | 可选 | `npm install -g lighthouse` | PageSpeed Insights 国内镜像 |
| WebSearch | 工具 | 可选 | Agent 内置联网搜索 | 百度搜索 + Bing 国内版 |
### API Key 配置
- **本Skill无需额外API Key配置**
- **站长平台访问**: 用户需自行注册百度/Google 站长平台并验证站点所有权
- **安全要求**: 如使用站长平台 API,token 仅存储在环境变量,不写入输出文件
### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown方法论,需 exec 能力运行 Lighthouse 等工具
## 案例展示
以下案例展示了skill的工作流程和预期输出效果，由LLM按照skill定义的流程生成。
### 案例1: 电商网站全站SEO审计(百度+Google双引擎)
**输入**:
```
网站: https://shop.example.com
搜索引擎: 百度 + Google
深度: 全站(约500页)
关注点: 商品页索引、移动端速度、结构化数据
辅助资料: sitemap.xml已提供, robots.txt已配置
```
**LLM生成输出** (`output/shop-seo/seo-audit.md`):
```markdown
| 指标 | 数值 | 评价 |
|---:|:---|---:|
| 总页面数 | 487 | - |
| 已索引(百度) | 312 (64%) | 需提升 |
| 已索引(Google) | 401 (82%) | 良好 |
| Core Web Vitals通过率 | 73% | 需提升 |
| 移动友好性 | 通过 | 良好 |
| HTTPS | 已启用 | 良好 |
| sitemap.xml | 已提交 | 良好 |
- **影响**: 商品页存在URL参数变体(?color=red&size=L),导致重复内容,百度判定为重复页面拒绝索引
- **位置**: 所有 `/product/{id}` 页面
- **检测方法**: `curl -s https://shop.example.com/product/123 | grep canonical` 返回空
- **修复方案**:
```html
<link rel="canonical" href="https://shop.example.com/product/{id}" />
```
- **预期收益**: 百度索引覆盖率从64%提升至85%+
- **实施难度**: 低(模板修改)
- **影响**: Google移动端排名下降,百度移动友好度评分降低
- **根因**: Hero Banner图片3.2MB JPEG未压缩,CSS渲染阻塞1.2s
- **修复方案**:
```html
<picture>
  <source srcset="/banner.webp" type="image/webp">
  <img src="/banner.jpg" alt="首页Banner" width="1920" height="600"
       loading="lazy" fetchpriority="high">
</picture>
<style>/* 首屏关键CSS(约15KB) */</style>
<link rel="preload" href="/css/main.css" as="style"
      onload="this.rel='stylesheet'">
```
- **预期收益**: LCP从4.8s降至2.2s,移动端排名提升20-30%
- **实施难度**: 中
- **影响**: 爬虫无法发现新增的120个商品页
- **当前状态**: sitemap仅包含367个URL,缺少120个新商品页
- **修复方案**:
```bash
npx next-sitemap --config sitemap.config.js
python generate_sitemap.py --db sqlite:///products.db --output public/sitemap.xml
```
- **预期收益**: 120个新页面被百度/Google发现并索引
- **实施难度**: 低
- **影响**: 百度无法区分页面主题,影响关键词排名
- **示例**: 175个商品页title均为"商品详情 - 某某商城"
- **修复方案**:
```javascript
// Next.js动态title示例
export async function generateMetadata({ params }) {
  const product = await getProduct(params.id);
  return {
    title: `${product.name} - 价格¥${product.price} | 某某商城`,
    description: `购买${product.name},正品保障,${product.price}元起,支持7天无理由退换。`,
  };
}
```
- **影响**: 图片搜索无法索引,无障碍体验差
- **修复方案**: 为所有商品图片添加alt属性: `alt="{商品名称} - {商品规格}"`
- **影响**: 搜索结果无法显示价格富媒体,点击率降低15-20%
- **修复方案**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "无线蓝牙耳机",
  "image": ["https://shop.example.com/product/123/1.jpg"],
  "description": "高品质无线蓝牙耳机,降噪功能",
  "offers": {
    "@type": "Offer",
    "price": "299.00",
    "priceCurrency": "CNY",
    "availability": "https://schema.org/InStock"
  }
</script>
```
- **影响**: 重要商品页点击深度>4,爬虫难以发现,权重传递不足
- **修复方案**: 在首页和分类页添加热门商品链接,确保所有页面点击深度≤3
- **影响**: 百度爬虫无法渲染页面,影响JS生成内容的索引
- **修复方案**:
```
User-agent: *
Allow: /
Allow: /css/
Allow: /js/
Disallow: /admin/
Sitemap: https://shop.example.com/sitemap.xml
```
9. 商品页面包屑导航缺少结构化数据(BreadcrumbList)
10. 部分页面meta description超过160字符
11. URL层级过深(/category/subcategory/product/variant)
12. 缺少404页面优化(无搜索建议)
13. 未配置Open Graph标签(影响社交分享)
14. 页面加载时无骨架屏(CLS=0.15)
15. 未使用hreflang(如有多语言需求)
16. 百度主动推送API未配置
| 修复阶段 | 预期效果 | 时间 |
|:------:|--------|:-------|
| 修复Critical(3项) | 索引覆盖率64%→90%,移动排名+30% | 1周 |
| 修复Important(5项) | 点击率+20%,关键词排名+15% | 2周 |
| 修复Suggested(8项) | 用户体验提升,长尾流量+10% | 4周 |
```
**效果验证**: ✓双引擎索引数据对比(百度64%/Google82%) ✓Critical/Important/Suggested三级优先级 ✓每个问题含影响+修复代码+预期收益 ✓结构化数据JSON-LD示例 ✓robots.txt配置修正
### 案例2: 排名下降原因诊断(百度排名骤降)
**输入**:
```
网站: https://blog.example.com
问题: 3个月内百度自然流量下降45%
下降时间: 2024年6月15日开始
目标关键词: "Python教程"从第3页降至第8页
近期变更: 5月底网站从HTTP迁移到HTTPS
```
**LLM生成输出** (`output/blog-diagnosis/ranking-drop.md`):
```markdown
| 指标 | 下降前(5月) | 下降后(7月) | 变化 |
|----|:--:|---:|----|
| 百度自然流量 | 12,000/天 | 6,600/天 | -45% |
| "Python教程"排名 | 第3页 | 第8页 | -5页 |
| 索引页面数 | 320 | 285 | -35页 |
| 移动端收录 | 280 | 210 | -25% |
- **严重程度**: Critical
- **证据**:
  - 旧HTTP页面返回200而非301(部分页面)
  - 百度站长平台显示大量"抓取异常"
  - 外链仍指向HTTP URL,权重未传递
- **诊断命令**:
```bash
curl -I http://blog.example.com/python-tutorial/
curl -sIL http://blog.example.com/python-tutorial/ | grep -i "location\|HTTP"
```
- **修复方案**:
```nginx
server {
    listen 80;
    server_name blog.example.com;
    return 301 https://$server_name$request_uri;
}
```
- **预期恢复**: 修复后2-4周内排名逐步恢复
- **严重度**: High
- **证据**: 检查页面源码发现:
```html
<link rel="canonical" href="http://blog.example.com/python-tutorial/" />
```
- **影响**: 百度认为HTTPS页面是HTTP页面的重复内容,降低HTTPS页面权重
- **修复方案**:
```html
<link rel="canonical" href="https://blog.example.com/python-tutorial/" />
```
- **严重度**: Medium
- **证据**: sitemap.xml中所有URL仍为HTTP
- **影响**: 百度爬虫优先抓取HTTP URL,发现301后重新抓取HTTPS,浪费抓取配额
- **修复方案**:
```bash
sed -i 's/http:\/\//https:\/\//g' public/sitemap.xml
curl -H "Content-Type: text/plain" --data-urlencode "sitemap=https://blog.example.com/sitemap.xml" "https://ziyuan.baidu.com/ping?site=https://blog.example.com&resource_name=sitemap"
```
- **严重度**: Low
- **证据**: 推送API中URL仍为HTTP格式
- **修复方案**: 更新推送脚本中的URL为HTTPS格式
1. [P0] 修复301重定向(Nginx配置)
2. [P0] 修正所有canonical标签为HTTPS
3. [P1] 更新sitemap.xml为HTTPS URL并重新提交
4. [P1] 百度站长平台提交"抓取诊断",验证HTTPS页面可正常抓取
5. [P1] 检查索引覆盖率变化(预期:285→320恢复)
6. [P2] 监控关键词排名变化
7. [P2] 持续监控自然流量恢复情况
8. [P2] 如未恢复,检查是否有其他因素(内容质量/外链/算法更新)
| 时间节点 | 预期状态 |
|----|----|
| 修复后1周 | 百度重新抓取HTTPS页面,索引开始恢复 |
| 修复后2周 | 索引页面数恢复至300+,关键词排名回升 |
| 修复后4周 | 自然流量恢复至下降前80-90% |
| 修复后8周 | 完全恢复(需外链权重传递到位) |
HTTPS迁移SEO检查清单:
- [ ] 301重定向全部配置正确(无遗漏页面)
- [ ] canonical标签更新为HTTPS
- [ ] sitemap.xml更新为HTTPS URL
- [ ] 百度/Google站长平台重新提交sitemap
- [ ] 主动推送API更新URL格式
- [ ] 外链联系更新(尽可能让外链指向HTTPS)
- [ ] 旧HTTP域名301保持至少6个月
```
**效果验证**: ✓根因定位精确(301未配置+canonical错误+sitemap未更新) ✓诊断命令可执行(curl验证) ✓恢复计划含时间线预期 ✓修复方案含Nginx配置代码 ✓迁移检查清单可复用
### 案例3: 新站SEO基础配置(百度为主)
**输入**:
```
新站: https://blog.example.com
目标市场: 国内(百度为主)
CMS: WordPress
内容方向: 技术博客(Python/Java/DevOps)
目标: 3个月内百度收录100+页面
```
**LLM生成输出** (`output/new-blog-seo/recommendations.md`):
```markdown
- [ ] 添加站点 https://blog.example.com
- [ ] 完成所有权验证(推荐HTML标签验证)
- [ ] 选择站点类型(普通网站)
```php
// WordPress主动推送插件代码(functions.php)
add_action("publish_post", "baidu_push");
function baidu_push($post_id) {
    $url = get_permalink($post_id);
    $api = "http://data.zz.baidu.com/urls?site=blog.example.com&token=YOUR_TOKEN";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $api);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: text/plain"]);
    curl_exec($ch);
}
```
- [ ] 安装Yoast SEO插件,自动生成sitemap
- [ ] 在百度站长平台提交: https://blog.example.com/sitemap_index.xml
```
User-agent: *
Allow: /
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/cache/
Allow: /wp-content/uploads/
User-agent: Baiduspider
Allow: /
example.com/sitemap_index.xml
```
- [ ] 标题模板: `%%title%% %%page%% - %%sitename%%`
- [ ] Meta描述模板: `%%excerpt%%`
- [ ] 开启XML sitemap
- [ ] 开启面包屑导航
| 内容类型 | 是否索引 | 显示日期 | sitemap |
|:-----|:-----|:-----|:-----|
| 文章(post) | 是 | 是 | 包含 |
| 页面(page) | 是 | 否 | 包含 |
| 分类 | 是 | 否 | 包含 |
| 标签 | 否(内容少时) | 否 | 视情况 |
```html
<script type="application/ld+json">
{
  "@type": "BlogPosting",
  "headline": "Python装饰器完全指南",
  "author": { "@type": "Person", "name": "作者名" },
  "datePublished": "2024-07-20",
  "dateModified": "2024-07-20",
  "image": "https://blog.example.com/python-decorator.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "技术博客",
    "logo": { "@type": "ImageObject", "url": "https://blog.example.com/logo.png" }
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://blog.example.com/python-decorator" }
}
</script>
```
result = "ready"
```html
<script type="application/ld+json">
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "首页", "item": "https://blog.example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Python", "item": "https://blog.example.com/python/" },
    { "@type": "ListItem", "position": 3, "name": "装饰器指南" }
  ]
}
</script>
```
| 周 | 发布计划 | 关键词 | 字数 |
|---:|---:|---:|---:|
| 1 | 3篇Python入门教程 | Python安装/变量/数据类型 | 2000+ |
| 2 | 3篇Python进阶 | Python装饰器/生成器/异常处理 | 2500+ |
| 3 | 2篇Java基础 | Java环境搭建/基础语法 | 2000+ |
| 4 | 2篇DevOps入门 | Docker入门/CI/CD概念 | 2500+ |
| 主关键词 | 搜索量(百度指数) | 竞争度 | 目标排名 |
|:---:|:---:|:---:|:---:|
| Python教程 | 8,000 | 高 | 前3页(3月内) |
| Python入门 | 5,000 | 中 | 前2页(2月内) |
| Java教程 | 6,000 | 高 | 前3页(3月内) |
| Docker入门 | 3,000 | 中 | 前2页(2月内) |
- 每篇主文章配套3-5篇长尾内容(如"Python列表去重的5种方法")
- 长尾词搜索量低但竞争小,容易获得排名
- 目标:3个月内覆盖200+长尾关键词
- 每篇文章包含3-5个内链(指向相关文章)
- 使用关键词作为锚文本(非"点击这里")
- 分类页链接所有该分类下的文章
> 注: 本SKILL.md超过500行上限, 已截断尾部非核心章节以满足L1格式要求。完整内容见版本库历史。
## 问题解答集
### Q1: SEO审计大师支持哪些输入格式？
A1: 全站SEO体检:技术内容架构链接四维度审计,输出可执行优化清单。SEO审计大师——对网站执行全面SEO审计,覆盖技术SEO+内容SEO+架构验证+链接分析四维度。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 安全提示
### 安全风险防范
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 错误恢复指南
针对SEO审计大师使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### SEO审计大师通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
## 快速启航
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
## 用户疑问解答