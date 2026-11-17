# 摸鱼票据 · 门票卡

emerald + 硬阴影卡片，适合测评和对照。建议语法：卡片流、对照流。

## Token

```
主色 primary     #059669
辅色 accent      #F59E0B
正文 text        #3F3F3F
次要 muted       #6B7280
线   line        #A7F3D0
描边 stroke      #1F2933
浅底 wash        #ECFDF5
作品底 canvas    #FFFEF7
```

琥珀只用于星级，不描边、不做底。

## 形态（一篇一套）

- **标题**：flex 行。主色编号块 + 深字标题，底边 `2px solid #1F2933`。主标题 20–24px；二级 18px 同样带编号。
- **分割**：撕票虚线 `2px dashed #A7F3D0`，不要绿色短实线。
- **卡片**：圆角 10px，描边 `2px solid #1F2933`，硬阴影 `4px 4px 0 #1F2933`。
- **图注**：居中。
- **下划线**：`border-bottom:2px solid #A7F3D0;font-weight:600;`。每段 1–3 个短短语。

## 写法参考

版首：

```html
<section style="padding:20px 10px 16px;">
  <span style="display:inline-block;font-size:11px;letter-spacing:2px;color:#059669;font-weight:700;">TICKET · 01</span>
  <p style="margin:10px 0 0;font-size:22px;font-weight:700;color:#3F3F3F;line-height:1.3;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:20px 10px 12px;padding-bottom:12px;border-bottom:2px solid #1F2933;">
  <section style="display:flex;align-items:center;">
    <span style="display:inline-block;background:#059669;color:#FFFEF7;font-size:12px;font-weight:800;padding:6px 12px;letter-spacing:2px;">01</span>
    <p style="margin:0 0 0 12px;font-size:18px;font-weight:700;color:#3F3F3F;">小标题</p>
  </section>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:16px;background:#ECFDF5;border:2px solid #1F2933;border-radius:10px;box-shadow:4px 4px 0 #1F2933;">
  <p style="margin:0;font-size:16px;line-height:1.75;color:#3F3F3F;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：门票票据拼贴，墨色描边与硬阴影，翠绿编号，趣味信息卡
- lightingHint：平光，边缘清晰，轻微纸票质感
