# 江岸夜巡 · 剧本

本例只演示 `layered-scroll` 的新层级契约与组件白名单。视觉方向是一次中性选择，不是默认模板。

受众：本地居民与访客。语气：沉静、夜游手记。format：三层视差滑动。

默认滑动视口 620、首屏画布 600。中间固定层给出航标；scroller 内依次是背景图专用层、透明前景内容层和承担长叙事的背景内容层。

## 四层职责

1. **中间固定内容层** `middleFixed`：透明航标停在视口右上，作为始终可见的方向参照。
2. **背景图专用层** `backgroundImage`：不用 SVG 包裹；把一张可垂直循环的 390×1170 长背景直接重复两次，总显示高度 2340，覆盖高度 1972 的背景内容层。
3. **前景内容层** `foregroundContent`：透明窗棂从左侧框住首屏；画布内用 autoplay animationGroup 做克制入场；热点弹窗与透明图片按钮位于此层。
4. **背景内容层** `backgroundContent`：开场图文、弹窗同高透明占位、三张沿途图集、SVG 图注、收口和 AI 声明依次向下排列，由本层提供滚动高度。

## 叙事路径

1. **固定航标** middleFixed svg 600：右上透明标记，不覆盖主要滑动区域。
2. **江岸底景** backgroundImage imageStack 2340：同一张长背景用两个直接 image 连续堆叠，无间距、无动效。
3. **窗棂前景** foregroundContent svg 600：左侧透明框景，以动画组轻微渐现。
4. **开场** backgroundContent svg 600：上半留白露出底景，下半用局部色块与 foreignObject 写标题和正文。
5. **场景探索** foregroundContent clickPopup 520：两个 72px 透明图片按钮，点开看码头细节；核心信息在底图 14px hint 中可见。backgroundContent 同位置放 520px 透明 spacer 保持滚动对齐。
6. **沿途图集** backgroundContent slideshow 520：三张同尺寸图片自动淡入切换。
7. **图注** backgroundContent svg 72：独立 SVG 承载图注，不使用流式 richText。
8. **收口** backgroundContent svg 220：透明船影与一句可独立成立的金句。
9. **AI 声明** backgroundContent svg 40：背景内容层最后一个直接子节点。

## 素材

| assetId             | 占位     | 裁切         | 用途                       |
| ------------------- | -------- | ------------ | -------------------------- |
| background-tile     | 390×1170 | contain 循环 | 背景图层重复使用的唯一长图 |
| middle-marker       | 90×90    | contain 透明 | 固定航标                   |
| foreground-lattice  | 220×600  | contain 透明 | 前景窗棂                   |
| story-boat          | 220×220  | contain 透明 | 开场与收口情境物           |
| popup-scene         | 390×520  | cover        | 热点底图                   |
| popup-detail        | 310×200  | cover        | 弹窗细节图                 |
| popup-open          | 72×72    | contain 透明 | 弹窗热点图片按钮           |
| slideshow-1 / 2 / 3 | 390×520  | cover        | 沿途图集                   |

文本只写在 SVG 的 `<text>` 或 `<foreignObject>` 中；本例不使用独立 richText、details 或 clickSwitch。
