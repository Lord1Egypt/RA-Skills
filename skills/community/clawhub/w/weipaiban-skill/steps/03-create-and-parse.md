# Step 3-4：创建作品 + 获取元素数据 + 模板画像分析

> Step 3、Step 4、Step 4.1 将连续自动执行（克隆模板 → 获取元素数据 → 生成模板画像），无需等待用户确认。

## 前置读取

从任务目录读取 `meta.json`，获取 `templateId` 和 `theme`。

## 执行门禁与中止规则

- Step 3-4.1 虽为连续步骤，但只允许在 Step 2 已完成用户模板选择后进入
- 本文命令均为受控执行模板：仅在用户未要求暂停/取消时执行
- 任一请求失败或用户中途明确中止时，停止后续自动步骤并返回当前状态

## 数据发送范围（透明披露）

- 发送到微排版 API 的数据仅包括：认证头、克隆标题、作品 ID、elements 更新内容
- 不发送本地任务目录中的其他文件内容；本地 JSON 仅用于构建请求参数

## Step 3：从模板创建作品

基于用户选择的模板创建新作品：

```bash
# 受控执行模板：仅在已完成模板选择且用户未中止时执行
curl -s -X POST \
  -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"基于用户主题的标题"}' \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/templates/选中的模板ID/clone"
```

响应格式详见 [references/api-formats.md](../references/api-formats.md#克隆模板响应)。

记录返回的作品 ID。然后将任务目录从临时路径重命名为正式路径：

```bash
mv /tmp/weipaiban-task-tmp-{时间戳} /tmp/weipaiban-task-{作品ID}
```

说明：

- 该重命名仅作用于 `/tmp/weipaiban-task-*` 任务目录命名规范化，便于断点恢复
- 不会移动系统其他路径文件；任务结束后可由用户手动清理对应目录
- 如重命名失败，保留原目录并停止进入后续步骤，避免路径不一致

更新 `meta.json` 中的 `workId` 和 `taskDir` 为新路径。

## Step 4：获取简化元素数据

调用 parser 接口获取作品的简化元素数据：

```bash
# 受控执行模板：仅在 Step 3 已成功获得作品 ID 后执行
curl -s -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/vectors/作品ID/parser"
```

响应格式详见 [references/api-formats.md](../references/api-formats.md#parser-获取响应)。

### 元素类型说明

- `text` 元素：包含文本内容和 `fill` 颜色属性
- `rect` 元素：提取所有非透明填充的矩形元素，包含 `fill` 颜色、`width` 和 `height`
- `image` 元素：包含图片信息，请注意完整识别图片的src地址信息
- `slideshow` 元素：轮播图组件，包含 `assets` 数组，每个 asset 代表轮播中的一张图片

**重要**：将 parser 接口返回的完整 `data.elements` 数组写入任务目录的 `elements.json` 文件。后续步骤将从该文件按需读取。

## Step 4.1：模板画像分析（自动执行，不打断用户）

> 这是一次**内部的客观分析**，不调用任何 API，也不设交互点。完成后立即进入 Step 5。
>
> **目的**：用户已经在 Step 2 选定了特定模板，该模板本身就携带了排版规划意图（类型、色系、节奏）。后续 Step 5-8 如果只按"主题驱动"生成，会丢失原模板的视觉调性。本步骤产出一份 `template_profile` 内部上下文对象，作为 Step 5-8 的额外约束输入，让生成结果"有方向"而不是"从零重建"。

基于 Step 4 获取的 `elements` 数据，从三个客观维度分析模板：

### ① 排版类型识别（layout_type）

统计 elements 中各类型的数量与比例：

- `text_count`：`type: "text"` 的元素数
- `image_count`：`type: "image"` 的元素数
- `has_slideshow`：是否存在 `type: "slideshow"` 元素
- `large_rect_count`：宽高均 > 300 的 `type: "rect"` 元素数

按以下规则判定 `layout_type`（命中即停止）：

| 优先级 | layout_type    | 判定条件                                               |
| ------ | -------------- | ------------------------------------------------------ |
| 1      | **轮播展示型** | `has_slideshow=true` 且 slideshow.assets.length ≥ 3    |
| 2      | **封面单图型** | `image_count=1` 且 `text_count ≤ 3` 且有大尺寸背景图   |
| 3      | **图片主导型** | `image_count ≥ text_count` 且 `image_count ≥ 3`        |
| 4      | **纯文字型**   | `image_count ≤ 1` 且 `text_count ≥ 5`                  |
| 5      | **卡片堆叠型** | `large_rect_count ≥ 3` 且存在成组重复的 text/rect 结构 |
| 6      | **图文混排型** | 其他情况（文本与图片数量接近，元素混合排布）           |

### ② 原始色系提取（original_palette）

遍历所有 `type: "rect"` 和 `type: "text"` 元素的 `fill` 字段：

1. **频次归纳**：统计每种颜色出现的次数（rect 因面积大权重 ×2），取最高频为 `dominant`，次高频 2-3 个为 `secondary`，出现频次低但色相差异大的 1 个为 `accent`
2. **HSL 转换**：将 dominant 从 hex 转 HSL，得到 (h, s, l)
3. **特征判定**：
   - `temperature`：`h ∈ [0°, 60°] ∪ [300°, 360°]` → warm；`h ∈ [180°, 270°]` → cool；其他 → neutral
   - `saturation`：`s < 30%` → low；`30% ≤ s < 70%` → medium；`s ≥ 70%` → high
   - `brightness`：`l < 35%` → dark；`35% ≤ l < 70%` → medium；`l ≥ 70%` → light
   - `contrast`：对比 dominant 与 secondary 中最深色的 L 值差；差 < 20 → soft；20-50 → balanced；> 50 → strong

### ③ 内容密度与结构（content_density）

- `text_elements`：text 元素总数
- `avg_char_count` / `max_char_count` / `min_char_count`：基于 `charCount` 字段的统计
- `text_roles`：根据每个 text 元素的 `name` 字段分类推断（title/subtitle/body/caption），关键词匹配：
  - `title`：包含"标题"、"title"、"主标"、"大标"
  - `subtitle`：包含"副标"、"subtitle"、"小标"
  - `body`：包含"正文"、"内容"、"body"、"段落"
  - `caption`：包含"注释"、"说明"、"caption"、"脚注"
  - 无匹配时：按 `charCount` 判断——≤ 8 字归入 title，8-20 归入 subtitle，20-50 归入 body，> 50 归入 body，< 4 归入 caption
- `image_elements` / `slideshow_assets`：图片数量统计
- `density_level`：
  - `sparse`：`text_elements ≤ 4` 且 `avg_char_count ≤ 12`
  - `dense`：`text_elements ≥ 10` 或 `avg_char_count ≥ 25`
  - `balanced`：其他

### 输出 template_profile

将以上分析结果组装为一份 JSON 对象，并基于客观维度推导三条**自然语言排版规划**：

```json
{
  "template_profile": {
    "layout_type": "图文混排型",
    "layout_signals": {
      "text_count": 8,
      "image_count": 3,
      "has_slideshow": false,
      "large_rect_count": 2
    },
    "original_palette": {
      "dominant": "#A3D9A5",
      "secondary": ["#F5F5F5", "#5E8B73"],
      "accent": "#FF6B6B",
      "temperature": "cool",
      "saturation": "low",
      "brightness": "light",
      "contrast": "soft"
    },
    "content_density": {
      "text_elements": 8,
      "avg_char_count": 15,
      "max_char_count": 42,
      "min_char_count": 4,
      "text_roles": { "title": 1, "subtitle": 2, "body": 4, "caption": 1 },
      "image_elements": 3,
      "slideshow_assets": 0,
      "density_level": "balanced"
    },
    "typography_plan": "本模板为图文混排，正文偏短句（avg 15 字），标题精炼；生成新文本时保持相近字数节奏，避免长段堆砌。",
    "color_plan": "原模板为低饱和度冷色调、柔和对比；即使切换到新主题色系，新配色需保持 low 饱和度与 soft 对比层次，避免突兀的高饱和冲击。",
    "image_plan": "以简洁构图为主，明度偏亮（light）、饱和度低；生成图应遵循相近的明度与饱和度，与模板原有氛围协调。"
  }
}
```

三条 `*_plan` 文本由对应客观维度自动推导得出，需真实反映当前模板的特征（不要使用模板化文本）。

**重要**：将 `template_profile` 对象写入任务目录的 `template-profile.json` 文件。**后续 Step 5、Step 6、Step 7、Step 8a 必须从该文件读取 template_profile 并作为生成约束输入**。

## 后置写入

确认以下文件已写入任务目录：

- `meta.json`（已更新 workId、taskDir、currentStep="03"）
- `elements.json`（完整 elements 数组）
- `template-profile.json`（完整 template_profile 对象）

本步骤不输出任何用户可见内容，直接进入 Step 5。
