# 亚马逊平台规则库（Harness 权威源 · RAG 数据源）

> 更新日期：2026-05-24（v1.1 扩库）  
> 用途：Listing / SEO / 客服 scene 注入；超长时由关键词 RAG 按 query 选段。  
> 数据来源：Seller Central 政策摘要 + 行业实践（生成文案须可核对，勿编造认证）。

---

## A9 搜索与排名核心要素

### 相关性信号

- **标题**权重最高：核心搜索词应出现在标题前 80 字符内。
- **Bullet Points**：补充标题未覆盖的长尾词与使用场景。
- **Backend Search Terms**：250 字节上限，不重复标题已有词，用空格分隔。
- **类目节点（Browse Node）**：选错类目会导致流量错位，文案需与类目属性一致。

### 转化信号

- 主图点击率、Review 星级与数量、价格竞争力、FBA 配送时效。
- 文案目标：提高 CTR（标题钩子）与 CVR（五点解决痛点），而非关键词堆砌。

---

## 标题（Title）规则

### 通用限制

- 大多数类目上限 **200 字符**（部分类目 150 字符，以 Seller Central 为准）。
- 结构建议：`[品牌] + [核心关键词] + [核心功能/规格] + [型号/数量] + [适用场景]`。
- 每个单词首字母大写（介词 in/on/for、连词 and/or 除外）。
- **禁止**：全部大写、促销用语（Sale、Free Shipping）、特殊符号（! ? $ # @）。

### 标题禁用模式

- 重复同一关键词 3 次以上（被视为 spam）。
- 堆砌竞品品牌名或未授权兼容表述（如 "for iPhone" 需 MFi 或明确通用描述）。
- 时效词：New、Latest、2026 Edition（除非产品型号本身含年份且属实）。
- 主观排名：Best Seller、#1、Top Rated、Amazon's Choice（文案中不得宣称）。

### 子类目标题差异

- **电子产品**：型号、协议（Bluetooth 5.3、USB-C PD）、容量/续航数字优先。
- **服装鞋帽**：性别/年龄段、材质亮点、版型（Slim/Regular），避免均码无范围。
- **家居**：尺寸（L×W×H）、容量、材质、适用空间。
- **美妆个护**：容量（ml/oz）、肤质/发质、关键成分，禁止医疗功效词。

---

## 五点描述（Bullet Points）

### 格式要求

- 共 **5 条**，每条上限 **500 字符**。
- 每条以 **大写核心卖点词** 开头，后接具体说明。
- 包含可验证数字：重量(g)、尺寸(cm/inch)、续航(h)、功率(W)等。
- 避免与标题完全重复的句子。

### 内容结构建议

1. 核心功能 + 解决的主要痛点  
2. 关键参数 / 兼容性 / 适用人群  
3. 材质 / 工艺 / 耐用性 / 安全认证（如有）  
4. 包装清单 / 保修 / 售后政策表述（不夸大）  
5. 使用场景 / 差异化（与竞品区隔，不点名攻击）

### 五点禁用内容

- 外部链接、邮箱、电话、社交媒体账号。
- 要求买家好评、改评、返现等操纵 Review 的表述。
- 绝对化：100% Guaranteed、Miracle、Cure、FDA Approved（无批文时）。

---

## 产品描述（Description）

- 普通描述：纯文本，建议 1000–2000 字符内，段落清晰。
- A+ Content：需品牌备案，图文模块；Harness 输出以文本描述为主，可提示「可转 A+ 模块」。
- 使用场景化语言，避免大段参数表复制五点内容。
- HTML 标签：多数类目不允许在描述中使用复杂 HTML（以当前类目为准）。

---

## Backend Search Terms（后台搜索词）

- **250 字节**上限（非 250 字符；中文等多字节语言需特别注意）。
- 用**空格**分隔，不用逗号、顿号。
- 不包含：标题/五点已出现的词、品牌名（自己的可省略）、禁售词。
- 应包含：同义词、拼写变体、口语搜索词、场景词（如 travel gym office）。
- 禁止：竞品 ASIN、竞品品牌、侮辱性词汇。

---

## 禁用词汇与合规表述（全局）

### 绝对化与促销类

| 禁用 | 替代表述 |
|------|----------|
| Best / #1 / Top / Cheapest | Premium quality / High-performance |
| 100% Guaranteed / Risk-free | Backed by warranty / Satisfaction-focused support |
| Free Gift / On Sale / Limited Time | （不在 Listing 写促销，用 Coupon 工具） |
| Amazon's Choice / Best Seller | （不得出现在卖家自拟文案） |

### 医疗与健康宣称

- 禁止：cure, treat, diagnose, prevent disease, anti-virus（无证据时）, prescription strength。
- 美妆：用 "helps improve the appearance of" 替代 "eliminates wrinkles"。
- 膳食补充剂：需符合 FDA DSHEA 及当地法规，勿写治疗疾病。

### 环保与认证

- Eco-friendly / Organic / Non-toxic：**仅在有对应认证**时可用，并注明认证类型。
- FCC / CE / UL / RoHS：须与实际上架站点及库存 SKU 资质一致。
- 儿童产品 CPSIA、食品 FDA：无资质不得暗示。

### 侵权与对比

- 不得使用其他品牌商标作为关键词堆砌。
- "Compatible with [Brand]" 需真实兼容且不暗示官方授权。
- 不得复制竞品 Listing 原文。

---

## 类目合规要点

### 电子产品

- 无线设备：FCC ID（美）、CE（欧）、SRRC（中）等按站点声明。
- 锂电池：UN38.3、MSDS、Wh 额定容量；航空运输限制需在说明中准确。
- 充电器：输入电压 100–240V、输出功率(W)、协议（PD/QC）须准确。
- 禁止：未实测的 IP 防水等级（如写 IPX7 需检测报告）。

### 服装鞋帽

- 成分百分比：如 95% Cotton, 5% Spandex，忌「优质面料」等模糊词。
- 尺码：标明 US/EU/Asian 尺码体系及 Size Chart 位置。
- 护理说明：Machine wash cold / Do not bleach 等。
- 儿童服装：CPSIA 铅/邻苯二甲酸酯等（美国站）。

### 家居

- 尺寸单位明确（cm 与 inch 对照可选）。
- 承重上限、是否需墙锚、是否含甲醛/ VOC 认证。
- 尖锐边角、小零件窒息警告（儿童可接触时）。

### 美妆个护

- 成分表关键项、过敏原（nuts, fragrance）。
- 防晒 SPF 值需 FDA/当地注册；染发剂需警示语。
- 禁止：立即见效、100% 有效、替代医疗。

### 食品与补充剂

- 保质期、储存条件、过敏原、净含量。
- 健康声称受严格限制；有机需 USDA Organic 等。

---

## 各站点差异（文案侧提示）

### 美国站 (amazon.com)

- 英文地道表达，计量常用 inch、oz、lb。
- FTC 对 Made in USA 声明有严格要求。
- 加州 Prop 65 警告（如适用）。

### 欧洲站 (DE/FR/IT/ES 等)

- 本地语言或英语+本地语言策略；CE、WEEE、ERP 能效标签。
- GPSR（2024 起）产品安全与责任人信息趋势，文案可预留 manufacturer contact 提示。

### 日本站 (amazon.co.jp)

- 标题与五点常较短；敬语与礼貌表达；PSE、TELEC 等认证。

---

## 图片与 Listing 一致性（文案须对齐）

- 主图：白底 RGB 255,255,255，产品占帧 85%+，无文字/logo/水印（主图规则）。
- 文案不得描述主图未展示的功能或配件。
- 变体（颜色/尺寸）：标题与五点需与 Parent/Child 关系一致，避免混淆。

---

## 常见下架与审核拒绝原因

1. **违禁词**：标题或五点含 Best、Free、促销信息。  
2. **类目错放**：如把配件放在主机类目。  
3. **认证缺失**：宣称 FCC/CE/UL 但后台无对应文件。  
4. **Medical claims**：护肤、器械类越界宣称。  
5. **Intellectual Property**：品牌词侵权、图片盗用。  
6. **Restricted Products**：刀具、化学品、电池未按政策申报。  
7. **Variation abuse**：变体主题与属性不符。  
8. **Review manipulation**：文案引导留评。

---

## 2025–2026 政策趋势（运营关注）

- **AI 生成内容**：亚马逊要求卖家对 Listing 准确性负责；AI 输出必须人工审核。
- **合规审查加严**：消费品安全（CPSC、GPSR）与环保声明抽查增加。
- **Brand Registry**：A+、Brand Store、vine 与文案品牌调性绑定更紧。
- **Low-price store / 低价商城**：部分 SKU 需简化五点，强调极致性价比与合规底价。

---

## 关键词策略（与 SEO scene 协同）

- 核心词 1–3 个放标题；长尾词放五点与 Backend。
- 使用 Brand Analytics / 第三方词库验证搜索量（Harness 输出为建议，需运营确认）。
- 避免高竞争泛词独占标题（如仅写 "Headphones"）。

---

## 客服与消息政策（chat_reply 交叉引用）

- Buyer-Seller Messaging：24h 内回复（绩效）；禁止营销外链与索评。
- 不得在消息中承诺 Listing 未写的退款政策。
- 详见 `scenes/chat_reply/policies/messaging-guard.md`。

---

## 质量自检清单（生成后人工核对）

- [ ] 标题 ≤200 字符且含核心词  
- [ ] 五点 =5 条且每条 ≤500 字符  
- [ ] 无禁用词表命中  
- [ ] 认证表述与资质文件一致  
- [ ] 计量单位与包装/实物一致  
- [ ] 无竞品商标侵权表述  
- [ ] Backend 词不重复标题词  

---

## 子类目禁用词与敏感表述（RAG 检索锚点）

> 生成时若 payload 含 `category`，Composer 会注入对应 `platforms/amazon/categories/*.md`；本节为跨类目全局禁词与高风险词补充。

### 电子产品（electronics）

| 高风险词 | 原因 | 建议替换 |
|----------|------|----------|
| Military-grade / 军工级 | 无法验证 | Durable construction / Reinforced design |
| Hacking / 监听 / 偷拍 | 受限品类 | （勿用于普通 3C） |
| Unlimited range | 虚假宣传 | Up to Xm wireless range (实测值) |
| Fast charging 100% in 5 min | 需可验证 | Supports XXW PD, charges to 50% in X min |
| Waterproof without IP rating | 合规风险 | Splash-resistant / IPX4 (with test report) |
| FDA Approved（非医疗器械） | 越界 | N/A — 删除 |

### 服装鞋帽（apparel）

| 高风险词 | 原因 | 建议替换 |
|----------|------|----------|
| One size fits all | 高退货 | Free size, bust/waist range XX–XX cm |
| Slimming / 显瘦 10 斤 | 不可验证 | Flattering fit / Comfortable stretch |
| Anti-radiation（无证据） | 医疗暗示 | （删除或提供检测报告） |
| Genuine leather（非真皮） | 材质欺诈 | PU leather / Faux leather / 100% Cowhide |
| Child / Kid 无 CPSIA | 美国站合规 | 确认类目资质后再写 age range |

### 家居（home）

| 高风险词 | 原因 | 建议替换 |
|----------|------|----------|
| Formaldehyde-free（无检测） | 环保宣称 | Low-VOC materials (cert XXX) |
| Load-bearing XXX kg（无测试） | 安全风险 | Max load XX kg (lab tested) |
| Food-grade（非食品接触） | 误导 | BPA-free (if applicable) |
| Mold-proof / 永不发霉 | 绝对化 | Easy to clean, dry after use |

### 美妆个护（beauty）

| 高风险词 | 原因 | 建议替换 |
|----------|------|----------|
| Whitening / 漂白（部分站点敏感） | 功效越界 | Brightening / Even skin tone appearance |
| Anti-aging miracle | 医疗暗示 | Helps reduce the appearance of fine lines |
| SPF 50+（无注册） | 法规 | 删除或填写真实 SPF 注册号 |
| Pregnancy-safe（无证据） | 责任风险 | Consult physician if pregnant or nursing |
| Removes wrinkles in 7 days | 绝对化 | With regular use, skin feels smoother |

### 食品与补充剂（food / supplement）

- 禁止：lose weight fast、cure diabetes、replace medication、doctor recommended（无授权）。
- 过敏原必须明示：Contains milk, soy, tree nuts, wheat, eggs, fish, shellfish。
- Organic / Non-GMO 需 USDA 或对应认证编号。

---

## 欧盟 GPSR 与产品安全（2024 起 · 文案侧）

General Product Safety Regulation (GPSR) 影响在欧销售的大多数非食品消费品。

### 卖家须在合规渠道提供（Listing 文案可提示「见包装/说明书」）

- **制造商名称与 postal address**（欧盟境内或负责人 EU Responsible Person）。
- **产品标识**（型号、批次 traceability）。
- **安全警示与使用限制**（语言需匹配销售国）。
- **CE 标记**（适用时）及符合性声明可追溯。

### Listing 文案建议

- 五点或描述末尾可加：`Manufacturer: [Brand Legal Name]. EU Responsible Person available per GPSR.`（仅当后台已配置）。
- 勿在文案中虚构 CE 或 GPSR 联系人。
- 玩具 EN71、电器 LVD/EMC、儿童产品 需与类目要求一致。

### WEEE 与包装

- 电子电气设备：WEEE 注册与回收标识（德国 ElektroG 等）按站点执行。
- 包装法 EPR：德法等国包装注册号不在 Listing 正文堆砌，但产品描述避免「无需回收」类误导。

---

## 英国 / 欧盟 VAT 与税务（文案勿越界）

- **Listing 正文不得写含税/不含税最终价**（价格由 Offer 层管理）。
- 避免 `VAT included`、`Duty-free` 除非运营确认与 Buy Box 价格策略一致。
- 英国站：UKCA 标记（替代 CE 的过渡已结束，按品类确认）。
- 北爱尔兰：双重标记策略需运营确认，文案勿自行解释税务。
- 跨境 B2C 低价值包税规则变更频繁：**Harness 不生成税务建议**，仅提示卖家咨询会计师。

---

## 北美合规补充（CPSC / FTC / Prop 65）

### CPSC（美国消费品安全委员会）

- 儿童产品（12 岁及以下）：CPSIA 铅、邻苯二甲酸酯、追踪标签（制造商、生产日期、批次）。
- 耐用婴童产品需 CPC (Children's Product Certificate)。
- 文案含 Small parts choking hazard 若适用 3 岁下。

### FTC Made in USA

- 宣称 `Made in USA` / `American-made` 需「几乎全部在美国生产」；否则用 `Assembled in USA` 并说明进口组件。
- 虚假原产地声明可被 FTC 处罚。

### 加州 Prop 65

- 若产品含 Listed Chemicals，需警告语；Listing 可写 `WARNING: Cancer and Reproductive Harm - www.P65Warnings.ca.gov`（仅当适用）。
- 勿默认所有产品加 Prop 65 警告。

---

## 变体（Parent/Child）与 Listing 一致性

### 主题（Variation Theme）

- 常见：Color、Size、Style、Flavor、Count。
- **标题**：Parent 不含单一变体值；Child 标题含 Color=Red 或 Size=Large（按主题）。
- **五点**：共享核心卖点；变体差异（颜色/尺码）在 Child 层微调，勿复制粘贴完全相同五点导致违规重复。

### 禁止变体滥用

- 不同产品（非真实变体）共挂 Parent 会被拆链或下架。
- 变体图片必须与对应 SKU 一致。
- 文案中的 ASIN 数量、包装件数须与 Child 属性一致。

---

## 受限与需审批品类（Restricted Products）

以下品类 Listing 需额外审批或禁止；Harness 生成通用文案时**不得暗示可售**：

| 类别 | 文案注意 |
|------|----------|
| 锂电池（独立寄送） | 容量 Wh、UN38.3；勿鼓励航空随身大容量 |
| 激光指示器 | 功率 mW 限制因国而异 |
| 农药 / 杀生物剂 | 需 EPA 等注册号 |
| 医疗器材 | FDA 510(k) 等，禁止 consumer 文案写 prescription |
| 酒精 / 烟草 | 多数站点禁止第三方卖家 |
| 武器、弹药、零件 | 禁止 |
| 加密设备 / 监听 | 出口管制，Restricted |
| 召回品 / 仿牌 | 禁止 |

卖家中心路径：Inventory → Add a Product → 查看 Approval Required。

---

## 2026 政策与平台动态（运营日历）

| 时间 | 事项 | 对 Listing 的影响 |
|------|------|-------------------|
| 2026 Q1 | GPSR 执法常态化 | 欧站需完整安全与责任人信息 |
| 2026 | AI 生成内容披露趋势 | 部分站点要求标注 AI-assisted；卖家对准确性全责 |
| 2026 | 低价商城 / Haul 分流 | 部分 SKU 需更短标题、强调 unit price |
| 2026 | 评论政策持续收紧 | 文案、包装插页、消息均禁止索评 |
| 2026 | 品牌滥用投诉增多 | 标题/backend 勿堆砌他人商标 |
| 持续 | 库存绩效 IPI | 文案准确性降低退货率，间接影响 IPI |

---

## Backend 关键词示例（勿直接复制，需去重）

**示例 A — 蓝牙耳机**  
`wireless earphones gym running commute noise isolation ear hooks replacement tips`

**示例 B — 厨房收纳**  
`pantry organizer cabinet stackable bins kitchen closet small apartment rental`

**规则**：与标题/五点去重后填入；字节计数用 Seller Central 后台工具验证。

---

## A+ Content 与 Brand Story（文案延伸）

- **A+ Basic**：5 模块以内，品牌备案后可用；Harness 文本描述可拆为：品牌故事、对比表、场景图说明。
- **A+ Premium**：视频、热点图；文案需与主 Listing 五点一致，不得矛盾。
- **Brand Story**：情感叙事，仍受禁用词与认证规则约束。
- 生成 JSON 中的 `description` 可作为 A+ 模块草稿，须人工排版上传。

---

## 退货率与文案关联（运营指标）

- **尺码不清** → 服装类退货主因；文案必须指向 Size Chart。
- **颜色/材质预期不符** → 写明 Matte / Glossy、Light Gray vs Dark Gray。
- **功能夸大** → 3C 类差评与退货；参数必须与说明书一致。
- **缺少兼容列表** → 手机壳/充电器退货；列出或链接兼容型号范围。

Harness 效果闭环（`external_id` + outcomes）用于对比 template 版本对退货/转化的影响。

---

*本文件为 TokenApi Harness Layer 2 权威规则源；技能目录 references/ 仅为副本。*
