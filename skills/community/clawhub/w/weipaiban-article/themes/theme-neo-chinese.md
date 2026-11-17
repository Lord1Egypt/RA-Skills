# 新中式 · 宋式留白

低饱和墨色、大幅留白、竖排点缀、宣纸肌理。建议语法：章节流、叙事流。

## Token

```
主色 primary     #2C3E38
辅色 accent      #B03A2E
正文 text        #33332E
次要 muted       #7A7568
线   line        #C8C2B4
浅底 wash        #F7F4EC
作品底 canvas    #FAF8F2
```

主色为墨松绿（标题、正文），辅色为朱砂红（仅用于印章、编号、一处点睛）。正文用暖墨色而非纯黑。背景为带宣纸肌理感的暖白。强调「计白当黑」——留白本身就是内容。

## 形态（一篇一套）

- **标题**：横排大号宋体感 + 朱砂方印点缀。主标题 28–32px、字距宽松；二级 19px。无竖条、无色块底。
- **分割**：细线 + 留白呼吸，或 1px 渐变线 `background:linear-gradient(90deg,transparent,#C8C2B4,transparent)`。
- **卡片**：圆角 2px（近乎直角），背景 `#F7F4EC`，描边 `1px solid #D8D2C4`，无阴影。左侧 2px 墨色竖线模拟古籍版框。
- **图注**：左齐，小字。

## 写法参考

版首（大字距 + 印章）：

```html
<section style="padding:40px 16px 28px;background:#FAF8F2;text-align:center;">
  <span style="display:inline-block;font-size:11px;letter-spacing:4px;color:#7A7568;">壬寅 · 小满</span>
  <p style="margin:20px 0 0;font-size:32px;font-weight:400;color:#2C3E38;letter-spacing:8px;line-height:1.4;">主标题</p>
  <span style="display:inline-block;margin-top:16px;width:20px;height:20px;background:#B03A2E;color:#FAF8F2;font-size:9px;line-height:20px;text-align:center;">印</span>
</section>
```

二级标题（横排 + 细线）：

```html
<section style="margin:32px 10px 14px;padding-bottom:10px;border-bottom:1px solid #C8C2B4;">
  <span style="font-size:11px;color:#B03A2E;letter-spacing:2px;">壹</span>
  <p style="margin:6px 0 0;font-size:19px;font-weight:700;color:#2C3E38;line-height:1.4;">小标题</p>
</section>
```

卡片小结（古籍版框感）：

```html
<section style="margin:16px 10px 0;padding:24px 20px;background:#F7F4EC;border-left:2px solid #2C3E38;border-radius:2px;">
  <p style="margin:0;font-size:16px;line-height:2;color:#33332E;">一句话带走。</p>
</section>
```

## 适配场景

传统文化、节气文案、诗词赏析、茶道香道、文旅景区、博物馆/非遗、古籍阅读、中式美学品牌、国风设计。核心理念：宋式美学的「含蓄与留白」。一件器物、一枝花木、一枚印章，足以传达东方气质。散文呼吸感、医疗健康请用 `zen-whitespace`。

## 挑图气质

- styleAnchor：宋式宣纸肌理，水墨淡彩，暖墨与朱砂点缀，计白当黑
- lightingHint：侧窗柔光，纸面微纹理，低饱和
