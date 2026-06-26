---
name: yunlv-product-desc
description: >-
  Use when user needs to generate differentiated product descriptions for foreign trade.
  Use when creating product listings for B2B platforms, e-commerce sites, or catalogs.
  Use when translating and localizing product descriptions for international markets.
  Use when writing SEO-optimized product content for B2B export websites.
  Use when user mentions "产品描述", "产品文案", "差异化", "卖点提炼", "多语言产品", "B2B产品", "产品详情", "产品卖点", "product description".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.4
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、支持的平台、语言列表"
    - name: instructions
      tokens: 3500
      loaded: trigger
      description: "产品描述生成全流程、差异化策略、多语言适配、SEO优化"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "行业产品词库、差异化话术模板、平台适配指南"
  resource_paths:
    - references/industry_vocabulary.md
    - references/differentiation_templates.md
    - references/platform_guide.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: customer-development
    subCategory: product-content
    tags: ["产品描述", "差异化文案", "多语言产品", "B2B内容", "卖点提炼", "产品详情", "产品文案", "SEO优化"]
    requires:
      env:
        - TRADEGPT_API_KEY
    apis:
      - name: 云旅AI TradeGPT API
        url: https://api.yunlvai.com
        purpose: "产品描述内容生成与多语言翻译"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "📦"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每天5篇产品描述", "3种语言", "基础模板"]
      basic:
        price: 199
        currency: CNY
        period: month
        features: ["无限描述生成", "15种语言", "差异化策略", "SEO关键词", "平台适配"]
      pro:
        price: 499
        currency: CNY
        period: month
        features: ["批量生成", "行业竞品对比", "品牌故事撰写", "多版本A/B测试"]
triggers:
  - "产品描述"
  - "产品文案"
  - "卖点提炼"
  - "差异化"
  - "多语言产品"
  - "产品详情"
  - "B2B产品"
  - "SEO"
  - "product description"
  - "产品页面"
---

# 产品差异化描述生成：外贸全平台AI内容创作

> 在B2B外贸中，同质化产品描述是杀死询盘的第一杀手。云旅AI产品差异化描述生成技能，帮助外贸企业基于产品核心参数辅助提炼差异化卖点，生成平台适配的多语言产品内容，让产品详情页从"参数堆砌"变成"询盘机器"。

---

## 一、技能定位

**解决什么问题**：产品描述和竞争对手千篇一律，没有差异化卖点，海外买家看了没感觉？

**核心价值**：将产品描述从"参数表"升级为"价值主张"，询盘转化率提升 **200-400%**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 差异化卖点提炼 | 从产品参数中提炼3-5个差异化卖点，避免同质化 |
| 多语言产品描述 | 15种语言地道翻译，智能适配目标市场表达习惯 |
| 平台智能适配 | 针对Alibaba/MIC/独立站/亚马逊/线下展会不同平台输出不同格式 |
| SEO关键词优化 | 智能嵌入Google/平台搜索关键词，提升自然流量 |
| 标题生成 | 生成SEO友好、点击率高的产品标题（多版本） |
| 规格表整理 | 辅助整理产品规格参数为标准化表格 |
| 竞品对比表 | 制作"我方 vs 竞品"对比表，凸显优势 |
| 应用场景描述 | 针对不同行业应用场景定制描述内容 |

### 【支持的平台】

| 平台 | 输出格式重点 |
|------|----------|
| Alibaba / MIC | 标准化B2B描述结构，含FAQ |
| 独立站（Shopify等） | SEO长描述，含产品故事 |
| Amazon B2B | 场景化描述，含BULK报价 |
| 线下展会目录 | 简洁专业，含实拍参数 |
| 海关申报 | 规范产品描述，满足报关要求 |
| 社交媒体 | Instagram/Pinterest短描述 |

---

## 三、操作步骤

### 第1步：输入产品信息

**方式A - 详细产品参数**
```
产品名称：LED Panel Light
产品规格：
- 尺寸：600x600x12mm
- 功率：40W
- 色温：4000K/5000K/6500K
- 光通量：4800lm
- CRI：>80
- 寿命：50000小时
- 认证：CE/ETL/RoHS/UKCA
- 材质：铝合金+PS扩散板
- 安装方式：嵌入/悬挂/表面安装

目标市场：United States / Germany
目标平台：Alibaba
竞争对手产品：[粘贴竞品描述（可选）]
差异化重点：希望突出"美国ETL认证+长寿命+无频闪"
```

**方式B - 竞品参考**
```
竞品描述：[粘贴竞争对手的产品描述]
我的差异化：
- 价格比他低15%
- 认证更全（多了UKCA）
- 交期比他快5天
- 提供5年质保（他只有2年）
目标语言：English
```

### 第2步：AI分析与内容生成

系统辅助执行：
1. **差异化分析**：对比产品参数，提炼真正差异点（而非通用卖点）
2. **场景化构建**：基于目标市场使用场景定制描述角度
3. **平台适配**：按目标平台格式要求重构内容
4. **SEO关键词**：植入搜索量和竞争度适宜的关键词
5. **多语言翻译**：生成目标语言版本，适配当地表达习惯

### 第3步：输出产品内容包

```json
{
  "product_name": "LED Panel Light 600x600mm",
  "target_market": "United States",
  "target_platform": "Alibaba",
  "language": "English",
  "content_package": {
    "seo_title": "ETL Certified 40W LED Panel Light 600x600mm - 4800lm Commercial Ceiling Light",
    "seo_keywords": ["LED panel light 600x600", "commercial ceiling light ETL", "40W LED flat panel"],
    "short_description": "ETL certified 40W LED panel light with 4800lm output, 50000hrs lifespan, and 5-year warranty. Ideal for US commercial buildings.",
    "long_description": "...",
    "key_selling_points": [
      {
        "point": "🏆 ETL Certified for US Market",
        "explanation": "Fully compliant with UL standards, smooth customs clearance in North America"
      },
      {
        "point": "⏱️ 50,000hrs Lifespan = 5X Longer than Competitors",
        "explanation": "Based on LM-80 testing. Reduces replacement costs by 80% over 10 years"
      },
      {
        "point": "⚡ Flicker-Free Technology",
        "explanation": "Eliminates visual fatigue in office environments. Passes IEEE 1789 test"
      }
    ],
    "specification_table": [...],
    "faq": [
      {"question": "What's the MOQ?", "answer": "50pcs with logo customization" },
      {"question": "Lead time?", "answer": "15-20 days after deposit" }
    ],
    "competitor_comparison": [
      {"feature": "Certification", "us": "ETL+CE+RoHS+UKCA", "competitor": "CE only" },
      {"feature": "Warranty", "us": "5 years", "competitor": "2 years" }
    ]
  },
  "seo_score": 92,
  "differentiation_score": 85,
  "recommendations": "✅ 建议将'Flicker-Free'作为首要差异化卖点，这是竞品的普遍弱点"
}
```

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 新产品上线 | 输入参数 → 生成多平台产品描述，一次生成全平台适配 |
| 老描述优化 | 粘贴现有描述 → AI诊断同质化问题 → 重新提炼差异化卖点 |
| 多语言拓展 | 生成英文描述 → 一键翻译德语/法语/日语等多语言版本 |
| 展会准备 | 整理展会产品册内容，快速生成中英双语产品描述 |
| 竞品分析 | 参考竞品描述 → 我方与竞品对比表 → 凸显我方优势 |
| 独立站SEO | 生成SEO长描述，植入关键词，提升Google搜索排名 |

---

## 五、资源索引

- **行业产品词库**: 见 `references/industry_vocabulary.md`（何时读取：生成特定行业产品描述时，参考专业术语）
- **差异化话术模板**: 见 `references/differentiation_templates.md`（何时读取：学习如何将参数差异转化为价值主张）
- **平台适配指南**: 见 `references/platform_guide.md`（何时读取：针对不同B2B平台调整描述格式时）

---

## 六、注意事项

### ⚠️ SEO关键词质量
- 避免堆砌无搜索量的泛词
- 目标关键词应有合理搜索量（避免过于小众或过于竞争激烈）
- 关键词自然融入，不影响阅读流畅性

### ⚠️ 差异化真实性
- 所有差异化卖点必须真实可验证，禁止虚构数据
- 认证信息必须与实际证书一致
- 竞品对比数据需有据可查

### ⚠️ 平台政策
- Alibaba/MIC等平台对描述字数和格式有要求，需适配
- 亚马逊B2B禁止某些极限词（#1/Best等）

---

## 七、使用示例

### 示例 1：LED灯具产品描述优化
**用户需求**：我们是做LED面板灯的，现有描述太同质化，帮我重新优化，目标市场美国，平台Alibaba

**执行结果**：
- 从40W/4800lm/ETL认证等参数中提炼3个核心差异化卖点
- 生成Alibaba平台格式的完整产品描述（含SEO标题、卖点、规格表、FAQ）
- 竞品对比表：我方（ETL+5年质保+无频闪）vs 市场常见产品（CE+2年质保）

### 示例 2：机械配件多语言批量生成
**用户需求**：我们出口工业阀门，需要生成英语、德语、法语、阿拉伯语4种语言的产品描述，目标平台独立站

**执行结果**：
- 生成4种语言的高质量产品描述
- 适配独立站SEO要求（长描述+关键词布局）
- 每种语言考虑当地市场习惯（阿拉伯语RTL排版适配）

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "产品参数好就够了" | 同质化市场，参数一样的情况下，描述决定转化率 |
| "越详细越好" | B2B平台首屏最重要，长描述放在折叠区域 |
| "和竞品对比越狠越好" | 对比需基于事实，过度贬低竞品会引发平台处罚 |
| "SEO关键词越多越好" | 关键词堆砌会被搜索引擎惩罚，自然融入最佳 |

---

## 九、Verification

完成产品描述生成流程后：
- [ ] 确认差异化卖点真实可验证（有数据支撑）
- [ ] SEO关键词与产品高度相关（非泛流量词）
- [ ] 多语言版本无翻译错误（已通过语法检查）
- [ ] 平台格式适配正确（字数/结构符合平台规范）
- [ ] 竞品对比数据有据可查（无虚假夸大）
- [ ] 产品描述不含平台禁止词（极限词/虚假数据）
- [ ] 规格表与实物一致

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/productDesc/
├── products/          # 导入的产品信息
├── generated/         # 生成的产品描述
├── seo/               # SEO关键词配置
└── logs/              # 运行日志
```

### 数据处理原则
- **内容保护**：生成的产品描述内容归用户所有，云旅AI不存储、不共享
- **参数安全**：产品技术参数不写入日志
- **竞品数据**：竞品信息仅用于对比分析，不用于其他目的

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI TradeGPT API生成描述内容
- ✅ **允许**：写入 `./data/yunlv-skills/productDesc/` 生成的描述
- ❌ **禁止**：使用竞品商标或注册信息进行营销
- ❌ **禁止**：生成含虚假数据或未经证实的竞品对比内容

---

## ⚠️ 不要在以下情况使用

- 需要法律专业意见时（请咨询律师）
- 涉及特殊行业监管时（请咨询行业专家）

---

## 交付标准

- 方案结构完整，覆盖所有章节
- 建议具体可执行，不含模糊表述
- 内容适配用户提供的行业和场景
- 输出格式清晰，便于直接使用

---

## 相关技能推荐

- **yunlv-pricing** — 定价策略，配合产品卖点制定价格
- **yunlv-pod-agent** — POD运营，为按需印刷产品定制描述
- **yunlv-pod-templates** — POD模板，获取产品设计灵感
