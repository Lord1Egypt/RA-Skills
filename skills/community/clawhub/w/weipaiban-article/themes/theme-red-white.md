# 红白 · 编辑风

正红克制点睛，黑字加粗。建议语法：章节流、叙事流。

## Token

```
主色 primary     #DC2626
辅色 accent      #991B1B
正文 text        #3F3F3F
次要 muted       #6B7280
线   line        #E5E7EB
浅底 wash        #FEF2F2
作品底 canvas    #FAF7F5
```

辅色是深红，只用于英文小标，不要大面积铺开。

## 形态（一篇一套）

- **标题**：flex 行。红底编号胶囊 + 英文小标 + 深字标题，底边 `3px solid #DC2626`。不要左竖条。主标题 24–28px；二级 18px 同结构。
- **分割**：双实线夹空白（上 1px 线、8px 空、下 1px 线，色 `#E5E7EB`）。不要红色渐变。
- **卡片**：圆角 8px，描边 `1px solid #E5E7EB`，阴影 `0 4px 12px rgba(220,38,38,0.06)`。
- **图注**：左齐。
- **下划线**：`border-bottom:2px solid #FECACA;font-weight:600;`。每段 1–3 个短短语。

## 写法参考

版首：

```html
<section style="padding:20px 10px 16px;">
  <span style="display:inline-block;font-size:11px;letter-spacing:3px;color:#DC2626;font-weight:700;">COLUMN</span>
  <p style="margin:10px 0 0;font-size:26px;font-weight:700;color:#3F3F3F;letter-spacing:1px;line-height:1.25;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:28px 10px 12px;padding-bottom:14px;border-bottom:3px solid #DC2626;">
  <section style="display:flex;align-items:center;">
    <span style="display:inline-block;background:#DC2626;color:#FAF7F5;font-size:18px;font-weight:900;padding:4px 14px;border-radius:6px;line-height:1.3;">01</span>
    <section style="margin-left:14px;">
      <p style="margin:0;font-size:10px;color:#991B1B;font-weight:700;letter-spacing:3px;">COLUMN</p>
      <p style="margin:2px 0 0;font-size:18px;font-weight:700;color:#3F3F3F;line-height:1.4;">小标题</p>
    </section>
  </section>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:16px;background:#FEF2F2;border:1px solid #E5E7EB;border-radius:8px;">
  <p style="margin:0;font-size:16px;line-height:1.75;color:#3F3F3F;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：庄重编辑摄影，正红克制点睛，暖白纸面，仪式感
- lightingHint：均匀室内光，低对比阴影
