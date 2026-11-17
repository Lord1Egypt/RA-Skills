# 合规 · 关键词与文案

> 由 [`google-ads-compliance.md`](google-ads-compliance.md) 索引。**何时 Read**：关键词生成、多语言、修饰语、Headlines/Descriptions 清单、新广告主验证

## Contents

- 七、关键词生成规则
- 八、多语言关键词规则
- 九、高风险与安全修饰语速查
- 十、广告文案（Headlines / Descriptions）合规清单
- 十〇.三、新广告主身份验证与 Limited Ad Serving

---

## 七、关键词生成规则

### 7.1 匹配类型选择

| 场景               | 推荐匹配类型             | 理由                     |
| ------------------ | ------------------------ | ------------------------ |
| 新账户/探索期      | Broad Match              | 最大覆盖，收集搜索词数据 |
| 高转化已验证词     | Exact Match `[keyword]`  | 控制成本，最大 ROI       |
| 平衡方案           | Phrase Match `"keyword"` | 兼顾覆盖和精准           |
| 自有品牌词         | Exact + Phrase           | 保护品牌，捕获变体       |
| 长尾词（5+ 字）    | Phrase Match             | 捕获自然语言变体         |
| 竞品词（如已授权） | Broad Match              | 避免精确匹配触发商标     |

> 与 `ad campaign-create` 的 `--keywords` 格式对照：`词→BROAD`、`"词"→PHRASE`、`[词]→EXACT`

### 7.2 否定关键词策略

**必生成的通用否定词**（除非与用户业务直接相关）：

```
free, torrent, download free, crack, hack, pirated,
jobs, salary, career, hiring, interview,
DIY, how to make, tutorial,
scam, fraud, complaint, lawsuit,
reddit, quora, wiki, youtube,
sample, template, example
```

**按行业追加否定词**：

| 行业         | 推荐否定词                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------- |
| 电商/零售    | `used`、`second hand`、`repair`、`manual`、`recall`、`review`（如不投信息流）、`vs`（如不投比较） |
| SaaS/软件    | `open source`、`free alternative`、`crack`、`keygen`、`torrent`、`github`、`self-hosted`          |
| 教育/培训    | `free course`、`pirated`、`PDF download`、`answer key`、`cheat sheet`、`exam answers`             |
| B2B/企业服务 | `B2C`、`consumer`、`personal`、`small business`（如仅做大客户）、`intern`、`entry level`          |
| 旅游/酒店    | `jobs`、`careers`、`salary`、`volunteer`、`free stay`、`hostel`（如高端定位）                     |
| 房产/地产    | `rent`（如仅售卖）、`free`、`government housing`、`homeless`、`foreclosure`（如非相关业务）       |
| 医疗/健康    | `home remedy`、`DIY`、`natural cure`、`side effects of`（如非药品信息类）                         |
| 金融/保险    | `scam`、`complaint`、`lawsuit`、`free money`、`payday`（如非发薪日贷款）                          |
| 法律服务     | `DIY legal`、`free lawyer`、`pro bono`（如非公益服务）、`law school`、`paralegal jobs`            |

### 7.3 每广告组关键词数量

| 指标           | 建议值               |
| -------------- | -------------------- |
| 正向关键词最少 | 5                    |
| 正向关键词推荐 | 10-20                |
| 正向关键词最多 | 30（超出拆分广告组） |
| 否定关键词最少 | 3                    |
| 否定关键词推荐 | 5-10                 |

### 7.4 关键词长度

| 类型           | 适用场景                          |
| -------------- | --------------------------------- |
| 1-2 词（短尾） | 高竞争、广泛意图；配 Phrase/Exact |
| 3-4 词（中尾） | 平衡意图与特异性；**理想长度**    |
| 5+ 词（长尾）  | 低流量高转化；配 Phrase           |
| 单词上限       | 80 字符（Google 技术限制）        |

---

## 八、多语言关键词规则

| 语言/地区                | 规则                                                                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 中文（CJK）              | 使用中文字符，不用拼音；简体/繁体按目标市场区分；字符双倍计数（见 3.2.1）                                                           |
| 日语                     | 避免 "効く"（有效）——无药事法许可不能用；"No.1" 需注明调查来源；片假名品牌名须与官方写法一致                                        |
| 韩语                     | 助词连写（"러닝화를"）；品牌名用官方韩文写法或保留英文原文；避免 "최고"（最高）等绝对化                                             |
| 西班牙语/葡萄牙语        | 注意地区变体（es-ES vs es-MX，pt-BR vs pt-PT）；重音符号不可省略（\"información\" ≠ \"informacion\"）；巴西葡语与欧洲葡语拼写差异大 |
| 阿拉伯语/希伯来语（RTL） | 确保关键词文本方向正确；数字和英文品牌名在 RTL 中可能显示异常——测试后投放                                                           |
| 德语/EU                  | 健康声明须符合 EU Regulation (EC) No. 1924/2006；德语复合词（如 "Laufschuhe"）是合法关键词                                          |
| **混合语言文案**         | 同一条 headline/description 中**不混用两种语言**（"Buy 跑步鞋" ❌）；品牌名保留原文除外（"iPhone 保护壳" ✅）                       |
| 所有语言通用             | 同样适用编辑规则（大小写/标点/间距对应该语言的规范）；**关键词语言须与落地页语言一致**                                              |

---

## 九、高风险与安全修饰语速查

### 高风险修饰语（频繁触发审核）

| 修饰语       | 风险场景                  | 处理方式                               |
| ------------ | ------------------------- | -------------------------------------- |
| "cheap"      | 金融/医疗场景高风险       | 替换为 "affordable"                    |
| "fast"       | 搭配健康结果高风险        | 搭配物流/效率可用                      |
| "instant"    | 搭配医疗/金融结果极高风险 | 仅用于明确可实现的场景（即时下载）     |
| "secret"     | 被标记为 clickbait        | 避免使用                               |
| "guaranteed" | 几乎总触发审核            | 用 "backed by" / "with warranty"       |
| "cure"       | 非药企禁用                | 用 "may support"、"helps with"         |
| "hack"       | 歧义词                    | "life hack" 可用；"account hack" 禁止  |
| "best"       | 需第三方证据              | 用 "top-rated"（需有评分）或 "popular" |

### 安全修饰语（低风险、广泛接受）

```
near me, reviews, vs, compare, how to, for beginners,
for [audience], professional, affordable, certified, licensed,
[year] (如 "best CRM 2026"), top-rated (需有评分),
trusted, reliable, expert, custom, premium
```

---

## 十、广告文案（Headlines / Descriptions）合规清单

`ad ad-create` 与 `campaign-create` JSON 内 RSA 的 `headlines` / `descriptions` 必须满足：

| #   | 检查项           | 规则                                                                                                    |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------- |
| 1   | 字符限制         | 每条 headline ≤ 30 字符；每条 description ≤ 90 字符                                                     |
| 2   | 数量             | `campaign-create` JSON：**Headlines = 15**、**Descriptions = 4**（须写满）；`ad ad-create` 仍为 ≥3 / ≥2 |
| 3   | 无 ALL CAPS      | 除非缩写                                                                                                |
| 4   | 无多余感叹号     | Headlines 里 0 个；Descriptions 里最多 1 个                                                             |
| 5   | 无电话/邮箱      | 用 extension 代替                                                                                       |
| 6   | 无商标侵权       | 不含未授权品牌名                                                                                        |
| 7   | 无虚假承诺       | 不含 "guaranteed"、"instant cure" 等                                                                    |
| 8   | 与落地页一致     | 承诺的优惠/功能在 `--final-url` 页面可见                                                                |
| 9   | 无重复内容       | Headlines 之间不重复；Descriptions 之间不重复                                                           |
| 10  | Path 合规        | `--path1` / `--path2` 各 ≤ 15 字符，不含特殊字符                                                        |
| 11  | 价格/折扣可验证  | 文案提到价格或折扣 → 落地页同步可见（见 3.5 节）                                                        |
| 12  | CJK 字符双倍计数 | 中文 headline 最多约 15 字；description 最多约 45 字（见 3.2.1 节）                                     |

### 10.1 RSA（自适应搜索广告）专项合规

RSA 的特殊性在于 Google 会**自动组合**你的 headlines 和 descriptions。这意味着：

| 规则                                       | 说明                                                                    |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| **任意两条 headline 组合须合规**           | H1 = "Free Consultation"，H2 = "Guaranteed Results" → 组合后 = 双重违规 |
| **任意 headline + description 组合须合规** | 不能依赖特定顺序来使文案合理                                            |
| **Pinning 不免除合规**                     | 即使 pin H1 到位置 1，其余 headlines 仍会自由组合                       |
| **避免矛盾信息**                           | H1 = "最低价" + H3 = "高端定制" → 组合后语义矛盾                        |
| **每条独立可用**                           | 每条 headline / description 单独看也要有意义且合规                      |

**RSA 合规生成策略**：

1. 先生成所有 headlines 和 descriptions
2. 随机取任意 2 条 headlines + 1 条 description 组合
3. 检查组合后是否有矛盾、重复、或违规
4. 如有问题，修改或移除问题文案

### 10.2 广告附加信息（Extensions）合规

`ad extension sitelink/call/callout/snippet` 同样受审核：

| 类型                                 | 合规要点                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **Sitelink**（附加链接）             | 链接文本 ≤ 25 字符；每条指向不同落地页；不可 4 条都指向同一 URL；文本须与目标页内容相关                 |
| **Call**（附加电话）                 | 电话号码须真实可拨通；国家代码须正确；不能指向付费高价电话（premium-rate）                              |
| **Callout**（宣传信息）              | ≤ 25 字符；不可重复广告正文内容；不含感叹号；描述性而非行动性（"Free Shipping" ✅，"Buy Now!" ❌）      |
| **Structured Snippet**（结构化摘要） | Header 须从 Google 预设列表选择（Brands/Services/Types 等）；Values 须与 Header 类别匹配；≥ 3 个 values |

**Extensions 通用规则**：

- 同样适用编辑规则（大小写、标点、间距）
- 不可包含电话号码在非 Call Extension 中
- 不可包含虚假承诺或误导信息
- 所有链接目标须可访问且与内容相关

---

## 十〇.三、新广告主身份验证与 Limited Ad Serving

Google 2023 年起对新广告主实施 **Limited Ad Serving**（有限广告投放）策略，2025-2026 年持续强化：

### 什么是 Limited Ad Serving

| 阶段       | 说明                                                |
| ---------- | --------------------------------------------------- |
| 新账户初期 | Google 会限制广告展示量，直到建立足够的广告主信任度 |
| 信任建立期 | 通常需要**数周到数月**的合规投放记录                |
| 限制解除   | 持续合规 + 完成广告主身份验证后，展示逐步恢复正常   |

### 如何加速通过 Limited Ad Serving

| 做法                   | 说明                                                                         |
| ---------------------- | ---------------------------------------------------------------------------- |
| **完成广告主身份验证** | Google Ads → 设置 → 验证 → 提交企业文件                                      |
| **首批广告高度合规**   | 新账户的前几个广告被拒 → 信任度降低 → 限制更严。**新账户首投必须 100% 合规** |
| **避免频繁修改**       | 反复改文案/落地页触发重新审核                                                |
| **初期预算适中**       | 不要一上来就高预算，逐步提升                                                 |
| **使用已验证域名**     | 优先使用已通过 Google Merchant Center 或 Search Console 验证的域名           |

> **对 Agent 的影响**：在新开户（`open-account google`）后首次创建广告时，应提醒用户完成身份验证，并确保首批关键词和文案**严格合规**——新账户容错率极低。

---
