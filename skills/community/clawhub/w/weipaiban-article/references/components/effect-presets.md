# 动效 preset（1.1 推荐）

写法：

```html
<animate data-preset="上浮渐现" data-trigger="load" data-delay="0.12" data-duration="0.7" />
```

名字必须是下面名单里的中文。写错即 400。不要发明新名字。

## 组内用这些

入场（一次性）：渐现、上浮渐现、左滑渐现、弹入、盖章

循环（常 `data-repeat="indefinite"`）：漂浮、呼吸、钟摆

图文 SVG 装饰贴纸只用这三套循环，见 [image-svg.md](image-svg.md)。

组内只用 opacity / translate / scale / rotation。**不要** width/height 类动效（套组 wrapper 的尺寸是整组，不是该子元素）。

## 点击组配对（可选）

appear 用入场名；若做 disappear，成对换：渐现↔渐隐，上浮渐现↔下沉渐隐，左滑渐现↔左滑消失，盖章↔弹起消失。

摇摆是一次性衰减，不要 `indefinite`。等幅循环用「呼吸」「漂浮」或「钟摆」。
