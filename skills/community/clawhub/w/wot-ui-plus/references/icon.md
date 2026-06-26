# Icon 图标


## 组件概况

### 组件概述
Icon 组件用于显示图标，支持内置图标字体和自定义图片图标。它提供了丰富的样式定制选项，包括颜色、大小、粗细和形状等，可以轻松融入各种设计风格。

### 核心功能
- 支持内置图标字体
- 支持自定义图片图标
- 支持颜色、大小、粗细定制
- 支持圆形图标
- 支持点击交互
- 支持自定义图标字体前缀

### 适用业务场景
- 导航菜单图标
- 功能按钮图标
- 状态指示图标
- 表单验证图标
- 通知提示图标
- 自定义图标字体集成

## 完整API参考

### Props
| 名称 | 类型 | 默认值 | 必填项 | 描述 |
| --- | --- | --- | --- | --- |
| name | string | - | 是 | 使用的图标名字，可以使用链接图片 |
| round | boolean | false | 否 | 是否显示为圆角按钮 |
| bold | boolean | false | 否 | 图标是否加粗 |
| color | string | - | 否 | 图标的颜色 |
| size | number / string | - | 否 | 图标的字体大小 |
| classPrefix | string | 'wd-icon' | 否 | 类名前缀，用于使用自定义图标 |
| customStyle | string | '' | 否 | 自定义样式，对象格式 |
| customClass | string | '' | 否 | 自定义类名 |

### Events
| 事件名 | 触发条件 | 参数说明 |
| --- | --- | --- |
| click | 点击图标时触发 | event: 事件对象 |
| touch | 触摸图标时触发 | - |

### Methods
Icon 组件不直接对外暴露方法。

### Slots
Icon 组件不包含插槽。

## 多场景使用示例代码

### 基础用法

```vue
<template>
  <wd-icon name="home" />
  <wd-icon name="search" />
  <wd-icon name="user" />
</template>
```

### 自定义颜色和大小

```vue
<template>
  <wd-icon name="star" color="#ffc800" size="32px" />
  <wd-icon name="heart" color="#ff4d4f" size="24" />
  <wd-icon name="success" color="#07c160" size="20" />
</template>
```

### 圆形和加粗图标

```vue
<template>
  <wd-icon name="plus" round color="#1989fa" size="24" />
  <wd-icon name="minus" round color="#ff4d4f" size="24" />
  <wd-icon name="phone" bold color="#333" size="28" />
</template>
```

### 使用图片作为图标

```vue
<template>
  <wd-icon name="https://example.com/icon.png" size="40" />
  <wd-icon name="/static/icons/custom-icon.png" size="32" />
</template>
```

### 自定义图标字体

```vue
<template>
  <wd-icon name="custom-icon" class-prefix="my-icon" size="28" />
  <wd-icon name="another-icon" class-prefix="my-icon" color="#1989fa" />
</template>

<style>
/* 引入自定义图标字体 */
@font-face {
  font-family: 'MyIcon';
  src: url('/static/fonts/my-icon.ttf') format('truetype');
}

.my-icon {
  font-family: 'MyIcon' !important;
  font-size: 28px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.my-icon-custom-icon::before {
  content: '\e600';
}

.my-icon-another-icon::before {
  content: '\e601';
}
</style>
```

### 点击交互

```vue
<template>
  <wd-icon 
    name="delete" 
    color="#ff4d4f" 
    size="24" 
    @click="handleDelete"
  />
  <wd-icon 
    name="edit" 
    color="#1989fa" 
    size="24" 
    @click="handleEdit"
  />
</template>

<script setup lang="ts">
const handleDelete = () => {
  console.log('Delete clicked')
}

const handleEdit = () => {
  console.log('Edit clicked')
}
</script>
```

## 样式定制指南

### 使用 customStyle 自定义样式

```vue
<template>
  <wd-icon 
    name="settings" 
    :custom-style="{
      color: '#1989fa',
      fontSize: '24px',
      fontWeight: 'bold',
      borderRadius: '50%',
      backgroundColor: '#f0f9ff',
      padding: '8px'
    }"
  />
</template>
```

### 使用 customClass 自定义类名

```vue
<template>
  <wd-icon name="notification" custom-class="my-notification-icon" />
</template>

<style scoped>
.my-notification-icon {
  color: #ff976a;
  font-size: 28px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
</style>
```

## 注意事项

1. **图标类型判断**：组件通过判断 `name` 属性是否包含 '/' 来决定是显示图标字体还是图片图标。

2. **图标大小**：`size` 属性支持数字（默认单位 px）和字符串（带单位），例如：
   - `size="24"` 等价于 `size="24px"`
   - `size="2rem"` 使用 rem 单位
   - `size="2em"` 使用 em 单位

3. **自定义图标字体**：使用 `classPrefix` 属性时，需要确保已正确引入自定义字体文件，并定义了相应的 CSS 类。

4. **圆形图标**：`round` 属性会为图标添加圆形背景，配合 `color` 属性可以创建彩色圆形图标按钮。

5. **加粗效果**：`bold` 属性仅对图标字体有效，对图片图标无效。

6. **性能优化**：对于频繁使用的图标，建议使用内置图标字体，比图片图标具有更好的性能和渲染效果。

7. **兼容性**：自定义图片图标需要确保图片资源可访问，建议使用相对路径或CDN链接。