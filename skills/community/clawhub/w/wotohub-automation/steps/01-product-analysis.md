# Step 1: 产品分析

## 目标

将用户提供的**产品链接**或**文字描述**统一转换为：
- 产品画像
- 产品卖点总结
- 目标受众判断
- 高相关达人方向
- 可直接映射到 WotoHub 搜索接口的搜索条件

这个步骤的重点不是只做浅层关键词提取，而是要生成**后续红人搜索可直接使用的结构化结论**。

---

## 输入方式

本 Skill 必须支持两种输入方式：

### 方式一：产品链接

示例：

```bash
帮我推广产品：https://www.tiktok.com/shop/pdp/1729606769780232427
```

### 方式二：文字描述

示例：

```bash
我想推广一款针对美国市场的电动牙刷，价格$50，主打美白功能
```

---

## 执行规则

### 规则 A：如果输入是产品链接

必须优先使用 `scripts/product_resolve.py`，而不是把 `web_fetch` 作为默认主链路。

推荐职责分工：
- **脚本优先执行**：抓取页面、解析平台、抽取标题/品牌/价格/features/description
- **宿主模型优先分析**：基于 `urlModelInput` 输出更完整的产品语义、营销理解、达人方向
- **兼容边界原则**：在宿主 analysis 尚未提供时，本地 fallback 只可作为保守兼容/调试产物，帮助 shaping、提示补充信息或支撑 `product_analysis`；不要把它当成核心执行任务的默认放行条件

优先提取：
- 产品名称
- 价格
- 品牌 / 店铺
- 产品描述
- 核心卖点
- 适用人群
- 类目线索
- 平台线索（TikTok Shop / Amazon / Shopify / 独立站等）

如果页面抓取不完整：
- 明确告诉用户抓取信息有限
- 只基于已抓到的内容做保守总结
- 不要编造页面不存在的商品信息
- 如宿主具备 browser / web 能力，优先发起轻量 `hostUrlAnalysisRequest` 做二次取证与 `hostAnalysis` 回写
- 若宿主侧也无法补取证，再进入用户补充信息流程，而不是硬失败

抓取后要做两步：
1. 先由脚本构造可分析输入
2. 再由模型补全产品理解并提炼高相关搜索条件

### 规则 B：如果输入是文字描述

默认主路径不是本地规则提词，而是：
- 上层模型先理解产品描述
- 输出结构化 `model_analysis`
- 编排器优先消费该分析结果

需要补出的信息包括：
- 产品类型
- 价格带
- 卖点
- 目标市场
- 目标受众
- 高相关内容关键词
- 适合的达人内容方向

不要只提一个产品名；要补出更适合搜索的语义层信息。

例如：
- “电动牙刷” 不仅要得到 `电动牙刷`
- 还要补出 `口腔护理 / teeth whitening / dental routine / smart toothbrush`

---

## 推荐执行步骤

### 1.1 先判断输入类型

- 以 `http://` 或 `https://` 开头 → 视为链接输入
- 其他情况 → 视为文字描述输入

### 1.2 链接输入的标准流程

1. 优先调用 `scripts/product_resolve.py`
2. 由脚本负责页面抓取、平台解析、结构化提取
3. 若返回正常 URL 理解结果，直接消费 `analysis + productSummary`
4. 若返回 `hostUrlAnalysisRequest`，宿主拿这个 request 做二次取证 / browser 分析
5. 宿主只回写 `hostAnalysis + productSummary` 到原请求的 canonical 字段：`input.hostAnalysis`、`input.productSummary`
6. 使用同一个 task 重新执行，而不是手搓 search payload 直接跳过理解层
7. 产出可直接进入搜索链路的结构化结果

### 1.3 文字描述输入的标准流程

1. 宿主模型先根据用户描述输出结构化 `model_analysis`
2. 编排器优先消费 `model_analysis`
3. 若宿主未提供或字段不足，再回退到 `scripts/product_resolve.py`
4. `scripts/product_analyze.py` 只作为极轻量、保守 fallback 补位层，不是默认主分析路径；不要在这里做重分类、重语义推理、强达人画像推断，这些都应优先交给宿主模型层。
5. 输出结构化搜索条件

---

## 产品分析时必须补出的信息

无论输入是链接还是文字，都要尽量补齐以下字段：

### 产品基础信息
- 产品名称
- 产品类型
- 价格或价格区间
- 品牌 / 店铺（如可获得）
- 来源平台 / 来源域名（如可获得）

### 营销理解
- 核心卖点
- 使用场景
- 目标受众
- 适合的达人内容方向
- 更偏种草 / 测评 / 教程 / 对比 / 开箱 哪一种

### 搜索结构化条件
- platform
- blogCateIds
- regionList
- blogLangs
- minFansNum / maxFansNum
- advancedKeywordList
- hasEmail

---

## 如何归纳“高相关搜索条件”

这是这个 skill 本次改造的核心。

不要只把用户原话塞进搜索；要把产品信息扩展成**更适合找红人的搜索条件**。

### 需要输出的搜索条件层次

#### 1. 核心产品词
例如：
- electric toothbrush
- skincare set
- kids smartwatch
- wig

#### 2. 功能卖点词
例如：
- teeth whitening
- hydration
- anti-aging
- GPS tracking
- smart features

#### 3. 场景/内容词
例如：
- dental routine
- before and after
- morning routine
- unboxing
- review
- tutorial

#### 4. 受众词
例如：
- moms
- beauty lovers
- skincare beginners
- parents
- women 25-34

#### 5. 达人方向词
例如：
- oral care creator
- beauty creator
- family creator
- tech reviewer
- lifestyle influencer

---

## 平台与达人方向判断规则

如果用户没有明确指定平台，不要机械地只给 TikTok。

默认建议：
- 短平快种草商品 → TikTok 优先
- 需要详细解释或长测评的商品 → 可补充 YouTube
- 视觉审美驱动商品 → 可补充 Instagram

输出时可以保留多个候选平台，但构造 payload 时优先给一个主平台。

---

## 类目映射规则

类目映射按需读取：
- `references/category-mapping.md`
- `references/category-tree.md`
- `references/category-flat-map.md`
- `references/category-source.json`

优先级：

```text
三级分类 > 二级分类 > 一级分类
```

示例：
- 电动牙刷 → `080302`
- 口腔护理 → `0803`
- 个人护理 → `08`

如果命中多个类目：
- 只保留最相关的 1~3 组
- 不要为了覆盖面把很多不相干类目都塞进去

---

## 输出格式

推荐输出为三段：

### 一、产品总结

```text
产品名称：xxx
产品类型：xxx
价格：$xxx
核心卖点：xxx / xxx / xxx
目标受众：xxx
达人方向：xxx / xxx
```

### 二、高相关搜索条件

```text
主平台：TikTok
候选平台：TikTok / YouTube / Instagram
推荐类目：080302, 0803, 08
目标地区：US（会在 payload 中映射为所属业务区域锚点 id）
语言：en
粉丝范围：10000 - 500000
关键词：electric toothbrush, oral care, teeth whitening, dental routine
```

### 三、可直接用于搜索接口的 payload 提示

```json
{
  "platform": "tiktok",
  "blogCateIds": ["08", "0803", "080302"],
  "regionList": [{"id": 153115, "country": ["us"]}],
  "blogLangs": ["en"],
  "minFansNum": 10000,
  "maxFansNum": 500000,
  "hasEmail": true,
  "searchType": "KEYWORD",
  "advancedKeywordList": [
    {"value": "electric toothbrush", "exclude": false},
    {"value": "oral care", "exclude": false},
    {"value": "teeth whitening", "exclude": false},
    {"value": "dental routine", "exclude": false}
  ]
}
```

---

## 脚本

默认优先使用：

```bash
python3 scripts/product_resolve.py --input "推广一款美国市场的电动牙刷，价格$50，强调美白和口腔护理"
```

URL 场景：

```bash
python3 scripts/product_resolve.py --input "https://www.amazon.com/..."
```

脚本职责：
- 判断输入是链接还是文本
- 在 URL 场景下负责抓取、平台识别、字段抽取、fallback 管理
- URL 抓取应采用多 header profile + 通用 JSON-LD / OG fallback 的保守策略，以提高对页面可抓性、轻度反爬、页面结构变化、非标准商品页的适应能力
- 输出基础产品画像
- 产出可供模型消费的 URL bridge / 分析输入
- 为后续 payload 编译提供结构化基础

`product_analyze.py` 的职责：
- 仅做本地保守 fallback 提取
- 用于主分析缺失时的补位
- 不作为默认主分析路径

---

## 示例

### 示例 1：产品链接输入

输入：

```text
https://www.tiktok.com/shop/pdp/1729606769780232427
```

期望处理方式：
1. 优先由 `scripts/product_resolve.py` 抓取页面、识别平台并抽取结构化字段
2. 基于抽取结果构造 `urlModelInput`，再由宿主模型补全产品语义和营销理解
3. 归纳搜索条件，并输出可进入后续 payload 编译链的结构化结果

推荐输出：

```text
产品名称：Medicube Glass Glow Skincare Set
产品类型：护肤套装
价格：$237
核心卖点：PDRN、胶原蛋白、玻尿酸、玻璃肌护理
目标受众：关注提亮、保湿、韩系护肤的人群
达人方向：护肤博主、美妆测评博主、生活方式博主

高相关搜索条件：
- 主平台：TikTok
- 候选平台：TikTok / Instagram / YouTube
- 类目：08 / 0802
- 地区：US
- 语言：en
- 关键词：skincare set, glass skin, hydration, k-beauty, serum routine
```

### 示例 2：文字描述输入

输入：

```text
推广一款儿童智能手表，适合6-12岁，售价$80，强调安全定位功能
```

推荐输出：

```text
产品名称：儿童智能手表
产品类型：儿童穿戴设备
价格：$80
核心卖点：安全定位、儿童通讯、家长安心
目标受众：有儿童看护需求的家庭
达人方向：母婴博主、家庭博主、儿童教育博主、科技测评博主

高相关搜索条件：
- 主平台：TikTok
- 候选平台：TikTok / YouTube
- 类目：13 / 14 / 09 / 0903
- 地区：US
- 语言：en
- 关键词：kids smartwatch, GPS watch for kids, child safety watch, parent tech, family routine
```

---

## 注意事项

- 链接输入时，优先相信 `scripts/product_resolve.py` 抓回来的正文与结构化抽取结果，而不是凭域名猜商品
- 文本输入时，要做“营销理解 + 搜索扩写”，不能只抽几个词
- 如果信息不足，要明确说“以下是基于当前输入推断的建议搜索条件”
- 不要伪造价格、评分、销量、品牌等未出现的信息
