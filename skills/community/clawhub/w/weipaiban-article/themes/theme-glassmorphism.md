# 弥散光感 · 轻卡片

柔和低饱和渐变底、半透明浅卡、轻盈信息密度。建议语法：卡片流。

## Token

```
主色 primary     #7C6CBF
辅色 accent      #E88A8A
正文 text        #3D3A4A
次要 muted       #8B8798
线   line        #E4DFF0
浅底 wash        #F3F0F7
作品底 canvas    #F3F0F7
```

主色为雾紫（弥散底色基调），辅色为雾粉（仅用于高亮标签、CTA）。正文用低饱和暖灰紫。卡片底用半透明浅色，**不要** `backdrop-filter`（入库会被剥掉）。

## 形态（一篇一套）

- **标题**：居中、字距宽松、细体大号。主标题 26–32px、字距 2px、font-weight 600；二级 18px。无竖条、无边框。
- **分割**：居中短渐变线，`width:48px;height:2px;background:linear-gradient(90deg,#7C6CBF,#E88A8A)`。
- **卡片**：圆角 20px，背景 `rgba(255,255,255,0.72)`，描边 `1px solid rgba(255,255,255,0.9)`，阴影 `0 8px 32px rgba(124,108,191,0.12)`，内边距 24px。
- **图注**：居中，浅灰小字。

## 写法参考

版首（弥散渐变底 + 浅卡标签）：

```html
<section style="padding:36px 16px 28px;text-align:center;background:linear-gradient(135deg,#E8E0F4 0%,#F5E8EC 50%,#E0EAF4 100%);">
  <span style="display:inline-block;padding:8px 18px;border-radius:20px;background:rgba(255,255,255,0.72);font-size:11px;letter-spacing:3px;color:#7C6CBF;">WEEKLY · 03</span>
  <p style="margin:18px 0 0;font-size:28px;font-weight:600;color:#3D3A4A;letter-spacing:2px;line-height:1.3;">主标题五到九字</p>
</section>
```

二级标题：

```html
<section style="margin:28px 10px 14px;text-align:center;">
  <p style="margin:0;font-size:18px;font-weight:600;color:#7C6CBF;letter-spacing:1px;">小标题</p>
</section>
```

卡片小结：

```html
<section style="margin:14px 10px 0;padding:24px;background:rgba(255,255,255,0.72);border:1px solid rgba(255,255,255,0.9);border-radius:20px;box-shadow:0 8px 32px rgba(124,108,191,0.12);">
  <p style="margin:0;font-size:16px;line-height:1.85;color:#3D3A4A;">一句话带走。</p>
</section>
```

## 适配场景

科技产品发布、效率工具推荐、职场干货、设计灵感、生活方式品牌、美妆护肤。适合「卡片信息密度高 + 视觉轻盈」。AI/电竞/赛博请用 `cyber-dark`；商务科技灰请用 `graphite-minimal`。

## 挑图气质

- styleAnchor：柔和弥散渐变，雾面玻璃质感，低饱和紫粉与冷灰蓝
- lightingHint：漫射顶光，浅景深，干净高光
