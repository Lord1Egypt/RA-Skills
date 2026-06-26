# Card 卡片


## 组件概况

Card 卡片组件是一种用于承载、展示内容信息的容器组件，通过清晰的视觉边界将相关内容组织在一起。该组件支持标题、内容区域和底部操作区域三个部分，提供默认圆角阴影样式与矩形样式两种卡片形态，适用于信息展示、订单列表、服务提醒等多种业务场景。卡片组件结构灵活，支持通过插槽自定义标题、内容和底部区域，满足不同业务需求。

## 核心功能描述

- **双形态卡片**：支持默认圆角卡片与矩形（rectangle）卡片两种形态，矩形卡片去除圆角和阴影，内容区域与底部区域以分割线分隔
- **三段式布局**：提供标题区域、内容区域和底部操作区域，标题与底部区域按需显示
- **全面插槽支持**：支持默认插槽（内容区）、title 插槽（标题区）和 footer 插槽（底部区），可实现高度自定义布局
- **自定义样式类**：支持为标题、内容、底部区域分别设置自定义样式类名
- **暗色模式支持**：内置 dark 主题样式，自动适配系统主题切换
- **虚拟宿主**：开启 virtualHost，组件根节点样式不影响内部结构

## 适用业务场景

- **信息展示卡片**：展示文本、图片、列表等内容，如文章摘要、商品详情简介等
- **订单卡片**：在订单列表中展示商品图片、名称、数量、金额、买家信息等
- **服务提醒卡片**：展示服务到期提醒、状态变更通知等，搭配操作按钮引导用户处理
- **用户信息卡片**：展示用户头像、昵称、个人简介等信息

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| type | string | - | 否 | 卡片类型，设置为 'rectangle' 时显示矩形卡片（去除圆角和阴影，内容区域与底部区域带分割线） |
| title | string | - | 否 | 卡片标题，显示在卡片顶部标题区域；传入 title 或使用 title 插槽时显示标题区域 |
| customClass | string | '' | 否 | 自定义根节点类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customTitleClass | string | '' | 否 | 自定义标题区域样式类名 |
| customContentClass | string | '' | 否 | 自定义内容区域样式类名 |
| customFooterClass | string | '' | 否 | 自定义底部区域样式类名 |

### Events

组件不对外暴露事件。

### Methods

组件不对外暴露方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 卡片内容区域，可插入任意内容，如文本、图片、列表等 |
| title | - | 自定义标题区域内容，当需要复杂标题布局（如图标+文字组合）时使用；不传 title 属性时使用此插槽自定义标题 |
| footer | - | 自定义底部操作区域内容，如按钮组、操作链接等；不传此插槽时底部区域不显示 |

## 使用示例

### 示例 1：基础用法

最基本的卡片展示，通过 `title` 属性设置标题，使用默认插槽填充内容，`footer` 插槽定义底部操作按钮。

```vue
<template>
  <view>
    <wd-card title="《静夜思》">
      {{ content }}
      <template #footer>
        <wd-button size="small" plain>查看详情</wd-button>
      </template>
    </wd-card>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const content = ref('床前明月光，疑是地上霜。举头望明月，低头思故乡。')
</script>
```

该示例展示了最基本的卡片用法，卡片带有标题、内容区域和底部操作按钮。默认样式为圆角带阴影的卡片形态。

### 示例 2：矩形卡片

通过设置 `type="rectangle"` 显示矩形卡片，去除圆角和阴影效果，内容区域与底部区域以分割线分隔。

```vue
<template>
  <view>
    <wd-card title="《静夜思》" type="rectangle">
      {{ content }}
      <template #footer>
        <wd-button size="small" plain>查看详情</wd-button>
      </template>
    </wd-card>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const content = ref('床前明月光，疑是地上霜。举头望明月，低头思故乡。')
</script>
```

该示例中，矩形卡片铺满容器宽度，无圆角无阴影，标题区域、内容区域、底部区域之间使用细线分割，适用于列表式布局。

### 示例 3：订单信息卡片

在内容区域展示图片与文字组合的订单信息，底部搭配操作按钮。

```vue
<template>
  <view>
    <wd-card title="新订单">
      <view class="content">
        <image
          src="/static/img/jd.png"
          alt="商品图片"
          style="width: 70px; height: 70px; border-radius: 4px; margin-right: 12px"
        />
        <view>
          <view>蜜滋兰(mizland)新西兰进口多花种…</view>
          <view>数量：1件</view>
          <view>金额：29.08</view>
          <view>买家昵称：Joy</view>
        </view>
      </view>
      <template #footer>
        <wd-button size="small" plain>查看详情</wd-button>
      </template>
    </wd-card>
  </view>
</template>
<style lang="scss" scoped>
  .content {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
</style>
```

该示例展示了典型的订单卡片布局，左侧为商品图片，右侧为订单详情信息，底部提供查看详情的操作按钮。

### 示例 4：去除 footer 的卡片

不传入 `footer` 插槽时，底部区域不会显示，适用于仅需展示内容无需操作的场景。

```vue
<template>
  <view>
    <wd-card title="头像" type="rectangle">
      <view>
        <wd-avatar src="/static/img/a1.png" />
        <text>你好，世界！</text>
      </view>
    </wd-card>
  </view>
</template>
```

该示例中没有使用 footer 插槽，卡片仅展示标题和内容区域，适用于纯信息展示场景。

### 示例 5：自定义标题插槽

通过 `title` 插槽自定义标题区域内容，可实现复杂的标题布局，如图标、文字组合，标题与辅助信息并排等。

```vue
<template>
  <view>
    <wd-card>
      <template #title>
        <view class="title">
          <view>2025-10-01服务到期</view>
          <view class="title-tip">
            <wd-icon name="attention" size="14px" custom-style="vertical-align: bottom" />
            您可以去电脑上使用该服务
          </view>
        </view>
      </template>

      <view style="height: 40px" class="content">
        <image
          src="/static/img/jd.png"
          width="40"
          height="40"
          alt="商品图片"
          style="width: 40px; height: 40px; border-radius: 4px; margin-right: 12px"
        />
        <view>
          <view class="custom-main">智云好客CRM短信_催评营销</view>
          <view class="custom-sub">高级版 - 快速吸粉</view>
        </view>
      </view>
      <template #footer>
        <view>
          <wd-button size="small" plain custom-style="margin-right: 8px">评价</wd-button>
          <wd-button size="small">立即使用</wd-button>
        </view>
      </template>
    </wd-card>
  </view>
</template>
<style lang="scss" scoped>
  .content,
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .content {
    justify-content: flex-start;
  }

  .title {
    justify-content: space-between;
  }

  .title-tip {
    color: rgba(0, 0, 0, 0.25);
    font-size: 12px;
  }

  .custom-main {
    color: rgba(0, 0, 0, 0.85);
    font-size: 16px;
  }

  .custom-sub {
    color: rgba(0, 0, 0, 0.25);
    font-size: 12px;
  }
</style>
```

该示例通过 title 插槽自定义标题布局，标题左侧显示服务到期日期，右侧显示带有提醒图标的辅助说明文字。底部提供两个操作按钮。

### 示例 6：底部多按钮操作

在 footer 插槽中放置多个按钮，用于提供多个操作入口。

```vue
<template>
  <view>
    <wd-card type="rectangle">
      <template #title>
        <view class="title">
          <view>2025-10-01服务到期</view>
          <view class="title-tip">
            <wd-icon name="attention" size="14px" custom-style="vertical-align: bottom" />
            您可以去电脑上使用该服务
          </view>
        </view>
      </template>

      <view style="height: 40px" class="content">
        <image
          src="/static/img/jd.png"
          width="40"
          height="40"
          alt="商品图片"
          style="width: 40px; height: 40px; border-radius: 4px; margin-right: 12px"
        />
        <view>
          <view class="custom-main">智云好客CRM短信_催评营销</view>
          <view class="custom-sub">高级版 - 快速吸粉</view>
        </view>
      </view>
      <template #footer>
        <view>
          <wd-button size="small" plain custom-style="margin-right: 8px">评价</wd-button>
          <wd-button size="small">立即使用</wd-button>
        </view>
      </template>
    </wd-card>
  </view>
</template>
<script lang="ts" setup>
  // 无额外脚本逻辑
</script>
<style lang="scss" scoped>
  .content,
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .content {
    justify-content: flex-start;
  }

  .title {
    justify-content: space-between;
  }

  .title-tip {
    color: rgba(0, 0, 0, 0.25);
    font-size: 12px;
  }

  .custom-main {
    color: rgba(0, 0, 0, 0.85);
    font-size: 16px;
  }

  .custom-sub {
    color: rgba(0, 0, 0, 0.25);
    font-size: 12px;
  }
</style>
```

该示例展示了矩形卡片底部放置多个按钮的用法，通过自定义样式控制按钮间距。底部区域默认右对齐。

## 注意事项

1. **标题显示条件**：标题区域仅在传入 `title` 属性或使用 `title` 插槽时显示，两者均未设置时标题区域不会渲染
2. **底部区域显示条件**：底部区域仅在使用 `footer` 插槽时显示，不传入 footer 插槽时底部区域不会渲染
3. **矩形卡片形态**：设置 `type="rectangle"` 时，卡片去除圆角和阴影，左右边距归零，内容区域和底部区域上方会添加分割线
4. **底部区域对齐**：默认样式下，底部区域内容为右对齐（text-align: right），如需左对齐或其他对齐方式可通过 `customFooterClass` 自定义
5. **样式自定义优先级**：`customTitleClass`、`customContentClass`、`customFooterClass` 仅用于添加自定义样式类名，具体样式需自行定义
6. **内容区域无默认分割线**：默认卡片形态下，内容区域与底部区域之间没有分割线；矩形卡片形态下，内容区域和底部区域上方均有分割线
7. **暗色模式适配**：组件内置暗色主题样式，当父级包含 `wot-theme-dark` 类名时自动切换为暗色样式
