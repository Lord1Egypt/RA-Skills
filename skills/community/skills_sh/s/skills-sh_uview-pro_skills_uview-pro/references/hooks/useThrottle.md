---
name: "useThrottle"
description: "节流 composable，用于控制函数在指定时间间隔内只执行一次。. Invoke when user needs to use useThrottle hook."
url: "https://uviewpro.cn/zh/hooks/useThrottle.html"
triggers: ["useThrottle","节流钩子"]
---

# useThrottle 节流

节流 composable，用于控制函数在指定时间间隔内只执行一次。

## 概述

`useThrottle` 是一个轻量级的节流 hook，适用于滚动监听、点击防重复提交等需要限制执行频率的场景。

## 引入方式

```typescript
import { useThrottle } from 'uview-pro';
```

## API

### 返回值

`useThrottle()` 返回一个包含以下方法的对象：

| 方法 | 参数 | 说明 |
|------|------|------|
| `throttle` | `(callback: () => void, throttleTime?: number) => void` | 执行节流函数 |

### throttle(callback, throttleTime)

节流函数，确保在指定时间间隔内只执行一次回调。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `callback` | `() => void` | 是 | - | 要执行的回调函数 |
| `throttleTime` | `number` | 否 | 500 | 节流间隔时间，单位毫秒 |

## 使用示例

### 防止按钮重复点击

```typescript
<script setup lang="ts">
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(500);

// 提交表单
const submitForm = () => {
    console.log('提交表单');
    // uni.request({...})
};

// 节流版本：500ms 内只能提交一次
const throttledSubmit = throttle(submitForm);
</script>

<template>
    <button @click="throttledSubmit">提交</button>
</template>
```

### 滚动到底部加载更多

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(1000);

const page = ref(1);
const hasMore = ref(true);

// 加载更多数据
const loadMore = async () => {
    if (!hasMore.value) return;
    
    const res = await uni.request({
        url: '/api/list',
        data: { page: page.value }
    });
    
    // 处理数据...
    page.value++;
    
    // 如果没有更多数据
    if (res.data.length === 0) {
        hasMore.value = false;
    }
};

// 节流：滚动到底部时 1000ms 内只触发一次加载
const throttledLoadMore = throttle(loadMore, 1000);

// 页面滚动事件处理
const onReachBottom = () => {
    throttledLoadMore();
};
</script>
```

### 窗口滚动监听

```typescript
<script setup lang="ts">
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(200);

// 滚动处理函数
const handleScroll = () => {
    const scrollTop = window.scrollY;
    console.log('滚动位置:', scrollTop);
    
    // 显示/隐藏回到顶部按钮
    if (scrollTop > 500) {
        showBackTop.value = true;
    } else {
        showBackTop.value = false;
    }
};

// 节流：200ms 内只执行一次
const throttledScroll = throttle(handleScroll, 200);

onMounted(() => {
    window.addEventListener('scroll', throttledScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', throttledScroll);
});
```

### 搜索建议（节流版本）

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(300);

const keyword = ref('');
const suggestions = ref([]);

// 获取搜索建议
const fetchSuggestions = async () => {
    if (!keyword.value) {
        suggestions.value = [];
        return;
    }
    
    const res = await uni.request({
        url: '/api/suggestions',
        data: { q: keyword.value }
    });
    suggestions.value = res.data;
};

// 节流：300ms 内只请求一次
const throttledFetch = throttle(fetchSuggestions, 300);

const onInput = (e: any) => {
    keyword.value = e.detail.value;
    throttledFetch();
};
```

### 动态调整节流时间

```typescript
<script setup lang="ts">
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(1000); // 默认 1000ms

// 普通点击：1000ms 间隔
const normalClick = throttle(() => {
    console.log('普通点击');
});

// 快速操作：200ms 间隔
const quickAction = throttle(() => {
    console.log('快速操作');
}, 200);

// 极速操作：50ms 间隔
const fastAction = throttle(() => {
    console.log('极速操作');
}, 50);
```

### 点赞按钮防抖

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useThrottle } from 'uview-pro';

const { throttle } = useThrottle(1000); // 1秒内只能点赞一次

const liked = ref(false);
const likeCount = ref(100);

// 点赞/取消点赞
const toggleLike = async () => {
    if (liked.value) {
        likeCount.value--;
        liked.value = false;
        // 取消点赞接口
    } else {
        likeCount.value++;
        liked.value = true;
        // 点赞接口
    }
};

// 节流：防止连续点击
const throttledToggle = throttle(toggleLike, 1000);
</script>

<template>
    <view class="like-button" @click="throttledToggle">
        <text :class="{ liked: liked }">
            {{ liked ? '已点赞' : '点赞' }}
        </text>
        <text>{{ likeCount }}</text>
    </view>
</template>
```

## 注意事项

1. 节流函数在首次调用时会立即执行，后续调用会等待间隔结束
2. 节流适用于"固定频率执行"的场景
3. 建议根据实际需求调整节流时间
4. 在组件卸载时，需要移除事件监听器
5. 节流常用于：滚动、点击、输入等高频操作

## 原理简述

```typescript
// 核心原理
let previous: number = 0;

function throttle(callback: () => void, throttleTime: number = 500) {
    const now = Date.now();
    if (now - previous > throttleTime) {
        callback(); // 执行回调
        previous = now; // 更新时间戳
    }
}
```

## 对比防抖

| 特性 | 节流 (useThrottle) | 防抖 (useDebounce) |
|------|-------------------|-------------------|
| 执行时机 | 按固定频率执行 | 停止操作后执行一次 |
| 首次调用 | 立即执行 | 等待延迟后执行 |
| 适用场景 | 滚动监听、点击提交 | 搜索输入、验证 |
| 示例 | 滚动到底部加载更多 | 搜索框输入建议 |

## 使用建议

| 场景 | 推荐时间 | 说明 |
|------|----------|------|
| 按钮点击 | 500-1000ms | 防止重复提交 |
| 滚动事件 | 100-300ms | 平滑滚动体验 |
| 输入搜索 | 300-500ms | 平衡响应速度 |
| 窗口 resize | 200-500ms | 避免频繁计算 |
| 点赞/收藏 | 500-1000ms | 防止连续操作 |
