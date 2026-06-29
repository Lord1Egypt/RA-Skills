---
name: "scrollList"
description: "ScrollList 横向滚动列表 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs ScrollList 横向滚动列表 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/scrollList.html"
---

---

## [#](#scrolllist-横向滚动列表) ScrollList 横向滚动列表 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般用于同时展示多个商品、分类的场景，也可以完成左右滑动的列表。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

通过 slot 传入内容

```
<template>
  <u-scroll-list>
    <view v-for="(item, index) in list" :key="index">
      <image :src="item.thumb"></image>
    </view>
  </u-scroll-list>
</template>

<script>
  export default {
    data() {
      return {
        list: [
          {
            thumb: "https://uviewui.com/goods/1.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/2.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/3.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/4.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/5.jpg",
          },
        ],
      };
    },
  };
</script>
```

# [#](#指示器的使用) 指示器的使用

-   `indicator` 用于控制指示器是否显示
-   `indicatorWidth` 用于控制指示器整体的宽度
-   `indicatorBarWidth` 用于控制指示器滑块的宽度
-   `indicatorColor` 指示器的颜色
-   `indicatorActiveColor` 滑块的颜色
-   `indicatorStyle` 指示器的位置/样式控制

```
<template>
  <u-scroll-list
    :indicator="indicator"
    indicatorColor="#fff0f0"
    indicatorActiveColor="#f56c6c"
  >
    <view v-for="(item, index) in list" :key="index">
      <image :src="item.thumb"></image>
    </view>
  </u-scroll-list>
</template>

<script>
  export default {
    data() {
      return {
        indicator: true,
        list: [
          {
            thumb: "https://uviewui.com/goods/1.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/2.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/3.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/4.jpg",
          },
          {
            thumb: "https://uviewui.com/goods/5.jpg",
          },
        ],
      };
    },
  };
</script>
```

### [#](#兼容性与性能) 兼容性与性能

-   此组件是在 nvue 中引入 bindingx，此库类似于微信小程序 wxs，目的是让 js 运行在视图层，减少视图层和逻辑层的通信折损，在 nvue 中会有更好的体验。
-   此组件是在 APP-VUE、H5、小程序中使用的是 wxs。
-   其他平台则使用 js 完成。

当滑动到最左边/最右边时，uView 提供了事件`left`和`right`可供调用，用于对列表滑动到端点处的业务实现。

```
<template>
  <u-scroll-list @right="right" @left="left">
    <view class="scroll-list" style="flex-direction: row;">
      <view
        class="scroll-list__goods-item"
        v-for="(item, index) in list"
        :key="index"
        :class="[(index === 9) && 'scroll-list__goods-item--no-margin-right']"
      >
        <image class="scroll-list__goods-item__image" :src="item.thumb"></image>
        <text class="scroll-list__goods-item__text">￥{{ item.price }}</text>
      </view>
      <view class="scroll-list__show-more">
        <text class="scroll-list__show-more__text">查看更多</text>
        <u-icon name="arrow-leftward" color="#f56c6c" size="12"></u-icon>
      </view>
    </view>
  </u-scroll-list>
</template>
<script>
  export default {
    data() {
      return {
        list: [
          {
            price: "230.5",
            thumb: "https://uviewui.com/goods/1.jpg",
          },
          {
            price: "74.1",
            thumb: "https://uviewui.com/goods/2.jpg",
          },
          {
            price: "8457",
            thumb: "https://uviewui.com/goods/6.jpg",
          },
          {
            price: "1442",
            thumb: "https://uviewui.com/goods/5.jpg",
          },
          {
            price: "541",
            thumb: "https://uviewui.com/goods/2.jpg",
          },
          {
            price: "234",
            thumb: "https://uviewui.com/goods/3.jpg",
          },
          {
            price: "562",
            thumb: "https://uviewui.com/goods/4.jpg",
          },
          {
            price: "251.5",
            thumb: "https://uviewui.com/goods/1.jpg",
          },
        ],
      };
    },
    methods: {
      left() {
        console.log("left");
      },
      right() {
        console.log("right");
      },
    },
  };
</script>

<style lang="scss">
  .scroll-list {
    @include flex(column);

    &__goods-item {
      margin-right: 20px;

      &__image {
        width: 60px;
        height: 60px;
        border-radius: 4px;
      }

      &__text {
        color: #f56c6c;
        text-align: center;
        font-size: 12px;
        margin-top: 5px;
      }
    }

    &__show-more {
      background-color: #fff0f0;
      border-radius: 3px;
      padding: 3px 6px;
      @include flex(column);
      align-items: center;

      &__text {
        font-size: 12px;
        width: 12px;
        color: #f56c6c;
        line-height: 16px;
      }
    }
  }
</style>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/scrollList/scrollList.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/scrollList/scrollList.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| indicatorWidth | 指示器的整体宽度 | String | Number | 50 | \- |
| indicatorBarWidth | 滑块的宽度 | String | Number | 20 | \- |
| indicator | 是否显示面板指示器 | Boolean | true | false |
| indicatorColor | 指示器非激活颜色 | String | #f2f2f2 | \- |
| indicatorActiveColor | 指示器滑块颜色 | String | #3c9cff | \- |
| indicatorStyle | 指示器样式，可通过 bottom，left，right 进行定位 | String | Object | \- | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| left | 滑动到左边时触发 | \- |
| right | 滑动到右边时触发 | \- |

← [Modal 模态框](https://www.uviewui.com/components/modal.html) [Line 线条](https://www.uviewui.com/components/line.html) →


