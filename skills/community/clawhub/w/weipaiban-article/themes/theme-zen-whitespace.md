# 留白禅意 · 墨绿

大留白、墨绿细线、枯叶金点缀。建议语法：叙事流。

## Token

```
主色 primary     #4A5D52
辅色 accent      #C9A961
正文 text        #4F5B52
次要 muted       #7B8479
线   line        #C7C5BB
浅底 wash        #F4F1E8
作品底 canvas    #FAF8F2
```

正文用 `#4F5B52`（绿灰，仍不是纯黑）。辅色金只出现在短线或一个点上。

## 形态（一篇一套）

- **标题**：居中、字距 1–2px。主标题 22–26px；二级 18px 同样居中。无竖条。
- **分割**：居中短细线，`width:40px;height:1px;background:#4A5D52`。
- **卡片**：圆角 2px，描边 `1px solid #D8D5CB`，无阴影，内边距偏大。
- **图注**：居中。
- **下划线**：`border-bottom:1.5px solid #B5C8BC;font-weight:500;`。每段 1–3 个短短语。枯叶金不拿来划线。

## 写法参考

版首：

```html
<section style="padding:32px 10px 24px;text-align:center;">
  <span style="display:inline-block;font-size:11px;letter-spacing:4px;color:#4A5D52;">节气 · 专栏</span>
  <p style="margin:16px 0 0;font-size:24px;font-weight:700;color:#4A5D52;letter-spacing:2px;line-height:1.35;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:24px 10px 12px;text-align:center;">
  <p style="margin:0;font-size:18px;font-weight:700;color:#4A5D52;letter-spacing:1px;">小标题</p>
</section>
```

卡片小结：

```html
<section style="margin:16px 10px 0;padding:24px;border:1px solid #D8D5CB;border-radius:2px;text-align:center;">
  <p style="margin:0;font-size:16px;line-height:2;color:#4F5B52;">一句话带走。</p>
</section>
```

## 挑图气质

- styleAnchor：东方留白，墨绿细线与枯叶金点缀，散文呼吸感，宣纸暖白
- lightingHint：窗边柔光，大面积负空间
