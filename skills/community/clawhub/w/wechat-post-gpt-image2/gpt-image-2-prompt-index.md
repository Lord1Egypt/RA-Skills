# GPT Image-2 Prompt 智能匹配索引

> 用于 wechat-post skill 配图生成时自动匹配最优 Prompt 模板
> 数据来源：awesome-gpt-image-2-API-and-Prompts（483+ curated cases）

## 依赖安装

**Prompt 案例库需要单独下载**：

```bash
git clone --depth 1 https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts.git
```

默认路径：`./awesome-gpt-image-2-API-and-Prompts/`（当前目录）

---

## 使用方式

当用户输入产品/服务主题时，匹配以下关键词 → 选择对应分类和案例 → 提取 Prompt 模板 → 适配 wechat-post 配图需求。

---

## 关键词 → 分类映射

| 关键词（优先级从高到低匹配） | 分类 | 说明 |
|---------------------------|------|------|
| 香水/香氛/美妆/化妆品 | `ecommerce` | 奢华产品摄影 |
| 护肤/面霜/乳液/精华 | `ecommerce` | 柔和自然风格 |
| 食品/饮料/零食/咖啡/茶 | `ecommerce` + `poster` | 食品摄影 + 美食插画 |
| 手表/腕表/珠宝/钻石 | `ad-creative` | 高端奢侈品广告 |
| 巧克力/甜点/蛋糕/甜品 | `ad-creative` | 高端食品广告 |
| 城市/旅游/旅行/地方/景点 | `poster` | 城市海报/旅行插画 |
| 餐饮/餐厅/外卖/美食 | `ad-creative` + `ecommerce` | 餐饮广告 + 食品摄影 |
| 运动鞋/球鞋/潮牌/服装 | `ad-creative` | 潮流街头风格 |
| 耳机/音箱/数码/电子 | `ecommerce` | 科技产品摄影 |
| 品牌/IP/吉祥物/卡通 | `character` + `ad-creative` | 品牌视觉系统 |
| UI/网页/界面/设计 | `ui` | UI 设计 mockup |
| 人像/头像/摄影/写真 | `portrait` | 人像摄影 |
| 培训/教育/课程/讲座 | `poster` + `ad-creative` | 活动海报 + 教育广告 |
| AI/科技/软件/SaaS | `ui` + `ad-creative` | 科技风格 |
| 游戏/娱乐/动漫 | `poster` + `character` | 游戏海报 + 角色 |
| 健康/医疗/健身 | `ad-creative` + `portrait` | 健康生活方式 |
| 家居/家具/装修 | `ecommerce` | 家居产品摄影 |
| 汽车/交通/出行 | `ad-creative` | 汽车广告 |
| 通用/默认 | `poster` | 通用海报模板 |

---

## 精选案例模板（Top 20）

### 1. 香水/美妆 → `ecommerce` Case 113
**场景**：高端香水、化妆品主图
**Prompt 核心**：
```
A luxurious cinematic product photograph of a classic rectangular perfume bottle...
placed on a glossy black marble surface with white veining...
Dramatic warm lighting from the upper left creates golden highlights...
Dark background, shallow depth of field, ultra-detailed studio product photography...
```
**适配要点**：替换产品名称、调整背景色与品牌色一致

---

### 2. 护肤品 → `ecommerce` Case 114
**场景**：护肤品、面膜、精华液
**Prompt 核心**：
```
A soft {color} bottle with a {pump} pump stands on a matte podium...
surrounded by silky foam and {flowers}...
The background is a pale gradient with subtle bubble details...
```
**适配要点**：替换瓶子颜色、花朵种类、背景渐变颜色

---

### 3. 食品/饮料 → `ecommerce` Case 115
**场景**：果汁、碳酸饮料、零食
**Prompt 核心**：
```
A vibrant tropical product advertisement featuring a {product}...
surrounded by fresh citrus fruits, ice cubes, and splashing water...
Bright, energetic lighting with vivid colors...
```
**适配要点**：替换产品类型、调整水果/配料

---

### 4. 手表/奢侈品 → `ad-creative` Case 144
**场景**：手表、珠宝、高端饰品
**Prompt 核心**：
```
A dramatic luxury product advertising image for a {product} in a dark studio...
Center-left foreground, standing upright at a slight three-quarter angle...
Cinematic red and white horizontal light streaks crossing behind...
Glossy wet ground plane with reflective texture...
```
**适配要点**：替换产品描述、调整光效颜色（与品牌色一致）

---

### 5. 巧克力/甜品 → `ad-creative` Case 169
**场景**：巧克力、蛋糕、高端甜品
**Prompt 核心**：
```
A premium, square (1:1) product advertisement for a {brand}...
High-end editorial campaign combining luxury food photography...
Matte black wrapper, subtle gold foil, elegant serif typography...
```
**适配要点**：替换品牌名、调整包装颜色和字体风格

---

### 6. 城市/旅游 → `poster` Case 1-5
**场景**：城市宣传、旅游推广、地方特产
**Prompt 核心**：
```
A vibrant {city} city poster in modern illustration style...
Featuring iconic landmarks, local cuisine, and cultural elements...
Bold typography with {city} name prominently displayed...
Color palette inspired by local culture and scenery...
```
**适配要点**：替换城市名、地标、文化元素

---

### 7. 餐饮/外卖 → `ad-creative` Case 166
**场景**：餐厅推广、外卖平台、美食节
**Prompt 核心**：
```
A Japanese-style food delivery flyer featuring {cuisine}...
Clean layout with appetizing food photography...
Bold red and white color scheme with Japanese typography elements...
```
**适配要点**：替换菜系、调整配色方案

---

### 8. 运动鞋/潮牌 → `ad-creative` Case 146
**场景**：运动鞋、街头服饰、潮流品牌
**Prompt 核心**：
```
A bold streetwear sneaker poster ad featuring {product}...
Urban background with graffiti and concrete textures...
High contrast lighting, dramatic shadows...
```
**适配要点**：替换产品、调整背景城市元素

---

### 9. 耳机/数码 → `ecommerce` Case 117
**场景**：耳机、音箱、智能设备
**Prompt 核心**：
```
A premium tech product infographic featuring {product}...
Clean white background with subtle gradient...
Multiple angles and feature callouts...
Minimalist tech aesthetic with precise typography...
```
**适配要点**：替换产品、调整功能标注

---

### 10. 品牌/吉祥物 → `ad-creative` Case 107
**场景**：品牌视觉、IP形象、企业吉祥物
**Prompt 核心**：
```
A comprehensive brand identity document featuring {mascot}...
Multiple panels showing logo variations, color palette, and usage guidelines...
Professional corporate design system aesthetic...
```
**适配要点**：替换吉祥物描述、调整品牌色系

---

### 11. 培训/教育 → `poster`（通用教育海报模板）
**场景**：课程宣传、讲座海报、训练营
**Prompt 核心**：
```
A professional education/training event poster...
Clean modern layout with bold headline typography...
Feature icons for key learning outcomes...
Professional color scheme with accent colors for emphasis...
```
**适配要点**：替换标题、课程内容、讲师信息

---

### 12. AI/科技/SaaS → `ui` Case 1
**场景**：科技产品、软件界面、SaaS服务
**Prompt 核心**：
```
A modern UI design mockup for {product/service}...
Clean interface with data visualization elements...
Professional color scheme with subtle gradients...
Showcasing key features and user benefits...
```
**适配要点**：替换产品名、调整界面元素

---

### 13. 健康/健身 → `ad-creative`（通用健康模板）
**场景**：健身房、健康产品、医疗服务
**Prompt 核心**：
```
A vibrant health and wellness advertisement...
Energetic composition with {activity/ product}...
Fresh, clean color palette with greens and whites...
Motivational typography with clear call-to-action...
```
**适配要点**：替换活动/产品、调整配色

---

### 14. 家居/家具 → `ecommerce`（通用家居模板）
**场景**：家具、家居用品、装修服务
**Prompt 核心**：
```
A sophisticated interior product photograph...
{Product} placed in a stylish living space...
Natural lighting with warm tones...
Lifestyle context showing product in use...
```
**适配要点**：替换产品、调整空间风格

---

### 15. 通用/默认 → `poster`（通用商业海报）
**场景**：任何未匹配到的主题
**Prompt 核心**：
```
A professional business marketing poster...
Clean modern design with clear visual hierarchy...
Bold headline with supporting details...
Professional color scheme appropriate for the industry...
```
**适配要点**：根据行业调整配色和元素

---

## 快速匹配规则

### 规则 1：关键词优先级
1. 首先匹配**具体产品词**（香水、手表、巧克力）
2. 其次匹配**行业词**（电商、餐饮、科技）
3. 最后匹配**风格词**（奢华、简约、活力）
4. 无匹配时 fallback 到通用海报模板

### 规则 2：组合匹配
当主题包含多个关键词时，取**最具体**的分类：
- "高端香水" → 香水（而非美妆或电商）
- "科技培训课程" → 培训（而非科技）
- "潮流运动鞋" → 运动鞋（而非服装）

### 规则 3：Prompt 适配流程
```
1. 匹配关键词 → 获取分类和案例
2. 提取案例 Prompt 模板
3. 替换模板中的 {变量} 为用户实际内容
4. 叠加 wechat-post 配图约束（分区布局、比例、配色）
5. 输出最终配图 Prompt
```

---

## 文件路径

- **Prompt 库（GitHub）**：https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts
- **Prompt 库（本地）**：`./awesome-gpt-image-2-API-and-Prompts/cases/`（需自行 clone）
- **本索引**：`skills/wechat-post/gpt-image-2-prompt-index.md`

> ⚠️ **注意**：本地路径取决于你的 clone 位置。如 clone 到 `/workspace/`，则路径为 `/workspace/awesome-gpt-image-2-API-and-Prompts/cases/`
