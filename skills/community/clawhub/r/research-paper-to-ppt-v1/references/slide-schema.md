# 中间 JSON 结构约定

生成 PPTX 前，先整理成统一 JSON。

```json
{
  "title": "中文标题或英文标题",
  "paper_meta": {
    "title_en": "",
    "title_zh": "",
    "authors": [""],
    "author_display": "",
    "author_display_mode": "first_et_al|full",
    "first_author": "",
    "corresponding_author": "",
    "journal": "",
    "year": "",
    "doi": "",
    "pmid": "",
    "source_id": ""
  },
  "slides": [
    {
      "slide_type": "title|overview|background|question|design|materials|methods|result|summary|mechanism|strengths|limitations|significance|takeaway|closing",
      "title": "",
      "subtitle": "",
      "bullets": [""],
      "sections": [
        {
          "heading": "",
          "points": [""]
        }
      ],
      "figure_refs": ["Figure 1", "Figure 3A-F"],
      "image_paths_or_urls": [""],
      "figure_explanations": [
        {
          "figure_ref": "Figure 1",
          "explanation": "中文解释"
        }
      ],
      "source_result_subtitle": "Results 原文小标题",
      "speaker_intent": "这一页想帮助听众理解什么"
    }
  ]
}
```

## 字段要求

### slide_type
用于提示版式和排版，不要求死板，但应尽量准确。

### bullets
适合纯文本页。
每页建议 3–6 条。

### sections
适合多栏结构，如“研究对象 / 样本 / 处理条件”。

### figure_refs
保留原文编号，方便追溯。

### image_paths_or_urls
只能填原文图片来源。
如果该页没有图，可以为空数组。

### figure_explanations
这是重点字段。
必须是“更适合 PPT 讲解的中文解释”，不是原始图注照抄。
默认可直接参照原文图注翻译，再做最小必要的中文讲解整理；不要额外发散编造成更复杂的机制说明。

### source_result_subtitle
优先填写该页对应的 Results 原文小标题。
- 若原小标题中文直译过长，可在不改变原意前提下压缩成更适合 PPT 的短标题。
- 结果页标题默认优先来自这里，而不是助手自行另写完全不同的标题。

## 结果页建议

结果页必须包含：
- 1 个标题
- 2–4 条结果要点
- 至少 1 张核心原文图
- 至少 1 段或 2–4 条对应图解释

## 强制字段建议

对于 `slide_type = result | mechanism`，应视为强制：
- `figure_refs`
- `image_paths_or_urls`
- `figure_explanations`

若这些字段为空，生成器应直接停止，而不是输出纯文字结果页。

## 禁止事项

- 不要把不存在的字段当成必要字段
- 不要在 `image_paths_or_urls` 中放伪造 URL
- 不要输出空白 slide 对象凑数
- 不要把整篇全文原文大段塞进 bullets
