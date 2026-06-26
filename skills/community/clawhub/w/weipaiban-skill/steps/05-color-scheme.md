# Step 5：生成配色方案

> Step 5 在生成文本和图片之前执行，因为配色方案决定了整体视觉基调。

## 前置读取

从任务目录读取以下文件：

1. **`meta.json`**：获取 `theme`（用户主题）
2. **`elements.json`**：仅筛选 `type: "rect"` 和 `type: "text"` 的元素，仅提取每个元素的 `id`、`name`、`type`、`fill` 字段（忽略其他类型和字段以节省上下文）
3. **`template-profile.json`**：仅读取 `original_palette`（temperature/saturation/brightness/contrast）和 `color_plan` 两个字段

如果 elements.json 中没有 `type: "rect"` 和 `type: "text"` 的元素，则跳过本步骤。

---

配色生成的核心原则是："**色相可以跟随用户主题切换，但饱和度层级、明度层次、对比强度必须延续原模板**"，这样替换后的作品在视觉感受上仍与原模板协调。

## 配色生成要求

- 分析用户指定的主题，确定整体色彩基调（如清明节 → 清新绿色系，春节 → 红金色系，科技 → 蓝色系）
- 生成 3-5 个互相协调的主色调，数量应与原模板 `original_palette` 的层级数量对齐（dominant + secondary + accent），避免强行扩展或收缩
- **保留原模板的饱和度等级**：`original_palette.saturation` 是 low，新配色也必须是 low（例：用户主题"春节红" → 低饱和胭脂红/豆沙红，而非高饱和正红）
- **保留原模板的明度层次**：`original_palette.brightness` 是 light，新配色的明度分布也应偏亮；是 dark 则整体偏深
- **保留原模板的对比强度**：`original_palette.contrast` 是 soft，新配色 dominant 与 secondary 的 L 值差应保持在 20 以内；balanced 保持 20-50；strong 保持 > 50
- **rect 元素**（大面积背景色块）：分配主色调中的背景色，通常使用较柔和或较深的色调
- **text 元素**：分配与对应背景有足够对比度的文字颜色，确保可读性（对比度建议至少 4.5:1）
- 保持配色方案在整体视觉上的协调统一
- 参考元素的 `name` 属性了解其用途（如"标题文字"应更醒目，"正文"应更柔和）

> ⏸️ **交互点**：展示配色方案时，**先用一句话说明画像依据**（例：「原模板为 low 饱和度 / cool 色调 / light 明度 / soft 对比；已在新配色中延续相同的饱和度、明度与对比层次，仅将色相切换至 {用户主题} 基调」），然后以表格形式展示所有配色替换方案（元素名称 | 类型 | 原颜色 | 新颜色），并用色块预览展示新旧颜色对比。等待用户确认或要求调整。**必须等到用户确认后才能继续。**

## 后置写入

用户确认后，将配色方案写入任务目录的 `color-changes.json`：

```json
{
  "palette": {
    "primary": "#主色调",
    "secondary": ["#辅助色1", "#辅助色2"],
    "accent": "#点缀色"
  },
  "changes": [
    {
      "elementId": "元素ID",
      "name": "元素名称",
      "type": "rect",
      "oldFill": "#原颜色",
      "newFill": "#新颜色"
    },
    {
      "elementId": "元素ID",
      "name": "元素名称",
      "type": "text",
      "oldFill": "#原颜色",
      "newFill": "#新颜色"
    }
  ]
}
```

同时更新 `meta.json` 的 `currentStep` 为 `"05"`。
