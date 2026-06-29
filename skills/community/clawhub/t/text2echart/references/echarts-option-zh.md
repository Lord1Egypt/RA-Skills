配置项 API GL配置 教程
setOption({
收起所有
title: {...} ,
legend: {...} ,
grid: {...} ,
xAxis: {...} ,
yAxis: {...} ,
polar: {...} ,
radiusAxis: {...} ,
angleAxis: {...} ,
radar: {...} ,
dataZoom: [{...}] ,
visualMap: [{...}] ,
tooltip: {...} ,
axisPointer: {...} ,
toolbox: {...} ,
brush: {...} ,
geo: {...} ,
parallel: {...} ,
parallelAxis: {...} ,
singleAxis: {...} ,
timeline: {...} ,
graphic: {...} ,
calendar: {...} ,
matrix: {...} ,
thumbnail: {...} ,
dataset: {...} ,
aria: {...} ,
series: [{...}] ,
darkMode ... ,
color ... ,
backgroundColor: 'transparent' ,
textStyle: {...} ,
animation: true ,
animationThreshold: 2000 ,
animationDuration: 1000 ,
animationEasing: 'cubicOut' ,
animationDelay: 0 ,
animationDurationUpdate: 300 ,
animationEasingUpdate: 'cubicInOut' ,
animationDelayUpdate: 0 ,
stateAnimation: {...} ,
blendMode: 'source-over' ,
hoverLayerThreshold: 3000 ,
useUTC: false ,
richInheritPlainLabel: true ,
options ... ,
media: [{...}] ,
title

标题组件，包含主标题和副标题。

在 ECharts 2.x 中单个 ECharts 实例最多只能拥有一个标题组件。但是在 ECharts 3 中可以存在任意多个标题组件，这在需要标题进行排版，或者单个实例中的多个图表都需要标题时会比较有用。

例如下面不同缓动函数效果的示例，每一个缓动效果图都带有一个标题组件：

所有属性
title. id
string

组件 ID。默认不指定。指定则可用于在 option 或者 API 中引用组件。

title. show = true
 试一试
boolean

是否显示标题组件。

title. text = ''
 试一试
string

主标题文本，支持使用 \n 换行。

[警告]: 如果使用了 toolbox.feature.saveAsImage，并且没有设置 toolbox.feature.saveAsImage.name，会用 title[0].text 替代。这种用法是历史实现但并不推荐，应该总是显式指定toolbox.feature.saveAsImage.name；否则，不得不考虑 title.text 是否是个正确的文件名，以及其 安全性。文档 “安全指南” 给出了安全使用建议。
title. link = ''
string

主标题文本超链接。

[警告]: 此 URL 字符串直接被使用，并未在内部做其他净化处理（sanitization） 如果他们来自于“不受信任”的来源，必须考虑 安全风险。文档 “安全指南” 给出了安全使用建议。
title. target = 'blank'
string

指定窗口打开主标题超链接。

可选：

'self' 当前窗口打开

'blank' 新窗口打开

 title. textStyle
Object
 title.textStyle. color = '#333'
 试一试
Color

主标题文字的颜色。

 title.textStyle. fontStyle = 'normal'
 试一试
string

主标题文字字体的风格。

可选：

'normal'
'italic'
'oblique'
 title.textStyle. fontWeight = 'bolder'
 试一试
stringnumber

主标题文字字体的粗细。

可选：

'normal'
'bold'
'bolder'
'lighter'
100 | 200 | 300 | 400...
 title.textStyle. fontFamily = 'sans-serif'
 试一试
string

主标题文字的字体系列。

还可以是 'serif' , 'monospace', 'Arial', 'Courier New', 'Microsoft YaHei', ...

 title.textStyle. fontSize = 18
 试一试
number

主标题文字的字体大小。

 title.textStyle. lineHeight
 试一试
number

行高。

rich 中如果没有设置 lineHeight，则会取父层级的 lineHeight。例如：

{
    lineHeight: 56,
    rich: {
        a: {
            // 没有设置 `lineHeight`，则 `lineHeight` 为 56
        }
    }
}

 title.textStyle. width
 试一试
number

文本显示宽度。

 title.textStyle. height
 试一试
number

文本显示高度。

 title.textStyle. textBorderColor
 试一试
Color

文字本身的描边颜色。

 title.textStyle. textBorderWidth
 试一试
number

文字本身的描边宽度。

 title.textStyle. textBorderType = 'solid'
 试一试
stringnumberArray

文字本身的描边类型。

可选：

'solid'
'dashed'
'dotted'

自 v5.0.0 开始，也可以是 number 或者 number 数组，用以指定线条的 dash array，配合 textBorderDashOffset 可实现更灵活的虚线效果。

例如：

{

textBorderType: [5, 10],

textBorderDashOffset: 5
}

 title.textStyle. textBorderDashOffset = 0
 试一试
number
从 v5.0.0 开始支持

用于设置虚线的偏移量，可搭配 textBorderType 指定 dash array 实现灵活的虚线效果。

更多详情可以参考 MDN lineDashOffset。

 title.textStyle. textShadowColor = 'transparent'
 试一试
Color

文字本身的阴影颜色。

 title.textStyle. textShadowBlur = 0
 试一试
number

文字本身的阴影长度。

 title.textStyle. textShadowOffsetX = 0
 试一试
number

文字本身的阴影 X 偏移。

 title.textStyle. textShadowOffsetY = 0
 试一试
number

文字本身的阴影 Y 偏移。

 title.textStyle. overflow = 'none'
 试一试
string

文字超出宽度是否截断或者换行。配置width时有效

'truncate' 截断，并在末尾显示ellipsis配置的文本，默认为...
'break' 换行
'breakAll' 换行，跟'break'不同的是，在英语等拉丁文中，'breakAll'还会强制单词内换行
 title.textStyle. ellipsis = '...'
string

在overflow配置为'truncate'的时候，可以通过该属性配置末尾显示的文本。

  title.textStyle. rich
Object

在 rich 里面，可以自定义富文本样式。利用富文本样式，可以在标签中做出非常丰富的效果。

例如：

label: {
    // 在文本中，可以对部分文本采用 rich 中定义样式。
    // 这里需要在文本中使用标记符号：
    // `{styleName|text content text content}` 标记样式名。
    // 注意，换行仍是使用 '\n'。
    formatter: [
        '{a|这段文本采用样式a}',
        '{b|这段文本采用样式b}这段用默认样式{x|这段用样式x}'
    ].join('\n'),

    rich: {
        a: {
            color: 'red',
            lineHeight: 10
        },
        b: {
            backgroundColor: {
                image: 'xxx/xxx.jpg'
            },
            height: 40
        },
        x: {
            fontSize: 18,
            fontFamily: 'Microsoft YaHei',
            borderColor: '#449933',
            borderRadius: 4
        },
        ...
    }
}


详情参见教程：富文本标签

所有属性
{ <style_name> }
 title.textStyle. richInheritPlainLabel = true
boolean
从 v6.0.0 开始支持

富文本样式是否继承普通文本样式。

此配置项用于向历史兼容。

从 v6 版本开始，富文本标签 (label.rich / textStyle.rich) 部分样式（fontStyle, fontWeight, fontSize, fontFamily, textShadowColor, textShadowBlur, textShadowOffsetX, textShadowOffsetY）默认继承 普通文本样式 (label / textStyle)。你可以设置 richInheritPlainLabel: false （可在最外层配置项或与同级文本样式配置项）来禁用此行为。

option = {
    richInheritPlainLabel: false, // In most cases, this is enough.
    xxx1: {
        // Can also set it here to only control this label.
        label: {
            richInheritPlainLabel: false,
            rich: {/* ... */},
        }
    },
    xxx2: {
        textStyle: {
            richInheritPlainLabel: false,
            rich: {/* ... */},
        }
    }
}

title. subtext = ''
 试一试
string

副标题文本，支持使用 \n 换行。

title. sublink = ''
string

副标题文本超链接。

[警告]: 此 URL 字符串直接被使用，并未在内部做其他净化处理（sanitization） 如果他们来自于“不受信任”的来源，必须考虑 安全风险。文档 “安全指南” 给出了安全使用建议。
title. subtarget = 'blank'
string

指定窗口打开副标题超链接，可选：

'self' 当前窗口打开

'blank' 新窗口打开

 title. subtextStyle
Object
 title.subtextStyle. color = '#aaa'
 试一试
Color

副标题文字的颜色。

 title.subtextStyle. fontStyle = 'normal'
 试一试
string

副标题文字字体的风格。

可选：

'normal'
'italic'
'oblique'
 title.subtextStyle. fontWeight = 'normal'
 试一试
stringnumber

副标题文字字体的粗细。

可选：

'normal'
'bold'
'bolder'
'lighter'
100 | 200 | 300 | 400...
 title.subtextStyle. fontFamily = 'sans-serif'
 试一试
string

副标题文字的字体系列。

还可以是 'serif' , 'monospace', 'Arial', 'Courier New', 'Microsoft YaHei', ...

 title.subtextStyle. fontSize = 12
 试一试
number

副标题文字的字体大小。

 title.subtextStyle. align
 试一试
string

文字水平对齐方式，默认自动。

可选：

'left'
'center'
'right'

rich 中如果没有设置 align，则会取父层级的 align。例如：

{
    align: right,
    rich: {
        a: {
            // 没有设置 `align`，则 `align` 为 right
        }
    }
}

 title.subtextStyle. verticalAlign
 试一试
string

文字垂直对齐方式，默认自动。

可选：

'top'
'middle'
'bottom'

rich 中如果没有设置 verticalAlign，则会取父层级的 verticalAlign。例如：

{
    verticalAlign: bottom,
    rich: {
        a: {
            // 没有设置 `verticalAlign`，则 `verticalAlign` 为 bottom
        }
    }
}

 title.subtextStyle. lineHeight
 试一试
number

行高。

rich 中如果没有设置 lineHeight，则会取父层级的 lineHeight。例如：

{
    lineHeight: 56,
    rich: {
        a: {
            // 没有设置 `lineHeight`，则 `lineHeight` 为 56
        }
    }
}

 title.subtextStyle. width
 试一试
number

文本显示宽度。

 title.subtextStyle. height
 试一试
number

文本显示高度。

 title.subtextStyle. textBorderColor
 试一试
Color

文字本身的描边颜色。

 title.subtextStyle. textBorderWidth
 试一试
number

文字本身的描边宽度。

 title.subtextStyle. textBorderType = 'solid'
 试一试
stringnumberArray

文字本身的描边类型。

可选：

'solid'
'dashed'
'dotted'

自 v5.0.0 开始，也可以是 number 或者 number 数组，用以指定线条的 dash array，配合 textBorderDashOffset 可实现更灵活的虚线效果。

例如：

{

textBorderType: [5, 10],

textBorderDashOffset: 5
}

 title.subtextStyle. textBorderDashOffset = 0
 试一试
number
从 v5.0.0 开始支持

用于设置虚线的偏移量，可搭配 textBorderType 指定 dash array 实现灵活的虚线效果。

更多详情可以参考 MDN lineDashOffset。

 title.subtextStyle. textShadowColor = 'transparent'
 试一试
Color

文字本身的阴影颜色。

 title.subtextStyle. textShadowBlur = 0
 试一试
number

文字本身的阴影长度。

 title.subtextStyle. textShadowOffsetX = 0
 试一试
number

文字本身的阴影 X 偏移。

 title.subtextStyle. textShadowOffsetY = 0
 试一试
number

文字本身的阴影 Y 偏移。

 title.subtextStyle. overflow = 'none'
 试一试
string

文字超出宽度是否截断或者换行。配置width时有效

'truncate' 截断，并在末尾显示ellipsis配置的文本，默认为...
'break' 换行
'breakAll' 换行，跟'break'不同的是，在英语等拉丁文中，'breakAll'还会强制单词内换行
 title.subtextStyle. ellipsis = '...'
string

在overflow配置为'truncate'的时候，可以通过该属性配置末尾显示的文本。

  title.subtextStyle. rich
Object

在 rich 里面，可以自定义富文本样式。利用富文本样式，可以在标签中做出非常丰富的效果。

例如：

label: {
    // 在文本中，可以对部分文本采用 rich 中定义样式。
    // 这里需要在文本中使用标记符号：
    // `{styleName|text content text content}` 标记样式名。
    // 注意，换行仍是使用 '\n'。
    formatter: [
        '{a|这段文本采用样式a}',
        '{b|这段文本采用样式b}这段用默认样式{x|这段用样式x}'
    ].join('\n'),

    rich: {
        a: {
            color: 'red',
            lineHeight: 10
        },
        b: {
            backgroundColor: {
                image: 'xxx/xxx.jpg'
            },
            height: 40
        },
        x: {
            fontSize: 18,
            fontFamily: 'Microsoft YaHei',
            borderColor: '#449933',
            borderRadius: 4
        },
        ...
    }
}


详情参见教程：富文本标签

所有属性
{ <style_name> }
 title.subtextStyle. richInheritPlainLabel = true
boolean
从 v6.0.0 开始支持

富文本样式是否继承普通文本样式。

此配置项用于向历史兼容。

从 v6 版本开始，富文本标签 (label.rich / textStyle.rich) 部分样式（fontStyle, fontWeight, fontSize, fontFamily, textShadowColor, textShadowBlur, textShadowOffsetX, textShadowOffsetY）默认继承 普通文本样式 (label / textStyle)。你可以设置 richInheritPlainLabel: false （可在最外层配置项或与同级文本样式配置项）来禁用此行为。

option = {
    richInheritPlainLabel: false, // In most cases, this is enough.
    xxx1: {
        // Can also set it here to only control this label.
        label: {
            richInheritPlainLabel: false,
            rich: {/* ... */},
        }
    },
    xxx2: {
        textStyle: {
            richInheritPlainLabel: false,
            rich: {/* ... */},
        }
    }
}

title. textAlign = 'auto'
 试一试
string

整体（包括 text 和 subtext）的水平对齐。

可选值：'auto'、'left'、'right'、'center'。

title. textVerticalAlign = 'auto'
 试一试
string

整体（包括 text 和 subtext）的垂直对齐。

可选值：'auto'、'top'、'bottom'、'middle'。

title. triggerEvent = false
 试一试
boolean

鼠标和触摸事件是否发送给开发者注册的监听器（chart.on('xxx', function (event) {})）。

支持的鼠标和触摸事件为 'click'、'dblclick'、'mouseover'、'mouseout'、'mousemove'、'mousedown'、'mouseup'、'globalout'、'contextmenu'。注意，鼠标和触摸事件都统一使用名字 'mouse{xxx}'。

可取值：

true: 允许对外发送事件。但是它也需要 silent 配置项为 false 才能真正发送事件。
false: 禁止对外发送事件，哪怕 silent 配置项为 false。

事件对象的内容为：

{
    componentType: 'title';
    // title 组件的 index（基于 echarts option）。
    componentIndex: number;
}

title. padding = 5
 试一试
numberArray

标题内边距，单位px，默认各方向内边距为5，接受数组分别设定上右下左边距。

使用示例：

// 设置内边距为 5
padding: 5
// 设置上下的内边距为 5，左右的内边距为 10
padding: [5, 10]
// 分别设置四个方向的内边距
padding: [
    5,  // 上
    10, // 右
    5,  // 下
    10, // 左
]

title. itemGap = 10
 试一试
number

主副标题之间的间距。

title. zlevel = 0
number

所有图形的 zlevel 值。

zlevel用于 Canvas 分层，不同zlevel值的图形会放置在不同的 Canvas 中，Canvas 分层是一种常见的优化手段。我们可以把一些图形变化频繁（例如有动画）的组件设置成一个单独的zlevel。需要注意的是过多的 Canvas 会引起内存开销的增大，在手机端上需要谨慎使用以防崩溃。

zlevel 大的 Canvas 会放在 zlevel 小的 Canvas 的上面。

title. z = 2
number

组件的所有图形的z值。控制图形的前后顺序。z值小的图形会被z值大的图形覆盖。

z相比zlevel优先级更低，而且不会创建新的 Canvas。

title. left = 'auto'
 试一试
stringnumber

标题（title）组件离容器左侧的距离。

left 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器宽度的百分比，也可以是 'left', 'center', 'right'。

如果 left 的值为 'left', 'center', 'right'，组件会根据相应的位置自动对齐。

title. top = 'auto'
 试一试
stringnumber

标题（title）组件离容器上侧的距离。

top 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高度的百分比，也可以是 'top', 'middle', 'bottom'。

如果 top 的值为 'top', 'middle', 'bottom'，组件会根据相应的位置自动对齐。

title. right = 'auto'
 试一试
stringnumber

标题（title）组件离容器右侧的距离。

right 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器宽度的百分比。

默认自适应。

title. bottom = 'auto'
 试一试
stringnumber

标题（title）组件离容器下侧的距离。

bottom 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高度的百分比。

默认自适应。

title. coordinateSystem = 'none'
string
从 v6.0.0 开始支持

指定另一个坐标系组件，本 title 布局在那个坐标系中。

可选值：

null、undefined 或者 'none'

不布局在任何坐标系中。自己独立完成布局。

'calendar'

布局在一个 日历坐标系 中。当一个 ECharts 实例中存在多个日历坐标系时，须通过 calendarIndex 或 calendarId 指定所使用的日历坐标系。

'matrix'

布局在一个 矩阵坐标系中。当一个 ECharts 实例中存在多个矩阵坐标系时，须通过 matrixIndex 或 matrixId 指定所使用的矩阵坐标系。

下表总结了“某系列或组件是否支持布局在某坐标系上”：

最左列列出了要布局的系列和组件（坐标系本身也是组件），最上行列出了所基于的坐标系。

	no coord sys	grid (cartesian2d)	polar	geo	singleAxis	radar	parallel	calendar	matrix
grid (cartesian2d)	✅	❌	❌	❌	❌	❌	❌	✅	✅
polar	✅	❌	❌	❌	❌	❌	❌	✅	✅
geo	✅	❌	❌	❌	❌	❌	❌	✅	✅
singleAxis	✅	❌	❌	❌	❌	❌	❌	✅	✅
calendar	✅	❌	❌	❌	❌	❌	❌	✅	✅
matrix	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-line	❌	✅	✅	❌	❌	❌	❌	❌ (✅ 如果通过其他坐标系，如 grid)	❌ (✅ 如果通过其他坐标系，如 grid)
series-bar	❌	✅	✅	❌	❌	❌	❌	❌ (✅ 如果通过其他坐标系，如 grid)	❌ (✅ 如果通过其他坐标系，如 grid)
series-pie	✅	✅	✅	✅	✅	❌	❌	✅	✅
series-scatter	❌	✅	✅	✅	✅	❌	❌	✅	✅
series-effectScatter	❌	✅	✅	✅	✅	❌	❌	✅	✅
series-radar	❌	❌	❌	❌	❌	✅	❌	❌ (✅ 如果通过 radar 坐标系)	❌ (✅ 如果通过 radar 坐标系)
series-tree	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-treemap	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-sunburst	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-boxplot	❌	✅	❌	❌	❌	❌	❌	❌ (✅ 如果通过其他坐标系，如 grid)	❌ (✅ 如果通过其他坐标系，如 grid)
series-candlestick	❌	✅	❌	❌	❌	❌	❌	❌ (✅ 如果通过其他坐标系，如 grid)	❌ (✅ 如果通过其他坐标系，如 grid)
series-heatmap	❌	✅	❌	✅	❌	❌	❌	✅	✅
series-map	✅ (create a geo coord sys exclusively)	❌	❌	✅	❌	❌	❌	✅	✅
series-parallel	❌	❌	❌	❌	❌	❌	✅	❌ (✅ 如果通过 parallel 坐标系)	❌ (✅ 如果通过 parallel 坐标系)
series-lines	❌	✅	✅	✅	✅	❌	❌	❌ (✅ 如果通过其他坐标系，如 geo)	❌ (✅ 如果通过其他坐标系，如 geo)
series-graph	✅ (create a "view" coord sys exclusively)	✅	✅	✅	❌	❌	❌	✅	✅
series-sankey	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-funnel	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-gauge	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-pictorialBar	❌	✅	✅	❌	❌	❌	❌	❌ (✅ 如果通过其他坐标系，如 grid)	❌ (✅ 如果通过其他坐标系，如 grid)
series-themeRiver	❌	❌	❌	❌	✅	❌	❌	❌ (✅ 如果通过其他坐标系，如 singleAxis)	❌ (✅ 如果通过其他坐标系，如 singleAxis)
series-chord	✅	✅	✅	✅	✅	❌	❌	✅	✅
title	✅	❌	❌	❌	❌	❌	❌	✅	✅
legend	✅	❌	❌	❌	❌	❌	❌	✅	✅
dataZoom	✅	❌	❌	❌	❌	❌	❌	✅	✅
visualMap	✅	❌	❌	❌	❌	❌	❌	✅	✅
toolbox	✅	❌	❌	❌	❌	❌	❌	✅	✅
timeline	✅	❌	❌	❌	❌	❌	❌	✅	✅
thumbnail	✅	❌	❌	❌	❌	❌	❌	✅	✅

也参见 title.coordinateSystemUsage。

title. coordinateSystemUsage = 'box'
string
从 v6.0.0 开始支持

如何在指定的 坐标系 上布局本 title。

在大多数情况下，无需显式指定 coordinateSystemUsage，除非默认行为不符合预期。

可选值：

'data'：（不适用于 title）

此系列的每个数据项（例如，每个 series.data[i]）将独立地在指定的坐标系进行布局。 注：当前没有任何“非系列组件”支持 coordinateSystemUsage: 'data'。

'box'：

此系列或组件作为一个整体，在指定的坐标系中进行布局——即根据坐标系计算整体的包围盒或基础锚点。

例如，grid 组件 可以布局在 matrix 坐标系 或 calendar 坐标系 中，这时其布局矩形是由 title.coords 在坐标系中计算出来的。参见示例：矩阵中的微型折线图。
又如，饼图系列 或 和弦图系列 可以布局在 geo 坐标系 或 cartesian2d 坐标系 中，这时其中心点是由 series-pie.coords 或 series-pie.center 在坐标系中计算出来的。参见示例：地理坐标系中的饼图。

另参考：title.coordinateSystem。

title. coord
Arraynumberstring
从 v6.0.0 开始支持

当 coordinateSystemUsage 为 'box' 时, coord 被输入给坐标系，计算得到布局位置（布局盒或者中心点）。

例子：矩阵中的微型折线图, 矩阵中的关系图.

注：当 coordinateSystemUsage 为 'data' 时，输入给坐标系的是 series.data[i] 而非此 coord。

coord 的具体格式定义，取决于每个坐标系，并且，和 chart.convertToPixel 的第二个参数相同。

title. calendarIndex = 0
number
从 v6.0.0 开始支持

布局时所基于的 日历坐标系 的 index。当一个 ECharts 实例中存在多个日历坐标系时，用其指定所使用的坐标系。

title. calendarId = undefined
number
从 v6.0.0 开始支持

布局时所基于的 日历坐标系 的 id。当一个 ECharts 实例中存在多个日历坐标系时，用其指定所使用的坐标系。

title. matrixIndex = 0
number
从 v6.0.0 开始支持

布局时所基于的 矩阵坐标系 的 index。当一个 ECharts 实例中存在多个矩阵坐标系时，用其指定所使用的坐标系。

title. matrixId = undefined
number
从 v6.0.0 开始支持

布局时所基于的 矩阵坐标系 的 id。当一个 ECharts 实例中存在多个矩阵坐标系时，用其指定所使用的坐标系。

title. backgroundColor = 'transparent'
 试一试
Color

标题背景色，默认透明。

颜色可以使用 RGB 表示，比如 'rgb(128, 128, 128)' ，如果想要加上 alpha 通道，可以使用 RGBA，比如 'rgba(128, 128, 128, 0.5)'，也可以使用十六进制格式，比如 '#ccc'

title. borderColor = '#ccc'
 试一试
Color

标题的边框颜色。支持的颜色格式同 backgroundColor。

title. borderWidth = 0
 试一试
number

标题的边框线宽。

title. borderRadius = 0
 试一试
numberArray

圆角半径，单位px，支持传入数组分别指定 4 个圆角半径。 如:

borderRadius: 5, // 统一设置四个角的圆角大小
borderRadius: [5, 5, 0, 0] //（顺时针左上，右上，右下，左下）

title. shadowBlur
 试一试
number

图形阴影的模糊大小。该属性配合 shadowColor,shadowOffsetX, shadowOffsetY 一起设置图形的阴影效果。

示例：

{
    shadowColor: 'rgba(0, 0, 0, 0.5)',
    shadowBlur: 10
}


注意：此配置项生效的前提是，设置了 show: true 以及值不为 transparent 的背景色 backgroundColor。

title. shadowColor
 试一试
Color

阴影颜色。支持的格式同color。

注意：此配置项生效的前提是，设置了 show: true。

title. shadowOffsetX = 0
 试一试
number

阴影水平方向上的偏移距离。

注意：此配置项生效的前提是，设置了 show: true。

title. shadowOffsetY = 0
 试一试
number

阴影垂直方向上的偏移距离。

注意：此配置项生效的前提是，设置了 show: true。

 预览