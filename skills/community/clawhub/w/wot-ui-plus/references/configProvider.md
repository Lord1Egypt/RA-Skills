# ConfigProvider 全局配置


## 组件概况

ConfigProvider 全局配置组件是 wot-ui-plus 的主题配置容器，用于统一管理整个应用的视觉风格和设计规范。该组件通过 CSS 变量（CSS Custom Properties）的方式注入主题变量，实现动态主题切换和全局样式定制。组件支持深色模式（dark）和浅色模式（light）的切换，并允许开发者通过 `theme-vars` 属性传入自定义主题变量，覆盖默认的设计规范。ConfigProvider 采用 provide/inject 模式向下传递主题配置，确保嵌套组件能够继承并应用统一的主题样式。

## 核心功能描述

- **主题模式切换**：通过 `theme` 属性轻松切换 light（浅色）和 dark（深色）两种主题模式，支持全局生效
- **自定义主题变量**：通过 `theme-vars` 属性传入自定义 CSS 变量对象，覆盖组件库的默认设计规范
- **CSS 变量注入**：利用 CSS 自定义属性机制动态注入主题变量，实现运行时主题切换
- **主题变量体系**：提供完整的主题变量体系，涵盖基础颜色、组件样式、间距、圆角、字体等多个维度
- **继承传递机制**：通过 provide/inject 模式将主题配置向下传递，确保子组件能正确应用主题
- **容器包装能力**：作为容器组件包裹其他组件，为后代组件提供统一的主题上下文环境
- **动态样式更新**：支持动态修改主题变量，实时更新应用外观而无需重新渲染组件树

## 适用业务场景

- **深色模式支持**：为应用提供一键切换深色/浅色主题的能力，满足用户在不同光线环境下的使用偏好
- **品牌主题定制**：根据企业品牌色彩规范自定义主题变量，实现组件库与品牌形象的一致性
- **多主题系统**：支持构建多套主题方案（如节日主题、季节主题等），提升用户体验
- **无障碍设计**：通过调整对比度、字体大小等主题变量，增强应用的可访问性
- **个性化设置**：允许用户自定义界面主题（如主色调、圆角大小等），提升个性化体验
- **产品差异化**：在相同组件库基础上，为不同产品线提供差异化的视觉风格
- **A/B 测试**：通过动态切换主题变量进行界面设计的 A/B 测试

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| theme | string | 'light' | 否 | 主题风格，可选值为 'light'（浅色）或 'dark'（深色），设置为 'dark' 开启深色模式 |
| theme-vars | object | {} | 否 | 自定义主题变量对象，通过 CSS 变量形式覆盖默认主题样式 |
| custom-style | string | '' | 否 | 自定义组件根元素的内联样式 |
| custom-class | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

当前组件未定义任何事件。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于包裹需要应用主题配置的子组件内容 |

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wot-theme-light | 应用浅色主题时的根节点样式类 |
| wot-theme-dark | 应用深色主题时的根节点样式类 |

## 主题变量体系

ConfigProvider 支持丰富的主题变量体系，覆盖应用的各个方面：

### 基础颜色变量
- `colorTheme`: 主题色
- `colorWhite`: 用于混合的白色
- `colorBlack`: 用于混合的黑色
- `colorSuccess`: 成功色
- `colorWarning`: 警告色
- `colorDanger`: 危险/错误色
- `colorInfo`: 信息色
- `colorPurple`: 紫色
- `colorYellow`: 黄色
- `colorBlue`: 蓝色

### 文字颜色变量
- `fontGray1`: 字体灰色1
- `fontGray2`: 字体灰色2
- `fontGray3`: 字体灰色3
- `fontGray4`: 字体灰色4
- `fontWhite1`: 字体白色1
- `fontWhite2`: 字体白色2
- `fontWhite3`: 字体白色3
- `fontWhite4`: 字体白色4
- `colorTitle`: 模块标题/重要正文
- `colorContent`: 普通正文
- `colorSecondary`: 次要信息
- `colorAid`: 辅助文字
- `colorTip`: 失效/默认提示文字

### 背景颜色变量
- `colorBg`: 背景色
- `darkBackground`: 深色背景1
- `darkBackground2`: 深色背景2
- `darkBackground3`: 深色背景3
- `darkBackground4`: 深色背景4
- `darkBackground5`: 深色背景5
- `darkBackground6`: 深色背景6
- `darkBackground7`: 深色背景7

### 边框颜色变量
- `colorBorder`: 控件边框线
- `colorBorderLight`: 分割线颜色
- `darkBorderColor`: 深色边框颜色

### 字体大小变量
- `fsBig`: 大型标题字号
- `fsImportant`: 重要数据字号
- `fsTitle`: 标题字号
- `fsContent`: 普通正文字号
- `fsSecondary`: 次要信息字号
- `fsAid`: 辅助文字字号

### 其他通用变量
- `fwMedium`: 字重500
- `fwSemibold`: 字重600
- `sizeSidePadding`: 屏幕两边留白padding

### 组件特定变量
组件库还提供了针对各个组件的详细主题变量，包括但不限于：
- Button 组件：`buttonSmallHeight`、`buttonPrimaryColor`、`buttonDisabledOpacity` 等
- Cell 组件：`cellPadding`、`cellTitleFs`、`cellValueColor` 等
- Input 组件：`inputPadding`、`inputBorderColor`、`inputFs` 等
- Popup 组件：`popupCloseSize`、`popupCloseColor` 等
- 更多组件变量详见源码中的类型定义

## 使用示例

### 示例 1：基础主题切换

效果说明：展示如何使用 ConfigProvider 在浅色和深色主题之间切换。通过修改 `theme` 属性的值来控制当前使用的主题模式。

```vue
<template>
  <wd-config-provider :theme="currentTheme">
    <view class="container">
      <wd-cell-group title="主题切换">
        <wd-cell title="当前主题" :value="currentTheme === 'dark' ? '深色' : '浅色'" />
        <wd-switch
          :model-value="currentTheme === 'dark'"
          @change="toggleTheme"
          active-text="深色"
          inactive-text="浅色"
        />
      </wd-cell-group>
      
      <wd-button type="primary" style="margin: 20px;">主要按钮</wd-button>
      <wd-cell title="普通单元格" value="测试内容" />
      <wd-badge :value="5" style="margin: 20px;">徽标</wd-badge>
    </view>
  </wd-config-provider>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentTheme = ref<'light' | 'dark'>('light')

function toggleTheme(value: boolean) {
  currentTheme.value = value ? 'dark' : 'light'
}
</script>

<style scoped lang="scss">
.container {
  padding: 20px;
}
</style>
```

### 示例 2：自定义主题颜色

效果说明：通过 `theme-vars` 属性自定义主题变量，将品牌主色调改为橙色，并调整按钮的相关样式。所有子组件都会继承这些自定义的样式变量。

```vue
<template>
  <wd-config-provider :theme-vars="customThemeVars">
    <view class="container">
      <wd-cell-group title="自定义主题">
        <wd-cell title="品牌色" value="#FF6B35" />
        <wd-button type="primary" style="margin: 10px;">主要按钮</wd-button>
        <wd-button type="success" style="margin: 10px;">成功按钮</wd-button>
        <wd-button type="warning" style="margin: 10px;">警告按钮</wd-button>
      </wd-cell-group>
      
      <wd-progress :percentage="60" style="margin: 20px 0;" />
      <wd-tag type="primary" style="margin: 0 10px;">主要标签</wd-tag>
    </view>
  </wd-config-provider>
</template>

<script setup lang="ts">
// 自定义主题变量对象
const customThemeVars = {
  // 基础颜色
  '--color-theme': '#FF6B35', // 品牌主色
  '--color-success': '#52C41A', // 成功色
  '--color-warning': '#FAAD14', // 警告色
  '--color-danger': '#F5222D', // 危险色
  
  // 按钮相关
  '--button-primary-color': '#fff',
  '--button-primary-bg-color': '#FF6B35',
  
  // 文字大小
  '--fs-title': '16px',
  '--fs-content': '14px',
  
  // 圆角
  '--button-small-radius': '20px',
  '--button-medium-radius': '22px',
  '--button-large-radius': '24px'
}
</script>

<style scoped lang="scss">
.container {
  padding: 20px;
}
</style>
```

### 示例 3：动态主题变量更新

效果说明：展示如何动态更新主题变量，实现实时的主题切换效果。通过响应式数据绑定，可以随时更改主题变量并立即看到效果。

```vue
<template>
  <wd-config-provider :theme-vars="dynamicThemeVars">
    <view class="container">
      <wd-cell-group title="动态主题配置">
        <wd-input
          label="主色调"
          v-model="primaryColor"
          placeholder="输入十六进制颜色值"
          suffix-icon="color"
        />
        <wd-input
          label="字体大小"
          v-model="fontSize"
          type="digit"
          placeholder="输入字体大小（px）"
          suffix-icon="edit"
        />
        <wd-slider
          label="圆角大小"
          v-model="borderRadius"
          :min="0"
          :max="20"
          :step="1"
        />
      </wd-cell-group>
      
      <view class="preview-area">
        <wd-button type="primary" style="margin: 10px;">预览按钮</wd-button>
        <wd-cell title="预览单元格" value="主题效果" />
        <wd-tag type="primary" style="margin: 10px;">预览标签</wd-tag>
      </view>
    </view>
  </wd-config-provider>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const primaryColor = ref<string>('#1989fa')
const fontSize = ref<string>('14')
const borderRadius = ref<number>(4)

// 动态计算主题变量
const dynamicThemeVars = computed(() => {
  return {
    '--color-theme': primaryColor.value,
    '--fs-content': `${fontSize.value}px`,
    '--button-small-radius': `${borderRadius.value}px`,
    '--button-medium-radius': `${borderRadius.value}px`,
    '--button-large-radius': `${borderRadius.value}px`,
    '--cell-radius': `${borderRadius.value}px`
  }
})
</script>

<style scoped lang="scss">
.container {
  padding: 20px;
}

.preview-area {
  margin-top: 20px;
  padding: 20px;
  background-color: var(--color-bg, #f5f5f5);
  border-radius: 8px;
}
</style>
```

## 注意事项

1. **主题变量命名规范**：在 `theme-vars` 对象中，主题变量应使用 CSS 变量格式，即以 `--` 开头，如 `--color-theme`、`--button-primary-color` 等。

2. **主题继承机制**：ConfigProvider 通过 provide/inject 机制向下传递主题配置，所有嵌套在其中的子组件都会继承该主题设置。

3. **性能考虑**：频繁更新 `theme-vars` 可能会影响性能，建议将主题变量的更新操作进行节流或防抖处理。

4. **主题变量覆盖优先级**：通过 `theme-vars` 传入的变量会覆盖组件库的默认主题变量，但不会影响已经通过组件属性直接设置的样式。

5. **深色模式兼容性**：当启用深色模式时，组件库会自动调整颜色对比度以确保可读性，但仍需测试确保所有组件在深色模式下的视觉效果符合预期。

6. **全局作用域**：ConfigProvider 的主题配置会影响其所有子组件，如果需要局部应用特定主题，可以嵌套使用多个 ConfigProvider。

7. **CSS 变量支持**：ConfigProvider 依赖 CSS 自定义属性，确保目标浏览器支持 CSS Variables 特性。

8. **组件样式隔离**：在某些情况下，可能需要考虑组件样式隔离策略（如 styleIsolation）对主题变量的影响。

9. **主题持久化**：实际项目中，用户的主题偏好通常需要持久化存储（如 localStorage），以便在应用重启后保持用户选择的主题。

10. **虚拟主机配置**：组件内部配置了 `virtualHost: true` 和 `styleIsolation: 'shared'`，在小程序平台组件的根节点样式会直接生效。
