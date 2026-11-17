# 杂志编辑 · 衬线

大号衬线感标题、隐形网格、破格张力。建议语法：章节流、叙事流。

## Token

```
主色 primary     #1A1A2E
辅色 accent      #C4903C
正文 text        #2D2D3A
次要 muted       #6B6B7B
线   line        #C8C6CE
浅底 wash        #F5F3EE
作品底 canvas    #FAF9F5
```

主色近墨蓝黑（标题、正文），辅色为旧金/古铜（仅用于引文线、页码、一处 CTA）。正文用暖灰黑，底色带纸感暖白。强调「字阶 + 网格 + 负空间」。不要指定 `font-family`，衬线感用字号阶梯、字距、行距表达。

## 形态（一篇一套）

- **标题**：左对齐、大号、极紧行距。主标题 30–36px、line-height 1.08、font-weight 700；下方紧跟一行小号英文副题（字距 1px、次要色）。二级 20px，下方接 1px 细线。
- **分割**：1px 实线 `#C8C6CE` 通栏，上方可加章节名（如 `CHAPTER 02`）。
- **卡片**：圆角 0px（直角），背景 `#F5F3EE`，无描边，左侧 3px 古铜色竖线作引文卡。
- **图注**：左齐，13px，次要色。金句用 `<em>`，不要靠 `font-style` 内联。

## 写法参考

版首（封面式）：

```html
<section style="padding:36px 14px 24px;">
  <span style="display:inline-block;font-size:10px;letter-spacing:4px;color:#C4903C;">FEATURE STORY</span>
  <p style="margin:16px 0 8px;font-size:36px;font-weight:700;color:#1A1A2E;line-height:1.08;letter-spacing:-0.5px;">主标题七字以内</p>
  <p style="margin:0;font-size:13px;color:#6B6B7B;letter-spacing:1px;">The subtitle in English</p>
</section>
```

二级标题（带章节编号 + 细线）：

```html
<section style="margin:32px 10px 14px;padding-bottom:8px;border-bottom:1px solid #C8C6CE;">
  <span style="font-size:11px;letter-spacing:2px;color:#C4903C;">CHAPTER 02</span>
  <p style="margin:6px 0 0;font-size:20px;font-weight:700;color:#1A1A2E;line-height:1.35;">小标题</p>
</section>
```

卡片小结（引文卡）：

```html
<section style="margin:16px 10px 0;padding:24px 20px;background:#F5F3EE;border-left:3px solid #C4903C;">
  <p style="margin:0;font-size:18px;line-height:1.7;color:#2D2D3A;"><em>一句话带走，像杂志金句。</em></p>
</section>
```

## 适配场景

深度报道、人物专访、文化评论、品牌故事、高端生活方式、旅行文学、财经深度、设计/建筑杂志。内刊温度请用 `olive-journal`；党政庄重请用 `red-white`。

## 挑图气质

- styleAnchor：纸质杂志摄影，隐形网格构图，暖白纸与古铜色点缀
- lightingHint：窗边自然光，柔和阴影，印刷纸质感
