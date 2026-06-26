# Waterfall 瀑布流


## 组件概况

Waterfall 瀑布流组件是一种基于多列布局的内容展示组件，广泛应用于电商、图片浏览、社交等场景。该组件采用智能分配算法，将数据项动态分配到高度最短的列中，确保各列高度均衡，提升视觉美观度和浏览体验。支持动态数据更新、单列高度追踪、指定数据删除与修改等功能，适用于图片、卡片等高度不规则的内容布局场景。

## 核心功能描述

- **智能列分配**：实时追踪各列高度，将新数据自动分配到高度最短的列中，保持视觉均衡
- **多列支持**：通过 `column` 属性配置瀑布流的列数，默认为 2 列
- **差值更新**：通过监听数据变化获取新增部分，智能追加到现有瀑布流中，避免重复渲染
- **单列分配延迟**：通过 `addTime` 属性控制每次插入数据的时间间隔，确保列高均衡
- **轮询分配**：当所有列高度相同时，使用轮询方式分配数据到各列
- **数据操作**：提供 `remove`、`modify`、`clear` 等方法，支持删除指定数据、修改数据属性、清空所有数据
- **自定义 ID 键**：通过 `idKey` 属性指定数据唯一标识字段，用于精准定位和操作数据
- **跨平台支持**：兼容 H5、小程序、App 等不同平台的元素位置查询机制
- **插槽渲染**：通过默认插槽传入自定义渲染模板，支持灵活的卡片内容自定义

## 适用业务场景

- **电商商品展示**：不规则高度的商品卡片布局，如淘宝、京东的商品流
- **图片浏览**：瀑布流形式的图片展示，如花瓣、Pinterest 等图片社交平台
- **内容信息流**：社交媒体、新闻资讯等信息卡片的瀑布流展示
- **作品展示**：设计师作品集、摄影作品等视觉内容的瀑布流排列
- **商品筛选结果**：筛选后的商品列表以瀑布流形式展示，提升浏览体验

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 瀑布流数据列表，支持 v-model 双向绑定 | array | - | [] | - |
| column | 瀑布流的列数，不可动态修改 | string / number | - | 2 | - |
| addTime | 每次向结构插入数据的时间间隔，单位为毫秒（ms） | string / number | - | 200 | - |
| idKey | 数据唯一标识字段名，用于删除/修改操作时定位数据 | string | - | id | - |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| update:modelValue | 瀑布流数据变化时触发，用于 v-model 双向绑定 | value: array |

### Methods

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| remove | 清除某条指定的数据 | id: string / number | void |
| modify | 修改某条数据的某个属性 | id: string / number, key: string, value: any | void |
| clear | 清空瀑布流所有数据 | - | void |

### Slots

| 插槽名 | 说明 | 作用域参数 |
|--------|------|------------|
| default | 默认插槽，用于自定义每列中数据项的渲染模板 | columnList: 当前列的数据列表, columnIndex: 当前列的索引 |

## 使用示例

### 示例 1：基础用法

展示瀑布流组件的基本使用方式，包含数据加载和卡片自定义。

```vue
<template>
  <page-wraper>
    <wd-waterfall v-model="flowList" :column="2" ref="waterfallRef">
      <template #default="{ columnList }">
        <view class="demo-item" v-for="(item, index) in columnList" :key="index">
          <image class="demo-image" :src="item.image" mode="widthFix" />
          <view class="demo-title">{{ item.title }}</view>
          <view class="demo-price">{{ item.price }}元</view>
        </view>
      </template>
    </wd-waterfall>
    <wd-loadmore :state="loadStatus" @reload="loadMoreData"></wd-loadmore>
  </page-wraper>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { onLoad, onReachBottom } from '@dcloudio/uni-app'

  interface ItemData {
    id?: string
    price: number
    title: string
    image: string
  }

  type LoadMoreState = 'loading' | 'error' | 'finished'

  const flowList = ref<ItemData[]>([])
  const waterfallRef = ref<any>(null)
  const loadStatus = ref<LoadMoreState>('loading')

  const sampleData = [
    {
      price: 99,
      title: '商品标题示例一',
      image: 'https://example.com/image1.jpg'
    },
    {
      price: 199,
      title: '商品标题示例二',
      image: 'https://example.com/image2.jpg'
    },
    {
      price: 299,
      title: '商品标题示例三，这是一个较长的商品标题用于测试换行效果',
      image: 'https://example.com/image3.jpg'
    }
  ]

  const getRandomIndex = (max: number): number => {
    return Math.floor(Math.random() * max)
  }

  const loadMoreData = (): void => {
    for (let i = 0; i < 10; i++) {
      const index = getRandomIndex(sampleData.length)
      const item: ItemData = JSON.parse(JSON.stringify(sampleData[index]))
      item.id = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      flowList.value.push(item)
    }
  }

  onLoad(() => {
    loadMoreData()
    setTimeout(() => {
      loadStatus.value = 'finished'
    }, 1500)
  })

  onReachBottom(() => {
    loadStatus.value = 'loading'
    setTimeout(() => {
      loadMoreData()
      loadStatus.value = 'finished'
    }, 1000)
  })
</script>

<style lang="scss" scoped>
  .demo-item {
    border-radius: 8px;
    margin: 5px;
    background-color: #ffffff;
    padding: 8px;
    position: relative;
  }

  .demo-image {
    width: 100%;
    border-radius: 4px;
  }

  .demo-title {
    font-size: 14px;
    margin-top: 5px;
    color: #303133;
    word-break: break-all;
  }

  .demo-price {
    font-size: 15px;
    color: #f56c6c;
    margin-top: 5px;
  }
</style>
```

该示例展示了瀑布流组件的基本用法。组件接收 `flowList` 作为数据源，根据 `column` 配置列数（此处为 2 列），内部通过智能算法自动将卡片分配到高度最短的列中。配合 `wd-loadmore` 组件实现上拉加载更多数据。

### 示例 2：三列布局与加载控制

配置瀑布流为三列布局，展示完整的加载更多流程。

```vue
<template>
  <page-wraper>
    <view class="waterfall-header">
      <wd-tabs v-model="activeTab" @change="onTabChange">
        <wd-tab title="两列" :name="2"></wd-tab>
        <wd-tab title="三列" :name="3"></wd-tab>
        <wd-tab title="四列" :name="4"></wd-tab>
      </wd-tabs>
    </view>

    <wd-waterfall v-model="flowList" :column="columns" ref="waterfallRef">
      <template #default="{ columnList }">
        <view class="product-card" v-for="(item, index) in columnList" :key="index">
          <image class="product-image" :src="item.image" mode="widthFix" />
          <view class="product-info">
            <view class="product-title">{{ item.title }}</view>
            <view class="product-price-row">
              <text class="product-price">¥{{ item.price }}</text>
              <text class="product-original-price">¥{{ item.originalPrice }}</text>
            </view>
            <view class="product-tags">
              <view class="product-tag tag-new" v-if="item.isNew">新品</view>
              <view class="product-tag tag-hot" v-if="item.isHot">热卖</view>
              <view class="product-tag tag-discount" v-if="item.discount">折扣</view>
            </view>
            <view class="product-shop">{{ item.shop }}</view>
          </view>
        </view>
      </template>
    </wd-waterfall>

    <wd-loadmore :state="loadStatus" @reload="loadMoreData"></wd-loadmore>
  </page-wraper>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue'
  import { onLoad, onReachBottom } from '@dcloudio/uni-app'

  interface ProductItem {
    id?: string
    price: number
    originalPrice: number
    title: string
    shop: string
    image: string
    isNew: boolean
    isHot: boolean
    discount: boolean
  }

  type LoadMoreState = 'loading' | 'error' | 'finished'

  const activeTab = ref<number>(2)
  const columns = ref<number>(2)
  const loadStatus = ref<LoadMoreState>('loading')
  const flowList = ref<ProductItem[]>([])
  const waterfallRef = ref<any>(null)

  const productData = [
    {
      price: 199,
      originalPrice: 299,
      title: '春季新款休闲鞋透气跑步鞋',
      shop: '运动品牌旗舰店',
      image: 'https://example.com/shoes1.jpg',
      isNew: true,
      isHot: false,
      discount: true
    },
    {
      price: 399,
      originalPrice: 599,
      title: '时尚百搭单肩包大容量手提包',
      shop: '箱包专营店',
      image: 'https://example.com/bag1.jpg',
      isNew: false,
      isHot: true,
      discount: true
    },
    {
      price: 59,
      originalPrice: 89,
      title: '居家必备懒人沙发舒适可拆洗',
      shop: '家居生活馆',
      image: 'https://example.com/sofa1.jpg',
      isNew: true,
      isHot: false,
      discount: false
    }
  ]

  const getRandomIndex = (max: number): number => {
    return Math.floor(Math.random() * max)
  }

  const loadMoreData = (): void => {
    for (let i = 0; i < 6; i++) {
      const index = getRandomIndex(productData.length)
      const item: ProductItem = JSON.parse(JSON.stringify(productData[index]))
      item.id = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      flowList.value.push(item)
    }
  }

  const onTabChange = (event: { name: number }) => {
    columns.value = event.name
    flowList.value = []
    loadMoreData()
  }

  onLoad(() => {
    loadMoreData()
    setTimeout(() => {
      loadStatus.value = 'finished'
    }, 1000)
  })

  onReachBottom(() => {
    loadStatus.value = 'loading'
    setTimeout(() => {
      loadMoreData()
      loadStatus.value = 'finished'
    }, 1000)
  })
</script>

<style lang="scss" scoped>
  .waterfall-header {
    margin-bottom: 10px;
  }

  .product-card {
    border-radius: 8px;
    margin: 5px;
    background-color: #ffffff;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .product-image {
    width: 100%;
  }

  .product-info {
    padding: 10px;
  }

  .product-title {
    font-size: 14px;
    color: #303133;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .product-price-row {
    display: flex;
    align-items: baseline;
    margin-top: 5px;
  }

  .product-price {
    font-size: 16px;
    color: #f56c6c;
    font-weight: bold;
  }

  .product-original-price {
    font-size: 12px;
    color: #999;
    margin-left: 5px;
    text-decoration: line-through;
  }

  .product-tags {
    display: flex;
    gap: 5px;
    margin-top: 5px;
  }

  .product-tag {
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 10px;
    color: #fff;
  }

  .tag-new {
    background-color: #409eff;
  }

  .tag-hot {
    background-color: #e6a23c;
  }

  .tag-discount {
    background-color: #f56c6c;
  }

  .product-shop {
    font-size: 11px;
    color: #909399;
    margin-top: 5px;
  }
</style>
```

该示例展示了三列（或多列）瀑布流的配置方式。通过 `wd-tabs` 组件动态切换列数，每次切换时清空数据并重新加载。每个商品卡片包含图片、标题、价格、标签等信息，展示更丰富的卡片样式。

### 示例 3：数据删除与修改操作

展示通过 ref 调用组件方法进行数据删除和修改操作。

```vue
<template>
  <page-wraper>
    <wd-waterfall v-model="flowList" :column="2" ref="waterfallRef">
      <template #default="{ columnList }">
        <view class="demo-card" v-for="(item, index) in columnList" :key="index">
          <image class="demo-image" :src="item.image" mode="widthFix" />
          <view class="demo-content">
            <view class="demo-title">{{ item.title }}</view>
            <view class="demo-price">¥{{ item.price }}</view>
            <view class="demo-actions">
              <wd-button size="small" @click="handleEdit(item)">编辑</wd-button>
              <wd-button size="small" type="danger" @click="handleDelete(item.id)">删除</wd-button>
            </view>
          </view>
        </view>
      </template>
    </wd-waterfall>
  </page-wraper>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { onLoad } from '@dcloudio/uni-app'

  interface ItemData {
    id?: string
    price: number
    title: string
    image: string
  }

  const flowList = ref<ItemData[]>([])
  const waterfallRef = ref<any>(null)

  const sampleData = [
    {
      price: 99,
      title: '商品一',
      image: 'https://example.com/image1.jpg'
    },
    {
      price: 199,
      title: '商品二',
      image: 'https://example.com/image2.jpg'
    },
    {
      price: 299,
      title: '商品三',
      image: 'https://example.com/image3.jpg'
    },
    {
      price: 399,
      title: '商品四',
      image: 'https://example.com/image4.jpg'
    }
  ]

  const getRandomIndex = (max: number): number => {
    return Math.floor(Math.random() * max)
  }

  const handleDelete = (id: string): void => {
    waterfallRef.value?.remove(id)
  }

  const handleEdit = (item: ItemData): void => {
    // 修改商品价格
    const newPrice = item.price * 0.8
    waterfallRef.value?.modify(item.id, 'price', newPrice)
  }

  const loadData = (): void => {
    for (let i = 0; i < 8; i++) {
      const index = getRandomIndex(sampleData.length)
      const item: ItemData = JSON.parse(JSON.stringify(sampleData[index]))
      item.id = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      flowList.value.push(item)
    }
  }

  onLoad(() => {
    loadData()
  })
</script>

<style lang="scss" scoped>
  .demo-card {
    border-radius: 8px;
    margin: 5px;
    background-color: #ffffff;
    padding: 8px;
  }

  .demo-image {
    width: 100%;
    border-radius: 4px;
  }

  .demo-content {
    padding: 5px;
  }

  .demo-title {
    font-size: 14px;
    color: #303133;
    margin-top: 5px;
  }

  .demo-price {
    font-size: 15px;
    color: #f56c6c;
    margin-top: 5px;
  }

  .demo-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }
</style>
```

该示例展示了瀑布流组件的数据操作功能。通过 `ref` 获取组件实例后，可以调用 `remove(id)` 方法删除指定 ID 的数据项，调用 `modify(id, key, value)` 方法修改指定数据项的属性。操作同时会更新父组件通过 v-model 绑定的数据。

### 示例 4：自定义插入间隔与 ID 键

配置瀑布流的插入间隔和 ID 字段名。

```vue
<template>
  <page-wraper>
    <view class="waterfall-controls">
      <wd-input-number v-model="addTime" label="插入间隔(ms)" :min="50" :max="500" :step="50" />
      <view class="control-desc">较短的间隔提升加载速度，但可能导致列高不均衡</view>
    </view>

    <wd-waterfall
      v-model="flowList"
      :column="2"
      :add-time="addTime"
      id-key="productId"
      ref="waterfallRef"
    >
      <template #default="{ columnList }">
        <view class="demo-item" v-for="(item, index) in columnList" :key="item.productId">
          <image class="demo-image" :src="item.cover" mode="widthFix" />
          <view class="demo-title">{{ item.productName }}</view>
          <view class="demo-price">¥{{ item.unitPrice }}</view>
        </view>
      </template>
    </wd-waterfall>
  </page-wraper>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { onLoad } from '@dcloudio/uni-app'

  interface ProductItem {
    productId: string
    productName: string
    unitPrice: number
    cover: string
  }

  const addTime = ref<number>(200)
  const flowList = ref<ProductItem[]>([])
  const waterfallRef = ref<any>(null)

  const productData = [
    {
      productName: '定制款产品 A',
      unitPrice: 128,
      cover: 'https://example.com/product1.jpg'
    },
    {
      productName: '经典款产品 B',
      unitPrice: 256,
      cover: 'https://example.com/product2.jpg'
    },
    {
      productName: '限量款产品 C',
      unitPrice: 512,
      cover: 'https://example.com/product3.jpg'
    }
  ]

  const loadData = (): void => {
    for (let i = 0; i < 12; i++) {
      const index = Math.floor(Math.random() * productData.length)
      const item: ProductItem = {
        ...productData[index],
        productId: `P_${Date.now()}_${i}`
      }
      flowList.value.push(item)
    }
  }

  onLoad(() => {
    loadData()
  })
</script>

<style lang="scss" scoped>
  .waterfall-controls {
    padding: 10px;
    background: #f5f5f5;
    margin-bottom: 10px;

    .control-desc {
      font-size: 12px;
      color: #999;
      margin-top: 5px;
    }
  }

  .demo-item {
    border-radius: 8px;
    margin: 5px;
    background-color: #ffffff;
    padding: 8px;
  }

  .demo-image {
    width: 100%;
    border-radius: 4px;
  }

  .demo-title {
    font-size: 14px;
    color: #303133;
    margin-top: 5px;
  }

  .demo-price {
    font-size: 15px;
    color: #f56c6c;
    margin-top: 5px;
  }
</style>
```

该示例演示了 `addTime` 和 `idKey` 属性的配置。`addTime` 控制每次向 DOM 插入数据的时间间隔，间隔越长，越能保证两列高度相近，但用户体验相对较慢。`idKey` 指定数据唯一标识的字段名，示例中使用了 `productId` 而不是默认的 `id`。

### 示例 5：清空瀑布流数据

展示清空瀑布流数据的操作。

```vue
<template>
  <page-wraper>
    <view class="waterfall-toolbar">
      <wd-button type="danger" @click="handleClear">清空所有数据</wd-button>
      <wd-button type="primary" @click="handleReload">重新加载</wd-button>
    </view>

    <wd-waterfall v-model="flowList" :column="2" ref="waterfallRef">
      <template #default="{ columnList }">
        <view class="demo-card" v-for="(item, index) in columnList" :key="index">
          <view class="card-number">{{ index + 1 }}</view>
          <view class="card-content">{{ item.content }}</view>
        </view>
      </template>
    </wd-waterfall>
  </page-wraper>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { onLoad } from '@dcloudio/uni-app'

  interface CardItem {
    id?: string
    content: string
  }

  const flowList = ref<CardItem[]>([])
  const waterfallRef = ref<any>(null)

  const generateContent = (index: number): string => {
    const contents = [
      '这是一段示例文本内容',
      '这是另一段不同的文本内容，长度稍长一些',
      '第三段内容，长度更长，用于测试不同高度的卡片在瀑布流中的展示效果',
      '较短的内容',
      '中等长度的内容，用于瀑布流示例'
    ]
    return contents[index % contents.length]
  }

  const loadData = (): void => {
    for (let i = 0; i < 20; i++) {
      const item: CardItem = {
        id: `${Date.now()}_${i}`,
        content: generateContent(i)
      }
      flowList.value.push(item)
    }
  }

  const handleClear = (): void => {
    waterfallRef.value?.clear()
  }

  const handleReload = (): void => {
    handleClear()
    loadData()
  }

  onLoad(() => {
    loadData()
  })
</script>

<style lang="scss" scoped>
  .waterfall-toolbar {
    display: flex;
    gap: 10px;
    padding: 10px;
    background: #f5f5f5;
  }

  .demo-card {
    border-radius: 8px;
    margin: 5px;
    background-color: #ffffff;
    padding: 15px;
    border: 1px solid #e5e5e5;
  }

  .card-number {
    font-size: 24px;
    font-weight: bold;
    color: #409eff;
    margin-bottom: 10px;
  }

  .card-content {
    font-size: 14px;
    color: #303133;
    line-height: 1.5;
  }
</style>
```

该示例展示了清空瀑布流数据的操作。通过 `ref` 获取组件实例后，调用 `clear()` 方法清空所有列数据和临时列表，同时将父组件的 v-model 绑定数据更新为空数组。

## 注意事项

1. **列数不可动态修改**：`column` 属性在组件初始化后不应动态修改，建议在组件挂载前确定列数或在切换列数时重新创建组件实例。

2. **差值更新机制**：组件通过监听 `modelValue` 的差值来获取新增数据，每次更新时会基于之前的数据长度计算新增部分的起始索引。如果直接替换整个数组而非 push 操作，可能导致更新逻辑异常。

3. **插入时间间隔**：`addTime` 属性控制每次向 DOM 插入数据的时间间隔，默认 200ms。较短的间隔能提升加载速度，但可能导致两列高度不均衡；较长的间隔能保证高度均衡，但用户体验较差。建议根据实际场景调整。

4. **ID 唯一性**：确保每条数据的 `idKey` 字段值唯一。使用 `remove`、`modify` 方法时，组件会根据该字段在数据中定位目标项。

5. **数据深拷贝**：组件内部使用 `JSON.parse(JSON.stringify())` 进行数据深拷贝，避免对象引用导致的数据混乱。因此数据项中的函数、日期等特殊类型可能无法正确处理。

6. **高度计算依赖**：瀑布流的列分配依赖于获取 DOM 节点的实际高度。在 H5 端使用 `getBoundingClientRect()`，在小程序端使用 `uni.createSelectorQuery()`。确保内容已渲染完成后再进行高度计算。

7. **快速滚动处理**：频繁快速上拉加载时，组件内置了防止数据混乱的机制。但建议在业务层做防抖处理，避免短时间内多次触发数据加载。

8. **性能优化**：大量数据场景下，建议结合虚拟列表、图片懒加载等技术进行性能优化，避免同时渲染过多 DOM 节点。

9. **数据修改同步**：调用 `modify` 方法会同时更新组件内部列数据和父组件的 `modelValue`，确保数据源保持同步。

10. **自定义列高追踪**：如果内容包含异步加载的图片或其他延迟渲染的元素，可能需要适当调整 `addTime` 或在图片加载完成后手动触发重新分配。