---
name: "useDebounce"
description: "防抖 composable，用于控制函数在指定时间间隔内只执行最后一次调用。. Invoke when user needs to use useDebounce hook."
url: "https://uviewpro.cn/zh/hooks/useDebounce.html"
triggers: ["useDebounce","防抖钩子"]
---

# useDebounce 防抖

防抖 composable，用于控制函数在指定时间间隔内只执行最后一次调用。

## 概述

`useDebounce` 是一个轻量级的防抖 hook，适用于搜索框输入、窗口缩放等需要限制频繁操作的场景。

## 引入方式

```typescript
import { useDebounce } from 'uview-pro';
```

## API

### 返回值

`useDebounce()` 返回一个包含以下方法的对象：

| 方法 | 参数 | 说明 |
|------|------|------|
| `debounce` | `(callback: () => void, debounceTime?: number) => void` | 执行防抖函数 |

### debounce(callback, debounceTime)

防抖函数，确保在延迟时间结束后才执行回调。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `callback` | `() => void` | 是 | - | 防抖结束后要执行的回调函数 |
| `debounceTime` | `number` | 否 | 500 | 防抖延迟时间，单位毫秒 |

## 使用示例

### 搜索框防抖

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useDebounce } from 'uview-pro';

const searchKeyword = ref('');
const searchResult = ref([]);

// 创建防抖函数，默认 500ms
const { debounce } = useDebounce();

// 搜索处理函数
const handleSearch = () => {
    console.log('执行搜索:', searchKeyword.value);
    // 调用搜索接口
    // searchApi(searchKeyword.value).then(...)
};

// 防抖版本：输入停止 500ms 后才执行搜索
const onSearchInput = debounce(handleSearch, 500);
</script>

<template>
    <input 
        v-model="searchKeyword" 
        @input="onSearchInput" 
        placeholder="请输入搜索关键词"
    />
</template>
```

### 表单验证防抖

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useDebounce } from 'uview-pro';

const username = ref('');
const errorMsg = ref('');

const { debounce } = useDebounce();

// 用户名验证
const validateUsername = () => {
    if (username.value.length < 3) {
        errorMsg.value = '用户名至少3个字符';
    } else {
        errorMsg.value = '';
    }
};

// 防抖验证：停止输入后 300ms 验证
const debouncedValidate = debounce(validateUsername, 300);
</script>

<template>
    <view>
        <input v-model="username" @input="debouncedValidate" />
        <text v-if="errorMsg" class="error">{{ errorMsg }}</text>
    </view>
</template>
```

### 窗口 resize 防抖

```typescript
<script setup lang="ts">
import { useDebounce } from 'uview-pro';

const { debounce } = useDebounce();

// 处理窗口大小变化
const handleResize = () => {
    console.log('窗口大小已调整');
    // 重新计算布局等操作
};

// 500ms 后执行，确保用户停止调整后再处理
const debouncedResize = debounce(handleResize, 500);

// 在 onMounted 中绑定事件
onMounted(() => {
    window.addEventListener('resize', debouncedResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', debouncedResize);
});
```

### 动态调整防抖时间

```typescript
<script setup lang="ts">
import { useDebounce } from 'uview-pro';

const { debounce } = useDebounce(1000); // 默认 1000ms

// 保存操作
const saveData = () => {
    console.log('保存数据');
};

// 使用默认 1000ms
const debouncedSave = debounce(saveData);

// 使用自定义时间：200ms
const quickAction = debounce(() => {
    console.log('快速操作');
}, 200);
```

### 与 API 请求结合

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useDebounce } from 'uview-pro';

const { debounce } = useDebounce();

const suggestions = ref([]);
const isLoading = ref(false);

// 获取搜索建议
const fetchSuggestions = async (keyword: string) => {
    if (!keyword) {
        suggestions.value = [];
        return;
    }
    
    isLoading.value = true;
    try {
        const res = await uni.request({
            url: '/api/suggestions',
            data: { q: keyword }
        });
        suggestions.value = res.data;
    } finally {
        isLoading.value = false;
    }
};

// 防抖获取建议：输入停止后 300ms
const debouncedFetch = debounce(fetchSuggestions, 300);

const onInput = (e: any) => {
    const keyword = e.detail.value;
    debouncedFetch(keyword);
};
</script>

<template>
    <view>
        <input @input="onInput" placeholder="搜索建议" />
        <view v-if="isLoading">加载中...</view>
        <view v-for="item in suggestions" :key="item.id">
            {{ item.name }}
        </view>
    </view>
</template>
```

## 注意事项

1. 防抖函数每次调用都会重置计时器
2. 如果在延迟时间内多次调用，之前未执行的回调会被取消
3. 防抖适用于"停止操作后执行"的场景
4. 建议根据实际需求调整防抖时间，避免过长影响用户体验
5. 在组件卸载时，需要手动清除防抖定时器（当前实现会在下次调用时自动清除）

## 原理简述

```typescript
// 核心原理
let timeout: ReturnType<typeof setTimeout> | null = null;

function debounce(callback: () => void, debounceTime: number = 500) {
    if (timeout) clearTimeout(timeout); // 清除之前的定时器
    timeout = setTimeout(() => {
        callback(); // 执行回调
    }, debounceTime);
}
```

## 对比节流

| 特性 | 防抖 (useDebounce) | 节流 (useThrottle) |
|------|-------------------|-------------------|
| 执行时机 | 停止操作后执行一次 | 按固定频率执行 |
| 适用场景 | 搜索输入、验证 | 滚动监听、点击提交 |
