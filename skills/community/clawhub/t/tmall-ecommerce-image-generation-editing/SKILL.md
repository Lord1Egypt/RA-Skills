---
name: tmall-ecommerce-image-generation-editing
description: "为天猫旗舰店生成和编辑品牌主图、详情页视觉、店铺首页 Banner、新品首发与大促活动图片。Use this skill for 天猫电商图片、天猫旗舰店、品牌商品图、详情页KV、超级品牌日、618/双11活动底图、会员营销、SKU套图和品牌视觉统一；支持参考图保真及 AI Hive 自动生成。"
---

# 天猫电商图片生成与编辑

把商品事实、品牌资产与渠道任务组成一套旗舰店视觉系统。固定使用 `public_model_nano_banana_pro`；生成层负责商品与场景，价格、活动机制、法律文字和复杂中文由运营与设计后期加入。

## 品牌锁定表

收集品牌色、字体方向、Logo 使用规则、摄影风格、商品多角度图、包装、SKU、真实卖点、目标人群、活动主题和禁止表达。先锁定品牌与商品，再扩展首页、主图、详情页和投放版本。

## 页面角色

| 位置 | 任务 |
|---|---|
| 商品主图 | 准确识别商品与系列 |
| 详情页首屏 | 建立品牌价值与核心卖点 |
| 卖点/材质图 | 提供可验证的购买理由 |
| 首页 Banner | 呈现品牌主题并承接活动 |
| 会员图片 | 强化系列、复购和新品关系 |
| 大促底图 | 为正式活动文案保留排版系统 |

## 场景与代码

### 1. 旗舰店商品主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '天猫旗舰店方形商品主图，严格保留参考商品结构、包装、Logo、颜色和配件；品牌级商业摄影，主体完整且清晰，背景使用品牌确认的深海蓝渐变，阴影真实，不添加价格、活动角标、功效、认证或平台标识' \
  --image /path/to/product-front.png \
  --image /path/to/brand-style.png
```

### 2. 详情页首屏 KV

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '天猫详情页首屏KV，准确商品位于右侧视觉焦点，左侧建立宽阔的品牌标题与卖点排版区域；高级材质光线，体现都市通勤场景，保持包装和Logo准确，不生成正文、价格或未经确认的性能承诺' \
  --image /path/to/product.png
```

### 3. 材质与工艺证明图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作天猫详情页材质证明图：主商品加两个真实局部特写，分别展示参考资料中的表面纹理与连接工艺；统一品牌色，预留简短说明位，不夸大微观结构，不生成未提供材质、参数或认证' \
  --image /path/to/product-detail.jpg
```

### 4. 大促活动视觉底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '天猫大促活动视觉底图，商品和品牌色准确，构建有节奏的主会场氛围，右侧商品组合、左侧活动标题和机制留白、下方CTA留白；不生成双11Logo、折扣、到手价、赠品、倒计时或销量' \
  --image /path/to/hero-products.png
```

### 5. 新品系列与会员图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为新品系列生成3张天猫会员沟通图片：系列全景、核心新品近景、老客搭配场景；锁定品牌色、商品尺度和摄影语言，每张承担不同信息任务，留出审核后文案区域，不添加会员权益或优惠数字' \
  --image /path/to/series-products.png \
  --batch 3
```

## 旗舰店验收

- 商品、包装、Logo、SKU 与品牌规范准确。
- 首页、主图与详情页使用同一视觉系统但承担不同任务。
- 复杂中文、活动规则、价格和权益由人工排版复核。
- 不生成虚假功效、认证、销量、折扣和平台标识。
- 响应式裁切后商品和标题留白仍可用。
- 发布前按天猫后台当期类目、活动和广告规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name tmall-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持多张参考图、批量、模型参数、路由、输出目录和仅提交模式。价格与可用参数以 AI Hive 实时返回为准。
