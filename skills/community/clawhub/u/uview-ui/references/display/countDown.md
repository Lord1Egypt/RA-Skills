---
name: "countDown"
description: "CountDown 倒计时 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs CountDown 倒计时 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/countDown.html"
---

---

## [#](#countdown-倒计时) CountDown 倒计时 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般使用于某个活动的截止时间上，通过数字的变化，给用户明确的时间感受，提示用户进行某一个行为操作。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`time`参数设置倒计时间，单位为`ms`

```
<template>
	<u-count-down :time="30 * 60 * 60 * 1000" format="HH:mm:ss"></u-count-down>
</template>
```

### [#](#自定义格式) 自定义格式

-   说明：通过绑定`change`回调的值，进行自定义格式

```
<template>
    <u-count-down
        :time="30 * 60 * 60 * 1000"
        format="DD:HH:mm:ss"
        autoStart
        millisecond
        @change="onChange"
    >
        <view class="time">
            <text class="time__item">{{ timeData.days }}&nbsp;天</text>
            <text class="time__item">{{ timeData.hours>10?timeData.hours:'0'+timeData.hours}}&nbsp;时</text>
            <text class="time__item">{{ timeData.minutes }}&nbsp;分</text>
            <text class="time__item">{{ timeData.seconds }}&nbsp;秒</text>
        </view>
    </u-count-down>
</template>

<script>
    export default {
        data() {
            return {
                timeData: {},
            }
        },
        methods: {
            onChange(e) {
                this.timeData = e
            }
        }
    }
</script>

<style lang="scss">
.time {
    @include flex;
    align-items: center;

    &__item {
         color: #fff;
         font-size: 12px;
         text-align: center;
     }
}
</style>
```

### [#](#毫秒级渲染) 毫秒级渲染

-   通过配置`millisecond`来开启毫秒级倒计时

```
<u-count-down :time="30 * 60 * 60 * 1000" format="HH:mm:ss:SSS" autoStart millisecond></u-count-down>
```

### [#](#自定义样式) 自定义样式

-   说明：通过绑定`change`回调的值，进行自定义格式

```
<template>
    <u-count-down
            :time="30 * 60 * 60 * 1000"
            format="HH:mm:ss"
            autoStart
            millisecond
            @change="onChange"
    >
        <view class="time">
            <view class="time__custom">
                <text class="time__custom__item">{{ timeData.hours>10?timeData.hours:'0'+timeData.hours}}</text>
            </view>
            <text class="time__doc">:</text>
            <view class="time__custom">
                <text class="time__custom__item">{{ timeData.minutes }}</text>
            </view>
            <text class="time__doc">:</text>
            <view class="time__custom">
                <text class="time__custom__item">{{ timeData.seconds }}</text>
            </view>
        </view>
    </u-count-down>
</template>

<script>
    export default {
        data() {
            return {
                timeData: {},
            }
        },
        methods: {
            onChange(e) {
                this.timeData = e
            }
        }
    }
</script>

<style lang="scss">
.time {
    @include flex;
    align-items: center;

    &__custom {
         margin-top: 4px;
         width: 22px;
         height: 22px;
         background-color: $u-primary;
         border-radius: 4px;

         display: flex;

         justify-content: center;
         align-items: center;

        &__item {
             color: #fff;
             font-size: 12px;
             text-align: center;
         }
    }

    &__doc {
         color: $u-primary;
         padding: 0px 4px;
     }

    &__item {
         color: #606266;
         font-size: 15px;
         margin-right: 4px;
     }
}
</style>
```

### [#](#手动控制) 手动控制

-   说明：通过绑定`ref`进行手动控制重置、开始、暂停

```
<template>
    <u-count-down
        ref="countDown"
        :time="3* 1000"
        format="ss:SSS"
        :autoStart="false"
        millisecond
        @change="onChange"
    >
    </u-count-down>
    <u-button text="重置" size="normal" type="info" @click="reset"></u-button>
    <u-button text="开始" size="normal" type="success" @click="start"></u-button>
    <u-button text="暂停" size="normal" type="error" @click="pause"></u-button>
</template>

<script>
    export default {
        data() {
            return {
                timeData: {},
            }
        },
        methods: {

            start() {
                this.$refs.countDown.start();
            },

            pause() {
                this.$refs.countDown.pause();
            },

            reset() {
                this.$refs.countDown.reset();
            },
            onChange(e) {
                this.timeData = e
            }
        }
    }
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/countDown/countDown.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/countDown/countDown.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| time | 倒计时时长，单位ms | String | Number | 0 | \- |
| format | 时间格式，DD-日，HH-时，mm-分，ss-秒，SSS-毫秒 | String | HH:mm:ss | \- |
| autoStart | 是否自动开始倒计时 | Boolean | true | false |
| millisecond | 是否展示毫秒倒计时 | Boolean | false | true |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 过程中，倒计时变化时触发 | time: 剩余的时间 |
| finish | 倒计时结束 | \- |

### [#](#methods) Methods

需要通过ref获取倒计时组件才能调用

| 名称 | 说明 |
| --- | --- |
| start | 开始倒计时 |
| pause | 暂停倒计时 |
| reset | 重置倒计时 |

← [LineProgress 线形进度条](https://www.uviewui.com/components/lineProgress.html) [CountTo 数字滚动](https://www.uviewui.com/components/countTo.html) →


