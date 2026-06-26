# Cell 单元格


## 组件概况

Cell 单元格组件是列表信息展示的基础组件，通常以列表的形式呈现单条信息，支持标题、描述、图标、内容等多种信息展示形式。由 `wd-cell-group` 单元格组容器和 `wd-cell` 单元格两个关联组件组成，可组合使用构建结构清晰的列表界面。

`wd-cell-group` 作为单元格的外层包裹容器，提供分组标题、分组边框、卡片风格等容器级别的控制能力；`wd-cell` 作为具体的单元格内容载体，提供标题、值、描述、图标、跳转等丰富的内容展示能力。两个组件之间通过 Vue 依赖注入机制进行联动，实现边框显示控制等协同效果。

## 核心功能描述

- **分组管理**：通过 `wd-cell-group` 对单元格进行分组，支持分组标题和分组右侧内容展示
- **信息展示**：支持标题（title）、内容值（value）、描述信息（label）三段式布局
- **图标集成**：内置图标支持（icon prop）和自定义图标插槽（#icon）
- **页面跳转**：支持配置跳转地址（to）、跳转方式（replace），自动处理页面导航
- **尺寸控制**：提供默认和 large 两种尺寸规格
- **表单集成**：支持与 `wd-form` 组件联动，展示必填标记、表单验证错误信息
- **布局灵活**：支持水平布局和上下垂直布局（vertical），支持垂直居中对齐
- **点击反馈**：支持 hover 效果，可配置点击响应区域
- **文本处理**：支持文本省略号显示（ellipsis）、自定义对齐方式
- **样式定制**：提供自定义类名、样式及多种 customClass 用于插槽样式定制

## 适用业务场景

- **设置页面**：用户设置、系统配置等列表式信息展示
- **表单布局**：作为表单域的外层容器，配合表单组件使用
- **信息列表**：个人信息展示、订单信息、账户详情等结构化数据展示
- **导航菜单**：带箭头指示的功能入口、帮助与反馈等跳转入口
- **卡片列表**：使用 `insert` 属性展示为圆角卡片风格的分组列表
- **混合内容**：单元格右侧可嵌入按钮、开关、滑块等各类交互组件

## API

### wd-cell-group Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| title | 分组标题 | string | - | - | - |
| value | 分组右侧内容 | string | - | - | - |
| useSlot | 是否启用插槽 | boolean | - | false | - |
| border | 是否展示边框线 | boolean | - | false | - |
| insert | 是否展示为圆角卡片风格 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-cell Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| title | 标题 | string | - | - | - |
| value | 右侧内容 | string \| number | - | '' | - |
| icon | 图标类名 | string | - | - | - |
| iconSize | 图标大小 | string \| number | - | - | - |
| label | 描述信息 | string | - | - | - |
| isLink | 是否为跳转链接 | boolean | - | false | - |
| to | 跳转地址 | string | - | - | - |
| replace | 跳转时是否替换栈顶页面 | boolean | - | false | - |
| clickable | 开启点击反馈，is-link 默认开启 | boolean | - | false | - |
| size | 设置单元格大小 | string | 'large' | - | - |
| border | 是否展示边框线 | boolean | - | undefined | - |
| titleWidth | 设置左侧标题宽度 | string | - | - | - |
| center | 是否垂直居中，默认顶部居中 | boolean | - | false | - |
| required | 是否必填 | boolean | - | false | - |
| vertical | 表单属性，上下结构 | boolean | - | false | - |
| prop | 表单域 model 字段名，在使用表单校验功能的情况下，该属性是必填的 | string | - | - | - |
| rules | 表单验证规则，结合 wd-form 组件使用 | FormItemRule[] | - | [] | - |
| customIconClass | icon 使用 slot 时的自定义样式 | string | - | '' | - |
| customLabelClass | label 使用 slot 时的自定义样式 | string | - | '' | - |
| customValueClass | value 使用 slot 时的自定义样式 | string | - | '' | - |
| customTitleClass | title 使用 slot 时的自定义样式 | string | - | '' | - |
| valueAlign | value 文字对齐方式 | string | 'left' \| 'right' | 'right' | - |
| ellipsis | 是否超出隐藏，显示省略号 | boolean | - | false | - |
| useTitleSlot | 是否启用 title 插槽，默认启用。用来解决插槽传递时 v-slot 和 v-if 冲突问题 | boolean | - | true | - |
| markerSide | 必填标记位置 | string | 'before' \| 'after' | 'before' | - |
| arrowDirection | 箭头方向，只在 is-link 为 true 时生效 | string | 'left' \| 'up' \| 'down' \| 'right' | 'right' | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-cell Events

| 事件名称 | 说明 | 回调参数 |
|----------|------|----------|
| click | 点击单元格时触发 | - |

> 注意：`click` 事件仅在 `clickable` 或 `isLink` 属性为 `true` 时触发。

### wd-cell Methods

组件实例暴露的方法，可通过 ref 调用：

| 方法名 | 说明 | 参数 |
|--------|------|------|
| - | 暂无暴露方法 | - |

### wd-cell-group Slots

| 插槽名 | 说明 |
|--------|------|
| title | 自定义分组标题 |
| value | 自定义分组右侧内容 |
| default | 单元格内容插槽，用于放置 `wd-cell` 组件 |

### wd-cell Slots

| 插槽名 | 说明 |
|--------|------|
| default | 自定义右侧内容（value）区域 |
| title | 自定义左侧标题区域（需配合 `use-title-slot` 属性使用） |
| label | 自定义左侧描述信息区域 |
| icon | 自定义左侧图标区域 |
| right-icon | 自定义右侧箭头区域（当 `isLink` 为 false 时生效） |

## 使用示例

### 示例一：基本用法

最基础的单元格展示，包含标题和内容值。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="标题文字" value="内容" />
    <wd-cell title="标题文字" label="描述信息" value="内容" />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

### 示例二：图标展示

单元格左侧展示图标，支持内置图标和自定义图标插槽。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="标题文字" value="内容" icon="setting" />
    <wd-cell title="标题文字" value="内容">
      <template #icon>
        <view class="cell-icon"></view>
      </template>
    </wd-cell>
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
  .cell-icon {
    display: block;
    box-sizing: border-box;
    width: 16px;
    height: 16px;
    margin: 4px 4px 4px 0;
    background: url('https://img10.360buyimg.com/jmadvertisement/jfs/t1/71075/7/3762/1820/5d1f26d1E0d600b9e/a264c901943080ac.png') no-repeat;
    background-size: cover;
  }
</style>
```

### 示例三：分组标题

为单元格组设置分组标题和分组右侧内容。

```vue
<template>
  <wd-cell-group title="交易管理" value="内容">
    <wd-cell title="标题文字" value="内容" />
    <wd-cell
      title="标题文字"
      label="黄鹤断矶头，故人今在否？旧江山浑是新愁。欲买桂花同载酒，终不似，少年游。"
      value="内容"
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

### 示例四：大尺寸单元格

使用 `size="large"` 设置大尺寸单元格，适合需要更大点击区域或更突出展示的场。

```vue
<template>
  <wd-cell-group>
    <wd-cell size="large" title="标题文字" value="内容" />
    <wd-cell size="large" title="标题文字" value="内容" icon="setting" is-link />
    <wd-cell size="large" title="标题文字" label="描述信息" value="内容" />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

### 示例五：边框线控制

通过 `wd-cell-group` 的 `border` 属性控制整体边框，也可通过 `wd-cell` 的 `border` 属性单独控制某个单元格的边框。

```vue
<template>
  <wd-cell-group title="交易管理" border>
    <wd-cell title="标题文字" value="内容" />
    <wd-cell :border="false" title="标题文字" label="这一个cell不想要边框" value="内容" />
    <wd-cell title="标题文字" label="描述信息" value="内容" />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

### 示例六：点击事件与页面跳转

配置点击事件回调，或设置跳转链接实现页面导航。

```vue
<template>
  <wd-toast />
  <wd-cell-group>
    <wd-cell title="标题文字" value="内容" clickable @click="handleClick" />
    <wd-cell title="帮助与反馈" is-link to="/pages/index/Index" />
    <wd-cell title="设置" value="内容" is-link to="/pages/button/Index" replace />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const toast = useToast()

  function handleClick() {
    toast.show('点击了单元格')
  }
</script>

<style lang="scss" scoped>
</style>
```

### 示例七：表单属性

与表单组件结合使用，展示必填标记、上下布局等表单相关特性。

```vue
<template>
  <wd-cell-group border>
    <wd-cell title="必填" required>
      <wd-rate v-model="rate" icon="dong" active-icon="dong" @change="handleRateChange" />
    </wd-cell>
    <wd-cell title="必填星号在右" required marker-side="after">
      <wd-rate v-model="rate1" icon="dong" active-icon="dong" @change="handleRateChange" />
    </wd-cell>
    <wd-cell title="上下结构" vertical required marker-side="after">
      <wd-slider v-model="slider" @change="handleSliderChange" />
    </wd-cell>
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const rate = ref(0)
  const rate1 = ref(0)
  const slider = ref(0)

  function handleRateChange({ value }: any) {
    console.log(value)
  }
  function handleSliderChange({ value }: any) {
    console.log(value)
  }
</script>

<style lang="scss" scoped>
</style>
```

### 示例八：自定义插槽内容

通过插槽在单元格右侧嵌入按钮、开关、自定义文本等丰富内容。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="标题文字" center>
      <wd-button custom-class="custom-value" size="small" plain>按钮</wd-button>
    </wd-cell>
    <wd-cell title="标题文字" center>
      <view class="custom-value" style="height: 32px">
        <wd-switch v-model="switchValue" @change="handleSwitchChange" />
      </view>
    </wd-cell>
    <wd-cell title="标题文字" is-link to="/pages/index/index">
      <view class="custom-text">订购</view>
    </wd-cell>
    <wd-cell>
      <template #title>
        <view>
          <view style="display: inline-block">标题文字</view>
          <view class="end-time">30天后到期</view>
        </view>
      </template>
    </wd-cell>
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const switchValue = ref('')

  function handleSwitchChange({ value }: any) {
    console.log(value)
  }
</script>

<style lang="scss" scoped>
  .custom-value {
    position: absolute;
    top: 50%;
    right: 0;
    transform: translate(0, -50%);
    white-space: nowrap;
  }
  .custom-text {
    color: #f0883a;
  }
  .end-time {
    display: inline-block;
    margin-left: 8px;
    border: 1px solid #faa21e;
    padding: 0 4px;
    font-size: 10px;
    color: #faa21e;
  }
</style>
```

### 示例九：文本省略显示

当内容较长时，使用 `ellipsis` 属性控制文本超出时显示省略号，并配合 `value-align` 设置对齐方式。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="正常显示" value="这是一段很长的文字内容，通常情况下会完整显示" />
    <wd-cell
      title="省略号显示"
      value="这是一段很长的文字内容，当启用ellipsis属性时，超出部分将显示省略号"
      ellipsis
    />
    <wd-cell
      title="左对齐省略"
      value="这是一段很长的文字内容，左对齐并启用省略号功能"
      value-align="left"
      ellipsis
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

### 示例十：设置标题宽度与卡片风格

通过 `title-width` 控制标题宽度保持一致，使用 `insert` 属性展示卡片风格。

```vue
<template>
  <wd-cell-group>
    <wd-cell
      title="标题文字"
      label="这里是文字描述这里是文字描述这里是文字描述"
      title-width="200px"
      value="内容"
    />
  </wd-cell-group>

  <wd-cell-group title="交易管理" insert>
    <wd-cell title="标题文字" value="内容" />
    <wd-cell title="标题文字" value="内容" />
  </wd-cell-group>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
</script>

<style lang="scss" scoped>
</style>
```

## 注意事项

1. **边框显示机制**：当 `wd-cell` 嵌套在 `wd-cell-group` 中时，边框显示受父组件控制。`wd-cell-group` 设置 `border` 为 `true` 时，除第一个子单元格外的其他单元格会自动显示顶部边框。若 `wd-cell` 单独使用或未设置 `border`，则 `border` 值为 `undefined`，不显示边框。

2. **插槽启用条件**：使用 `#title` 插槽时，必须同时设置 `use-title-slot` 属性（默认为 `true`），否则插槽不会渲染。这是为了解决 uni-app 中 `v-slot` 和 `v-if` 冲突的问题。

3. **左侧区域显示逻辑**：`wd-cell` 的左侧区域（`wd-cell__left`）仅在满足以下条件之一时才渲染：存在 `icon` 属性或 `#icon` 插槽、存在 `title` 属性或 `#title` 插槽（配合 `useTitleSlot`）、存在 `label` 属性或 `#label` 插槽。

4. **点击事件触发条件**：`click` 事件仅在 `clickable` 或 `isLink` 为 `true` 时触发。若两者均为 `false`，点击单元格不会触发 `click` 事件。

5. **页面跳转行为**：设置 `to` 属性的同时必须设置 `isLink` 为 `true` 才会触发跳转。`replace` 为 `true` 时使用 `uni.redirectTo` 替换当前页面，否则使用 `uni.navigateTo` 打开新页面。

6. **表单验证联动**：`prop` 属性用于与 `wd-form` 组件的 `model` 字段名对应，配合 `rules` 属性可实现表单验证。验证错误信息会通过 `errorMessage` 计算属性从父级 `wd-form` 获取并显示在单元格底部。

7. **必填标记显示**：`required` 属性为 `true` 时显示红色星号标记。标记位置可通过 `markerSide` 设置为 `'before'`（标题前，默认）或 `'after'`（标题后）。此外，如果父级 `wd-form` 中配置了包含 `required: true` 的校验规则，也会自动显示必填标记。

8. **垂直布局**：设置 `vertical` 为 `true` 时，单元格切换为上下布局模式，右侧内容显示在标题下方，此时 `value-align` 属性不生效（默认左对齐）。

9. **样式定制**：`customIconClass`、`customLabelClass`、`customValueClass`、`customTitleClass` 分别用于在使用对应插槽时为插槽内容添加自定义 CSS 类名，方便对插槽内容进行样式定制。

10. **暗色模式**：组件原生支持暗色模式，当根节点包含 `wot-theme-dark` 类名时，组件会自动切换为暗色主题样式。
