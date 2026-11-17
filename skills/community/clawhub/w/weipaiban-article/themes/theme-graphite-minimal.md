# 石墨极简 · 灰阶

全灰阶、极小圆角、大留白。建议语法：章节流、对照流。

## Token

```
主色 primary     #52525B
辅色 accent      #F97316
正文 text        #3F3F3F
次要 muted       #71717A
线   line        #E4E4E7
浅底 wash        #F4F4F5
作品底 canvas    #FAFAFA
```

辅色橙只用于全篇 ≤3 处点睛，不要做底、不要做分割线。

## 形态（一篇一套）

- **标题**：浅灰大号编号在上（正常流，不要 `position`），其下英文小标 + 深字标题，底边 1px `#E4E4E7`。主标题 24–30px、字距 1px；二级 18px、字距 0.5px。
- **分割**：1px 通栏细线 `#E4E4E7`，不要 32px 近黑短线。
- **卡片**：圆角 4px，描边 `1px solid #E4E4E7`，无阴影。
- **图注**：左齐。
- **下划线**：`border-bottom:2px solid #52525B;font-weight:600;`。每段 1–3 个短短语。橙色下划线不算这一条，只占那 ≤3 处点睛。

## 写法参考

版首：

```html
<section style="padding:28px 10px 20px;">
  <span style="display:inline-block;font-size:11px;letter-spacing:5px;color:#71717A;">BRIEFING</span>
  <p style="margin:12px 0 0;font-size:28px;font-weight:700;color:#3F3F3F;letter-spacing:1px;line-height:1.2;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:28px 10px 12px;padding-bottom:16px;border-bottom:1px solid #E4E4E7;">
  <p style="margin:0;font-size:48px;font-weight:900;color:#E4E4E7;line-height:1;letter-spacing:-2px;">01</p>
  <p style="margin:8px 0 0;font-size:10px;letter-spacing:3px;color:#71717A;">SECTION</p>
  <p style="margin:6px 0 0;font-size:18px;font-weight:700;color:#3F3F3F;letter-spacing:0.5px;line-height:1.4;">小标题</p>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:20px;background:#F4F4F5;border:1px solid #E4E4E7;border-radius:4px;">
  <p style="margin:0;font-size:16px;line-height:1.85;color:#3F3F3F;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：理性灰阶，极简商务摄影，冷中性色，暖橙点睛，大留白
- lightingHint：柔和顶光，几乎无色偏
