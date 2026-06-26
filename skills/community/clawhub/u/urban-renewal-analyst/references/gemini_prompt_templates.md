# Gemini 3 图生图提示词模板与优化指南

## 一、Prompt 构建公式

```
[基础场景描述] + [改造要素描述] + [人群活动描述] + [光线/时间/气候] + [风格关键词] + [质量参数] + [负面词]
```

---

## 二、场景类型词库

### 2.1 场景基础描述（按场景类型选用）

| 场景类型 | 英文描述词 |
|---------|-----------|
| 老旧住宅小区 | old residential neighborhood, urban community renewal |
| 商业街道 | commercial street renovation, urban retail corridor |
| 历史街区 | historic district regeneration, heritage neighborhood |
| 工业遗存 | industrial heritage adaptive reuse, factory conversion |
| 城中村 | urban village renewal, informal settlement upgrade |
| 市政广场 | civic plaza redesign, public square renovation |
| 滨水空间 | waterfront revitalization, riverside promenade |

---

## 三、改造要素描述词库

### 3.1 外立面改造描述词

| 改造方向 | 描述词 |
|---------|-------|
| 涂料翻新 | fresh textured render in warm beige/light gray/terracotta tones |
| 面砖翻新 | new ceramic tile cladding, uniform color and pattern |
| 金属格栅 | perforated metal screen, powder-coated dark gray |
| 木格栅 | natural timber louver, horizontal rhythm |
| 清水混凝土 | exposed concrete finish, fine-textured, modernist aesthetic |
| 白墙黛瓦（江南） | whitewashed walls, dark gray roof tiles, traditional Chinese vernacular |
| 红砖（闽南） | handmade terracotta brick, traditional Southern Fujian style |
| 玻璃幕墙 | floor-to-ceiling glass curtain wall, reflective, modern |

### 3.2 景观改造描述词

| 改造方向 | 描述词 |
|---------|-------|
| 行道树增植 | newly planted mature street trees, dappled shade, leafy canopy |
| 花境种植 | colorful perennial flower border, layered planting design |
| 草坪铺设 | lush green lawn, well-maintained, soft ground cover |
| 水景设置 | decorative fountain / reflecting pool / rain garden |
| 竹景 | bamboo grove, zen aesthetic, gentle rustling |
| 垂直绿化 | green wall, climbing plants, living facade |
| 屋顶绿化 | rooftop garden, green roof terrace |

### 3.3 硬质更新描述词

| 改造方向 | 描述词 |
|---------|-------|
| 透水铺装 | permeable paving, natural stone pattern, warm gray tones |
| 木平台 | elevated timber deck, warm natural wood tones |
| 彩色沥青 | colored asphalt pavement, terracotta / dark red |
| 花岗岩广场 | granite plaza, fine-hammered finish |
| 步行化改造 | pedestrianized street, no vehicles, wide comfortable walkway |
| 座椅设置 | integrated stone/timber benches, shaded seating areas |

### 3.4 设施更新描述词

| 改造方向 | 描述词 |
|---------|-------|
| 统一招牌 | unified shop signage, clean typography, consistent brand colors |
| 景观灯 | warm-toned LED landscape lighting, vintage-style lamp posts |
| 艺术装置 | public art installation, sculptural element |
| 共享单车设施 | bike-sharing station, integrated street furniture |
| 外摆区 | outdoor dining terrace, parasols, cafe chairs |

---

## 四、光线与时间描述词

| 时间/天气 | 描述词 |
|----------|-------|
| 晴天正午 | bright midday sunlight, clear sky, sharp shadows |
| 午后阳光 | warm afternoon light, long shadows, golden tones |
| 黄金时刻 | golden hour, warm sunlight, soft glowing light |
| 蓝调时刻 | blue hour, twilight, ambient artificial lighting begins |
| 阴天 | overcast sky, soft diffused light, no harsh shadows |
| 雨后 | after rain, wet pavement reflection, fresh greenery |
| 夜景 | night scene, artificial lighting, warm glow from windows |

---

## 五、风格关键词

### 5.1 写实效果图（Photorealistic）

```
核心词：
photorealistic, architectural photography, ultra-realistic,
high fidelity, professional photography

质量词：
8K resolution, hyper-detailed, sharp focus, RAW photo quality,
professional DSLR, 24mm lens, award-winning photography

负面词（可选）：
no CGI artifacts, no lens distortion, no cartoon, no illustration
```

### 5.2 建筑渲染图（Architectural Visualization）

```
核心词：
architectural visualization, CGI rendering, 3D render,
architectural concept art, urban design rendering

质量词：
Unreal Engine 5 quality, V-Ray render, photorealistic materials,
global illumination, ambient occlusion, ultra HD, 8K

负面词（可选）：
no flat design, no 2D, no cartoon, no sketch
```

### 5.3 水彩 / 手绘分析图（Watercolor / Hand-drawn）

```
核心词：
architectural watercolor, urban sketch, hand-drawn illustration,
loose watercolor wash, pen and ink rendering

质量词：
professional architectural illustration, A3 paper texture,
detailed line work, warm color palette, artistic quality

负面词（可选）：
no photorealistic, no 3D render, no digital-only
```

---

## 六、完整 Prompt 模板

### 6.1 写实效果图模板

```
Photorealistic architectural photography, [场景类型] urban renewal project in China,
[改造后外立面描述],
[新增景观描述],
[硬质更新描述],
[设施更新描述],
[人群活动描述],
[光线描述],
shot with professional camera, 50mm lens, high detail, 8K resolution,
realistic textures, award-winning architectural photography,
no clutter, no old signage, no dilapidated structures, no exposed wires
--ar 16:9
```

### 6.2 建筑渲染图模板

```
High-end architectural visualization, CGI rendering, urban regeneration design,
[改造后整体空间描述],
[立面材质与色彩系统],
[景观体系：乔木/灌木/地被层次],
[街道家具与设施系统],
[人群活动与氛围],
dramatic natural lighting, soft shadows, photorealistic materials,
Unreal Engine 5 quality, 3D render, hyper-detailed,
clean modern atmosphere, vibrant yet calm urban life,
no old elements, no graffiti, no damaged surfaces
--ar 16:9
```

### 6.3 水彩手绘模板

```
Architectural watercolor sketch, urban renewal conceptual illustration,
[场景类型与空间氛围描述],
[改造后主要要素描述],
[人群活动与生活气息],
loose brushwork, warm earthy color palette, soft washes of color,
hand-drawn line work over watercolor base,
professional architectural illustration style,
A3 watercolor paper texture, detailed yet artistic,
concept design board aesthetic, vibrant but harmonious tones
--ar 16:9
```

---

## 七、场景化 Prompt 示例

### 示例 A：老旧住宅底商街道改造

```
【Photorealistic】
Photorealistic architectural photography, old residential neighborhood commercial street
urban renewal in China, freshly painted warm cream facade with subtle texture,
unified shop signage in muted tones with clean typography,
newly planted mature street trees with lush green canopy,
granite paving in herringbone pattern, street benches with timber seats,
warm afternoon light filtering through tree canopy,
local residents walking, cycling, children playing,
shot with professional camera, 50mm lens, 8K resolution,
award-winning architectural photography,
no exposed wires, no cluttered signage, no damaged pavement
--ar 16:9
```

### 示例 B：历史街区活化改造

```
【Architectural Visualization】
High-end architectural visualization, historic district regeneration,
traditional Jiangnan architecture with whitewashed walls and dark gray roof tiles,
restored timber lattice windows, carefully preserved historic facade elements,
lush courtyard garden with bamboo, stone path and koi pond,
warm timber outdoor seating areas for tea house,
golden hour sunlight, soft warm glow,
tourists and locals mingling, cultural atmosphere,
Unreal Engine 5 quality, 3D render, hyper-detailed,
cultural heritage preservation aesthetic
--ar 16:9
```

### 示例 C：工业遗存改造为创意园区

```
【Watercolor / Hand-drawn】
Architectural watercolor sketch, industrial heritage adaptive reuse,
former factory converted to creative park,
exposed brick walls with climbing plants and green wall,
large steel-framed windows with warm interior glow,
cobblestone courtyard with creative installations and pop-up markets,
young professionals, cyclists, outdoor cafe,
loose brushwork, warm earthy tones mixed with industrial gray,
hand-drawn line work over watercolor base,
professional architectural illustration style, vibrant urban creative energy
--ar 16:9
```

---

## 八、Prompt 优化检查清单

生成 Prompt 前，完成以下优化检查：

```
□ 场景类型已明确描述
□ 改造后立面特征已具体化（材质+色彩+细部）
□ 植被描述包含层次（乔/灌/地被）
□ 人群活动描述已添加（体现场所活力）
□ 光线/时间描述已选择
□ 风格关键词已选定（三个版本各自独立）
□ 质量参数已添加（8K/高细节/专业级别）
□ 负面提示词已添加（排除旧元素/杂乱）
□ 画幅比例已设置（--ar 16:9 或 4:3）
□ Prompt 总长度适当（建议 100-200 词）
```
