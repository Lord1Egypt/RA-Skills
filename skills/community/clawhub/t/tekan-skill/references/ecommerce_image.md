# 电商图模块

> **⚠️ Agent 必读：收到电商图请求（如"做商品详情图"）时，不要提问、不要分析、不要列选项。用户发了图就直接执行 `run` 命令。所有参数都有默认值，脚本会自动处理。**

使用 AI 为电商场景生成各类商品图片——商品详情图、电商主图、虚拟穿搭、换背景等 13 种功能，统一入口。

## 支持的功能类型

| tool-type | 名称 | Pipeline | 输入 | 状态 |
|-----------|------|----------|------|------|
| `product_detail_image` | 商品详情图 | multi_enhance | 商品图 + 模块选择 | 已实现 |
| `product_main_image_ecomm` | 商品主图 | enhance_then_submit | 商品图 + 参考图 + 功能点/营销点 | 已实现 |
| `virtual_try_on_ecomm` | 虚拟穿搭 | enhance_then_submit | 商品图 + 模特图 | 已实现 |
| `garment_detail_view_ecomm` | 服装细节图 | direct_submit | 服装图 + 服装类型 + 部位 | 已实现 |
| `product_3d_render_ecomm` | 商品3D图 | direct_submit | 商品图 + 可选参考图 | 已实现 |
| `background_replacement_ecomm` | 商品换背景 | direct_submit | 商品图 + 场景图/描述 | 已实现 |
| `image_retouching_ecomm` | 商品图精修 | direct_submit | 商品图 + 精修类型 | 已实现 |
| `product_flat_lay_ecomm` | 商品平铺图 | enhance_then_submit | 商品图 | 已实现 |
| `product_set_images_ecomm` | 商品套图 | enhance_then_submit | 商品图 + 可选描述 | 已实现 |
| `lifestyle_fashion_photo_ecomm` | 服装种草图 | enhance_then_submit | 商品图 | 已实现 |
| `smart_watermark_removal_ecomm` | 智能去水印 | direct_submit | 带水印图 | 已实现 |
| `texture_enhancement_ecomm` | 服装材质增强 | direct_submit | 待修复图 + 参考图 | 已实现 |
| `trending_style_set_ecomm` | 爆款套图 | multi_enhance_submit | 商品图 + 模特参考 + 场景参考 | 已实现 |

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|--------|---------|--------|
| `run` | **默认。** 提交并等待完成 | 是 |
| `submit` | 批量：提交后立即退出 | 否 |
| `query` | 恢复：对已有 taskId 继续轮询 | 是 |
| `list-tools` | 查看所有 13 种功能类型 | 否 |
| `list-modules` | 查看 16 个详情模块（仅 product_detail_image） | 否 |
| `extract-selling-points` | 仅提取卖点（仅 product_detail_image） | 否 |
| `estimate-cost` | 估算费用 | 否 |

## 用法

```bash
python {baseDir}/scripts/ecommerce_image.py <subcommand> --tool-type <type> [options]
```

## 通用参数

| 参数 | 说明 |
|------|------|
| `--tool-type` | 功能类型（必选，见上表） |
| `--images` | 商品图片文件（本地路径或 URL，可多个） |
| `--prompt` | 用户提示词/描述 |
| `--modules` | 逗号分隔的模块 ID（仅 product_detail_image） |
| `--selling-points` | 手动提供卖点文本（跳过 AI 提取） |
| `--aspect-ratio` | 宽高比（如 3:4、1:1、16:9） |
| `--resolution` | 分辨率（如 1K、2K、4K） |
| `--image-count` | 每个任务生成图片数量 |
| `--model-id` | 模型 ID（默认：nano_banana_2） |
| `--board-id` | 看板 ID |
| `--timeout` | 最大轮询时间（默认：600秒） |
| `--interval` | 轮询间隔（默认：5秒） |
| `--json` | 输出完整 JSON |
| `-q, --quiet` | 静默模式 |

---

## 商品详情图 (product_detail_image) — 完整指南

### 概述

商品详情图是一套多模块的电商详情页图片，每个模块对应一种内容类型（如首页主视觉、核心卖点图、产品多角度等）。流程为：

1. 上传商品图
2. AI 提取商品卖点
3. AI 根据卖点 + 模块生成每个模块的生图提示词
4. 逐模块提交生图任务
5. 轮询所有任务直到完成

### 16 个详情模块

| ID | 名称 |
|----|------|
| `hero` | 首页主视觉 |
| `selling_points` | 核心卖点图 |
| `model_efficacy` | 痛点共鸣图 |
| `multi_angle` | 产品多角度 |
| `vibe` | 氛围展示图 |
| `texture_detail` | 细节微距图 |
| `ingredient_core` | 核心成分图 |
| `clinical_data` | 科研数据图 |
| `contrast` | 前后对比图 |
| `specs` | 详细规格图 |
| `tech_hud` | 渗透工艺图 |
| `flatlay` | 赠品全家图 |
| `sku` | SKU矩阵图 |
| `expert_lab` | 专家大楼图 |
| `after_sales` | 售后保证图 |
| `usage_guide` | 使用建议图 |

### Agent 行为规则（必须严格遵守）

> **核心原则：快速执行，不要反复提问。** Agent 负责决策，脚本负责执行。`--modules` 是必填参数，Agent 必须自己决定传什么值，绝不能因为用户没指定就卡住。

#### 1. 模块选择策略

- 用户明确指定了模块 → 直接使用
- **用户未指定（最常见情况）→ 不传 `--modules` 参数，使用脚本内置默认值（4 个模块：hero, selling_points, multi_angle, vibe）。** 不要自己判断品类选模块，直接执行即可。
  - 用户事后说「加上 XX」或「去掉 XX」→ 用 `--modules` 指定调整后的列表重新执行
- **禁止行为：** 不要问用户"你想选哪些模块"、不要列出 16 个模块让用户挑、不要因为模块选择而暂停执行

#### 2. 卖点处理策略

- **默认**：自动提取卖点，不展示、不等确认，直接进入生图流程。**不要问用户"要不要先看看卖点"**
- 用户主动说「我想看看卖点」或「先提取卖点看看」→ 才使用 `extract-selling-points` 单独展示
- 用户自己提供了卖点描述 → 通过 `--selling-points` 传入，跳过 AI 提取

#### 3. 批量确认策略

- 多个 SKU 批量执行前，Agent 统一确认一次模块选择和参数
- Agent 告知：「这批 SKU 都使用以下模块：...，开始生成？」
- 用户确认后全部自动执行，**不逐个 SKU 确认卖点或模块**

#### 4. 执行时机规则

- 用户说「开始」「好的」「可以」「继续」「做吧」或任何肯定回复 → **立即执行命令，不再提问**
- 用户发送了商品图但没说具体要求 → Agent 选择「通用」模块组合，立即执行
- **绝不能出现反复自问"该传什么参数"的情况** — 如果不确定，用通用默认值直接执行

### 品类→模块推荐参考

> Agent 根据商品类型自行判断品类，选择合适的模块组合。以下为建议，非强制。

| 品类 | 建议模块（用户主动要求更多模块时参考） |
|------|---------|
| 服饰 | hero, selling_points, multi_angle, vibe, texture_detail, sku |
| 美妆护肤 | hero, selling_points, model_efficacy, ingredient_core, clinical_data, contrast |
| 3C数码 | hero, selling_points, multi_angle, specs, tech_hud, contrast |
| 食品 | hero, selling_points, ingredient_core, flatlay, specs, usage_guide |
| 家居日用 | hero, selling_points, multi_angle, vibe, specs, usage_guide |

> 默认不传 `--modules` 时脚本自动使用 4 个模块：`hero, selling_points, multi_angle, vibe`

### 示例

#### 生成商品详情图（一键流程）

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_detail_image \
  --images product.jpg \
  --board-id <board_id>
```

#### 手动指定卖点

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_detail_image \
  --images product.jpg \
  --modules hero,selling_points \
  --selling-points "天然有机成分，24小时持久保湿，敏感肌适用，通过皮肤科测试"
```

#### 仅提取卖点

```bash
python {baseDir}/scripts/ecommerce_image.py extract-selling-points \
  --images product.jpg \
  --modules hero,selling_points,multi_angle
```

#### 查看可选模块

```bash
python {baseDir}/scripts/ecommerce_image.py list-modules
```

#### 查看所有功能类型

```bash
python {baseDir}/scripts/ecommerce_image.py list-tools
```

#### 估算费用

```bash
python {baseDir}/scripts/ecommerce_image.py estimate-cost \
  --tool-type product_detail_image
```

#### 自定义分辨率和宽高比

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_detail_image \
  --images product.jpg \
  --modules hero,selling_points \
  --resolution 4K \
  --aspect-ratio 1:1
```

---

## 商品3D效果图 (product_3d_render_ecomm) — 完整指南

将平铺的商品图（如服装平铺图）转为立体 3D 效果展示。

### 输入

- **商品图**（必须）— 产品平铺图
- **参考图**（可选）— 作为第二张 `--images` 传入，提供目标 3D 效果参考
- **用户提示词**（可选）— 不传时自动使用默认 prompt

### 默认行为

- 无参考图：自动使用默认 prompt（"将衣服变为立体效果..."）
- 有参考图：自动切换为参考模式 prompt（"参考图二的立体效果..."）
- 默认宽高比 `1:1`，分辨率 `2K`

### 示例

```bash
# 基础用法（自动使用默认 prompt）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_3d_render_ecomm \
  --images product.jpg

# 带参考图
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_3d_render_ecomm \
  --images product.jpg reference.jpg

# 自定义提示词
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_3d_render_ecomm \
  --images product.jpg \
  --prompt "将这件外套展示为挂在衣架上的效果，保持面料质感"
```

### Agent 行为规则

- 用户发了商品图说「3D」「立体」「立体效果」→ **必须调 `product_3d_render_ecomm`，禁止用 PIL/OpenCV/本地脚本做投影/浮雕等替代处理**
- 无需判断是否需要参考图，默认 prompt 即可生成良好效果
- 有两张图时，第二张自动作为 3D 效果参考

---

## 商品换背景 (background_replacement_ecomm) — 完整指南

将商品图的背景替换为指定的场景或描述。

### 输入

- **商品图**（必须）— `--images` 传入
- **场景图**（可选）— `--scene-image` 传入背景场景图
- **文字描述**（可选）— `--prompt` 描述想要的背景（与场景图二选一）

### 替换逻辑

- 有 `--scene-image` → 使用场景图作为背景参考，忽略文字描述
- 无 `--scene-image` → 使用 `--prompt` 中的文字描述替换背景
- 系统 prompt 模板从 API 获取（code: `background_replacement_ecomm`），`${user_prompt}` 替换为用户描述

### 默认参数

- 宽高比 `1:1`，分辨率 `2K`

### 示例

```bash
# 用场景图替换背景
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type background_replacement_ecomm \
  --images product.jpg \
  --scene-image beach.jpg

# 用文字描述替换背景
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type background_replacement_ecomm \
  --images product.jpg \
  --prompt "白色大理石桌面，柔和自然光，极简风格背景"

# 纯白底
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type background_replacement_ecomm \
  --images product.jpg \
  --prompt "纯白背景"
```

### Agent 行为规则

- 用户说"换个背景" + 商品图 → 询问想要什么样的背景（场景图或描述），然后执行
- 用户说"白底图" → `--prompt "纯白背景"` 直接执行
- 用户同时提供了场景图 → 用 `--scene-image` 传入，不再问描述

---

## 商品图精修 (image_retouching_ecomm) — 完整指南

AI 自动提升商品图质量，支持通用精修、光影调整、底部反射、水花效果等多种模式。

### 输入

- **商品图**（必须）— 1-4 张，`--images` 传入
- **精修类型**（可选）— `--retouch-type`，默认 `common`
- **商品位置**（可选）— `--position`，传入后覆盖精修类型的 prompt

### 精修类型选项

| 值 | 名称 | prompt_code |
|----|------|-------------|
| `common` | 通用精修 | `image_retouching_common` |
| `light` | 光影调整 | `image_retouching_light` |
| `reflex` | 底部反射 | `image_retouching_reflex` |
| `water` | 水花效果 | `image_retouching_water` |

### 商品位置选项

| 值 | 名称 | prompt_code |
|----|------|-------------|
| `front` | 正面 | `image_retouching_front` |
| `full_side` | 全侧 | `image_retouching_full_side` |
| `half_side` | 半侧面 | `image_retouching_half_side` |
| `back` | 背面 | `image_retouching_back` |
| `top` | 顶部 | `image_retouching_top` |
| `bottom` | 底部 | `image_retouching_bottom` |

### 默认参数

- 精修类型默认 `common`（通用精修），宽高比 `1:1`，分辨率 `2K`
- 最多 4 张商品图，每张带 `name: product_image_{n}` 索引

### 示例

```bash
# 通用精修（默认）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type image_retouching_ecomm \
  --images product.jpg

# 光影调整
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type image_retouching_ecomm \
  --images product.jpg \
  --retouch-type light

# 水花效果 + 多图
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type image_retouching_ecomm \
  --images product1.jpg product2.jpg product3.jpg \
  --retouch-type water

# 指定商品位置
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type image_retouching_ecomm \
  --images product.jpg \
  --position half_side
```

### Agent 行为规则

#### 精修类型关键词映射（`--retouch-type`）

| 用户可能说的 | `--retouch-type` |
|---|---|
| 精修、通用精修、提升画质、美化商品图（或无具体描述） | `common` |
| 光影、调光影、光影调整、补光、打光 | `light` |
| 反射、底部反射、倒影、镜面效果 | `reflex` |
| 水花、水花效果、溅水、水滴、加水 | `water` |

#### 与「服装材质增强」的区分

| | 商品图精修 | 服装材质增强 |
|---|---|---|
| 图片数量 | **1 张** | **2 张**（待修复 + 高清参考） |
| 关键词 | 精修、画质提升、光影、水花、反射 | 材质、纹理、图案修复 |
| 场景 | 提升单张图整体画质/效果 | 参考高清图修复服装细节 |

**判断规则**：用户发了**一张图**说「精修/修复」→ 走精修；发了**两张图**说「修复」→ 走材质增强。

#### 执行规则

- 用户说"精修商品图" + 商品图 → 默认 `--retouch-type common` 直接执行
- 用户提到具体效果 → 按上表映射
- **禁止**问用户选哪种精修类型，直接按描述判断或用默认值

---

## 商品主图 (product_main_image_ecomm) — 完整指南

生成电商白底图/场景主图，支持参考图、功能点和营销点。

### 与网页端一致：先去背景

默认会对 `--images` 中的商品图**先调用去背景**（与网页「上传商品图 → 自动去背景」一致），再 enhance + 生图。若需跳过（例如已是白底图），可加 `--no-remove-bg`。

### 输入

- **商品图**（必须）— `--images` 传入（默认会先 `remove_bg` 得到白底抠图再参与主图流程）
- **参考图**（推荐）— `--reference-image` 传入主图风格参考
- **功能点**（推荐）— `--features` 传入产品功能描述
- **营销点**（推荐）— `--marketing` 传入营销利益点
- **背景图**（可选）— `--background-image`
- **品牌 logo**（可选）— `--brand-logo`
- **跳过去背景**（可选）— `--no-remove-bg`

### 默认参数

- 宽高比 `1:1`，分辨率 `2K`

### 示例

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_main_image_ecomm \
  --images product.jpg \
  --reference-image ref.jpg \
  --features "防水透气，轻量化设计" \
  --marketing "限时8折，买二送一"

# 已是白底商品图，跳过去背景
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_main_image_ecomm \
  --images product_cutout.jpg \
  --reference-image ref.jpg \
  --no-remove-bg
```

### Agent 行为规则

- 用户说"做个主图" + 商品图 → 直接执行，不传 `--features`/`--marketing` 也可以
- 有参考图时用 `--reference-image` 传入
- 默认不要加 `--no-remove-bg`，与网页一致先抠图

---

## 虚拟穿搭 (virtual_try_on_ecomm) — 完整指南

把服装/饰品穿戴到模特身上。

### 输入

- **商品图**（必须）— `--images` 传入（最多 10 张）
- **模特图**（必须）— `--model-image` 传入模特照片
- **动作参考图**（可选）— `--pose-image` 传入动作姿势参考

### 特殊

submit 时 images 数组自动带 `id` 字段（`图1`、`图2`...），无需用户关心。

### 默认参数

- 宽高比 `3:4`，分辨率 `2K`

### 示例

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type virtual_try_on_ecomm \
  --images garment1.jpg garment2.jpg \
  --model-image model.jpg

# 带动作参考
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type virtual_try_on_ecomm \
  --images garment.jpg \
  --model-image model.jpg \
  --pose-image pose_ref.jpg
```

### Agent 行为规则

- 用户说"虚拟穿搭" + 商品图 + 模特图 → 直接执行
- 没有模特图时提醒用户提供一张模特照片

---

## 服装细节图 (garment_detail_view_ecomm) — 完整指南

为服装电商卖家生成特定部位的细节放大图。

### 输入

- **服装图**（必须）— `--images` 传入
- **服装类型**（可选）— `--garment-type`：`top`(上装) / `bottom`(下装) / `dress`(连衣裙) / `custom`(自定义)，默认 `top`
- **细节部位**（可选）— `--detail-part`：预设部位 ID（如 `top_collar`、`bottom_pocket`），或 `--detail` 自定义描述

### 可选部位

| 服装类型 | 部位 ID | 中文名 |
|---------|---------|--------|
| top | top_collar | 衬衣领口 |
| top | top_pocket | 衬衫口袋 |
| top | top_fabric | 衬衫面料 |
| top | top_pattern | 上装图案 |
| top | top_zipper | 外套拉链 |
| top | top_cuff | 上装袖口 |
| bottom | bottom_button | 下装扣子 |
| bottom | bottom_pocket | 下装口袋 |
| bottom | bottom_fabric | 下装面料 |
| bottom | bottom_pattern | 下装图案 |
| bottom | bottom_hem | 下装下摆 |
| bottom | bottom_leg_opening | 下装裤脚 |
| dress | dress_fabric | 连衣裙面料 |
| dress | dress_hem | 连衣裙下摆 |
| dress | dress_pattern | 连衣裙图案 |
| dress | dress_collar | 连衣裙领口 |
| dress | dress_strap | 吊带裙吊带 |
| dress | dress_cuff | 连衣裙袖口 |

### 默认参数

- 宽高比 `1:1`，分辨率 `2K`
- 默认 `--garment-type top`，默认部位 `衬衣领口`

### 示例

```bash
# 默认（上装领口细节）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type garment_detail_view_ecomm \
  --images shirt.jpg

# 指定部位
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type garment_detail_view_ecomm \
  --images shirt.jpg \
  --garment-type top \
  --detail-part top_fabric

# 自定义描述
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type garment_detail_view_ecomm \
  --images jacket.jpg \
  --detail "拉链和扣子的金属细节"
```

### Agent 行为规则

#### 1. 服装类型判断（`--garment-type`）

Agent 根据图片内容和用户描述自动判断，**不要问用户**：

| 用户说 / 图片特征 | `--garment-type` |
|---|---|
| 上衣、外套、衬衫、T恤、夹克、卫衣、西装、毛衣、羽绒服 | `top` |
| 裤子、裙子（半裙）、短裤、牛仔裤、阔腿裤 | `bottom` |
| 连衣裙、长裙、吊带裙、旗袍 | `dress` |
| 看不出 / 用户描述不明确 | 默认 `top` |

#### 2. 部位关键词映射（`--detail-part`）

用户说的自然语言 → 对应的 `--detail-part` 值：

| 用户可能说的 | `--detail-part` | 适用 garment-type |
|---|---|---|
| 领口、领子、衣领、圆领、V领、翻领、立领、polo领、衬衫领、帽领 | `top_collar` | top |
| 口袋、胸袋、衣兜、插手袋、贴袋 | `top_pocket` | top |
| 面料、布料、材质、质感、手感、纹理、织法 | `top_fabric` | top |
| 图案、花纹、印花、刺绣、logo、标志、字母 | `top_pattern` | top |
| 拉链、拉链头、拉锁、拉链扣 | `top_zipper` | top |
| 袖子、袖口、袖头、手腕处、袖管、臂部、袖型、灯笼袖、泡泡袖 | `top_cuff` | top |
| 扣子、纽扣、腰扣、裤扣、金属扣 | `bottom_button` | bottom |
| 口袋、裤兜、侧袋、后袋、插袋 | `bottom_pocket` | bottom |
| 面料、布料、材质、质感、手感、纹理 | `bottom_fabric` | bottom |
| 图案、花纹、印花、条纹 | `bottom_pattern` | bottom |
| 下摆、裙摆、衣摆、底边 | `bottom_hem` | bottom |
| 裤脚、裤腿、裤管、脚口、裤口、裤脚口 | `bottom_leg_opening` | bottom |
| 面料、材质、质感（连衣裙） | `dress_fabric` | dress |
| 下摆、裙摆、裙边、裙底 | `dress_hem` | dress |
| 图案、花纹、印花（连衣裙） | `dress_pattern` | dress |
| 领口、领子、衣领（连衣裙） | `dress_collar` | dress |
| 吊带、肩带、细带、挂脖 | `dress_strap` | dress |
| 袖子、袖口、袖头、袖管（连衣裙） | `dress_cuff` | dress |

#### 3. 执行规则

- 用户说"做服装细节图" + 服装图 → 默认 `--garment-type top --detail-part top_collar` 直接执行
- 用户提到具体部位（如"袖子"、"面料"）→ 按上表映射到对应 `--detail-part`
- 用户说"做全部细节" → 按服装类型选 2-3 个常用部位**并行执行**（如上装：领口+袖口+面料）
- 用户描述的部位不在预设表里 → 用 `--detail "用户原话描述"` 代替 `--detail-part`
- **禁止**：问用户"你想看哪个部位"，直接按描述判断或用默认值

---

## 商品平铺图 (product_flat_lay_ecomm) — 完整指南

从一张穿搭/模特图中提取商品，生成平铺展示图。

### 输入

- **商品图**（必须）— `--images` 传入（通常是穿搭照/模特图）
- **提取类型**（推荐）— `--extraction-target <类型>`，不传默认 `all`（整套提取）

### 提取类型选项

| `--extraction-target` | 中文名 | 说明 |
|---|---|---|
| `all` | 整套提取 | 提取图中所有穿搭单品（默认） |
| `tops` | 上装提取 | 只提取上衣/外套 |
| `bottoms` | 下装提取 | 只提取裤子/裙子 |
| `dress` | 衣裙提取 | 只提取连衣裙 |
| `shoes` | 鞋靴提取 | 只提取鞋子/靴子 |
| `jumpsuit` | 连体衣提取 | 只提取连体衣 |
| `bags` | 包包提取 | 只提取包袋 |
| `jewelry` | 首饰提取 | 只提取首饰/配饰 |
| `glasses` | 眼镜提取 | 只提取眼镜 |

### 默认参数

- 宽高比 `1:1`，分辨率 `2K`

### 示例

```bash
# 整套提取（默认）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_flat_lay_ecomm \
  --images outfit.jpg

# 只提取上装
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_flat_lay_ecomm \
  --images outfit.jpg \
  --extraction-target tops

# 只提取鞋靴
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_flat_lay_ecomm \
  --images outfit.jpg \
  --extraction-target shoes
```

### Agent 行为规则

#### 提取类型关键词映射（`--extraction-target`）

| 用户可能说的 | `--extraction-target` |
|---|---|
| 平铺图、整套、全部提取、所有单品（或无具体描述） | `all`（默认） |
| 上衣、上装、外套、衬衫 | `tops` |
| 裤子、下装、裙子（半裙） | `bottoms` |
| 连衣裙、裙装、长裙 | `dress` |
| 鞋子、鞋靴、靴子、运动鞋 | `shoes` |
| 连体衣、工装裤 | `jumpsuit` |
| 包、包包、手提包、背包 | `bags` |
| 首饰、项链、耳环、手链、配饰 | `jewelry` |
| 眼镜、墨镜、太阳镜 | `glasses` |

#### 执行规则

- 用户说"做平铺图" + 商品图 → 默认 `--extraction-target all` 直接执行
- 用户提到具体品类 → 按上表映射
- **禁止**问用户要提取什么，直接按描述判断或用默认值

---

## 商品套图 (product_set_images_ecomm) — 完整指南

从一张商品图多角度/多场景批量生成套图。

### 输入

- **商品图**（必须）— `--images` 传入
- **描述**（可选）— `--prompt` 提供生成引导

### 特殊

- 有 `--prompt` 时：使用模板 enhance + 用户描述 → submit
- 无 `--prompt` 时：使用后端 fallback 固定文案，不调用 enhance

### 默认参数

- 宽高比 `1:1`，分辨率 `2K`

### 示例

```bash
# 无描述（使用默认文案）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_set_images_ecomm \
  --images product.jpg

# 带描述
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type product_set_images_ecomm \
  --images product.jpg \
  --prompt "多角度展示，包含正面、侧面、细节"
```

### Agent 行为规则

- 用户说"做套图" + 商品图 → 直接执行，不需 prompt

---

## 服装种草图 (lifestyle_fashion_photo_ecomm) — 完整指南

生成服装穿搭种草风格的展示图。支持 8 种预设场景模板。

### 输入

- **商品图**（必须）— `--images` 传入（最多 3 张）
- **场景**（推荐）— `--scene <场景ID>`，不传则使用默认氛围文案
- **自定义提示词**（可选）— `--prompt`，替代场景模板

### 可选场景

| 场景 ID | 中文名 | 风格 |
|---------|--------|------|
| `scene_aesthetic` | 氛围美图 | 梦幻柔美、暖调光斑、胶片复古 |
| `scene_street` | 街道拍摄 | 都市街拍、真实抓拍质感 |
| `scene_mirror_selfie` | 对镜自拍 | 全身镜、手机自拍 |
| `scene_home` | 居家拍摄 | 温馨家居、自然光线 |
| `scene_coffee` | 咖啡店场景 | 文艺咖啡厅、暖棕色调 |
| `scene_canon` | 佳能滤镜 | 佳能直出色彩、暖调人像 |
| `scene_fuji` | 富士滤镜 | 富士胶片风、日系清新 |
| `scene_hat` | 帽子遮脸 | 帽檐遮面、神秘感 |

### 默认参数

- 宽高比 `3:4`，分辨率 `2K`

### 示例

```bash
# 默认（使用默认氛围文案）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type lifestyle_fashion_photo_ecomm \
  --images garment.jpg

# 指定场景
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type lifestyle_fashion_photo_ecomm \
  --images garment.jpg \
  --scene scene_street

# 自定义描述
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type lifestyle_fashion_photo_ecomm \
  --images garment.jpg \
  --prompt "户外花园下午茶场景，阳光温暖"
```

### Agent 行为规则

#### 场景自动选择

Agent 根据用户描述自动选择 `--scene`，**不要问用户选哪个场景**：

| 用户可能说的 | `--scene` |
|---|---|
| 种草图、做种草、小红书风、氛围感、梦幻、柔美、暖调、光斑（或无具体描述） | `scene_aesthetic`（默认） |
| 街拍、街道、街头、都市、城市、马路、斑马线、街头抓拍 | `scene_street` |
| 自拍、对镜、镜子、试衣间、全身镜、手机自拍、镜前 | `scene_mirror_selfie` |
| 居家、家里、沙发、客厅、飘窗、家居、室内休闲 | `scene_home` |
| 咖啡、咖啡店、咖啡馆、café、下午茶、咖啡厅、拿铁 | `scene_coffee` |
| 佳能、佳能风格、佳能滤镜、canon、暖调人像、佳能直出 | `scene_canon` |
| 富士、富士滤镜、富士胶卷、胶卷、胶片、胶片风、日系、fuji、富士色调、清新日系 | `scene_fuji` |
| 帽子遮脸、帽子、遮脸、神秘感、帽檐、压帽 | `scene_hat` |
| 用户有详细的自定义描述 | 不传 `--scene`，用 `--prompt "用户描述"` |

#### 执行规则

- 用户说"做种草图" + 商品图 → 默认 `--scene scene_aesthetic` 直接执行
- 用户提到具体风格 → 按上表映射
- 用户给了详细描述 → 用 `--prompt` 传入，不传 `--scene`

---

## 智能去水印 (smart_watermark_removal_ecomm) — 完整指南

去除商品图上的文字水印，保留产品和背景。

### 输入

- **带水印图**（必须）— `--images` 传入

### 默认参数

- 宽高比 `9:16`，分辨率 `2K`

### 示例

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type smart_watermark_removal_ecomm \
  --images watermarked.jpg
```

### Agent 行为规则

- 用户说"去水印" + 图片 → 直接执行

---

## 服装材质增强 (texture_enhancement_ecomm) — 完整指南

修复服装图中丢失的材质细节，参考高清图进行增强。

### 输入

- **待修复图 + 参考图**（必须）— `--images img1.jpg img2.jpg`（第一张为待修复图，第二张为高清参考图）

### 默认参数

- 宽高比 `9:16`，分辨率 `2K`

### 示例

```bash
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type texture_enhancement_ecomm \
  --images low_quality.jpg high_quality_ref.jpg
```

### Agent 行为规则

#### 关键词（与「商品图精修」不重叠）

材质增强专属关键词：材质、纹理、图案修复、图案不全、纹理修复、材质细节

**注意**：「精修」「修复」「画质」等通用词属于「商品图精修」，不要走材质增强。

#### 区分规则

- 用户发**两张图** + 提到「材质/纹理/图案」→ 材质增强
- 用户发**一张图** + 说「修复/精修」→ 商品图精修（不是材质增强）

#### 执行规则

- 用户提供**两张图** → 第一张=待修复图，第二张=高清参考图，直接执行（脚本自动对参考图去背景）
- 用户只提供**一张图** → 提醒需要再提供一张高清参考图
- **禁止**问用户其他问题，有两张图就直接执行

---

## 爆款套图 (trending_style_set_ecomm) — 完整指南

参考爆款风格，多轮生成穿搭套图（默认 4 轮，每轮独立 enhance + submit）。

### 输入

- **任务类型**（推荐）— `--mission-type`，不传默认 `网红地打卡`
- **商品图**（按类型）— `--images` 传入
- **模特参考**（按类型）— `--model-ref` 传入
- **场景参考**（按类型）— `--scene-ref` 传入（可多张，sceneRotate 时各轮轮替）

### 任务类型配置

| `--mission-type` | 名称 | 商品图 `--images` | 模特 `--model-ref` | 场景 `--scene-ref` | sceneRotate |
|---|---|---|---|---|---|
| `网红地打卡` | 网红打卡地 | 穿搭(可选,1张) | 模特(可选,1张) | **打卡地(必须,1-4张)** | ✅ |
| `好物plog` | 好物Plog | **物品(必须,1-4张)** | — | **场景(必须,1-4张)** | ✅ |
| `穿搭OOTD` | 穿搭OOTD | — | **穿搭(必须,1张)** | **模板(必须,1张)** | ❌ |
| `萌宠带货` | 萌宠带货 | 商品(可选,1张) | **宠物(必须,1张)** | **场景(必须,1-4张)** | ✅ |
| `一衣多穿` | 一衣多穿 | **服饰(必须,1张)** | **模特(必须,1张)** | **场景(必须,1张)** | ❌ |

### 特殊

- 固定 4 轮，每轮独立构建 metadata（图片编号 + 角色分配），独立 enhance + submit
- sceneRotate=true 时：多张场景图每轮依次使用不同的

### 默认参数

- 宽高比 `3:4`，分辨率 `2K`

### 示例

```bash
# 网红打卡（默认）
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type trending_style_set_ecomm \
  --mission-type 网红地打卡 \
  --images outfit.jpg \
  --model-ref model.jpg \
  --scene-ref place1.jpg place2.jpg place3.jpg place4.jpg

# 好物plog
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type trending_style_set_ecomm \
  --mission-type 好物plog \
  --images item1.jpg item2.jpg \
  --scene-ref bg1.jpg bg2.jpg

# 穿搭OOTD
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type trending_style_set_ecomm \
  --mission-type 穿搭OOTD \
  --model-ref ootd.jpg \
  --scene-ref template.jpg

# 一衣多穿
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type trending_style_set_ecomm \
  --mission-type 一衣多穿 \
  --images garment.jpg \
  --model-ref model.jpg \
  --scene-ref scene.jpg
```

### Agent 行为规则

#### 任务类型关键词映射（`--mission-type`）

| 用户可能说的 | `--mission-type` |
|---|---|
| 爆款套图、网红打卡、打卡地、旅游穿搭 | `网红地打卡`（默认） |
| 好物、好物推荐、plog、物品展示 | `好物plog` |
| 穿搭、OOTD、每日穿搭、穿搭模板 | `穿搭OOTD` |
| 萌宠、宠物、宠物带货、猫咪/狗狗 | `萌宠带货` |
| 一衣多穿、多场景穿搭、同一件衣服 | `一衣多穿` |

#### 执行规则

- 根据用户描述选择 `--mission-type`，按上面的任务类型配置表确定哪些图必传
- 用户没指定任务类型 → 默认 `网红地打卡`
- **禁止**问用户选哪种任务类型，根据描述和图片自动判断
  --images product.jpg \
  --model-ref model.jpg \
  --scene-ref scene1.jpg scene2.jpg

# 仅商品图
python {baseDir}/scripts/ecommerce_image.py run \
  --tool-type trending_style_set_ecomm \
  --images product.jpg
```

### Agent 行为规则

- 用户说"做爆款套图" + 商品图 → 直接执行
- 有模特/场景参考时传入对应参数

---

## 注意事项

- 商品详情图每个模块产生一个独立的生图任务，模块越多耗时越长
- 默认模型为 `nano_banana_2`（全能图片模型 V2），无需用户指定
- 默认分辨率为 2K
- 商品详情图默认宽高比 3:4（竖版详情页），其他功能各有默认值
- 结果 URL 使用 Markdown 链接格式输出：`[查看图片](url)`
- 看板编辑链接格式：`[在看板中查看](url)`
