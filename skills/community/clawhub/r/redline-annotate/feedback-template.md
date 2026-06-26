# 标注反馈模板

本文件给 SKILL.md 的"阶段 2：应用"使用。模型从 UserPromptSubmit hook 注入的 additionalContext 里拿到标注 JSON 后，按下面的格式组装成结构化反馈，再据此修改原始 HTML 文件，并在最后**删除 inbox 文件**。

## 装配规则

输入 JSON 形如：

```json
{
  "file": "output.html",
  "timestamp": "2026-05-20T10:30:00Z",
  "annotations": [
    {
      "id": 1,
      "selector": "main > .hero > button.cta",
      "elementHTML": "<button class=\"cta\">立即购买</button>",
      "elementText": "立即购买",
      "boundingBox": {"x": 480, "y": 320, "w": 120, "h": 40},
      "comment": "颜色改成红的，再大 1.5 倍"
    }
  ]
}
```

模型应在脑内先把 JSON 转成下面的"渲染后反馈"，然后基于它调用 Edit/Write 修改 `<file>`：

---

## 渲染后反馈（模型自我提示）

> 用户对 `{{file}}` 提交了 **{{annotations.length}}** 条修改意见。请按以下要求处理：
>
> ### 修改原则
> 1. **只动被标注元素及其相关样式**——未被标注的元素不要动（除非用户明确要求"全局调整 X")。
> 2. **以 selector 定位元素**——如果 selector 在文件中找不到，先用 `elementHTML`/`elementText` 兜底匹配；都失败时在最终汇报里列出"未匹配 #ID"。
> 3. **保留原有结构**——不要重写整页或大块重排，除非反馈明确要求。
> 4. **样式改动优先就近**：内联 style 改内联，class 改对应规则；不要为一条小改动新建一整个 CSS 块。
> 5. **改完简明汇报**：列出每条标注 ID + 实际改动摘要（一行一条），不展开 diff。
>
> ### 标注列表
>
> 对每条 annotation 按下列格式渲染：
>
> ```
> 【标注 #{{id}}】
> 选择器: {{selector}}
> 当前 HTML: {{elementHTML}}
> 文本片段: "{{elementText}}"
> 视觉位置: ({{boundingBox.x}}, {{boundingBox.y}}) 尺寸 {{boundingBox.w}}×{{boundingBox.h}}
> 用户反馈: {{comment}}
> ```
>
> ### 汇报模板（修改完成后输出给用户）
>
> ```
> 已应用 {{N}} 条反馈到 {{file}}：
>   #1 ✓ <selector> — <一句话说明改了什么>
>   #2 ✓ ...
>   #3 ✗ <selector> — 未找到匹配元素，已跳过
> ```
>
> ### 收尾（强制）
>
> apply 完成后**必须**执行：
>
> ```bash
> rm <inbox_path>
> ```
>
> 不删除会导致下一次 prompt 被 hook 反复注入同一份反馈。inbox 路径在 hook 注入的 context 里有给出（通常是 `<cwd>/.redline-inbox.json`）。

## 边界情况

- **标注数为 0**：提示用户"剪贴板里 annotations 为空，没什么可改的"。
- **selector 无法匹配且 elementHTML 也找不到唯一对应**：不要乱猜元素，把这条标注列入"未匹配"由用户决定。
- **多条反馈互相冲突**（如 #1 说"按钮变红"、#2 同元素说"按钮变蓝"）：以最后一条为准，但在汇报里指出冲突。
- **反馈里包含模糊词**（"再好看一点"、"再大一点"）：做出合理具体的修改（如默认 +20%），并在汇报里说明用了什么具体值。
- **反馈跨多个元素的全局改动**（"所有按钮都改圆角"）：识别为全局意图，改 CSS 类规则而不是逐个修改。
