# IndexBar 索引栏


## 组件概况

IndexBar 索引栏组件由 `wd-index-bar`（索引栏容器）和 `wd-index-anchor`（索引锚点）两个关联组件组成，用于展示带字母或自定义索引的列表结构。组件右侧固定显示索引侧边栏，用户可通过点击或滑动侧边栏索引快速定位到对应的列表区域。索引锚点支持吸顶效果，在滚动过程中始终显示当前分区的标题。该组件适用于联系人列表、城市选择、商品分类等需要快速定位的长列表场景。

## 核心功能描述

- **索引侧边栏**：组件右侧自动生成索引字母导航栏，垂直居中排列，支持点击和滑动操作快速跳转
- **锚点定位**：通过 `wd-index-anchor` 定义每个分区的锚点标题，滚动或点击索引时自动滚动到对应锚点位置
- **锚点吸顶**：通过 `sticky` 属性开启索引锚点吸顶功能，当前分区的锚点标题在滚动时会固定在列表顶部
- **高亮当前索引**：侧边栏中当前可视区域对应的索引字母会自动高亮显示，使用主题色标识
- **滚动监听**：组件内部通过 scroll-view 的 scroll 事件实时监听滚动位置，自动计算并更新当前激活的索引
- **触摸滑动**：支持在侧边栏上按住滑动，手指经过的索引会实时高亮并触发列表滚动到对应位置
- **动态内容适配**：组件挂载时自动测量各锚点的位置信息，动态更新索引列表
- **暗色模式支持**：内置暗色主题样式，侧边栏索引和锚点背景会自动适配暗色模式

## 适用业务场景

- **通讯录联系人列表**：按照姓名首字母 A-Z 分组展示联系人，右侧提供字母索引导航，点击字母快速跳转到对应分组
- **城市选择器**：按照城市拼音首字母分组展示城市列表，配合搜索功能实现城市快速选择
- **商品品牌列表**：在电商应用中按照品牌首字母分类展示品牌列表，用户可通过索引快速找到目标品牌
- **地址管理**：省市区选择、收货地址管理等场景中按照字母或区域索引组织数据
- **音乐歌曲列表**：按照歌曲名称或歌手名称首字母分组展示歌曲列表

## API

### wd-index-bar Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| sticky | boolean | false | 否 | 索引锚点是否开启吸顶效果，开启后当前分区的锚点标题会固定在列表顶部 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### wd-index-bar Events

当前组件未通过 `defineEmits` 派发自定义事件。

### wd-index-bar Methods

当前组件未通过 `defineExpose` 暴露实例方法。内部通过 provide/inject 机制与 `wd-index-anchor` 子组件通信。

### wd-index-bar Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于放置 `wd-index-anchor` 组件及对应的列表内容，支持任意自定义布局 |

### wd-index-anchor Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| index | string / number | - | **是** | 索引标识符，对应侧边栏中显示的索引文字，也用于判断当前激活的索引 |
| customStyle | string | '' | 否 | 自定义锚点根元素样式 |
| customClass | string | '' | 否 | 自定义锚点根元素类名 |

### wd-index-anchor Events

当前组件未通过 `defineEmits` 派发自定义事件。

### wd-index-anchor Methods

通过 `defineExpose` 暴露以下属性：

| 属性名称 | 类型 | 说明 |
| --- | --- | --- |
| top | `Ref<number>` | 锚点元素距离页面顶部的距离（px），由 `wd-index-bar` 内部读取用于滚动定位 |

### wd-index-anchor Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 锚点标题内容。不提供时默认显示 `index` 属性的值，可提供任意自定义内容（如图标 + 文字组合） |

### CSS 变量

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --wot-index-bar-index-font-size | $-fs-aid | 侧边栏索引文字大小 |

### 样式变量

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| $-index-bar-index-font-size | $-fs-aid | 索引栏字体大小 |
| $-index-bar-index-active-color | $-color-theme | 索引栏激活状态颜色（通过 `is-active` 类应用） |
| $-index-anchor-bg | $-color-gray-2 | 锚点背景色 |
| $-index-anchor-padding | 10px | 锚点内边距 |
| $-index-anchor-font-size | 14px | 锚点文字大小 |
| $-index-anchor-color | $-color-title | 锚点文字颜色 |
| $-index-anchor-sticky-z-index | 1 | 吸顶状态层级 |

## 使用示例

### 示例 1：基础用法

效果说明：展示一个基础的索引栏列表，按照 A-Z 字母分组。右侧侧边栏显示对应的索引字母，点击字母可快速跳转到对应分组。每个分组的锚点标题默认显示索引字母。

```vue
<template>
  <view class="wrapper">
    <wd-index-bar>
      <view v-for="group in cityList" :key="group.index">
        <wd-index-anchor :index="group.index" />
        <wd-cell
          v-for="city in group.data"
          :key="city"
          :title="city"
          border
          clickable
          @click="handleClick(group.index, city)"
        />
      </view>
    </wd-index-bar>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const cityList = ref([
  {
    index: 'A',
    data: ['阿坝', '阿拉善', '阿里', '安康', '安庆', '鞍山', '安顺', '安阳', '澳门']
  },
  {
    index: 'B',
    data: ['北京', '白银', '保定', '宝鸡', '保山', '包头', '巴中', '北海', '蚌埠', '本溪', '毕节', '滨州', '百色', '亳州']
  },
  {
    index: 'C',
    data: ['重庆', '成都', '长沙', '长春', '沧州', '常德', '昌都', '长治', '常州', '巢湖', '潮州', '承德', '郴州', '赤峰', '池州', '崇左', '楚雄', '滁州', '朝阳']
  },
  {
    index: 'D',
    data: ['大连', '东莞', '大理', '丹东', '大庆', '大同', '大兴安岭', '德宏', '德阳', '德州', '定西', '迪庆', '东营']
  }
])

function handleClick(index: string, city: string) {
  uni.showToast({
    title: `当前点击索引: ${index}, 城市: ${city}`,
    icon: 'none'
  })
}
</script>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - var(--window-top));
}
</style>
```

### 示例 2：锚点吸顶

效果说明：通过设置 `sticky` 属性开启锚点吸顶功能。当列表滚动时，当前分区的锚点标题会固定在列表顶部，直到下一个分区的锚点将其顶替。方便用户始终知晓当前浏览的是哪个分区。

```vue
<template>
  <view class="wrapper">
    <wd-index-bar sticky>
      <view v-for="group in list" :key="group.index">
        <wd-index-anchor :index="group.index" />
        <wd-cell
          v-for="item in group.data"
          :key="item"
          :title="item"
          border
        />
      </view>
    </wd-index-bar>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ref([
  {
    index: 'A',
    data: ['安徽', '澳门']
  },
  {
    index: 'B',
    data: ['北京', '保定', '包头', '百色']
  },
  {
    index: 'C',
    data: ['重庆', '成都', '长沙', '长春', '常州']
  },
  {
    index: 'D',
    data: ['大连', '东莞', '大庆', '大同', '德州']
  },
  {
    index: 'E',
    data: ['鄂尔多斯', '恩施', '鄂州']
  },
  {
    index: 'F',
    data: ['福州', '防城港', '佛山', '抚顺', '阜新', '阜阳']
  },
  {
    index: 'G',
    data: ['广州', '桂林', '贵阳', '赣州', '甘孜', '广安', '广元', '贵港']
  }
])
</script>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - var(--window-top));
}
</style>
```

### 示例 3：自定义锚点内容

效果说明：通过 `wd-index-anchor` 的默认插槽自定义锚点标题内容，不仅限于显示索引字母，可以展示更丰富的信息如图标、数字等。

```vue
<template>
  <view class="wrapper">
    <wd-index-bar sticky>
      <view v-for="group in brandList" :key="group.index">
        <!-- 自定义锚点内容：显示索引字母 + 品牌数量 -->
        <wd-index-anchor :index="group.index">
          <view class="anchor-content">
            <text class="anchor-index">{{ group.index }}</text>
            <text class="anchor-count">{{ group.data.length }} 个品牌</text>
          </view>
        </wd-index-anchor>
        <wd-cell
          v-for="brand in group.data"
          :key="brand"
          :title="brand"
          border
        />
      </view>
    </wd-index-bar>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const brandList = ref([
  {
    index: 'A',
    data: ['Apple', 'Adidas', 'AMD', 'ASUS', 'AOC']
  },
  {
    index: 'B',
    data: ['BMW', 'Bose', 'Bosch', 'BenQ', 'Brother']
  },
  {
    index: 'C',
    data: ['Canon', 'Casio', 'Cisco', 'Corsair', 'Cooler Master']
  },
  {
    index: 'D',
    data: ['Dell', 'DJI', 'Dyson', 'Denon', 'D-Link']
  }
])
</script>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - var(--window-top));
}

.anchor-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.anchor-index {
  font-size: 14px;
  font-weight: bold;
}

.anchor-count {
  font-size: 12px;
  color: #999;
}
</style>
```

### 示例 4：结合搜索功能

效果说明：将索引栏与搜索组件结合，输入关键词后过滤列表数据并重新渲染索引栏。搜索结果为空时显示空状态提示。

```vue
<template>
  <view class="page">
    <wd-search v-model="keyword" placeholder="搜索城市" @search="handleSearch" @clear="handleClear" />
    <view class="wrapper" v-if="showList.length > 0">
      <wd-index-bar sticky>
        <view v-for="group in showList" :key="group.index">
          <wd-index-anchor :index="group.index" />
          <wd-cell
            v-for="city in group.data"
            :key="city"
            :title="city"
            border
            clickable
            @click="handleSelect(city)"
          />
        </view>
      </wd-index-bar>
    </view>
    <view v-else class="empty">
      <text>未找到匹配的城市</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

const keyword = ref('')
const showList = ref<any[]>([])

const allList = ref([
  {
    index: 'A',
    data: ['阿坝', '阿拉善', '阿里', '安康', '安庆', '鞍山', '安顺', '安阳', '澳门']
  },
  {
    index: 'B',
    data: ['北京', '白银', '保定', '宝鸡', '保山', '包头', '巴中', '北海', '蚌埠', '本溪', '毕节', '滨州', '百色', '亳州']
  },
  {
    index: 'C',
    data: ['重庆', '成都', '长沙', '长春', '沧州', '常德', '昌都', '长治', '常州', '巢湖', '潮州', '承德', '郴州']
  },
  {
    index: 'D',
    data: ['大连', '东莞', '大理', '丹东', '大庆', '大同', '大兴安岭', '德宏', '德阳', '德州', '定西', '迪庆', '东营']
  }
])

function handleSearch() {
  showList.value = []
  nextTick(() => {
    if (keyword.value) {
      showList.value = allList.value
        .map((group) => ({
          ...group,
          data: group.data.filter((city) => city.includes(keyword.value))
        }))
        .filter((group) => group.data.length > 0)
    } else {
      showList.value = allList.value
    }
  })
}

function handleClear() {
  keyword.value = ''
  handleSearch()
}

function handleSelect(city: string) {
  uni.showToast({
    title: `已选择: ${city}`,
    icon: 'success'
  })
}
</script>

<style scoped lang="scss">
.page {
  min-height: 100vh;
}

.wrapper {
  height: calc(100vh - var(--window-top) - 44px);
}

.empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #999;
  font-size: 14px;
}
</style>
```

### 示例 5：数字索引

效果说明：使用数字作为索引标识符，适用于按数字分组的场景，如楼层索引、期号索引等。

```vue
<template>
  <view class="wrapper">
    <wd-index-bar>
      <view v-for="floor in floorList" :key="floor.index">
        <wd-index-anchor :index="floor.index">
          <view class="floor-anchor">
            <text>第 {{ floor.index }} 层</text>
          </view>
        </wd-index-anchor>
        <wd-cell
          v-for="shop in floor.shops"
          :key="shop"
          :title="shop"
          border
        />
      </view>
    </wd-index-bar>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const floorList = ref([
  {
    index: 1,
    shops: ['化妆品专柜', '珠宝首饰店', '钟表眼镜店', '手机数码店']
  },
  {
    index: 2,
    shops: ['女装店', '男装店', '运动品牌', '鞋帽店']
  },
  {
    index: 3,
    shops: ['儿童乐园', '母婴用品店', '书店', '文具店']
  },
  {
    index: 4,
    shops: ['电影院', 'KTV', '电玩城', '咖啡厅']
  },
  {
    index: 5,
    shops: ['美食广场', '中餐厅', '西餐厅', '快餐店']
  }
])
</script>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - var(--window-top));
}

.floor-anchor {
  font-size: 14px;
  font-weight: bold;
}
</style>
```

## 注意事项

1. **wd-index-anchor 的 index 必填**：`wd-index-anchor` 的 `index` 属性为必填项，用于标识当前锚点对应的索引值。侧边栏会自动收集所有子锚点的 `index` 值生成索引列表。

2. **sticky 吸顶实现**：锚点吸顶通过 CSS `position: sticky` 实现，当前激活的锚点（即 `indexBar.anchorState.activeIndex === props.index` 时）会应用 `is-sticky` 类名。需要注意的是，`sticky` 定位在某些低版本浏览器或特殊容器中可能不支持。

3. **容器高度设置**：建议为 `wd-index-bar` 的父容器设置固定高度（如 `calc(100vh - var(--window-top))`），以确保 scroll-view 能正常滚动和计算位置。

4. **初始化延迟**：组件在 `onMounted` 后会延迟 100ms 通过 `getRect` 获取各元素的位置信息（包括索引栏整体位置、侧边栏位置、索引项高度等）。如果页面中存在动态渲染或异步数据，可能需要确保在数据加载完成后再渲染索引栏组件。

5. **触摸事件处理**：侧边栏的触摸事件（`touchstart`、`touchmove`、`touchend`、`touchcancel`）均使用 `.stop.prevent` 修饰符阻止事件冒泡和默认行为，确保滑动索引时不会触发页面滚动。

6. **滚动状态管理**：组件内部通过 `scrollState.touching` 标记区分程序触发的滚动和用户手动滚动。当用户触摸侧边栏时 `touching` 设为 `true`，此时 `scroll` 事件不会触发索引高亮更新，避免滚动定位过程中产生冲突。

7. **索引高亮计算逻辑**：侧边栏通过 `getAnchorByPageY` 方法根据触摸点的 Y 坐标计算对应的索引。计算公式为 `(pageY - sidebarInfo.offsetTop) / sidebarInfo.indexHeight`，其中 `sidebarInfo.indexHeight` 默认 24px，在组件初始化时通过 `getRect` 获取实际值。

8. **滚动位置强制触发**：当目标滚动位置与当前位置相同时，组件会先将 `scrollTop` 设为上一次的值，再在 `nextTick` 中设回目标值。这是为了在相同位置时也能触发 scroll-view 的滚动事件。

9. **动态列表重渲染**：当列表数据发生变化时（如搜索过滤），建议先将 `showList` 清空再赋值（如示例 4 所示），以便组件重新测量各锚点位置。`wd-index-bar` 会监听 `children` 数组的变化，自动重置激活索引为第一个子项的索引。

10. **侧边栏索引样式**：侧边栏绝对定位于容器右侧（`right: 4px`），垂直居中（`top: 50%; transform: translateY(-50%)`）。索引文字默认字号 12px，激活状态使用主题色高亮。

11. **钉钉小程序兼容**：组件针对钉钉小程序（`MP-DINGTALK`）做了特殊处理，使用独立的 `wd-index-anchor-ding` 包裹层实现吸顶效果。

12. **锚点暴露 top 属性**：`wd-index-anchor` 通过 `defineExpose({ top })` 暴露自身距离页面顶部的距离，`wd-index-bar` 通过读取子锚点的 `$.exposed!.top.value` 来计算滚动目标位置。
