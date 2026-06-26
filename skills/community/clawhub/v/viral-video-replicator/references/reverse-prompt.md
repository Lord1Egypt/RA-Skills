# Reverse Prompt Assembly

> **Role:** Defines the 4-mode prompt assembly logic for converting Vision analysis into Seedance 2.0 prompts.
> Load at: Step 6-7 (building prompt and SOP). Uses the analysis JSON from Step 4 as input.
> It does NOT replace execution — these are assembly rules, not prebuilt prompts.

## Helper Functions

### _get_gender_info(analysis)
Extract gender, gender_word (男性/女性), pronoun (他/她) from analysis.

### _build_person_desc(person)
Assemble: age_range + face + skin_tone + hair + build + makeup, joined by ，

### _build_clothing_desc(clothing)
Assemble: color + material_look + type, then fit, sleeve, neckline, length, pattern, details, accessories

### _build_scene_desc(scene)
Assemble: location + background_objects + floor + wall + lighting_source + color_temperature + overall_tone

### _build_camera_desc(camera)
Assemble: movement_type + orientation + timeline. Default: "手持vlog镜头感，竖屏9:16"

### _build_audio_desc(audio)
Assemble: speech info + background + music

## Clothing Generalization Map (for outfit/full swap)

Used to replace clothing-specific words with generic equivalents:

| Specific | Generic |
|----------|---------|
| 裙摆 | 衣角 |
| 裙子 | 衣服 |
| 裙装 | 服装 |
| 连衣裙 | 衣服 |
| 半身裙 | 下装 |
| 短裙 | 下装 |
| 裤脚 | 衣角 |
| 裤腿 | 下装 |
| 醋酸缎面 | 面料 |
| 雪纺 | 面料 |
| 丝绸 | 面料 |
| 蕾丝 | 面料 |
| 牛仔 | 面料 |
| 针织 | 面料 |
| 碎花 | 图案 |
| 条纹 | 图案 |
| 格纹 | 图案 |
| A字 | 版型 |
| 修身 | 版型 |
| 宽松 | 版型 |
| 伞摆 | 下摆 |
| 鱼尾 | 下摆 |

## Four Prompt Builders

### 1. clone — Pure text, no @image refs
```
一位{person_desc}的年轻{gender_word}，穿着{clothing_desc}。
{scene_desc}。
{pronoun}的动作：{actions}。
对着镜头说：「{dialogue}」{speech_style}。
镜头：{camera_desc}。
音频：{audio_desc}。
```

### 2. face_swap — @图片1=face ref, keep original clothing
```
一位面容和身材参考@图片1的年轻{gender_word}{hair/makeup}，穿着{clothing_desc}。
{style_transfer if stylized}
{scene}, {actions}, {dialogue}, {camera}, {audio}
```

### 3. outfit_swap — @图片1=garment, keep original person
```
一位{person_desc}的年轻{gender_word}，穿着@图片1中的服装。
{scene}, {generalized_actions}, {generalized_dialogue}
Do not alter clothing pattern, color, texture or style.
{camera}, {audio}
```

### 4. full_swap — @图片1=garment + @图片2=face ref
```
一位{model_ref}年轻{gender_word}穿着@图片1中的服装，{scene}。
{style_transfer if stylized}
{generalized_actions}, {generalized_dialogue}
Do not alter clothing pattern, color, texture or style.
{camera}, {audio}
```

## Mode Determination

```python
has_person = has_face_ref or has_body_ref
if has_garment and has_person: "full_swap"
elif has_garment: "outfit_swap"
elif has_person: "face_swap"
else: "clone"
```

## SOP Generation

Mode-specific upload instructions:
- clone: 0 images, text-only generation
- face_swap: 1 image (@图片1=人脸参考)
- outfit_swap: 1 image (@图片1=衣服商品图)
- full_swap: 2 images (@图片1=衣服, @图片2=人脸参考)

## Replacement Summary

Tracks what was replaced vs preserved:
```python
{
  mode: "full_swap",
  face_replaced: true,
  body_replaced: false,
  garment_replaced: true,
  original_preserved: ["body", "scene", "actions", "dialogue", "camera"]
}
```
