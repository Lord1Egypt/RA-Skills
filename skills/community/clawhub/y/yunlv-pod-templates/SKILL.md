---
name: yunlv-pod-templates
description: >-
  Use when user needs ready-to-use POD (Print on Demand) design keyword templates and listing copy writing guides.
  Use when generating AI design prompts for custom print products.
  Use when creating POD product listing copy and pricing reference.
  Use when user mentions "POD模板", "POD关键词", "POD文案指南", "POD设计提示词", "POD标题", "按需打印模板", "POD copywriting guide", "POD design keywords".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.2
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、模板分类、平台适配说明"
    - name: instructions
      tokens: 4000
      loaded: trigger
      description: "POD设计关键词库、标题模板、五点描述、短描述、定价速算"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "30组AI设计关键词、10条标题模板、上架执行表"
  resource_paths:
    - references/pod_design_keywords.md
    - references/pod_title_templates.md
    - references/pod_listing_copy.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: e-commerce-automation
    subCategory: pod-template-pack
    tags: ["POD模板", "POD关键词", "按需打印", "设计指南", "设计提示词", "文案创作", "POD标题", "POD描述"]
    requires:
      env:
        - TRADEGPT_API_KEY
    apis:
      - name: 云旅AI TradeGPT API
        url: https://api.yunlvai.com
        purpose: "生成POD设计关键词与文案内容"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "🎨"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["10组设计关键词", "3条标题模板", "基础五点描述"]
      basic:
        price: 149
        currency: CNY
        period: month
        features: ["30组设计关键词", "10条标题模板", "全平台五点描述", "短描述模板", "定价速算表"]
      pro:
        price: 399
        currency: CNY
        period: month
        features: ["无限关键词生成", "自定义品类模板", "A/B测试标题", "竞品关键词分析", "专属定制方案"]
triggers:
  - "POD模板"
  - "POD关键词"
  - "POD文案指南"
  - "POD设计提示词"
  - "POD标题"
  - "按需打印模板"
  - "POD文案"
  - "POD design keywords"
  - "POD copywriting guide"
  - "POD标题模板"
  - "POD描述"
---

# 全球POD模板包：垂直品类专属模板，直接复制上架

> 做POD最耗时的不是选品，而是从设计到上架的每一步重复劳动——写关键词、想标题、写描述、算定价……云旅AI POD模板包，提供30组AI设计关键词、10条标题模板、全平台通用五点描述、短描述和定价速算表，直接复制，只换关键词即可上架，把上架时间从2小时压缩到10分钟。

---

## 一、技能定位

**解决什么问题**：POD上架流程繁琐，每个SKU都要重新写关键词、标题、描述，耗时巨大？

**核心价值**：提供**垂直品类专属模板包**，直接复制，全平台通用，不改结构，只换关键词即可上架。上架单个SKU的时间从**30分钟**压缩到**3分钟**。

---

## 二、模板包内容

### 【六大核心模板】

| 模板 | 数量 | 用途 |
|------|------|------|
| AI设计关键词 | 30组（10大品类×3组） | 直接复制到AI绘图工具生成设计 |
| 标题模板 | 10条 | 替换括号内容即可全平台使用 |
| 五点描述 | 1套（全平台通用） | 直接复制到Amazon/Etsy/TikTok/Shopify |
| 短描述 | 1套 | TikTok/独立站/Etsy首页用 |
| 定价速算表 | 1套 | 复制到Excel，输入成本自动算售价 |
| 30天上架执行表 | 1套 | 从0到上架的完整执行计划 |

### 【覆盖10大品类】

1. 复古风格
2. 宠物系列
3. 家庭亲情
4. 趣味职场/社恐
5. 户外旅行
6. 美式乡村/田园
7. 节日通用
8. 情侣/婚礼
9. 健身/运动
10. 读书/文艺

---

## 三、使用步骤

### 第1步：选择品类和产品

确认你要上架的：
- **品类**：复古/宠物/家庭/职场/户外/乡村/节日/情侣/健身/文艺
- **产品**：T恤/卫衣/马克杯/帆布袋/手机壳
- **平台**：TikTok / Etsy / Amazon / Shopify

### 第2步：复制设计关键词

从关键词库中选择对应品类的AI设计关键词，复制到AI绘图工具（如Midjourney、DALL-E、HICUSTOM）生成设计稿。

**关键词使用要点**：
- 每组关键词已包含：风格+元素+配色+产品适配+版权声明
- 关键词末尾的"no copyright, commercial use"确保生成内容可用于商业
- 建议每个关键词生成3-5个变体，选择最佳效果

### 第3步：套用标题模板

从标题模板中选择对应品类的模板，替换括号中的内容：

**模板格式**：`Retro (Dog Mom) T-Shirt | Funny (Pet Lover) Gift For (Women)`

**替换规则**：
- 第1个括号：核心关键词（如Dog Mom → Cat Dad）
- 第2个括号：目标人群（如Pet Lover → Coffee Lover）
- 第3个括号：性别/年龄（如Women → Men / Teens）

### 第4步：复制五点描述

全平台通用五点描述，直接复制粘贴，无需修改：

```
✅ Premium soft cotton blend, lightweight and breathable for all-day comfort
✅ High quality durable print, will not crack, fade or peel after regular wash
✅ Classic regular fit, runs true to size, suitable for men, women, teens and adults
✅ Perfect gift for birthday, holiday, anniversary, Christmas, Mother's Day, Father's Day
✅ Printed on demand, professionally made, shipped worldwide with reliable fulfillment
```

### 第5步：复制短描述

用于TikTok/独立站/Etsy首页：

```
Unique and stylish (product) for (target audience). Great for daily wear, casual outings, vacations and gifting. Designed with simple, clean aesthetic, printed professionally and shipped globally.
```

### 第6步：定价速算

使用定价速算公式：
```
建议售价 = (成本 + 运费) × 2.8
```

**速算示例**：
| 产品 | 成本 | 运费 | 建议售价 | 毛利率 |
|------|------|------|----------|--------|
| T恤 | $8 | $4 | $33.60 | ~52% |
| 卫衣 | $15 | $5 | $56.00 | ~50% |
| 马克杯 | $5 | $6 | $30.80 | ~48% |
| 帆布袋 | $6 | $4 | $28.00 | ~50% |
| 手机壳 | $4 | $3 | $19.60 | ~50% |

---

## 四、30天上架执行表

| 阶段 | 时间 | 任务 | 目标 |
|------|------|------|------|
| 基础搭建 | Day 1-3 | 注册店铺 + 绑定Printful/Printify/Gelato | 店铺可上架 |
| 首批上架 | Day 4-7 | 做10款设计 + 全部上架 | 10个SKU上线 |
| 持续上新 | Day 8-15 | 每天上新3-5款 + 优化标题关键词 | 40+SKU |
| 优化迭代 | Day 16-30 | 分析流量，保留爆款，下架无流量款 | 筛出3-5个爆款 |

---

## 五、定制化服务

如果通用模板不够用，回复以下3个信息，获取专属定制版：

1. **主攻平台**：TikTok / Etsy / Amazon / Shopify
2. **目标人群**：宠物/家庭/职场/复古/户外/情侣
3. **主要产品**：T恤/卫衣/马克杯/帆布袋/手机壳

定制版包含：
- 30个精准标题
- 20条AI设计关键词
- 完整上架文案一套
- 直接可粘贴上架，不用再改

---

## 六、适用场景

| 场景 | 使用方式 |
|------|----------|
| 新手首批上架 | 从10大品类中选3个最熟悉的，每个做3-5个SKU |
| 批量铺货 | 用标题模板+关键词库，每天上新5-10款 |
| 节日营销 | 节日通用品类关键词+标题模板，提前30天上架 |
| 多平台铺开 | 同一设计，不同平台用相同五点描述+微调标题 |
| 店群运营 | 每个店铺选2-3个品类，用模板包快速铺满 |

---

## 七、资源索引

- **30组AI设计关键词**: 见 `references/pod_design_keywords.md`（何时读取：需要AI绘图提示词时直接复制）
- **10条标题模板**: 见 `references/pod_title_templates.md`（何时读取：上架写标题时替换括号内容）
- **五点描述+短描述+定价表**: 见 `references/pod_listing_copy.md`（何时读取：写产品描述和定价时直接复制）

---

## 八、注意事项

### ⚠️ 版权安全
- 所有关键词末尾已标注"no copyright, commercial use"，但AI生成内容仍需人工审核
- 禁止直接使用迪士尼、漫威等IP形象
- 建议每个设计用Google图片反搜确认无近似版权
- 遵循设计安全公式：**AI生成 + 人工精修 + 侵权排查 = 安全的POD设计**

### ⚠️ 平台差异
- Amazon标题可较长（200字符），Etsy建议短标题（140字符以内）
- TikTok Shop对描述长度有限制，优先使用短描述模板
- Shopify独立站可自由发挥，建议用完整五点描述

### ⚠️ 定价注意
- 2.8倍速算为基准参考，需根据平台竞争情况调整
- Etsy建议定价略高于Amazon（Etsy用户对价格敏感度较低）
- TikTok Shop适合低价走量，可适当降低倍率到2.2-2.5

---

## 九、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "模板千篇一律，没有差异化" | 模板是框架，差异化靠你替换的关键词和设计 |
| "直接复制上架会被判重复" | 标题和描述是框架，换关键词后内容独一无二 |
| "AI设计质量不够好" | 关键词是起点，AI生成+人工精修才能出精品 |
| "POD模板包只适合新手" | 老手更需要模板来提效，把时间留给选品和策略 |

---

## 十、Verification

使用POD模板包上架后：
- [ ] 每个SKU的标题已替换括号内容，无残留模板标记
- [ ] AI设计关键词已生成设计稿，经过侵权排查
- [ ] 五点描述适配目标平台（长度、格式符合要求）
- [ ] 定价根据速算公式计算，并参考竞品价格微调
- [ ] 首批10个SKU在7天内完成上架

---

## 十一、Security & Privacy

### 数据流透明声明 (Data Flow Transparency)

本技能的数据处理流程完全透明，所有数据传输均有明确目的：

| 数据流 | 方向 | 内容 | 用途 | 保护措施 |
|--------|------|------|------|----------|
| 用户 → 本技能 | 输入 | 品类选择、平台类型、产品类型 | 生成对应模板 | 本地处理 |
| 本技能 → 云旅AI API | 请求 | 品类+平台描述 | 获取关键词扩展和文案优化建议 | TLS 1.3加密传输 |
| 云旅AI API → 本技能 | 响应 | 扩展关键词+优化文案 | 输出给用户 | 服务端不存储请求 |
| 本技能 → 用户 | 输出 | 格式化的模板内容 | 辅助POD上架 | 数据保留在用户环境 |

**关键保证**：
- 📌 **本技能不访问任何电商平台**：不连接TikTok/Etsy/Amazon/Shopify，不采集平台数据
- 📌 **API仅用于文案优化**：云旅AI API接收品类描述，返回关键词和文案建议
- 📌 **不传输店铺数据**：不收集、不存储、不转发任何店铺运营数据
- 📌 **模板内容用户可控**：所有模板内容用户可自由修改，技能不自动上架

### 数据保护措施

- **加密传输**：所有API通信使用TLS 1.3加密
- **不存储原始数据**：API请求和响应仅用于当前会话，不持久化存储
- **最小化留存**：使用记录保留30天，超期自动删除
- **本地优先**：所有模板内容保存在用户本地目录

### 合规声明

- **GDPR合规**：不处理个人数据，模板内容属于通用商业信息
- **PIPL合规**：不收集或处理个人信息
- **版权合规**：关键词包含"no copyright, commercial use"声明，生成内容需人工审核
- **数据主权**：所有数据保留在用户自有环境中

### 权限边界声明
- ✅ **允许**：读取 `./skills/pod-template-pack/references/` 下的参考文件
- ✅ **允许**：调用云旅AI API获取关键词扩展和文案优化
- ✅ **允许**：输出模板内容供用户复制使用
- ❌ **禁止**：访问或连接任何电商平台
- ❌ **禁止**：自动上架或修改店铺商品
- ❌ **禁止**：采集平台商品数据或竞品信息

### 本技能不做的事 (What This Skill Does NOT Do)
- ❌ 不访问、登录或采集任何电商平台数据
- ❌ 不自动上架商品（仅提供模板供用户手动使用）
- ❌ 不生成侵权设计（关键词包含版权安全声明）
- ❌ 不收集或存储用户的店铺运营数据

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

- **yunlv-pod-agent** — POD运营，模板落地到店铺运营
- **yunlv-product-desc** — 产品描述，为模板产品编写专业描述
- **yunlv-pricing** — 定价策略，模板产品的定价方案
