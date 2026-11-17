# 作品动效 preset（/api/v1/vectors/svg）

本页是**作品生成 API** 的 preset 名单。

写法：

```html
<animate
  data-preset="左滑渐现"
  data-trigger="load"
  data-delay="0.12"
  data-duration="0.7"
/>
```

写错名字即 400。时序也可用原生 `begin` / `dur` / `repeatCount`。
仍禁止 `<animateMotion>` 与 `stroke-dashoffset`（路径运动 / 描绘）。

「钟摆」是元素绕顶边摆动的强调动效，不是轮播组件的「钟摆轮播」。

## 名单（54）

入场（一次性，`data-repeat="1"`）：

- 单属性：渐现、渐隐、放大、缩小、飞入、飞出、旋转
- 组合：弹入、放大出现、缩小出现、上浮渐现、下沉渐现、左滑渐现、右滑渐现、旋转飞入、展开出现、向上翻书进入、向下翻书进入、横向翻书进入、竖向翻书进入、弹性落入、盖章

强调（一次性，`data-repeat="1"`）：

摇摆（顶端支点衰减摆动，不要 `indefinite`；等幅循环请用「钟摆」）

循环 / 强调（常配 `data-repeat="indefinite"`）：

闪烁、心跳、漂浮、抖动、弹跳、钟摆、欢呼、果冻、呼吸、波浪、翻转、摇一摇

出场（一次性）：

缩小渐隐、缩小消失、放大消失、弹起消失、弹性飞出、下沉渐隐、上浮渐隐、左滑消失、右滑消失、收拢消失、撕纸移出、向上翻书移出、向下翻书移出、横向翻书移出、竖向翻书移出、立即消失

工具型（一次性，`data-repeat="1"`，默认 0.001s）：

- **立即消失**：把元素挪到画布外，不挡点击。热区一次性点击用这个。
- **设置隐藏 / 设置显示**：跳变 `visibility`，人留在原位。过零换面用这对，不要用渐隐或立即消失。

进出成对（动画组切 appear/disappear 时编辑器也会按这对换）：

- 渐现 ↔ 渐隐
- 放大 ↔ 缩小
- 飞入 ↔ 飞出
- 放大出现 ↔ 缩小消失
- 缩小出现 ↔ 放大消失
- 上浮渐现 ↔ 下沉渐隐
- 下沉渐现 ↔ 上浮渐隐
- 左滑渐现 ↔ 左滑消失
- 右滑渐现 ↔ 右滑消失
- 展开出现 ↔ 收拢消失
- 向上翻书进入 ↔ 向上翻书移出
- 向下翻书进入 ↔ 向下翻书移出
- 横向翻书进入 ↔ 横向翻书移出
- 竖向翻书进入 ↔ 竖向翻书移出
- 盖章 ↔ 弹起消失
- 弹性落入 ↔ 弹性飞出
- 设置显示 ↔ 设置隐藏

## 高度归零（画布或普通元素）

`<animate data-preset="高度归零" data-trigger="pointerUp" data-delay="1.5" data-duration="0.001" data-repeat="1" fill="freeze" restart="never" />`

从元素实际高度变到 0，释放它的布局占位。默认时长沿用编辑器的 1s；场景切换须显式指定 `data-duration="0.001"`，delay 等于本幕内容动画的播放总时间。`fill="freeze"` 保持归零，`restart="never"` 防止重复触发。

场景转场时直接挂在场景 `<svg>` 下，末幕不用；不要挂在外层占位画布，也不要放进 appear/disappear 动画组。原生 height SMIL 写法继续兼容。发布服务须包含新增白名单的代码版本；旧服务若报 unsupported preset，使用原生 height 写法。

## 动画组里不要用尺寸类动效

`appear` / `disappear` 动画组会自动把子元素的**触发动效搬到套组 wrapper** 上。
wrapper 的宽高是**整组**尺寸，不是该子元素的盒子，因此：

- **不要**在动画组子节点上写 SMIL `attributeName="width"` / `"height"`（含 `data-unit="%"`）
- **不要**指望「宽度拉伸、高度拉伸、顶部展现、打印展现、打印收起、左侧展现」这类尺寸动画在组内有效
- 出现组内请用 **opacity / translate / scale / rotation**：渐现、上浮渐现、下沉渐现、左滑渐现、右滑渐现、弹入、盖章、放大出现、缩小出现、展开出现、弹性落入
- 消失组内请用 **opacity / translate / scale / rotation**：渐隐、缩小消失、放大消失、下沉渐隐、上浮渐隐、左滑消失、右滑消失、收拢消失、弹起消失、弹性飞出等

`autoplay` 类型的动画组， 不套组，尺寸通道理论上能作用到元素自身，仍优先用 transform/opacity，避免和布局打架。

普通画布元素（不在动画组里）用 SMIL 改宽高仍然可以，例如卷帘：

```html
<rect x="24" y="40" width="342" height="160" fill="#fff6e0">
  <animate attributeName="height" values="0;160" data-duration="0.8" />
</rect>
```
