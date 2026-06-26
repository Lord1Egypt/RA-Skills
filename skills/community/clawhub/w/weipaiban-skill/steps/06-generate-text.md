# Step 6：生成新文本

## 前置读取

从任务目录读取以下文件：

1. **`meta.json`**：获取 `theme`（用户主题）
2. **`elements.json`**：仅筛选 `type: "text"` 的元素，仅提取每个元素的 `id`、`name`、`text`、`charCount` 字段
3. **`template-profile.json`**：仅读取 `content_density`（density_level、text_roles）和 `typography_plan` 两个字段

---

文本生成的核心原则是："**内容可以围绕用户主题，但字数节奏与文本角色风格必须延续原模板**"，避免替换后的文字超出排版框、或让整体密度失衡。

## 生成要求

- 参考原始文本的字数（`charCount`），生成**相近长度**的替换文本，单个元素的新文本字数应严格贴近原字数（允许 ±20% 的浮动，禁止大幅偏离，保护原排版不溢出）
- **遵循 density_level**：
  - `sparse` → 精炼短句、留白优先，整体信息密度低
  - `balanced` → 中等长度、有呼吸感，信息密度适中
  - `dense` → 允许较多信息量，但保持层次清晰
- **按 text_roles 区分风格**：
  - `title`（标题）：精炼有力，字数短，用词醒目
  - `subtitle`（副标题）：辅助说明主题，承上启下
  - `body`（正文）：连贯成段，逻辑清晰
  - `caption`（注释/脚注）：简洁点题，不抢主角戏份
- 内容要契合用户指定的主题
- 注意元素的 `name` 属性，它描述了文本的用途，生成内容应匹配其用途
- 保持文本之间的逻辑连贯性
- 语言风格要统一

> ⏸️ **交互点**：以表格形式展示所有文本替换方案（原文本 → 新文本），等待用户确认或要求修改。**必须等到用户确认后才能继续。**

## 后置写入

用户确认后，将文本变更写入任务目录的 `text-changes.json`：

```json
{
  "changes": [
    {
      "elementId": "元素ID",
      "name": "元素名称",
      "oldText": "原始文本",
      "newText": "新文本",
      "oldCharCount": 7,
      "newCharCount": 7
    }
  ]
}
```

同时更新 `meta.json` 的 `currentStep` 为 `"06"`。
