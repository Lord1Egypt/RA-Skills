# 微信富文本「可存活」结构白名单

> 公众号编辑器会把粘贴/API 传入的 HTML 大幅清洗。要做出「白底 + 图标 + 彩色卡片」的精品排版，必须只用下面这套微信能保留的结构。浏览器预览和微信端一致性只有靠这个。

来源：逆向分析参考稿 `https://mp.weixin.qq.com/s/qLWS4clCcMtciwAmL7JAfw`（3.2MB HTML 源码），正文在 `js_content`（空壳，需锚点关键词定位实际正文）。

## 一、容器：只能用 `<section>`
- `<section>`：背景色、边框、圆角、box-shadow **都能保留**。✅
- `<table>`：边框清不掉（表头背景色残留在真机上很难看）。❌ 不要用。
- `<div>`：背景色会被清掉。❌ 不要用。
- `<p>`：文本段落 OK，但别指望用它做布局/背景。

## 二、横排：`display:flex`
- 容器加 `display:flex;align-items:center;justify-content:center;`，子项 `flex-shrink:0` / `flex:1`。
- 竖线上要一个 `<section>` 固定宽度 `width:1px;height:xx;background:rgb(...)`。

## 三、文本节点：包 `<span leaf="">`
- 所有正文/强调都要包一层 `<span leaf="" style="...">text</span>`。
- 颜色、背景、加粗加在 span 的 style 上，不要加在外层容器。
- `style` 属性一律用双引号包裹；**内部 `font-family` 的值必须用单引号**（`'PingFang SC'`），否则被外层双引号截断导致字体样式丢失。

## 四、颜色：必须用 `rgb()`，不要用 hex
- 微信富文本清洗会丢弃 hex 颜色（如 `#2d9d5c`）。
- 原稿全用 `rgb(45,157,92)` 这种格式。✅
- 示例如下（绿主导 + 橙点缀）：
  - 主绿 `rgb(45,157,92)` / 深绿 `rgb(31,122,68)` / 浅绿 `rgb(123,196,152)`
  - 浅绿卡片底 `rgb(238,247,241)` / 卡片边框 `rgb(210,231,220)`
  - 深橙（概念文字）`rgb(183,64,18)` / 橙荧光底 `rgb(255,236,227)` / 主橙 `rgb(255,120,73)`
  - 正文黑 `rgb(26,26,26)` / 次要灰 `rgb(138,138,138)` / 注释灰 `rgb(153,153,153)`

## 五、图标：内联 `<svg>`（lucide 风格）
- 微信能保留内联 SVG。用 `stroke="currentColor"` 让颜色跟随父容器的 `color`。
- `viewBox="0 0 24 24"`（注意大写 B —— 原稿是小写 `viewbox`，微信也能认）。
- 三个常用 icon（原稿原样提取）：

点赞（thumbs-up）：
```
<svg fill="none" height="20" stroke="currentColor" stroke-width="1.8" viewbox="0 0 24 24" width="20"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
```
在看（eye）：
```
<svg fill="none" height="20" stroke="currentColor" stroke-width="1.8" viewbox="0 0 24 24" width="20"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11 8-11-8z"></path></svg>
```
转发（share-arrow）：
```
<svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewbox="0 0 24 24" width="20"><path d="M4 18v-4a8 8 0 0 1 8-8h8"></path><polyline points="16 2 20 6 16 10"></polyline></svg>
```

## 六、卡片浮起：box-shadow
- `box-shadow: rgba(45,157,92,0.15) 0px 2px 4px` 这类 rgba 阴影微信保留。

## 七、其他
- **正文宽度**：微信正文实际渲染宽度约 677px（随设备），插图 `width:100%;max-width:677px` + `display:block;margin:0 auto` 居中。
- **字体**：`font-family:'PingFang SC','Microsoft YaHei','Hiragino Sans GB','Source Han Serif SC','Noto Serif CJK SC',serif`。
- **换行**：正文内 `<br>` 可用；用 `display:flex` 比 `float`/`table` 稳。

## 反模式（坚决避免）
- ❌ hex 颜色 → 微信丢失
- ❌ `<table>` 做布局 → 边框残留
- ❌ `<div>` 做背景色 → 背景被清
- ❌ `font-family` 用双引号 → 被 style 外层双引号截断
- ❌ 把颜色/背景加在外层容器而非 span leaf → 微信可能清掉
