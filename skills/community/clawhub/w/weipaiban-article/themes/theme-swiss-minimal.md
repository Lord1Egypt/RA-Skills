# 极简黑白 · 瑞士风

近黑近白灰、非衬线粗体、硬朗几何网格。建议语法：对照流、章节流。

## Token

```
主色 primary     #111111
辅色 accent      #FF3B30
正文 text        #1A1A1A
次要 muted       #6E6E6E
线   line        #111111
浅底 wash        #F2F2F2
作品底 canvas    #FAFAFA
```

主色近黑（标题、线条、几何），辅色信号红（整篇只用一次，关键数字或 CTA）。正文 `#1A1A1A`。作品底 `#FAFAFA`，**不要** `#000` / `#FFF`（方言禁止纯黑纯白做作品底）。全篇只用黑/白/灰 + 一个红点。

## 形态（一篇一套）

- **标题**：左对齐、超大非衬线粗体、极紧字距。主标题 32–40px、letter-spacing -1px、line-height 1.05；副题用细体小号。无竖条、无装饰线。
- **分割**：近黑 2px 粗线通栏（硬切割），或大面积近黑底反浅字区块切换。
- **卡片**：圆角 0px，背景 `#F2F2F2`，描边 `1px solid #111111`，无阴影。编号用超大数字（如 `01`，48–60px）。
- **图注**：左齐，12px 次要色，可加粗前缀。

文字稀疏时容易显空，信息密度高时才有力量。不建议用于碎片化轻内容。

## 写法参考

版首（硬切割封面感）：

```html
<section style="padding:32px 14px 24px;background:#FAFAFA;border-bottom:3px solid #111111;">
  <span style="display:inline-block;font-size:10px;letter-spacing:3px;color:#6E6E6E;font-weight:700;">ISSUE No.07</span>
  <p style="margin:14px 0 0;font-size:38px;font-weight:900;color:#111111;letter-spacing:-1px;line-height:1.05;">主标题四到七字</p>
</section>
```

二级标题（编号 + 黑线）：

```html
<section style="margin:32px 10px 14px;padding-bottom:10px;border-bottom:2px solid #111111;">
  <span style="font-size:11px;font-weight:700;color:#6E6E6E;">01 / 04</span>
  <p style="margin:6px 0 0;font-size:20px;font-weight:800;color:#111111;line-height:1.3;">小标题</p>
</section>
```

卡片小结（数据/观点卡）：

```html
<section style="margin:14px 10px 0;padding:24px;background:#F2F2F2;border:1px solid #111111;border-radius:0;">
  <span style="display:block;font-size:48px;font-weight:900;color:#111111;line-height:1;">01</span>
  <p style="margin:12px 0 0;font-size:16px;line-height:1.75;color:#1A1A1A;">一句话带走。</p>
</section>
```

## 适配场景

时尚大片、深度访谈、财经资讯、建筑设计、艺术展览、先锋品牌、年度报告、编辑精选。克制商务灰请用 `graphite-minimal`。碎片化轻内容不要用本主题。

## 挑图气质

- styleAnchor：瑞士国际主义，几何网格，高对比黑白摄影，一点信号红
- lightingHint：硬光、利落阴影、博物馆展陈感
