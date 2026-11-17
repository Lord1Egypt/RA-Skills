# 角色立绘工作流

将此工作流用于游戏角色立绘、表情、姿势和由多视图设定图衍生的精灵图。

## 连续性

生成前检查源资产、场景脚本、对话和相邻立绘。记录角色、服装、发型、表情、姿势、画布尺寸和预期位置。将在同一连续场景中出现的立绘归为一组。

- 在连续组内保持身份、面部、年龄表现、体型、发色、服装和发型一致。
- 保留有意设计的变体，例如制服、便装、季节服装和命名的替换发型。
- 脚本不能证明外观变化是有意设计时，保留原始服装和发型。
- 每个角色、服装、发型组合使用一张已批准的参考立绘。

## 生成

在正式项目资产之外单独生成候选立绘。将原始立绘作为第一张参考图；需要时在其后添加已批准的连续性参考图。

提示词应要求全身透明立绘，并保持原始构图和预期位置。明确说明：

```text
匹配参考立绘的构图、比例和位置。
保持原始画布布局。不要场景、文字、裁剪或额外角色。
```

```bash
seagames-cli image generate \
  --model microsoft_gpt_image_2 \
  --reference-file ./assets/portraits/hero_uniform_neutral.png \
  --reference-file ./assets/portraits/hero_uniform_reference.png \
  --prompt "以已批准的风格重新绘制这张全身角色立绘。保留身份、服装、发型、姿势、透明背景、原始画布构图和位置。不要场景、文字、裁剪或额外角色。" \
  --output ./art_output/portrait_regeneration/hero_uniform_neutral_generated.png
```

替换正式立绘前审核候选图。不得直接用原始交付物替换正式立绘。

## 经验证的替换

使用 `image align-portrait` 将生成候选图与原始立绘进行验证。`--original` 必须是 PNG，因为验证通过后它可能被原地替换。

```bash
seagames-cli image align-portrait \
  --original ./assets/portraits/hero_uniform_neutral.png \
  --generated ./art_output/portrait_regeneration/hero_uniform_neutral_generated.png \
  --report ./art_output/portrait_regeneration/hero_uniform_neutral.json
```

几何校验通过后，命令先检查指定或已绑定项目的入图能力，再替换原始文件并上传最终 PNG。几何校验失败或入图能力前置检查失败时，不替换原始文件。只需离线替换时显式使用 `--no-attach`。

替换后若上传或入图失败，已替换的 PNG 和交付回执保留；使用 `canvas operation retry --operation-id ID` 补交付，不再执行对齐或覆盖原文件。几何报告的 `accepted` 只表示立绘校验通过，入图成功需检查 `canvas.delivery`。

## 验证

替换正式资产前：

1. 确认最终文件是符合所需画布尺寸的 RGBA PNG。
2. 审核主体位置和画布构图。
3. 即使画布尺寸匹配，也要拒绝验证失败的候选图。
4. 并排审核同一角色、服装组合中的所有表情和姿势。
5. 在代表性场景背景上预览，并运行目标引擎场景验证落地位置、头顶留白、层级和缩放。
6. 审核后仅通过 `image align-portrait` 替换原始文件。
