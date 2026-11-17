# 效果规格卡

复制这张卡填。它是「锁定」的载体：写完这张卡，后续写码、改码、验收都以卡为准。

## 模板

```
【效果规格】<中文名> / <英文名>
职能   <反馈 / 状态转移 / 空间连续 / 引导>
触发   <元素> 上，<时机>；延迟 <n>ms
变化   <属性 1：起 → 止>；<属性 2：起 → 止>
参数   duration.<token> / ease.<token>；幅度 <px 或 scale>
收尾   <停在原位 / 还原 / 只播一次 / 自动消失>
降级   触屏：<替代方案>；reduced-motion：<保留什么>
约束   只动 <属性列表>；不改 width / height / top / left
验收   <时长内到位；无残留中间态；不引起相邻位移；掉落帧为零>
```

## 填写要点

| 字段 | 最容易糊弄的地方 |
| --- | --- |
| 职能 | 不写职能就会用错时长。一次点击配 600ms 必卡顿 |
| 触发 | 必须写元素选择器或组件名，写「卡片」等于没写 |
| 变化 | 写具体属性与起止值，不写「淡入淡出」 |
| 参数 | 引用 token 名而不是临时数字，否则全站无法统一 |
| 收尾 | 最容易漏。动画结束停半路是最常见的廉价感 |
| 降级 | 触屏 + reduced-motion 两条都必须有内容 |
| 约束 | 这句话必须原样写进需求，AI 才知道不能用 width |
| 验收 | 可测。写不出验收项，说明这个效果没想清楚 |

## 示例：三张卡一套

```
【效果规格 1/3】悬停上浮 / Hover Lift
职能   反馈
触发   .card 上 hover；延迟 0
变化   translateY 0 → -4px；box-shadow shadow-1 → shadow-2
参数   duration.200 / ease.standard；幅度 4px
收尾   离开同参数回原位，不留中间态
降级   触屏：@media (hover:hover) 内生效，改为 :active scale .98；reduced-motion：只保留阴影变化
约束   只动 transform / box-shadow；不改 width、height、top、left
验收   200ms 到位；移出不残留 translate；相邻卡片不位移

【效果规格 2/3】滚动显现 / Scroll Reveal
职能   引导
触发   section 进入视口 80% 位置；只播一次
变化   translateY 20px → 0；opacity 0 → 1
参数   duration.400 / ease.emphasized-decelerate；幅度 20px
收尾   停在最终态，来回滚动不重播
降级   reduced-motion：opacity 直接 1，不做位移；不支持 animation-timeline 时保持可见
约束   animation-timeline: view()，用 @supports 包裹；不改布局属性
验收   首屏内容不闪；滚动 3 个来回不重复播放

【效果规格 3/3】轻提示 / Toast
职能   反馈
触发   操作成功后 0ms 出现，停留 2s
变化   translateY 12px → 0；opacity 0 → 1；离场 180ms 反向
参数   duration.250 进 / duration.180 出；ease.standard
收尾   自动消失，不遮挡后续操作
降级   reduced-motion：只做透明度；用 @starting-style 实现首帧
约束   只动 transform / opacity；不改 height
验收   aria-live="polite" 可被读屏播报；连续触发不堆叠超过 3 条
```
