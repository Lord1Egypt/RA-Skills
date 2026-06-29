# Prompt 模板库 - 跨境电商文生图

按类目和场景分类的 Prompt 模板，可直接用于 `image_generator.py` 或手动贴到 Midjourney/Flux。

---

## 1. 厨具 / 厨房用品 (kitchenware)

### modern_kitchen（现代厨房场景）
```
A premium [产品名], placed on a modern marble kitchen counter,
soft natural light from window on the left, professional food photography,
warm and inviting atmosphere, shallow depth of field, 8K resolution,
commercial photography, no text, no watermark
```

### cooking_action（烹饪动作感）
```
A [产品名] in use, steam rising, fresh ingredients scattered naturally nearby,
warm kitchen lighting, motion blur on hands, cinematic food photography style,
professional lighting, no text, no watermark
```

### minimal_white（极简白底）
```
A [产品名] isolated on pure white background, studio lighting,
clean product photography, sharp focus, e-commerce style, 8K,
no text, no watermark, no logo
```

---

## 2. 家具 (furniture)

### living_room（客厅场景）
```
A [产品名] in a bright Scandinavian style living room, natural morning light
through large windows, cozy atmosphere, interior design photography,
8K, commercial quality, no text, no watermark
```

### bedroom（卧室场景）
```
A [产品名] in a serene bedroom setting, soft warm lighting from bedside lamp,
minimalist decor, lifestyle interior photography, high resolution,
no text, no watermark
```

### office（办公场景）
```
A [产品名] in a modern home office, daylight from window, clean desk setup,
professional interior photography, sharp focus, 8K, no text
```

---

## 3. 电子产品 (electronics)

### desk_setup（桌面场景）
```
A [产品名] on a clean minimalist desk, soft desk lamp lighting from left,
tech aesthetic, dark gradient background, product photography, 8K,
no text, no watermark
```

### lifestyle（生活场景）
```
A [产品名] being used in a coffee shop, natural light through window,
casual lifestyle photography, shallow depth of field, no text
```

---

## 4. 服装 (fashion)

### street_style（街拍风格）
```
A model wearing [产品名], urban street setting, golden hour light,
fashion photography, candid style, high resolution, no text
```

### studio（棚拍）
```
A [产品名] on mannequin, fashion studio lighting, clean neutral background,
professional apparel photography, 8K, no text, no watermark
```

---

## 5. 珠宝 (jewelry)

### velvet（丝绒质感）
```
A [产品名] on dark velvet background, dramatic spotlight from above,
luxury jewelry photography, macro detail, diamond reflections, 8K,
no text, no watermark
```

### lifestyle（佩戴场景）
```
A model wearing [产品名], elegant evening setting, soft warm lighting,
luxury fashion photography, shallow depth of field, no text
```

---

## 6. 运动户外 (sports_outdoor)

### outdoor（户外场景）
```
A [产品名] in outdoor adventure setting, golden hour sunlight behind,
action sports photography, dynamic composition, 8K, no text
```

### studio（棚拍细节）
```
A [产品名] on dark backdrop, dramatic rim lighting highlighting texture,
product photography, sharp detail, 8K, no text, no watermark
```

---

## 8. 多角度展示 (multi-angle) — 需配合实拍 source_image

详见 `assets/prompts/multi-angle-v1.txt`。scene key：

| Key | 说明 |
|-----|------|
| `front_view` | 正视图 |
| `side_view` | 侧视图 |
| `top_view` | 俯视图 |
| `back_view` | 背视图 |
| `three_quarter_view` | 45° 三维视角 |
| `other_angles` | 其他角度 |
| `detail_closeup` | 细节特写 |
| `multi_angle_pack` | 批量生成默认 5 角度套装 |

img2img 自动追加一致性后缀，prompt_strength ≈ 0.58。

---

## 9. 节日 / 大促场景 (holiday)

详见 `assets/prompts/holiday-scenes-v1.txt`。

| Key | 说明 |
|-----|------|
| `christmas` | 圣诞 |
| `black_friday` | 黑五 |
| `prime_day` | Prime Day |
| `valentine` | 情人节 |
| `lunar_new_year` | 春节 / 农历新年 |
| `summer_sale` | 夏日促销 |

---

## 10. 品牌调性 (brand-tone)

详见 `assets/prompts/brand-tone-v1.txt`。

**整帧 scene：** `luxury_minimal` / `youthful_pop` / `eco_natural` / `pro_tech`

**叠加修饰：** 任意 scene + `brand_style` 字段（如白底 + 环保自然）

---

## 11. 社媒 / 营销 (social-marketing)

详见 `assets/prompts/social-marketing-v1.txt`。

| Key | 说明 |
|-----|------|
| `unboxing` | 开箱 |
| `gift_set` | 礼盒套装 |
| `influencer_flatlay` | 达人平铺 |
| `flash_sale` | 限时抢购视觉 |

---

## 7. Midjourney 专用 Prompt 模板

### 通用电商主图
```
[产品描述], pure white background, studio lighting, sharp focus,
professional e-commerce photography --ar 1:1 --style raw --v 6.1
--no text,watermark,logo,reflection
```

### 场景图
```
[产品描述] in [场景环境], [光线描述], [氛围],
product photography --ar 1:1 --style raw --v 6.1
--no text,watermark,logo,deformed
```

### 社交媒体竖版
```
[产品描述], [场景], lifestyle photography, warm lighting --
ar 3:4 --style raw --v 6.1 --no text,watermark
```

---

## 通用负面词（Negative Prompt）

适用于 Stable Diffusion / SDXL / SD3：

```
text, watermark, logo, signature, distorted, deformed, blurry,
low quality, bad anatomy, extra limbs, cropped, out of frame,
cluttered background, harsh lighting, oversaturated
```

---

## 使用建议

1. 把 `[产品名]` / `[产品描述]` 替换为实际产品
2. 产品描述建议格式：`[颜色] [材质] [产品名] with [关键特征]`
3. 例：「银色不锈钢平底锅 with 木质手柄」
4. Midjourney 需要加参数；Flux/SD 直接贴 Prompt
