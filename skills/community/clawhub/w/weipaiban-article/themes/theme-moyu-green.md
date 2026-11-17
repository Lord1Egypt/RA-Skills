# 摸鱼绿 · 杂志绿

emerald 主色、黄点缀、信息密度偏高。建议语法：章节流、卡片流。

## Token

```
主色 primary     #059669
辅色 accent      #EAB308
正文 text        #3F3F3F
次要 muted       #6B7280
线   line        #D1D5DB
浅底 wash        #ECFDF5
作品底 canvas    #F7FBF8
```

## 形态（一篇一套）

- **标题**：flex 行。左侧大号编号 + `PART`，1px 竖线，右侧标题与英文小标。不要左竖条。主标题 22–26px；二级 18px 同结构。
- **分割**：1px 实线 `#D1D5DB`，不要再加色条或虚线。
- **卡片**：圆角 16px，描边 `1px solid #BBF7D0`，阴影 `0 4px 16px rgba(0,0,0,0.06)`。
- **图注**：居中。
- **下划线**：`border-bottom:2px solid #A7F3D0;font-weight:600;`。每段 1–3 个短短语。

## 写法参考

版首：

```html
<section style="padding:20px 10px 16px;">
  <span style="display:inline-block;font-size:11px;letter-spacing:2px;color:#059669;font-weight:700;">栏目名</span>
  <span style="display:inline-block;margin-left:8px;font-size:11px;color:#6B7280;">约 1200 字 · 4 分钟</span>
  <p style="margin:12px 0 0;font-size:24px;font-weight:700;color:#3F3F3F;letter-spacing:0.5px;line-height:1.3;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:28px 10px 12px;">
  <section style="display:flex;align-items:center;">
    <section style="text-align:center;">
      <p style="margin:0;font-size:28px;font-weight:900;color:#059669;line-height:1;letter-spacing:-1px;">01</p>
      <p style="margin:0;font-size:8px;font-weight:700;color:#D1D5DB;letter-spacing:2px;">PART</p>
    </section>
    <span style="display:inline-block;width:1px;height:36px;background:#E5E7EB;margin:0 14px;font-size:0;line-height:0;overflow:hidden;">&nbsp;</span>
    <section>
      <p style="margin:0;font-size:18px;font-weight:700;color:#3F3F3F;line-height:1.4;">小标题</p>
      <p style="margin:2px 0 0;font-size:11px;font-weight:600;color:#6B7280;letter-spacing:1.5px;">ENGLISH</p>
    </section>
  </section>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:16px;background:#ECFDF5;border:1px solid #BBF7D0;border-radius:16px;box-shadow:0 4px 16px rgba(0,0,0,0.06);">
  <p style="margin:0;font-size:16px;line-height:1.75;color:#3F3F3F;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：清新杂志摄影，翠绿与暖黄点缀，信息密度偏高，干净纸面
- lightingHint：明亮散射光，轻微纸感
