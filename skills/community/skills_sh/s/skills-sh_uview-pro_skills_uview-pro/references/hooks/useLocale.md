---
name: "useLocale"
description: "国际化 composable，提供多语言支持，包括语言切换、翻译功能、响应式引用等。. Invoke when user needs to use useLocale hook."
url: "https://uviewpro.cn/zh/hooks/useLocale.html"
triggers: ["useLocale","国际化"]
---

# useLocale 国际化

国际化 composable，提供多语言支持，包括语言切换、翻译功能、响应式引用等。

## 概述

`useLocale` 是 uView-Pro 的国际化解决方案，支持：
- 多语言切换
- 带占位符的翻译
- 命名空间支持
- 响应式语言状态
- 语言包动态加载

## 引入方式

```typescript
import { useLocale } from 'uview-pro';
```

## API

### 基本用法

```typescript
const locale = useLocale();
// locale 包含所有国际化相关的方法和属性
```

### 命名空间用法

```typescript
// 为特定模块创建带有命名空间的翻译函数
const { t } = useLocale('common');
// t('title') 等同于 t('common.title')
```

### 返回值

`useLocale()` 返回一个包含以下属性的对象：

| 属性/方法 | 类型 | 说明 |
|----------|------|------|
| `currentLocale` | `Ref<LocaleInfo>` | 当前语言信息（响应式） |
| `locales` | `Ref<LocaleInfo[]>` | 可用语言列表（响应式） |
| `t` | `(key, replacements?, localeName?) => string` | 翻译函数 |
| `setLocale` | `(name: string) => void` | 切换语言 |
| `getLocales` | `() => LocaleInfo[]` | 获取可用语言列表 |
| `getCurrentLocale` | `() => LocaleInfo` | 获取当前语言信息 |
| `initLocales` | `(locales?, defaultLocaleName?, isForce?) => void` | 初始化语言包 |

## currentLocale

当前语言的响应式引用，包含语言代码、名称等信息。

```typescript
const { currentLocale } = useLocale();

console.log(currentLocale.value.name); // 'zh-CN'
console.log(currentLocale.value.label); // '简体中文'
console.log(currentLocale.value.locale); // 'zh-Hans'
```

### LocaleInfo 结构

```typescript
interface LocaleInfo {
    name: string;      // 语言代码，如 'zh-CN', 'en-US'
    label: string;      // 显示名称，如 '简体中文', 'English'
    locale: string;    // locale 标识，如 'zh-Hans', 'en'
}
```

## locales

所有可用语言的列表（响应式）。

```typescript
const { locales } = useLocale();

console.log(locales.value);
// [
//   { name: 'zh-CN', label: '简体中文', locale: 'zh-Hans' },
//   { name: 'en-US', label: 'English', locale: 'en' },
//   { name: 'ja-JP', label: '日本語', locale: 'ja' }
// ]
```

## t(key, replacements?, localeName?)

翻译函数，将语言 key 翻译为对应文本。

### 基本翻译

```typescript
const { t } = useLocale();

// 简单文本
t('hello'); // '你好'

// 带命名空间
const locale = useLocale('common');
t('title'); // 'common.title' 或对应的翻译文本
```

### 占位符替换

```typescript
const { t } = useLocale();

// 语言包
const messages = {
    greeting: '你好, {name}!',
    count: '共有 {count} 个项目'
};

// 替换占位符
t('greeting', { name: '张三' }); // '你好, 张三!'
t('count', { count: 10 });      // '共有 10 个项目'
```

### 指定语言

```typescript
const { t } = useLocale();

// 获取指定语言的翻译（不切换当前语言）
t('hello', {}, 'en-US'); // 'Hello'
t('title', {}, 'ja-JP'); // 'タイトル'
```

### 完整示例

```typescript
// language/zh-CN.ts
export default {
    common: {
        confirm: '确定',
        cancel: '取消',
        save: '保存',
        delete: '删除',
        edit: '编辑',
        loading: '加载中...',
        noData: '暂无数据'
    },
    home: {
        welcome: '欢迎回来，{name}',
        title: '首页',
        desc: '这是您的个人中心'
    },
    errors: {
        network: '网络连接失败，请检查网络',
        server: '服务器错误，请稍后重试',
        notFound: '页面不存在'
    }
};

// language/en-US.ts
export default {
    common: {
        confirm: 'Confirm',
        cancel: 'Cancel',
        save: 'Save',
        delete: 'Delete',
        edit: 'Edit',
        loading: 'Loading...',
        noData: 'No data'
    },
    home: {
        welcome: 'Welcome back, {name}',
        title: 'Home',
        desc: 'This is your personal center'
    },
    errors: {
        network: 'Network connection failed, please check your network',
        server: 'Server error, please try again later',
        notFound: 'Page not found'
    }
};
```

## setLocale(name)

切换当前语言。

```typescript
const { setLocale, currentLocale } = useLocale();

// 切换到英文
setLocale('en-US');
console.log(currentLocale.value.name); // 'en-US'

// 切换到日文
setLocale('ja-JP');
console.log(currentLocale.value.name); // 'ja-JP'
```

### 在模板中使用

```typescript
<script setup lang="ts">
import { useLocale } from 'uview-pro';

const { currentLocale, locales, setLocale } = useLocale();

const onLocaleChange = (e: any) => {
    setLocale(e.detail.value);
};
</script>

<template>
    <picker :value="currentLocaleIndex" :range="localeOptions" @change="onLocaleChange">
        <view>当前语言: {{ currentLocale.name }}</view>
    </picker>
</template>
```

## getLocales()

获取可用语言列表（非响应式）。

```typescript
const { getLocales } = useLocale();

const availableLocales = getLocales();
// 返回语言列表数组
```

## getCurrentLocale()

获取当前语言信息（非响应式）。

```typescript
const { getCurrentLocale } = useLocale();

const current = getCurrentLocale();
console.log(current.name);
console.log(current.label);
```

## initLocales(locales?, defaultLocaleName?, isForce?)

初始化语言包。

```typescript
const { initLocales } = useLocale();

// 定义语言包
const locales = [
    { name: 'zh-CN', label: '简体中文', locale: 'zh-Hans' },
    { name: 'en-US', label: 'English', locale: 'en' }
];

// 初始化
initLocales(locales, 'zh-CN', true);
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `locales` | `LocaleInfo[]` | 否 | 语言列表 |
| `defaultLocaleName` | `string` | 否 | 默认语言代码 |
| `isForce` | `boolean` | 否 | 是否强制重新初始化 |

## 使用示例

### 完整的语言切换功能

```html
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useLocale } from 'uview-pro';

// 定义语言包
const languageData = [
    {
        name: 'zh-CN',
        label: '简体中文',
        locale: 'zh-Hans',
        common: {
            confirm: '确定',
            cancel: '取消',
            save: '保存'
        }
    },
    {
        name: 'en-US',
        label: 'English',
        locale: 'en',
        common: {
            confirm: 'Confirm',
            cancel: 'Cancel',
            save: 'Save'
        }
    }
];

const locale = useLocale('common');

// 初始化语言包
locale.initLocales(languageData, 'zh-CN');

// 当前语言选项
const localeOptions = computed(() => {
    return locale.locales.value.map(l => l.name);
});

const currentLocaleIndex = computed(() => {
    return locale.locales.value.findIndex(l => l.name === locale.currentLocale.value.name);
});

const onLocaleChange = (e: any) => {
    const index = e.detail.value;
    const selected = locale.locales.value[index];
    locale.setLocale(selected.name);
};
</script>

<template>
    <view class="container">
        <!-- 语言选择器 -->
        <picker 
            :value="currentLocaleIndex" 
            :range="localeOptions" 
            @change="onLocaleChange"
        >
            <view class="picker">
                当前语言: {{ currentLocale.label }}
            </view>
        </picker>

        <!-- 翻译文本 -->
        <view class="content">
            <text>{{ t('common.confirm') }}</text>
            <text>{{ t('common.cancel') }}</text>
            <text>{{ t('common.save') }}</text>
        </view>
    </view>
</template>
```

### 在组件中使用翻译

```typescript
<script setup lang="ts">
import { useLocale } from 'uview-pro';

// 带命名空间的用法
const { t } = useLocale('button');

const buttonText = computed(() => t('submit'));
</script>

<template>
    <button>{{ buttonText }}</button>
</template>
```

### 结合 u-config-provider 使用

```html
<!-- App.vue 或页面组件 -->
<script setup lang="ts">
import { useLocale } from 'uview-pro';

const locale = useLocale();

// 监听语言变化
watch(() => locale.currentLocale.value.name, (newVal) => {
    console.log('语言切换为:', newVal);
});
</script>

<template>
    <u-config-provider :locale="locale.currentLocale.value.locale">
        <view class="app">
            <text>{{ t('hello') }}</text>
        </view>
    </u-config-provider>
</template>
```

## 注意事项

1. `t` 函数返回的是翻译后的字符串，不是响应式引用
2. 如果 key 不存在，会返回原始 key
3. 建议为不同模块使用命名空间，避免 key 冲突
4. 语言包通常在应用初始化时加载，建议配合 `initLocales` 使用
5. `currentLocale` 和 `locales` 是响应式的，可直接在模板中使用
