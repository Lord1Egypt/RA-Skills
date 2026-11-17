# 橄榄手记 · 内刊

墨色字、米纸底、橙色点睛。建议语法：章节流、叙事流。

## Token

```
主色 primary     #1E1F23
标题 title       #23251D
辅色 accent      #ED7B2F
正文 text        #4D4F46
次要 muted       #65675E
线   line        #BFC1B7
浅底 wash        #EEEFE9
作品底 canvas    #FDFDF8
```

主色近墨但不写 `#000`。标题用 `#23251D`。橙色只用于下划线、前导词、一处 CTA。

## 形态（一篇一套）

- **标题**：版首仍是橙色前导词 + 墨色大字。二级是 flex 行：大号 `01` / `PART` + 1px 竖线 + 标题。不要左墨条。主标题 22–26px；二级 18px。
- **分割**：1px 实线 `#BFC1B7` 通栏。
- **卡片**：圆角 6px，描边 `1px solid #BFC1B7`，无阴影。
- **图注**：左齐。
- **下划线**：`border-bottom:2px solid #ED7B2F;font-weight:600;`。每段 1–3 个短短语。

## 写法参考

版首：

```html
<section style="padding:20px 10px 16px;">
  <span style="display:inline-block;font-size:12px;letter-spacing:2px;color:#ED7B2F;">内刊手记</span>
  <p style="margin:10px 0 0;font-size:24px;font-weight:700;color:#23251D;letter-spacing:0.5px;line-height:1.3;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:24px 10px 12px;">
  <section style="display:flex;align-items:center;">
    <section style="text-align:center;">
      <p style="margin:0;font-size:24px;font-weight:800;color:#23251D;line-height:1;letter-spacing:-1px;">01</p>
      <p style="margin:0;font-size:8px;font-weight:700;color:#65675E;letter-spacing:2px;">PART</p>
    </section>
    <span style="display:inline-block;width:1px;height:36px;background:#BFC1B7;margin:0 14px;font-size:0;line-height:0;overflow:hidden;">&nbsp;</span>
    <section>
      <p style="margin:0;font-size:18px;font-weight:700;color:#23251D;line-height:1.4;">小标题</p>
    </section>
  </section>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:16px;background:#EEEFE9;border:1px solid #BFC1B7;border-radius:6px;">
  <p style="margin:0;font-size:16px;line-height:1.75;color:#4D4F46;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：内刊手记，米纸底与墨色字，橙色点睛，印刷温度
- lightingHint：台灯暖光，纸面微纹理
