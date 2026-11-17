# 拼贴手账 · Peak Journal

纸纹拼贴、胶带色条、邮票感，温暖不完美。建议语法：卡片流、叙事流。

## Token

```
主色 primary     #3D3A35
辅色 accent      #D4624A
正文 text        #3D3A35
次要 muted       #8C8578
线   line        #D4CDBE
浅底 wash        #F5F0E3
作品底 canvas    #FBF8F0
```

主色为墨棕，辅色为陶土红/橘（仅用于标签、胶带条、一处重点）。底色为牛皮纸暖米色。用手感温度对抗光滑感。禁止 `position` / `transform`（入库会剥掉）；胶带用 `inline-block` 色条表达。

## 形态（一篇一套）

- **标题**：衬线感加粗 + 陶土标签。主标题 24–32px；二级 18px。允许不对称 padding，不要旋转。
- **分割**：虚线 `border-bottom:1px dashed #C8BFAE`，不要直硬通栏实线。
- **卡片**：圆角 4px，背景 `#FBF8F0`，描边 `1px dashed #C8BFAE`。顶部一条陶土半透明胶带（`inline-block` 色条）。
- **图注**：左齐，手写感小字（略大字距）。

## 写法参考

版首（牛皮纸 + 标签）：

```html
<section style="padding:32px 14px 24px;background:#F5F0E3;">
  <span style="display:inline-block;padding:6px 14px;background:#D4624A;color:#FBF8F0;font-size:10px;letter-spacing:2px;">FIELD NOTE</span>
  <p style="margin:16px 0 0;font-size:28px;font-weight:700;color:#3D3A35;letter-spacing:0.5px;line-height:1.3;">主标题五到九字</p>
</section>
```

二级标题（胶带条 + 手写感）：

```html
<section style="margin:28px 10px 14px;padding-top:4px;border-bottom:1px dashed #C8BFAE;">
  <span style="display:inline-block;width:48px;height:10px;background:rgba(212,98,74,0.35);margin-bottom:8px;"></span>
  <p style="margin:0 0 10px;font-size:18px;font-weight:700;color:#3D3A35;line-height:1.4;">02 小标题</p>
</section>
```

卡片小结（拼贴卡）：

```html
<section style="margin:14px 10px 0;padding:8px 20px 20px;background:#FBF8F0;border:1px dashed #C8BFAE;border-radius:4px;">
  <span style="display:inline-block;width:36px;height:10px;background:rgba(212,98,74,0.28);margin:0 0 12px 12px;"></span>
  <p style="margin:0;font-size:16px;line-height:1.85;color:#3D3A35;">一句话带走。</p>
</section>
```

## 适配场景

旅行游记、生活方式、个人随笔、咖啡/烘焙、独立书店/文创、手作品牌、播客推荐、读书笔记。内刊请用 `olive-journal`；测评票据请用 `moyu-ticket`。

## 挑图气质

- styleAnchor：牛皮纸与胶带拼贴，胶片颗粒，陶土红与墨棕，手作温度
- lightingHint：桌面自然光，轻微阴影，纸纹可见
