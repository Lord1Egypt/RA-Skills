Option API GL Tutorial
setOption({
Collapse All
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
backgroundColor ... ,
textStyle: {...} ,
animation: true ,
animationThreshold: 2000 ,
animationDuration: 1000 ,
animationEasing: 'cubicOut' ,
animationDelay: 0 ,
animationDurationUpdate: 300 ,
animationEasingUpdate: 'cubicOut' ,
animationDelayUpdate: 0 ,
stateAnimation: {...} ,
blendMode: 'source-over' ,
hoverLayerThreshold: 3000 ,
useUTC: false ,
richInheritPlainLabel: true ,
options ... ,
media: [{...}] ,
title

Title component, including main title and subtitle.

In ECharts 2.x, a single instance of ECharts could contains one title component at most. However, in ECharts 3, there could be one or more than one title components. It is more useful when multiple diagrams in one instance all need titles.

Here are some instances of different animation easing functions, among which every instance has a title component:

Properties
title. id
string

Component ID, not specified by default. If specified, it can be used to refer the component in option or API.

title. show = true
 Try It
boolean

Set this to false to prevent the title from showing

title. text = ''
 Try It
string

The main title text, supporting for \n for newlines.

[WARNING]: When enabling toolbox.feature.saveAsImage, and toolbox.feature.saveAsImage.name is not provided, it has historically been using title[0].text instead. This usage is not recommended -- toolbox.feature.saveAsImage.name should always be specified explicitly; otherwise, correctness and security risks for a filename have to be considered in this title.text option. See document "Security Guidelines" for recommendations on safe usage.
title. link = ''
string

The hyper link of main title text.

[WARNING]: This URL string is accepted directly without any internal sanitization. Security risks must be considered if it comes from untrusted sources. See document "Security Guidelines" for recommendations on safe usage.
title. target = 'blank'
string

Open the hyper link of main title in specified tab.

options:

'self' opening it in current tab

'blank' opening it in a new tab

 title. textStyle
Object
 title.textStyle. color = '#333'
 Try It
Color

main title text color.

 title.textStyle. fontStyle = 'normal'
 Try It
string

main title font style.

Options are:

'normal'
'italic'
'oblique'
 title.textStyle. fontWeight = 'bolder'
 Try It
stringnumber

main title font thick weight.

Options are:

'normal'
'bold'
'bolder'
'lighter'
100 | 200 | 300 | 400...
 title.textStyle. fontFamily = 'sans-serif'
 Try It
string

main title font family.

Can also be 'serif' , 'monospace', ...

 title.textStyle. fontSize = 18
 Try It
number

main title font size.

 title.textStyle. lineHeight
 Try It
number

Line height of the text fragment.

If lineHeight is not set in rich, lineHeight in parent level will be used. For example:

{
    lineHeight: 56,
    rich: {
        a: {
            // `lineHeight` is not set, then it will be 56
        }
    }
}

 title.textStyle. width
 Try It
number

Width of text block.

 title.textStyle. height
 Try It
number

Height of text block.

 title.textStyle. textBorderColor
 Try It
Color

Stroke color of the text.

 title.textStyle. textBorderWidth
 Try It
number

Stroke line width of the text.

 title.textStyle. textBorderType = 'solid'
 Try It
stringnumberArray

Stroke line type of the text.

Possible values are:

'solid'
'dashed'
'dotted'

Since v5.0.0, it can also be a number or a number array to specify the dash array of the line. With textBorderDashOffset , we can make the line style more flexible.

For example：

{

textBorderType: [5, 10],

textBorderDashOffset: 5
}

 title.textStyle. textBorderDashOffset = 0
 Try It
number
Since v5.0.0

To set the line dash offset. With textBorderType , we can make the line style more flexible.

Refer to MDN lineDashOffset for more details.

 title.textStyle. textShadowColor = 'transparent'
 Try It
Color

Shadow color of the text itself.

 title.textStyle. textShadowBlur = 0
 Try It
number

Shadow blue of the text itself.

 title.textStyle. textShadowOffsetX = 0
 Try It
number

Shadow X offset of the text itself.

 title.textStyle. textShadowOffsetY = 0
 Try It
number

Shadow Y offset of the text itself.

 title.textStyle. overflow = 'none'
 Try It
string

Determine how to display the text when it's overflow. Available when width is set.

'truncate' Truncate the text and trailing with ellipsis.
'break' Break by word
'breakAll' Break by character.
 title.textStyle. ellipsis = '...'
string

Ellipsis to be displayed when overflow is set to truncate.

'truncate' Truncate the overflow lines.
  title.textStyle. rich
Object

"Rich text styles" can be defined in this rich property. For example:

label: {
    // Styles defined in 'rich' can be applied to some fragments
    // of text by adding some markers to those fragment, like
    // `{styleName|text content text content}`.
    // `'\n'` is the newline character.
    formatter: [
        '{a|Style "a" is applied to this snippet}'
        '{b|Style "b" is applied to this snippet}This snippet use default style{x|use style "x"}'
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


For more details, see Rich Text please.

Properties
{ <style_name> }
 title.textStyle. richInheritPlainLabel = true
boolean
Since v6.0.0

Whether rich text inherits plain text style.

This option is just for backward compatibility.

The label.rich / textStyle.rich fontStyle, fontWeight, fontSize, fontFamily, textShadowColor, textShadowBlur, textShadowOffsetX, textShadowOffsetY are changed to inherit the corresponding plain label styles since echarts v6. You can use richInheritPlainLabel: false to restore it. For example,

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
 Try It
string

Subtitle text, supporting for \n for newlines.

title. sublink = ''
string

The hyper link of subtitle text.

[WARNING]: This URL string is accepted directly without any internal sanitization. Security risks must be considered if it comes from untrusted sources. See document "Security Guidelines" for recommendations on safe usage.
title. subtarget = 'blank'
string

Open the hyper link of subtitle in specified tab, options:

'self' opening it in current tab

'blank' opening it in a new tab

 title. subtextStyle
Object
 title.subtextStyle. color = '#aaa'
 Try It
Color

subtitle text color.

 title.subtextStyle. fontStyle = 'normal'
 Try It
string

subtitle font style.

Options are:

'normal'
'italic'
'oblique'
 title.subtextStyle. fontWeight = 'normal'
 Try It
stringnumber

subtitle font thick weight.

Options are:

'normal'
'bold'
'bolder'
'lighter'
100 | 200 | 300 | 400...
 title.subtextStyle. fontFamily = 'sans-serif'
 Try It
string

subtitle font family.

Can also be 'serif' , 'monospace', ...

 title.subtextStyle. fontSize = 12
 Try It
number

subtitle font size.

 title.subtextStyle. align
 Try It
string

Horizontal alignment of text, automatic by default.

Options are:

'left'
'center'
'right'

If align is not set in rich, align in parent level will be used. For example:

{
    align: right,
    rich: {
        a: {
            // `align` is not set, then it will be right
        }
    }
}

 title.subtextStyle. verticalAlign
 Try It
string

Vertical alignment of text, automatic by default.

Options are:

'top'
'middle'
'bottom'

If verticalAlign is not set in rich, verticalAlign in parent level will be used. For example:

{
    verticalAlign: bottom,
    rich: {
        a: {
            // `verticalAlign` is not set, then it will be bottom
        }
    }
}

 title.subtextStyle. lineHeight
 Try It
number

Line height of the text fragment.

If lineHeight is not set in rich, lineHeight in parent level will be used. For example:

{
    lineHeight: 56,
    rich: {
        a: {
            // `lineHeight` is not set, then it will be 56
        }
    }
}

 title.subtextStyle. width
 Try It
number

Width of text block.

 title.subtextStyle. height
 Try It
number

Height of text block.

 title.subtextStyle. textBorderColor
 Try It
Color

Stroke color of the text.

 title.subtextStyle. textBorderWidth
 Try It
number

Stroke line width of the text.

 title.subtextStyle. textBorderType = 'solid'
 Try It
stringnumberArray

Stroke line type of the text.

Possible values are:

'solid'
'dashed'
'dotted'

Since v5.0.0, it can also be a number or a number array to specify the dash array of the line. With textBorderDashOffset , we can make the line style more flexible.

For example：

{

textBorderType: [5, 10],

textBorderDashOffset: 5
}

 title.subtextStyle. textBorderDashOffset = 0
 Try It
number
Since v5.0.0

To set the line dash offset. With textBorderType , we can make the line style more flexible.

Refer to MDN lineDashOffset for more details.

 title.subtextStyle. textShadowColor = 'transparent'
 Try It
Color

Shadow color of the text itself.

 title.subtextStyle. textShadowBlur = 0
 Try It
number

Shadow blue of the text itself.

 title.subtextStyle. textShadowOffsetX = 0
 Try It
number

Shadow X offset of the text itself.

 title.subtextStyle. textShadowOffsetY = 0
 Try It
number

Shadow Y offset of the text itself.

 title.subtextStyle. overflow = 'none'
 Try It
string

Determine how to display the text when it's overflow. Available when width is set.

'truncate' Truncate the text and trailing with ellipsis.
'break' Break by word
'breakAll' Break by character.
 title.subtextStyle. ellipsis = '...'
string

Ellipsis to be displayed when overflow is set to truncate.

'truncate' Truncate the overflow lines.
  title.subtextStyle. rich
Object

"Rich text styles" can be defined in this rich property. For example:

label: {
    // Styles defined in 'rich' can be applied to some fragments
    // of text by adding some markers to those fragment, like
    // `{styleName|text content text content}`.
    // `'\n'` is the newline character.
    formatter: [
        '{a|Style "a" is applied to this snippet}'
        '{b|Style "b" is applied to this snippet}This snippet use default style{x|use style "x"}'
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


For more details, see Rich Text please.

Properties
{ <style_name> }
 title.subtextStyle. richInheritPlainLabel = true
boolean
Since v6.0.0

Whether rich text inherits plain text style.

This option is just for backward compatibility.

The label.rich / textStyle.rich fontStyle, fontWeight, fontSize, fontFamily, textShadowColor, textShadowBlur, textShadowOffsetX, textShadowOffsetY are changed to inherit the corresponding plain label styles since echarts v6. You can use richInheritPlainLabel: false to restore it. For example,

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
 Try It
string

The horizontal align of the component (including "text" and "subtext").

Optional values: 'auto', 'left', 'right', 'center'.

title. textVerticalAlign = 'auto'
 Try It
string

The vertical align of the component (including "text" and "subtext").

Optional values: 'auto', 'top', 'bottom', 'middle'.

title. triggerEvent = false
 Try It
boolean

Whether to enable to dispatch mouse/touch events to user-registered listeners (i.e., chart.on('xxx', function (event) {})).

Supported mouse/touch events are 'click', 'dblclick', 'mouseover', 'mouseout', 'mousemove', 'mousedown', 'mouseup', 'globalout', 'contextmenu'. Note, both mouse and touch events are unified to the event type 'mouse{xxx}'.

Values:

true: Enable to trigger events. But dispatching also requires option silent to be falsy.
false: Disable to trigger mouse/touch events, even if option silent is falsy.

The parameters of the event:

{
    componentType: 'title';
    // The index of the title component (base on echarts option)
    componentIndex: number;
}

title. padding = 5
 Try It
numberArray

title space around content. The unit is px. Default values for each position are 5. And they can be set to different values with left, right, top, and bottom.

Examples:

// Set padding to be 5
padding: 5
// Set the top and bottom paddings to be 5, and left and right paddings to be 10
padding: [5, 10]
// Set each of the four paddings separately
padding: [
    5,  // up
    10, // right
    5,  // down
    10, // left
]

title. itemGap = 10
 Try It
number

The gap between the main title and subtitle.

title. zlevel = 0
number

zlevel value of all graphical elements in .

zlevel is used to make layers with Canvas. Graphical elements with different zlevel values will be placed in different Canvases, which is a common optimization technique. We can put those frequently changed elements (like those with animations) to a separate zlevel. Notice that too many Canvases will increase memory cost, and should be used carefully on mobile phones to avoid crash.

Canvases with bigger zlevel will be placed on Canvases with smaller zlevel.

title. z = 2
number

z value of all graphical elements in , which controls order of drawing graphical components. Components with smaller z values may be overwritten by those with larger z values.

z has a lower priority to zlevel, and will not create new Canvas.

title. left = 'auto'
 Try It
stringnumber

Distance between title component and the left side of the container.

left can be a pixel value like 20; it can also be a percentage value relative to the container width like '20%'; and it can also be 'left', 'center', or 'right'.

If the left value is set to be 'left', 'center', or 'right', then the component will be aligned automatically based on position.

title. top = 'auto'
 Try It
stringnumber

Distance between title component and the top side of the container.

top can be a pixel value like 20; it can also be a percentage value relative to the container height like '20%'; and it can also be 'top', 'middle', or 'bottom'.

If the top value is set to be 'top', 'middle', or 'bottom', then the component will be aligned automatically based on position.

title. right = 'auto'
 Try It
stringnumber

Distance between title component and the right side of the container.

right can be a pixel value like 20; it can also be a percentage value relative to the container width like '20%'.

Adaptive by default.

title. bottom = 'auto'
 Try It
stringnumber

Distance between title component and the bottom side of the container.

bottom can be a pixel value like 20; it can also be a percentage value relative to the container height like '20%'.

Adaptive by default.

title. coordinateSystem = 'none'
string
Since v6.0.0

Specifies another coordinate system component on which this title is laid out.

Options:

null/undefined/'none'

Not laid out in any coordinate system; instead, laid out independently.

'calendar'

Lay out based on a calendar coordinate system. When multiple calendar coordinate systems exist within an ECharts instance, the corresponding system should be specified using calendarIndex or calendarId.

'matrix'

Lay out based on a matrix coordinate system. When multiple matrix coordinate systems exist within an ECharts instance, the corresponding system should be specified using matrixIndex or matrixId.

Support for series and component layout on coordinate systems:

The leftmost column lists the series and components that will be laid out (coordinate systems themselves are also components), and the topmost row lists the coordinate systems that can be laid out on.

	no coord sys	grid (cartesian2d)	polar	geo	singleAxis	radar	parallel	calendar	matrix
grid (cartesian2d)	✅	❌	❌	❌	❌	❌	❌	✅	✅
polar	✅	❌	❌	❌	❌	❌	❌	✅	✅
geo	✅	❌	❌	❌	❌	❌	❌	✅	✅
singleAxis	✅	❌	❌	❌	❌	❌	❌	✅	✅
calendar	✅	❌	❌	❌	❌	❌	❌	❌	❌
matrix	✅	❌	❌	❌	❌	❌	❌	❌	❌
series-line	❌	✅	✅	❌	❌	❌	❌	❌ (✅ if via another coord sys like grid)	❌ (✅ if via another coord sys like grid)
series-bar	❌	✅	✅	❌	❌	❌	❌	❌ (✅ if via another coord sys like grid)	❌ (✅ if via another coord sys like grid)
series-pie	✅	✅	✅	✅	✅	❌	❌	✅	✅
series-scatter	❌	✅	✅	✅	✅	❌	❌	✅	✅
series-effectScatter	❌	✅	✅	✅	✅	❌	❌	✅	✅
series-radar	❌	❌	❌	❌	❌	✅	❌	❌ (✅ if via radar coord sys)	❌ (✅ if via radar coord sys)
series-tree	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-treemap	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-sunburst	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-boxplot	❌	✅	❌	❌	❌	❌	❌	❌ (✅ if via another coord sys like grid)	❌ (✅ if via another coord sys like grid)
series-candlestick	❌	✅	❌	❌	❌	❌	❌	❌ (✅ if via another coord sys like grid)	❌ (✅ if via another coord sys like grid)
series-heatmap	❌	✅	❌	✅	❌	❌	❌	✅	✅
series-map	✅ (create a geo coord sys exclusively)	❌	❌	✅	❌	❌	❌	✅	✅
series-parallel	❌	❌	❌	❌	❌	❌	✅	❌ (✅ if via parallel coord sys)	❌ (✅ if via parallel coord sys)
series-lines	❌	✅	✅	✅	✅	❌	❌	❌ (✅ if via another coord sys like geo)	❌ (✅ if via another coord sys like geo)
series-graph	✅ (create a "view" coord sys exclusively)	✅	✅	✅	❌	❌	❌	✅	✅
series-sankey	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-funnel	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-gauge	✅	❌	❌	❌	❌	❌	❌	✅	✅
series-pictorialBar	❌	✅	✅	❌	❌	❌	❌	❌ (✅ if via another coord sys like grid)	❌ (✅ if via another coord sys like grid)
series-themeRiver	❌	❌	❌	❌	✅	❌	❌	❌ (✅ if via another coord sys like singleAxis)	❌ (✅ if via another coord sys like singleAxis)
series-chord	✅	✅	✅	✅	✅	❌	❌	✅	✅
title	✅	❌	❌	❌	❌	❌	❌	✅	✅
legend	✅	❌	❌	❌	❌	❌	❌	✅	✅
dataZoom	✅	❌	❌	❌	❌	❌	❌	✅	✅
visualMap	✅	❌	❌	❌	❌	❌	❌	✅	✅
toolbox	✅	❌	❌	❌	❌	❌	❌	✅	✅
timeline	✅	❌	❌	❌	❌	❌	❌	✅	✅
thumbnail	✅	❌	❌	❌	❌	❌	❌	✅	✅

See also title.coordinateSystemUsage.

title. coordinateSystemUsage = 'box'
string
Since v6.0.0

Specify how to lay out this title based on the specified coordinateSystem.

In most cases, there is no need to specify coordinateSystemUsage, unless the default behavior is unexpected.

Options:

'data': (Not applicable in title)

Each data item of a series (e.g., each series.data[i]) is laid out separately based on the specified coordinate system. Currently no non-series component supports coordinateSystemUsage: 'data'.

'box':

The entire series or component is laid out as a whole based on the specified coordinate system - that is, the overall bounding rect or basic anchor point is calculated relative to the system.

For example, a grid component can be laid out in a matrix coordinate system or a calendar coordinate system, where its layout rectangle is calculated by the specified title.coords in that system. See example sparkline in matrix.
For example, a pie series or a chord series can be laid out in a geo coordinate system or a cartesian2d coordinate system, where the center is calculated by the specified series-pie.coords or series-pie.center in that system. See example pie in geo.

See also title.coordinateSystem.

title. coord
Arraynumberstring
Since v6.0.0

When coordinateSystemUsage is 'box', coord is used as the input to the coordinate system and calculate the layout rectangle or anchor point.

Examples: sparkline in matrix, grpah in matrix.

Note: when coordinateSystemUsage is 'data', the input of coordinate system is series.data[i] rather than this coord.

The format this coord is defined by each coordinate system, and it's the same as the second parameter of chart.convertToPixel.

title. calendarIndex = 0
number
Since v6.0.0

The index of the calendar coordinate system to base on. When mutiple calendar exist within an ECharts instance, use this to specify the corresponding calendar.

title. calendarId = undefined
number
Since v6.0.0

The id of the calendar coordinate system to base on. When mutiple calendar exist within an ECharts instance, use this to specify the corresponding calendar.

title. matrixIndex = 0
number
Since v6.0.0

The index of the matrix coordinate system to base on. When mutiple matrix exist within an ECharts instance, use this to specify the corresponding matrix.

title. matrixId = undefined
number
Since v6.0.0

The id of the matrix coordinate system to base on. When mutiple matrix exist within an ECharts instance, use this to specify the corresponding matrix.

title. backgroundColor = 'transparent'
 Try It
Color

Background color of title, which is transparent by default.

Color can be represented in RGB, for example 'rgb(128, 128, 128)'. RGBA can be used when you need alpha channel, for example 'rgba(128, 128, 128, 0.5)'. You may also use hexadecimal format, for example '#ccc'.

title. borderColor = '#ccc'
 Try It
Color

Border color of title. Support the same color format as backgroundColor.

title. borderWidth = 1
 Try It
number

Border width of title.

title. borderRadius = 0
 Try It
numberArray

The radius of rounded corner. Its unit is px. And it supports use array to respectively specify the 4 corner radiuses.

For example:

borderRadius: 5, // consistently set the size of 4 rounded corners
borderRadius: [5, 5, 0, 0] // (clockwise upper left, upper right, bottom right and bottom left)

title. shadowBlur
 Try It
number

Size of shadow blur. This attribute should be used along with shadowColor,shadowOffsetX, shadowOffsetY to set shadow to component.

For example:

{
    shadowColor: 'rgba(0, 0, 0, 0.5)',
    shadowBlur: 10
}


Attention: This property works only if show: true is configured and backgroundColor is defined other than transparent.

title. shadowColor
 Try It
Color

Shadow color. Support same format as color.

Attention: This property works only if show: true configured.

title. shadowOffsetX = 0
 Try It
number

Offset distance on the horizontal direction of shadow.

Attention: This property works only if show: true configured.

title. shadowOffsetY = 0
 Try It
number

Offset distance on the vertical direction of shadow.

Attention: This property works only if show: true configured.

 Preview