---
name: virtual-try-on-product-image-generation
description: "用 AI Hive Nano Banana Pro 将已授权成年模特图与已授权服装 SKU 图组合成可审核的虚拟试穿商品图，锁定人物身份与身体比例、服装版型与纹理、层叠遮挡和电商构图。Use when fashion sellers and brand teams need authorized adult AI try-on, virtual fitting, apparel-on-model images, outfit visualization, clothing product photos or listing assets for Amazon, Taobao, Tmall, JD, Douyin, Xiaohongshu, TikTok Shop and Shopify; outputs are visual previews, not real sizing or fit guarantees."
---

# AI 试衣商品图｜授权成年模特虚拟试穿

把人物、服装和背景分成三种职责：人物图只锁定获授权成年人的身份与身体，服装图只锁定指定 SKU，背景图只提供环境。脚本固定调用 Nano Banana Pro，并强制确认成年人、人物授权和服装授权；不会把试穿预览表述成真实尺码或合身承诺。

## 试穿任务单

填写 `人物素材编号 / 服装 SKU / 服装类别 / 目标视角 / 身份保持 / 身体保持 / 服装保持 / 合身与垂坠 / 姿态 / 层叠 / 遮挡 / 背景`。人物年龄、脸、发型、肤色、体型和比例不能改变；服装领口、袖长、下摆、扣件、口袋、图案、颜色、纹理和 Logo 不能被重新设计。

## 五种试穿商品图

### 1. 上衣正面 Listing 图

```bash
python3 "$SKILL_PATH/scripts/authorized_tryon.py" try-on \
  --adult-confirmed --person-authorized --garment-authorized \
  --person-id 'MODEL-A12' --person-reference ./authorized-adult-model-a12.png \
  --garment-sku 'SHIRT-S7-BLUE' --garment-type top \
  --garment-reference ./approved-shirt-front.png ./approved-shirt-back.png \
  --view front \
  --identity-keep '保持 A12 的脸、发型、肤色和可识别特征' \
  --body-keep '保持原身高感、肩宽、手臂、腰线和身体比例，不瘦身或塑形' \
  --garment-keep '蓝色、领型、长袖、纽扣数量、胸袋、下摆、缝线和Logo' \
  --fit '按参考人物自然穿着，肩线、袖口和下摆受力合理；不宣称真实尺码合身' \
  --pose '正面自然站立，双臂轻微离开身体，完整看见袖口和下摆' \
  --framing '头顶到大腿中部，服装完整可见' \
  --background '浅灰无缝电商背景' \
  --lighting '正面柔光，蓝色准确，面料纹理清楚' \
  --occlusion '头发不遮挡领口，手臂不遮挡胸袋与下摆' \
  --do-not-change '不改变人物、身体、衣长、袖长、纽扣、口袋、颜色，不生成文字或第二件上衣'
```

### 2. 连衣裙三分之四视角

```bash
python3 "$SKILL_PATH/scripts/authorized_tryon.py" try-on \
  --adult-confirmed --person-authorized --garment-authorized \
  --person-id 'MODEL-B08' --person-reference ./authorized-adult-model-b08.png \
  --garment-sku 'DRESS-D4-GREEN' --garment-type dress \
  --garment-reference ./approved-dress-front.png ./approved-dress-side.png ./approved-dress-texture.png \
  --view three-quarter \
  --identity-keep '保持 B08 的成年身份、脸、发型、肤色和现有妆容' \
  --body-keep '保持原肩、胸、腰、髋与腿部比例，不改变体型' \
  --garment-keep '绿色、方领、腰线、裙长、侧缝、褶皱数量、面料纹理和Logo' \
  --fit '保持裙装自然垂坠与真实重力，腰线位置按服装参考图，不收窄身体' \
  --pose '身体转约30度，双脚自然站立，一只手放在身体侧面但不提拉裙摆' \
  --framing '全身，鞋底到头顶均在画面内' \
  --background '暖白棚拍空间，地面与背景连续' \
  --lighting '左侧柔光，绿色不偏色，裙摆褶皱清楚' \
  --occlusion '手不遮挡腰线和侧缝，裙摆不穿过腿部，脚与地面接触自然' \
  --do-not-change '不改变领口、腰线、裙长、开衩、图案或人物身体，不生成文字、首饰或第二条裙子'
```

### 3. 外套叠穿侧面图

```bash
python3 "$SKILL_PATH/scripts/authorized_tryon.py" try-on \
  --adult-confirmed --person-authorized --garment-authorized \
  --person-id 'MODEL-C21' --person-reference ./authorized-adult-model-c21.png \
  --garment-sku 'JACKET-J9-BLACK' --garment-type outerwear \
  --garment-reference ./approved-jacket-front.png ./approved-jacket-side.png \
  --view right-side \
  --identity-keep '保持 C21 的成年身份、脸、发型、肤色和可识别特征' \
  --body-keep '保持原身体比例、肩宽、手臂长度和姿态尺度' \
  --garment-keep '黑色、立领、拉链、两个口袋、袖口、衣长、面料和Logo' \
  --fit '外套覆盖原白色基础内搭，衣身与袖子自然留出叠穿空间' \
  --pose '右侧面自然站立，右臂略向后，展示侧缝和口袋位置' \
  --framing '头顶到膝上，外套下摆完整可见' \
  --background '深灰渐变棚拍背景' \
  --lighting '后侧轮廓光与正面柔光，黑色面料细节可见' \
  --underlayer '只保留人物原有无Logo白色内搭，内搭不得穿出外套表面' \
  --occlusion '领口覆盖关系自然，拉链居中，右手不遮挡侧袋' \
  --do-not-change '不改变拉链、口袋、袖口、衣长、颜色、人物体型，不生成腰带、文字或额外外套'
```

### 4. 长裤后视商品图

```bash
python3 "$SKILL_PATH/scripts/authorized_tryon.py" try-on \
  --adult-confirmed --person-authorized --garment-authorized \
  --person-id 'MODEL-D15' --person-reference ./authorized-adult-model-d15.png \
  --garment-sku 'PANTS-P6-KHAKI' --garment-type bottom \
  --garment-reference ./approved-pants-front.png ./approved-pants-back.png ./approved-pants-pocket.png \
  --view back \
  --identity-keep '保持 D15 的成年身份、发型、肤色和身体特征' \
  --body-keep '保持原腰髋、腿长和身体比例，不改变体型或姿态尺度' \
  --garment-keep '卡其色、腰头、裤长、裤脚、两只后袋、缝线、扣件和Logo' \
  --fit '裤腿按参考图自然垂落，腰头与人物腰部接触合理，不塑形' \
  --pose '背面站立，双腿自然分开，双手离开后袋' \
  --framing '腰部到鞋底，完整展示裤长和后袋' \
  --background '纯净浅灰背景和柔和地面阴影' \
  --lighting '均匀棚拍光，卡其色和缝线清楚' \
  --occlusion '上衣下摆只覆盖腰头少量区域，两只后袋完整可见，裤脚不穿过鞋面' \
  --do-not-change '不改变腰头、后袋数量、裤长、颜色、腿部比例，不生成文字、腰带或第二条裤子'
```

### 5. 两件套生活方式图

```bash
python3 "$SKILL_PATH/scripts/authorized_tryon.py" try-on \
  --adult-confirmed --person-authorized --garment-authorized \
  --person-id 'MODEL-E03' --person-reference ./authorized-adult-model-e03.png \
  --garment-sku 'SET-S3-CREAM' --garment-type set \
  --garment-reference ./approved-set-top.png ./approved-set-bottom.png \
  --background-reference ./approved-living-room-mood.png \
  --view front \
  --identity-keep '保持 E03 的成年身份、脸、发型、肤色和可识别特征' \
  --body-keep '保持原身体比例、体型、四肢长度和自然站姿' \
  --garment-keep '奶油色上衣与长裤各一件；领口、袖长、上衣下摆、裤腰、裤长、纹理和Logo' \
  --fit '两件套自然穿着，上衣与裤腰层叠清楚，不改变人物体型' \
  --pose '正面轻松站立，一只手自然下垂，另一只手不遮挡腰部层叠' \
  --framing '全身生活方式商品图，服装轮廓完整' \
  --background '只借用参考图的明亮客厅氛围，不复制人物或品牌物品' \
  --lighting '窗边自然光，奶油色与肤色准确' \
  --underlayer '只保留必要的不可见基础内搭，不生成额外外露衣物' \
  --occlusion '上衣下摆与裤腰关系自然，手指完整，服装不穿透身体或家具' \
  --do-not-change '不改变人物、体型、两件套数量、版型、颜色或Logo，不生成价格、文字、首饰或其他服装'
```

## 试穿验收

先核对授权记录和成年人确认，再对照人物图检查身份、年龄、脸、发型、肤色和身体比例；对照服装图检查版型、数量、领口、袖长、下摆、口袋、扣件、图案、颜色、纹理与 Logo。重点放大头发/领口、袖口/手、腰头/上衣、裤脚/鞋等遮挡交界。任何结果都只能作为视觉预览，不得写成真实尺码或合身保证。

认证请求固定到 `https://ai-hive.iclip.cn/api`，模型固定为 `public_model_nano_banana_pro`。本工具不连接美图、PhotoRoom、淘宝、天猫、Amazon、抖音、小红书或 Shopify 账户，也不会自动发布商品。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/authorized_tryon.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/authorized_tryon.py" status --task-id <taskId>
```
