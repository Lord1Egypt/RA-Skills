---
name: "useToast"
description: "Toast 提示 composable，提供简洁的 Toast 显示功能，支持多种类型和全局/局部模式。. Invoke when user needs to use useToast hook."
url: "https://uviewpro.cn/zh/hooks/useToast.html"
triggers: ["useToast","轻提示钩子"]
---

# useToast 提示

<demo-model url="/pages/hooks/useToast/index"></demo-model>

Toast 提示 composable，提供简洁的 Toast 显示功能，支持多种类型和全局/局部模式。

## 概述

`useToast` 是一个函数式调用 Toast 的解决方案：
- 支持多种 Toast 类型：success、error、warning、info、loading
- 支持两种模式：全局模式（页面任意位置）和局部模式（页面内指定位置）
- 兼容函数式调用和 ref 调用两种方式

## 引入方式

必须要在全局根组件中引入 `u-toast` 组件，并设置 `global` 属性为 `true`

```html
<template>
    <u-toast global />
</template>
```

```typescript
<script setup lang="ts">
    import { useToast } from 'uview-pro';

    const toast = useToast();
    toast.success('操作成功');
</script>
```

## API

### 函数重载

`useToast` 支持以下调用方式：

```typescript
// 方式1：默认全局模式
const toast = useToast();

// 方式2：指定全局/局部模式
const toast = useToast({ global: true });   // 全局模式
const toast = useToast({ page: true });      // 局部模式（自动使用当前页面路由）
const toast = useToast({ page: 'myPageId' }); // 局部模式（指定 pageId）

// 方式3：简写形式
const toast = useToast(true);   // 全局
const toast = useToast(false);  // 局部（自动使用当前页面路由地址）
```

### 返回值

返回一个包含以下方法的对象：

| 方法 | 参数 | 说明 |
|------|------|------|
| `show(titleOrOptions)` | `string \| ToastPayload` | 显示 Toast |
| `close()` | - | 关闭 Toast |
| `success(titleOrOptions)` | `string \| ToastPayload` | 显示成功 Toast |
| `error(titleOrOptions)` | `string \| ToastPayload` | 显示错误 Toast |
| `warning(titleOrOptions)` | `string \| ToastPayload` | 显示警告 Toast |
| `info(titleOrOptions)` | `string \| ToastPayload` | 显示信息 Toast |
| `loading(titleOrOptions)` | `string \| ToastPayload` | 显示加载 Toast |

## ToastPayload 类型

```typescript
type ToastPayload = {
    title?: string;        // 提示内容
    type?: ThemeType;      // Toast 类型
    duration?: number;     // 显示时长（毫秒），0 表示不自动关闭
    loading?: boolean;     // 是否为加载状态
    icon?: boolean;         // 是否显示图标
    callback?: () => void; // 关闭后的回调
};
```

### ThemeType 类型

```typescript
type ThemeType = 'primary' | 'success' | 'warning' | 'error' | 'info' | 'default';
```

## 使用示例

### 基础用法

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

// 默认全局模式
const toast = useToast();

// 显示简单提示
toast.show('操作成功');

</script>
```

### 成功提示

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

// 方式1：直接传入字符串
toast.success('保存成功');

// 方式2：传入对象
toast.success({
    title: '保存成功',
    duration: 2000
});
</script>
```

### 错误提示

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

// 错误提示
toast.error('网络请求失败');

// 带时长
toast.error({
    title: '操作失败，请重试',
    duration: 3000
});
```

### 警告提示

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

toast.warning('请先登录后再操作');

toast.warning({
    title: '账号已过期，请重新登录',
    duration: 3000
});
```

### 信息提示

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

toast.info('新版本已发布');

toast.info({
    title: '您有 3 条未读消息',
    duration: 5000
});
```

### 加载提示

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

// 显示加载提示
toast.loading('正在提交...');

// 加载提示默认不自动关闭，需要手动调用 close
const submitForm = async () => {
    toast.loading('正在提交...');
    
    try {
        await uni.request({
            url: '/api/submit',
            method: 'POST',
            data: formData
        });
        toast.success('提交成功');
    } catch (error) {
        toast.error('提交失败');
    } finally {
        toast.close();
    }
};

// 自定义加载时长
toast.loading({
    title: '正在加载...',
    duration: 10000 // 10秒后自动关闭
});
```

### 关闭 Toast

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

// 显示加载
toast.loading('正在处理...');

// 延迟关闭
setTimeout(() => {
    toast.close();
}, 2000);

// 或在操作完成后关闭
const processData = async () => {
    toast.loading('处理中...');
    await process();
    toast.close();
    toast.success('处理完成');
};
```

### 使用全局模式

全局模式使用根目录下的 `<u-toast global />`，可在任何页面调用。

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

// 全局模式（默认）
const toast = useToast();
// 或
const toast = useToast({ global: true });
// 或
const toast = useToast(true);

toast.success('全局提示'); // 整个应用任意位置都能显示
</script>
```

### 使用局部模式

局部模式使用当前页面的 `<u-toast page />`，不影响其他页面。

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

// 局部模式
const toast = useToast(false);
// 或
const toast = useToast({ page: true });

toast.success('页面内提示'); // 只在当前页面显示
</script>
```

**注意：** 使用局部模式时，需要在当前页面添加 `<u-toast page />` 组件。

```vue
<template>
    <view>
        <!-- 其他内容 -->
        <u-toast page />
    </view>
</template>
```

### 使用自定义 pageId

当页面中存在多个 `<u-toast />` 组件，或者需要在子组件中调用 useToast 并指定特定的 Toast 组件响应时，可以使用自定义 pageId：

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

// 指定 pageId 为 'headerToast'
const toast = useToast({ page: 'headerToast' });

toast.success('只会显示在 headerToast 组件上');
</script>
```

在页面中使用带有 pageId 的 Toast 组件：

```vue
<template>
    <view>
        <!-- 普通页面级 Toast -->
        <u-toast page />

        <!-- 指定 pageId 的 Toast，只会响应 useToast({ page: 'headerToast' }) 的调用 -->
        <u-toast page="headerToast" />

        <!-- 另一个指定 pageId 的 Toast -->
        <u-toast page="footerToast" />
    </view>
</template>
```

**pageId 的作用机制：**

| useToast 调用方式                   | Toast 组件                       | 是否响应 | 说明                        |
| ----------------------------------- | -------------------------------- | -------- | --------------------------- |
| `useToast({ page: 'headerToast' })` | `<u-toast page="headerToast" />` | ✅        | 精确匹配                    |
| `useToast({ page: 'headerToast' })` | `<u-toast page />`               | ❌        | 未指定 pageId，不匹配       |
| `useToast({ page: true })`          | `<u-toast page />`               | ✅        | 使用当前页面路由作为 pageId |
| `useToast(true)` 或 `useToast()`    | `<u-toast global />`             | ✅        | 全局模式                    |

**适用场景：**

1. **子组件中调用**：在子组件中指定父页面的 Toast 组件响应
   ```typescript
   // 子组件中
   const toast = useToast({ page: 'parentToast' });
   toast.success('通过子组件触发父页面的 Toast');
   ```

2. **页面中多个 Toast**：不同区域显示不同的 Toast
   ```vue
   <template>
       <view>
           <!-- 顶部提示区域 -->
           <u-toast page="topArea" />
           <!-- 底部提示区域 -->
           <u-toast page="bottomArea" />
       </view>
   </template>
   ```

### 完整示例

```typescript
<script setup lang="ts">
import { ref } from 'vue';
import { useToast } from 'uview-pro';

const toast = useToast({ page: true }); // 局部模式

const formData = ref({
    username: '',
    password: ''
});

const login = async () => {
    // 验证
    if (!formData.value.username) {
        toast.error('请输入用户名');
        return;
    }
    
    if (!formData.value.password) {
        toast.error('请输入密码');
        return;
    }
    
    // 显示加载
    toast.loading('登录中...');
    
    try {
        // 发起请求
        const res = await uni.request({
            url: '/api/login',
            method: 'POST',
            data: formData.value
        });
        
        if (res.code === 0) {
            toast.success('登录成功');
            // 跳转到首页
            uni.navigateTo({ url: '/pages/home/index' });
        } else {
            toast.error(res.message || '登录失败');
        }
    } catch (error) {
        toast.error('网络错误，请重试');
    }
};
</script>

<template>
    <view class="login-page">
        <input 
            v-model="formData.username" 
            placeholder="用户名" 
        />
        <input 
            v-model="formData.password" 
            type="password" 
            placeholder="密码" 
        />
        <button @click="login">登录</button>
        
        <!-- 局部 Toast 组件 -->
        <u-toast page />
    </view>
</template>
```

### 结合回调使用

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

toast.show({
    title: '操作成功',
    duration: 2000,
    callback: () => {
        console.log('Toast 已关闭');
        // 执行后续操作
        uni.navigateBack();
    }
});
```

## 最佳实践

### API 请求封装

```typescript
// utils/request.ts
import { useToast } from 'uview-pro';

const toast = useToast();

interface RequestOptions {
    url: string;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    data?: any;
    loadingText?: string;
    successMessage?: string;
    errorMessage?: string;
}

export const request = async (options: RequestOptions) => {
    const {
        url,
        method = 'GET',
        data = {},
        loadingText = '加载中...',
        successMessage,
        errorMessage
    } = options;
    
    // 显示加载
    toast.loading(loadingText);
    
    try {
        const res = await uni.request({
            url,
            method,
            data
        });
        
        toast.close();
        
        if (res.code === 0) {
            if (successMessage) {
                toast.success(successMessage);
            }
            return res.data;
        } else {
            toast.error(errorMessage || res.message || '请求失败');
            throw new Error(res.message);
        }
    } catch (error) {
        toast.close();
        toast.error(errorMessage || '网络错误');
        throw error;
    }
};
```

### 表单提交

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const toast = useToast();

const submitOrder = async () => {
    // 验证
    if (!validateForm()) {
        return;
    }
    
    toast.loading('正在提交订单...');
    
    try {
        await createOrder(orderData);
        toast.success('订单提交成功');
        setTimeout(() => {
            uni.redirectTo({ url: '/pages/order/success' });
        }, 1500);
    } catch (error) {
        toast.error('订单提交失败，请重试');
    }
};
```

## 注意事项

1. **全局模式 vs 局部模式**：
   - 全局模式：使用根目录的 `<u-toast global />`，无需在每个页面添加组件
   - 局部模式：需要在当前页面添加 `<u-toast page />`
   - ref模式：使用 ref 获取组件实例，然后调用组件实例的方法 `<u-toast ref="toast" />`

2. **loading 不会自动关闭**：需要手动调用 `toast.close()` 关闭

3. **建议在请求场景使用 loading**：然后在成功/失败时调用 `close()` 再显示结果

4. **回调时机**：callback 在 Toast 关闭后执行，包括自动关闭和手动关闭

## 对比其他组件

| 特性 | useToast | u-toast 组件 |
|------|----------|-------------|
| 调用方式 | 函数式调用 | ref 引用调用 |
| 适用场景 | 快速提示 | 复杂交互 |
| 全局支持 | ✅ | ✅ |
| 局部支持 | ✅ | ✅ |
| 学习成本 | 低 | 中 |

<ArticleRecommend :articleLinks="['https://mp.weixin.qq.com/s/pkAZ96qITcdsbf7M73gJ-A']" />
