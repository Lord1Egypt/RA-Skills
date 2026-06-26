---
name: "useTheme"
description: "主题管理 composable，提供主题切换、持久化、CSS 变量注入、暗黑模式等功能。. Invoke when user needs to use useTheme hook."
url: "https://uviewpro.cn/zh/hooks/useTheme.html"
triggers: ["useTheme","主题管理"]
---

# useTheme 主题管理

主题管理 composable，提供主题切换、持久化、CSS 变量注入、暗黑模式等功能。

## 概述

`useTheme` 是 uView-Pro 的主题管理系统，支持：
- 多主题切换（品牌色、渐变色等）
- 主题持久化（保存到 Storage）
- CSS 变量自动注入
- 暗黑模式（跟随系统 / 强制亮色 / 强制暗黑）
- 暗黑模式持久化

## 引入方式

```typescript
import { useTheme } from 'uview-pro';
```

## API

### 返回值

`useTheme()` 返回一个包含以下属性和方法的对象：

| 分类 | 属性/方法 | 类型 | 说明 |
|------|----------|------|------|
| **响应式** | `currentTheme` | `Ref<Theme \| null>` | 当前主题信息 |
| | `themes` | `Ref<Theme[]>` | 所有可用主题 |
| | `darkMode` | `Ref<DarkMode>` | 暗黑模式设置 |
| | `cssVars` | `Ref<Record<string, string>>` | CSS 变量映射 |
| **主题方法** | `initTheme(themes?, defaultConfig?, isForce?)` | `function` | 初始化主题系统 |
| | `setTheme(themeName: string)` | `function` | 切换主题 |
| | `getCurrentTheme()` | `function` | 获取当前主题 |
| | `getAvailableThemes()` | `function` | 获取所有可用主题 |
| **暗黑模式** | `initDarkMode(darkMode?, isForce?)` | `function` | 初始化暗黑模式 |
| | `getDarkMode()` | `function` | 获取暗黑模式设置 |
| | `setDarkMode(mode: DarkMode)` | `function` | 设置暗黑模式 |
| | `isInDarkMode()` | `function` | 检查是否处于暗黑模式 |
| | `toggleDarkMode()` | `function` | 切换暗黑模式 |

## 响应式引用

### currentTheme

当前主题信息（响应式）。

```typescript
const { currentTheme } = useTheme();

console.log(currentTheme.value?.name); // 'default'
console.log(currentTheme.value?.color); // 主题颜色配置
console.log(currentTheme.value?.darkColor); // 暗黑模式颜色配置
```

### themes

所有可用主题列表（响应式）。

```typescript
const { themes } = useTheme();

console.log(themes.value);
// [
//   { name: 'default', color: {...}, darkColor: {...} },
//   { name: 'dark', color: {...}, darkColor: {...} }
// ]
```

### darkMode

当前暗黑模式设置（响应式）。

```typescript
const { darkMode } = useTheme();

console.log(darkMode.value); // 'auto' | 'light' | 'dark'
```

### DarkMode 类型

```typescript
type DarkMode = 'auto' | 'light' | 'dark';
```

- `auto` - 跟随系统
- `light` - 强制亮色
- `dark` - 强制暗黑

### cssVars

生成的 CSS 变量映射（响应式）。

```typescript
const { cssVars } = useTheme();

console.log(cssVars.value);
// {
//   '--u-type-primary': '#2979ff',
//   '--u-type-success': '#19be6b',
//   '--u-type-warning': '#ff9900',
//   '--u-type-error': '#fa3534',
//   '--u-bg-color': '#ffffff',
//   ...
// }
```

## 主题方法

### initTheme(themes?, defaultConfig?, isForce?)

初始化主题系统。

```typescript
const { initTheme } = useTheme();

// 使用默认内置主题
initTheme();

// 使用自定义主题
const customThemes = [
    {
        name: 'blue',
        color: {
            primary: '#1890ff',
            success: '#52c41a',
            warning: '#faad14',
            error: '#f5222d'
        }
    },
    {
        name: 'purple',
        color: {
            primary: '#722ed1',
            success: '#52c41a',
            warning: '#faad14',
            error: '#f5222d'
        }
    }
];

initTheme(customThemes, 'blue', true);
```

### setTheme(themeName)

切换主题。

```typescript
const { setTheme, currentTheme } = useTheme();

// 切换到蓝色主题
setTheme('blue');
console.log(currentTheme.value?.name); // 'blue'

// 切换到紫色主题
setTheme('purple');
console.log(currentTheme.value?.name); // 'purple'
```

### getCurrentTheme()

获取当前主题（非响应式）。

```typescript
const { getCurrentTheme } = useTheme();

const theme = getCurrentTheme();
console.log(theme?.name);
console.log(theme?.color);
```

### getAvailableThemes()

获取所有可用主题。

```typescript
const { getAvailableThemes } = useTheme();

const themes = getAvailableThemes();
console.log(themes.map(t => t.name)); // ['default', 'blue', 'purple']
```

## 暗黑模式方法

### initDarkMode(darkMode?, isForce?)

初始化暗黑模式。

```typescript
const { initDarkMode } = useTheme();

// 默认跟随系统
initDarkMode();

// 指定暗黑模式
initDarkMode('auto');
initDarkMode('light');
initDarkMode('dark');

// 强制重新初始化
initDarkMode('auto', true);
```

### getDarkMode()

获取当前暗黑模式设置。

```typescript
const { getDarkMode } = useTheme();

const mode = getDarkMode();
console.log(mode); // 'auto' | 'light' | 'dark'
```

### setDarkMode(mode)

设置暗黑模式。

```typescript
const { setDarkMode, darkMode, isInDarkMode } = useTheme();

// 跟随系统
setDarkMode('auto');

// 强制亮色
setDarkMode('light');

// 强制暗黑
setDarkMode('dark');

console.log(darkMode.value); // 'dark'
console.log(isInDarkMode()); // true（如果系统是暗黑主题）
```

### isInDarkMode()

检查当前是否处于暗黑模式。

```typescript
const { isInDarkMode } = useTheme();

if (isInDarkMode()) {
    console.log('当前是暗黑模式');
} else {
    console.log('当前是亮色模式');
}
```

### toggleDarkMode()

切换暗黑模式（在 light 和 dark 之间切换）。

```typescript
const { toggleDarkMode, isInDarkMode } = useTheme();

// 切换
toggleDarkMode();

console.log(isInDarkMode()); // 切换后的状态
```

## 使用示例

### 基础主题切换

```html
<script setup lang="ts">
import { useTheme } from '@/uni_modules/uview-pro/libs/hooks/useLocale';

const { 
    currentTheme, 
    themes, 
    setTheme, 
    darkMode,
    setDarkMode,
    isInDarkMode 
} = useTheme();

// 主题切换
const onThemeChange = (e: any) => {
    const index = e.detail.value;
    setTheme(themes.value[index].name);
};

// 暗黑模式切换
const onDarkModeChange = (e: any) => {
    const modes = ['auto', 'light', 'dark'];
    setDarkMode(modes[e.detail.value]);
};
</script>

<template>
    <view class="settings">
        <!-- 主题选择 -->
        <picker :value="currentThemeIndex" :range="themeNames" @change="onThemeChange">
            <view class="row">
                <text>主题</text>
                <text>{{ currentTheme?.name }}</text>
            </view>
        </picker>

        <!-- 暗黑模式 -->
        <picker :value="darkModeIndex" :range="darkModeOptions" @change="onDarkModeChange">
            <view class="row">
                <text>暗黑模式</text>
                <text>{{ darkMode }}</text>
            </view>
        </picker>

        <!-- 状态显示 -->
        <view>当前是否暗黑: {{ isInDarkMode() ? '是' : '否' }}</view>
    </view>
</template>
```

### 初始化完整主题系统

```html
<script setup lang="ts">
import { useTheme } from 'uview-pro';

const { initTheme, initDarkMode, currentTheme, darkMode } = useTheme();

// 定义主题
const themes = [
    {
        name: 'default',
        color: {
            primary: '#2979ff',
            success: '#19be6b',
            warning: '#ff9900',
            error: '#fa3534',
            info: '#909399'
        },
        darkColor: {
            primary: '#2979ff',
            success: '#19be6b',
            warning: '#ff9900',
            error: '#fa3534',
            info: '#909399'
        }
    },
    {
        name: 'dark-theme',
        color: {
            primary: '#4caf50',
            success: '#4caf50',
            warning: '#ff9800',
            error: '#f44336',
            info: '#2196f3'
        },
        darkColor: {
            primary: '#81c784',
            success: '#81c784',
            warning: '#ffb74d',
            error: '#e57373',
            info: '#64b5f6'
        }
    }
];

// 初始化
onMounted(() => {
    initTheme(themes, 'default', true);
    initDarkMode('auto');
});
</script>
```

### 结合 CSS 变量使用

```html
<script setup lang="ts">
import { useTheme } from 'uview-pro';

const { cssVars, isInDarkMode } = useTheme();

// 动态样式对象
const dynamicStyle = computed(() => ({
    '--primary-color': cssVars.value['--u-type-primary'],
    '--bg-color': cssVars.value['--u-bg-color'],
    '--text-color': cssVars.value['--u-main-color']
}));
</script>

<template>
    <view :style="dynamicStyle" class="container">
        <view class="card">
            <text class="title">卡片标题</text>
            <text class="desc">卡片内容描述</text>
        </view>
    </view>
</template>

<style>
.container {
    background-color: var(--bg-color);
    color: var(--text-color);
}

.card {
    background-color: var(--u-bg-color);
    border: 1px solid var(--u-border-color);
}

.title {
    color: var(--primary-color);
}
</style>
```

### 暗黑模式监听

```typescript
<script setup lang="ts">
import { useTheme } from 'uview-pro';
import { onShow } from '@dcloudio/uni-app';

const { isInDarkMode } = useTheme();

// 监听页面显示时的暗黑模式状态
onShow(() => {
    if (isInDarkMode()) {
        console.log('当前是暗黑模式');
        // 可以在这里执行暗黑模式相关的初始化操作
    }
});

// 监听主题变化
watch(() => isInDarkMode(), (dark) => {
    if (dark) {
        uni.showToast({ title: '已进入暗黑模式', icon: 'none' });
    } else {
        uni.showToast({ title: '已切换到亮色模式', icon: 'none' });
    }
});
</script>
```

### 主题持久化

主题设置会自动保存到本地存储：

- 主题设置：`uview-pro-theme`
- 暗黑模式：`uview-pro-dark-mode`

```typescript
<script setup lang="ts">
import { useTheme } from 'uview-pro';

const { setTheme, setDarkMode } = useTheme();

// 切换主题（会自动保存）
const changeTheme = (name: string) => {
    setTheme(name);
    // 已在内部保存到 Storage，下次打开应用会应用相同主题
};

// 切换暗黑模式（会自动保存）
const changeDarkMode = (mode: 'auto' | 'light' | 'dark') => {
    setDarkMode(mode);
    // 已在内部保存到 Storage
};
</script>
```

## 注意事项

1. 主题和暗黑模式设置会自动持久化到 Storage
2. `isInDarkMode()` 返回布尔值，表示当前实际显示状态
3. `darkMode` 是设置值，`isInDarkMode()` 是实际显示状态
4. CSS 变量会自动注入到页面，无需手动设置
5. 建议在 `App.vue` 或入口文件中调用 `initTheme` 初始化
6. 暗黑模式切换会触发响应式更新，UI 自动适配
