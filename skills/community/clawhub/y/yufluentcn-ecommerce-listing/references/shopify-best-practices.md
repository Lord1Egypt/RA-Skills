# Shopify 平台规则库（Harness 权威源 · RAG 数据源）

> 更新日期：2026-05-28（v1.2 扩库）  
> 用途：Listing / SEO / 客服 / `shopify_operator` scene 注入；超长时由关键词 RAG 按 query 选段。  
> 数据来源：Shopify Help Center 摘要 + 独立站 DTC 实践（生成文案须可核对，勿编造认证）。

---

## 店铺搜索与发现（Shopify Search + 站外 SEO）

### 站内搜索相关性

- **产品标题**是站内搜索权重最高的字段；核心词应靠前，避免无意义品牌后缀堆砌。
- **产品类型（Product type）**、**厂商（Vendor）**、**标签（Tags）**影响集合页与筛选；Tags 应用英文小写、连字符，勿与标题完全重复。
- **描述正文**中的 `h2`/`h3` 与列表项可被索引；首屏 160 字内应出现核心品类词。

### Google / 站外 SEO

- **SEO title（meta_title）**：建议 ≤60 字符（含空格），含 1 个核心词 + 品牌；勿与 H1 标题逐字相同。
- **Meta description**：建议 ≤160 字符，含利益点 + 弱 CTA（Shop now / Learn more），禁止虚假促销截止日。
- **URL handle**：短、含关键词、仅小写与连字符；改名会产生 301，旧链接需运营确认。
- **结构化数据**：Shopify 自动输出 Product schema；文案中的价格、库存、SKU 须与后台 Offer 一致，否则富摘要异常。

### 转化信号（DTC）

- 首屏：主图 + 标题 + 价格 + 加购按钮；移动端拇指区可操作。
- 信任：评价 App、支付图标、退换政策链接；文案可指向 Policy 页，勿在正文写过长条款。
- 速度：图片 WebP、懒加载；描述避免嵌入大段 base64 或外链脚本。

---

## 产品标题（Title / Product name）

### 通用限制

- Shopify **无硬性 200 字符上限**，但前台展示与 Google 标题常截断在 **~70 字符**可见区；建议总长 **≤150 字符**（含品牌）。
- 结构建议：`[品牌] · [核心品类词] – [关键规格/场景] – [型号/容量]`。
- **禁止**：全大写标题、连续感叹号、HTML 标签、未授权 emoji 堆砌（1–2 个点缀可接受，视品牌调性）。

### 标题禁用模式

- 「全网最低」「Official Store of [他人品牌]」「#1 in [品类]」等无法验证的排名宣称。
- 重复同一关键词 4 次以上（spam）。
- 把促销语写进标题（Sale 50% Off）——用 **Compare-at price** 与 **Discount** 工具管理。
- 侵权：未授权使用他人商标、影视 IP、球队 Logo 名。

### 子类目标题差异

- **电子产品**：协议（USB-C PD、Bluetooth 5.x）、容量 Wh、mAh、兼容型号范围。
- **服装鞋帽**：性别/版型、面料成分百分比、尺码体系（US/EU/Asian）。
- **家居**：尺寸 L×W×H、承重、材质、室内/户外场景。
- **美妆个护**：容量 ml/oz、肤质、关键成分；禁止医疗功效。

---

## 产品描述（Description / Body HTML）

### 格式要求

- 推荐结构：**痛点场景 1–2 句** → **3–5 个卖点小节（h2/h3）** → **规格表（ul/table）** → **包装/保修** → **FAQ 2–3 条**。
- 允许标签：`h2` `h3` `p` `ul` `ol` `li` `strong` `em` `br`；**禁止** `script` `iframe` 未审核第三方追踪。
- 单段不宜超过 120 字（移动端）；总长度建议 **800–2500 字**（视品类），避免复制 Amazon 五点 verbatim。

### 内容结构建议

1. 谁适合买 + 解决什么问题  
2. 核心功能与可验证参数  
3. 材质 / 工艺 / 认证（有则写编号）  
4. 包装清单与质保（链接到 Warranty Policy）  
5. 使用场景图说（与主图一致）

### 描述禁用内容

- 外部购买链接（引导去 Amazon/eBay 等）——违反多数主题与支付政策。
- 索取好评、返现改评、Discord/Telegram 私域引流（除非合规营销且不与订单绑定）。
- 绝对化：100% cure、miracle、doctor recommended（无授权）。

---

## 变体（Variants）与选项命名

- **选项名**清晰：`Color` / `Size` / `Material`；值用 `Midnight Blue` 而非 `样式1`。
- 变体 **SKU** 与库存、条码一致；文案中的「含配件」须对应正确变体。
- **组合变体**过多时：Parent 描述写共性，变体层可省略重复段落（通过 metafields 或 App 管理）。
- 预售 / 缺货：文案写清 **Preorder** 预计发货周，与 Inventory policy 一致。

---

## 集合（Collections）与标签策略

- **智能集合**规则与文案关键词对齐（如 Tag `wireless-earbuds` + Type `Electronics`）。
- 集合 SEO title/description 独立优化，勿留空。
- 避免为 SEO 创建空集合或仅 1 个产品的「关键词垃圾集合」。

---

## 禁用词汇与合规表述（全局）

### 绝对化与促销类

| 禁用 | 替代表述 |
|------|----------|
| Best / #1 / Cheapest on earth | Premium / Customer-favorite |
| 100% Guaranteed results | Covered by our warranty policy |
| Limited time only（无真实截止） | （用 Shopify Discount 配置） |
| Free gift if you buy now | Bundle offer（须在结账层配置） |

### 医疗与健康宣称

- 禁止：cure, treat, diagnose, prescription strength（非处方药场景）。
- 美妆：用 "helps improve the appearance of" 替代 "eliminates wrinkles overnight"。
- 膳食补充剂：符合当地法规；美国站注意 FDA structure/function claims。

### 环保与认证

- Organic / Eco-friendly / BPA-free：**仅在有检测或认证**时写，并注明标准（如 GOTS, OEKO-TEX）。
- CE / FCC / UKCA：与目标市场及实物一致；儿童产品 CPSIA（美国）。

### 侵权与对比

- 不得暗示官方授权（"Genuine Apple charger" 需 MFi 或真实授权）。
- Compatible with [Brand] 需真实兼容，且不复制竞品描述原文。

---

## 类目合规要点（与 categories/*.md 协同）

### 电子产品

- 充电器：输入 V、输出功率 W、协议（PD/PPS）；锂电池 Wh 与运输限制。
- 无线：频段、FCC/CE；勿写未实测的 IP 等级。
- 兼容性列表：手机型号年份范围，降低退货。

### 服装鞋帽

- 成分：95% Cotton, 5% Elastane；提供 Size chart 链接或内嵌表。
- 护理：Machine wash cold；国家站计量 inch/cm 对照可选。

### 家居

- 尺寸、承重、是否需墙锚；甲醛/VOC 须有报告才写 low-VOC。

### 美妆个护

- 成分过敏原；SPF 须注册；禁止 7 天去皱类绝对化。

---

## 跨境与多市场（Markets / Localization）

- **Shopify Markets**：各市场货币、关税、翻译可独立；Harness 输出需指定 `lang` 与站点。
- **欧盟 GPSR**：制造商与 EU RP 信息可在 Policy 页；描述可提示 "See product label for safety info"。
- **英国 UKCA**、**德国 WEEE/VerpackG**：合规标识不在正文堆砌注册号，但勿写误导性「无需回收」。
- **税务**：正文不写最终含税价；价格由 Market 与结账配置。

---

## 支付、配送与政策页（文案引用）

- 退换货：链接 **Refund policy**；正文写 "See our return policy" 而非与后台矛盾的 90 天无理由（若实际 30 天）。
- 配送时效：与 Shipping profile 一致；勿写 "ships today" 若处理时间 3–5 天。
- 订阅（Subscriptions）：清楚写计费周期与取消方式。

---

## 图片与文案一致性

- 主图：产品占画面主体；生活方式图可副图；Alt text 含品类词，勿关键词堆砌。
- 文案不得描述主图未展示的配件或功能。
- **对比图**：须真实拍摄或合法授权素材，禁止盗用竞品图。

---

## 常见审核与客户投诉原因

1. 误导性折扣或划线价（Compare-at 虚高）。  
2. 医疗/减肥绝对化宣称。  
3. 侵权商标或 IP。  
4. 尺码/颜色与实物不符导致退货。  
5. 描述含外链导流至站外支付。  
6. 违禁品（武器、管制化学品、未申报电池）。  
7. 儿童产品无适用警示语。

---

## 2025–2026 独立站趋势（运营关注）

- **AI 内容**：卖家对 PDP 准确性全责；生成后须人工审核。  
- **Core Web Vitals**：描述轻量化利于 SEO。  
- **UGC 评价**：Judge.me / Loox 等与文案卖点一致。  
- **邮件/SMS 合规**：文案与客服 scene 遵守 CAN-SPAM / GDPR 同意。  
- **TikTok Shop / Instagram Shop** 联动：PDP 信息可与频道一致，但各平台禁词表不同（见 `platforms/tiktok/rules.md`）。

---

## 关键词策略（与 seo_keywords scene 协同）

- 核心词在 **title + 首段 + meta_title**；长尾词在 **h2 小节与 Tags**。
- 博客内容（Shopify Blog）可做信息型长尾；Harness JSON 可输出 `blog_angle` 建议。
- 避免与 Google Ads 落地页 **完全重复** 导致质量分低——可共享核心卖点但调整句式。

---

## 客服与消息（chat_reply 交叉引用）

- Shopify Inbox / 邮件：24h 内回复提升转化；禁止站外支付链接。
- 不得承诺 Listing/Policy 未写的退款比例。
- 详见 `scenes/chat_reply/policies/messaging-guard.md`。

---

## 子类目高风险词（RAG 检索锚点）

### 电子产品（electronics）

| 高风险词 | 建议 |
|----------|------|
| Military-grade | Durable / Reinforced |
| Unlimited battery life | Up to X hours (tested) |
| FDA Approved（非器械） | 删除 |

### 服装（apparel）

| 高风险词 | 建议 |
|----------|------|
| One size fits all | Free size, bust/waist range |
| Genuine leather（非真皮） | Faux leather / 100% Cowhide |

### 家居（home）

| 高风险词 | 建议 |
|----------|------|
| Formaldehyde-free（无检测） | Low-VOC (cert XXX) |
| Load XXX kg（无测试） | Max load X kg (tested) |

### 美妆（beauty）

| 高风险词 | 建议 |
|----------|------|
| Whitening miracle | Brightening / Even tone appearance |
| SPF 50+（无注册） | 删除或真实 SPF |

---

## 质量自检清单（生成后人工核对）

- [ ] 标题 ≤150 字符且含核心词  
- [ ] meta_title ≤60、meta_description ≤160  
- [ ] 描述 HTML 无 script/外链购买  
- [ ] 无禁用词表命中  
- [ ] 认证与实物/Policy 一致  
- [ ] 变体 SKU/库存与文案一致  
- [ ] 价格与 Markets 配置一致（正文不写死含税价）  

---

*本文件为 TokenApi Harness Layer 2 权威规则源；`skills/*/references/` 仅为副本。*
