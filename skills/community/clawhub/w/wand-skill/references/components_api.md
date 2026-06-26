# Wand UI 组件 API 参考

本文档详细介绍 Wand UI 所有可用组件的 API、属性、事件和插槽。

## 表单组件

### Button 按钮

**引入方式**
```js
import { WandButton } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|-|-|-|-|-|
| size | 按钮大小 | String | normal | normal, small, large, biggest |
| type | 按钮类型 | String | primary | normal, primary, default, warn, error |
| transparent | 幽灵按钮 | Boolean | false | true, false |
| disabled | 是否禁用点击 | Boolean | false | true, false |
| customStyle | 自定义样式对象 | Object | - | - |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| click | 被点击且按钮状态不为禁用时调用 | - |
| disabled-click | 禁用时按钮点击事件 | - |

**Slots**
| 插槽名称 | 说明 |
|-|-|
| default | 按钮文本内容 |
| left-slot | 左侧图标插槽 |
| right-slot | 右侧图标插槽 |

**示例**
```html
<!-- 基础按钮 -->
<wand-button type="primary" size="large">确定</wand-button>

<!-- 幽灵按钮 -->
<wand-button type="primary" transparent>取消</wand-button>

<!-- 带图标的按钮 -->
<wand-button type="primary">
  <span slot="left-slot" class="we-iconfont we-icon-add"></span>
  提交
</wand-button>
```

### Input 输入框

**引入方式**
```js
import { WandInput } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 绑定值 | String/Number | - |
| type | 输入框类型 | String | text |
| placeholder | 占位文本 | String | - |
| disabled | 是否禁用 | Boolean | false |
| readonly | 是否只读 | Boolean | false |
| maxlength | 最大输入长度 | Number | - |
| clearable | 是否显示清空按钮 | Boolean | false |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| input | 输入值改变时触发 | value |
| focus | 获得焦点时触发 | event |
| blur | 失去焦点时触发 | event |
| clear | 点击清空按钮时触发 | - |

### Textarea 多行文本框

**引入方式**
```js
import { WandTextarea } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 绑定值 | String | - |
| placeholder | 占位文本 | String | - |
| disabled | 是否禁用 | Boolean | false |
| readonly | 是否只读 | Boolean | false |
| maxlength | 最大输入长度 | Number | - |
| rows | 显示行数 | Number | 2 |
| autosize | 是否自适应高度 | Boolean | false |

### Check 复选框

**引入方式**
```js
import { WandCheck } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 绑定值 | Boolean/Array | false |
| disabled | 是否禁用 | Boolean | false |
| label | 复选框对应的值 | String/Number/Boolean | - |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| change | 值变化时触发 | value |

### Switch 开关

**引入方式**
```js
import { WandSwitch } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 绑定值 | Boolean | false |
| disabled | 是否禁用 | Boolean | false |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| change | 值变化时触发 | value |

### Form 表单

**引入方式**
```js
import { WandForm, WandFormItem } from '@weiyi/wand-ui'
```

**Form Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| model | 表单数据对象 | Object | - |
| rules | 表单验证规则 | Object | - |

**FormItem Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| prop | 表单域 model 字段名 | String | - |
| label | 标签文本 | String | - |
| required | 是否必填 | Boolean | false |

**Form Methods**
| 方法名 | 说明 | 参数 |
|-|-|-|
| validate | 对整个表单进行校验 | callback(valid) |
| resetFields | 重置表单 | - |

## 选择器组件

### Picker 选择器

**引入方式**
```js
import { WandPicker } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| columns | 选择器数据 | Array | [] |
| value / v-model | 绑定值 | Array | [] |
| title | 顶部标题 | String | - |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| change | 值变化时触发 | value, index |
| confirm | 确认选择时触发 | value, index |
| cancel | 取消选择时触发 | - |

### PopupPicker 弹出式选择器

**引入方式**
```js
import { WandPopupPicker } from '@weiyi/wand-ui'
```

结合了 Popup 和 Picker 的功能，提供弹出式选择体验。

### Datetime 日期时间选择器

**引入方式**
```js
import { WandDatetime } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 绑定值 | Date/String | - |
| type | 类型 | String | datetime |
| minDate | 最小日期 | Date | 10年前 |
| maxDate | 最大日期 | Date | 10年后 |

### Cascade 级联选择器

**引入方式**
```js
import { WandCascade } from '@weiyi/wand-ui'
```

用于多级联动选择，如省市区选择。

## 反馈组件

### Toast 轻提示

**引入方式**
```js
import { WandToast } from '@weiyi/wand-ui'
// 或者通过 this.$toast 使用
```

**使用方式**
```js
// 文字提示
this.$toast('提示内容')

// 成功提示
this.$toast.success('操作成功')

// 失败提示
this.$toast.fail('操作失败')

// 加载中
this.$toast.loading('加载中...')
```

**Options**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| message | 提示内容 | String | - |
| duration | 显示时长(ms) | Number | 2000 |
| position | 位置 | String | middle |

### Loading 加载

**引入方式**
```js
import { WandLoading } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show | 是否显示 | Boolean | false |
| text | 加载文案 | String | - |

### Dialog 对话框

**引入方式**
```js
import { WandDialog } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show / v-model | 是否显示 | Boolean | false |
| title | 标题 | String | - |
| message | 内容 | String | - |
| showCancelButton | 是否显示取消按钮 | Boolean | true |
| confirmButtonText | 确认按钮文本 | String | 确定 |
| cancelButtonText | 取消按钮文本 | String | 取消 |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| confirm | 确认按钮点击时触发 | - |
| cancel | 取消按钮点击时触发 | - |

### Confirm 确认框

**引入方式**
```js
import { WandConfirm } from '@weiyi/wand-ui'
```

简化版的 Dialog，专门用于确认操作。

### Alert 警告框

**引入方式**
```js
import { WandAlert } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| type | 类型 | String | info |
| title | 标题 | String | - |
| closable | 是否可关闭 | Boolean | false |

### ActionSheet 动作面板

**引入方式**
```js
import { WandActionSheet } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show / v-model | 是否显示 | Boolean | false |
| actions | 动作列表 | Array | [] |
| cancelText | 取消按钮文本 | String | 取消 |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| select | 选择选项时触发 | action, index |
| cancel | 取消时触发 | - |

## 展示组件

### List 列表

**引入方式**
```js
import { WandList } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| finished | 是否加载完成 | Boolean | false |
| loading | 是否正在加载 | Boolean | false |
| finishedText | 加载完成文本 | String | 没有更多了 |
| loadingText | 加载中文本 | String | 加载中... |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| load | 滚动到底部时触发 | - |

### Swipe 轮播

**引入方式**
```js
import { WandSwipe, WandSwipeItem } from '@weiyi/wand-ui'
```

**Swipe Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| autoplay | 自动播放间隔(ms) | Number | 0 |
| duration | 动画时长(ms) | Number | 500 |
| initial | 初始位置索引 | Number | 0 |
| loop | 是否循环播放 | Boolean | true |
| showIndicators | 是否显示指示器 | Boolean | true |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| change | 切换时触发 | index |

### Collapse 折叠面板

**引入方式**
```js
import { WandCollapse, WandCollapseGroup } from '@weiyi/wand-ui'
```

**Collapse Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| name | 唯一标识符 | String/Number | - |
| title | 标题 | String | - |
| disabled | 是否禁用 | Boolean | false |

**CollapseGroup Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 当前展开项 | String/Number/Array | - |
| accordion | 是否手风琴模式 | Boolean | false |

### NoticeBar 通知栏

**引入方式**
```js
import { WandNoticeBar } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| text | 通知内容 | String | - |
| mode | 模式 | String | - |
| color | 文字颜色 | String | - |
| background | 背景颜色 | String | - |
| scrollable | 是否滚动 | Boolean | false |

## 导航组件

### Tab 标签页

**引入方式**
```js
import { WandTab, WandTabItem } from '@weiyi/wand-ui'
```

**Tab Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 当前激活标签 | String/Number | - |
| animated | 是否开启切换动画 | Boolean | false |

**TabItem Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| name | 标签名称 | String/Number | - |
| title | 标题 | String | - |
| disabled | 是否禁用 | Boolean | false |

### TabBar 底部导航栏

**引入方式**
```js
import { WandTabBar, WandTabBarItem } from '@weiyi/wand-ui'
```

**TabBar Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 当前激活项 | String/Number | - |
| fixed | 是否固定在底部 | Boolean | true |

**TabBarItem Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| name | 标签名称 | String/Number | - |
| icon | 图标 | String | - |
| dot | 是否显示小红点 | Boolean | false |
| badge | 徽标内容 | String/Number | - |

### NavBar 导航栏

**引入方式**
```js
import { WandNavBar } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| title | 标题 | String | - |
| leftText | 左侧文本 | String | - |
| rightText | 右侧文本 | String | - |
| leftArrow | 是否显示左侧箭头 | Boolean | false |
| fixed | 是否固定在顶部 | Boolean | false |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| click-left | 点击左侧按钮时触发 | - |
| click-right | 点击右侧按钮时触发 | - |

## 其他组件

### Popup 弹出层

**引入方式**
```js
import { WandPopup } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show / v-model | 是否显示 | Boolean | false |
| position | 弹出位置 | String | center |
| overlay | 是否显示遮罩 | Boolean | true |
| closeOnClickOverlay | 点击遮罩是否关闭 | Boolean | true |

### Popover 气泡弹出框

**引入方式**
```js
import { WandPopover } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show / v-model | 是否显示 | Boolean | false |
| actions | 选项列表 | Array | [] |
| placement | 弹出位置 | String | bottom |

### Search 搜索

**引入方式**
```js
import { WandSearch } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 当前输入值 | String | - |
| placeholder | 占位文本 | String | 请输入搜索关键词 |
| showAction | 是否显示右侧按钮 | Boolean | false |
| actionText | 右侧按钮文本 | String | 取消 |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| search | 确定搜索时触发 | value |
| cancel | 取消搜索时触发 | - |

### SwipeCell 滑动单元格

**引入方式**
```js
import { WandSwipeCell } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| disabled | 是否禁用滑动 | Boolean | false |

**Slots**
| 插槽名称 | 说明 |
|-|-|
| default | 内容 |
| left | 左侧滑动内容 |
| right | 右侧滑动内容 |

### Uploader 文件上传

**引入方式**
```js
import { WandUploader } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 已上传文件列表 | Array | [] |
| accept | 接受的文件类型 | String | image/* |
| multiple | 是否支持多选 | Boolean | false |
| maxCount | 最大上传数量 | Number | - |
| maxSize | 最大文件大小(byte) | Number | - |

**Events**
| 事件名称 | 说明 | 回调参数 |
|-|-|-|
| change | 文件列表变化时触发 | fileList |
| oversize | 文件超出大小限制时触发 | file |
| delete | 删除文件时触发 | file, index |

### PhotoViewer 图片预览

**引入方式**
```js
import { WandPhotoViewer } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| show / v-model | 是否显示 | Boolean | false |
| images | 图片列表 | Array | [] |
| startPosition | 初始索引 | Number | 0 |

### Rate 评分

**引入方式**
```js
import { WandRate } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| value / v-model | 当前分值 | Number | 0 |
| count | 图标总数 | Number | 5 |
| size | 图标大小 | String/Number | 20px |
| disabled | 是否禁用 | Boolean | false |
| allowHalf | 是否允许半选 | Boolean | false |

### Affix 固钉

**引入方式**
```js
import { WandAffix } from '@weiyi/wand-ui'
```

**Props**
| 参数 | 说明 | 类型 | 默认值 |
|-|-|-|-|
| offsetTop | 距离顶部多少距离开始固定 | Number | 0 |
| zIndex | 固定时的层级 | Number | 99 |
