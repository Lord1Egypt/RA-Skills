---
name: "useModal"
description: "Modal 弹窗 composable，提供简洁的模态框显示功能，支持全局/局部模式和函数式调用。. Invoke when user needs to use useModal hook."
url: "https://uviewpro.cn/zh/hooks/useModal.html"
triggers: ["useModal","模态框钩子"]
---

# useModal 弹窗

<demo-model url="/pages/hooks/useModal/index"></demo-model>

Modal 弹窗 composable，提供简洁的模态框显示功能，支持全局/局部模式和函数式调用。

## 概述

`useModal` 是一个函数式调用 Modal 的解决方案：
- 支持两种模式：全局模式（应用级）和局部模式（页面级）
- 提供 `show` 和 `confirm` 两种显示方式
- 支持回调函数（确认/取消事件）
- 兼容函数式调用，不影响原有的组件调用方式

## 引入方式

必须要在全局根组件中引入 `u-modal` 组件，并设置 `global` 属性为 `true`

```html
<template>
    <u-modal global />
</template>
```

```typescript
import { useModal } from 'uview-pro';
const modal = useModal();
modal.show('全局提示');
```

## API

### 函数重载

`useModal` 支持以下调用方式：

```typescript
// 方式1：默认全局模式
const modal = useModal();

// 方式2：指定全局/局部模式
const modal = useModal({ global: true });   // 全局模式
const modal = useModal({ page: true });      // 局部模式（自动使用当前页面路由）
const modal = useModal({ page: 'myPageId' }); // 局部模式（指定 pageId）

// 方式3：简写形式
const modal = useModal(true);   // 全局
const modal = useModal(false);  // 局部（自动使用当前页面路由地址）
```

### 返回值

返回一个包含以下方法的对象：

| 方法                        | 参数                     | 说明                     |
| --------------------------- | ------------------------ | ------------------------ |
| `show(contentOrOptions)`    | `string \| ModalPayload` | 显示 Modal（单按钮）     |
| `confirm(contentOrOptions)` | `string \| ModalPayload` | 显示确认 Modal（双按钮） |
| `close()`                   | -                        | 关闭 Modal               |
| `clearLoading()`            | -                        | 清空 loading 状态        |

## ModalPayload 类型

```typescript
type ModalPayload = Partial<Omit<ModalProps, 'modelValue'>> & {
    /** 标题 */
    title?: string;
    /** 内容 */
    content?: string;
    /** 确认回调 */
    onConfirm?: () => void;
    /** 取消回调 */
    onCancel?: () => void;
};
```

### ModalProps 常用属性

```typescript
type ModalProps = {
    /** 层级z-index */
    zIndex?: number | string;
    /** 弹窗宽度 */
    width?: number | string;
    /** 是否显示标题 */
    showTitle?: boolean;
    /** 是否显示确认按钮 */
    showConfirmButton?: boolean;
    /** 是否显示取消按钮 */
    showCancelButton?: boolean;
    /** 确认文案 */
    confirmText?: string;
    /** 取消文案 */
    cancelText?: string;
    /** 确认按钮颜色 */
    confirmColor?: string;
    /** 取消文字颜色 */
    cancelColor?: string;
    /** 圆角值 */
    borderRadius?: number | string;
    /** 是否开启缩放效果 */
    zoom?: boolean;
    /** 是否异步关闭 */
    asyncClose?: boolean;
    /** 是否允许点击遮罩关闭 */
    maskCloseAble?: boolean;
};
```

## 使用示例

### 基础用法

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

// 默认全局模式
const modal = useModal();

// 显示简单弹窗
modal.show('操作提示');
</script>
```

### 显示确认弹窗

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

// 方式1：直接传入字符串（作为内容）
modal.confirm('确定要删除这条数据吗？');

// 方式2：传入对象
modal.confirm({
    title: '确认删除',
    content: '删除后数据将无法恢复，请确认是否继续？',
    onConfirm: () => {
        console.log('用户点击了确认');
        // 执行删除操作
    },
    onCancel: () => {
        console.log('用户点击了取消');
    }
});
</script>
```

### 自定义按钮文案

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

modal.confirm({
    title: '温馨提示',
    content: '您确定要退出登录吗？',
    confirmText: '退出',
    cancelText: '取消',
    onConfirm: () => {
        // 退出登录
        uni.removeStorageSync('token');
        uni.reLaunch({ url: '/pages/login/index' });
    }
});
```

### 带有标题的弹窗

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

modal.show({
    title: '操作成功',
    content: '您的订单已提交成功，请在“我的订单”中查看详情。'
});
```

### 自定义弹窗宽度和样式

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

modal.confirm({
    title: '自定义弹窗',
    content: '这是一个自定义宽度和样式的弹窗',
    width: 500,
    confirmColor: '#ff4d4f',
    cancelColor: '#999',
    borderRadius: 8,
    onConfirm: () => {
        console.log('确认操作');
    }
});
```

### 异步关闭

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

modal.confirm({
    title: '提交表单',
    content: '确定要提交表单吗？',
    asyncClose: true, // 启用异步关闭
    onConfirm: async () => {
        // 模拟网络请求
        await submitForm();
        // 请求完成后手动关闭
        modal.close();
    },
    onCancel: () => {
        modal.close();
    }
});
```

### 关闭弹窗

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

// 显示弹窗
modal.show({
    title: '提示',
    content: '3秒后自动关闭',
    maskCloseAble: true // 允许点击遮罩关闭
});

// 手动关闭
setTimeout(() => {
    modal.close();
}, 3000);
```

### 使用全局模式

全局模式使用根目录下的 `<u-modal global />`，可在任何页面调用。

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

// 全局模式（默认）
const modal = useModal();
// 或
const modal = useModal({ global: true });
// 或
const modal = useModal(true);

modal.show('全局弹窗提示'); // 整个应用任意位置都能显示
```

**注意：** 使用全局模式时，需要在全局根组件中添加全局 Modal 组件：

```vue
<template>
    <u-modal global />
</template>
```

### 使用局部模式

局部模式使用当前页面的 `<u-modal page />`，不影响其他页面。

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

// 局部模式
const modal = useModal(false);
// 或
const modal = useModal({ page: true });

modal.show('页面内弹窗'); // 只在当前页面显示
```

**注意：** 使用局部模式时，需要在当前页面添加 `<u-modal />` 组件。

```vue
<template>
    <view>
        <!-- 其他内容 -->
        <u-modal page />
    </view>
</template>
```

### 使用自定义 pageId

当页面中存在多个 `<u-modal />` 组件，或者需要在子组件中调用 useModal 并指定特定的 Modal 组件响应时，可以使用自定义 pageId：

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

// 指定 pageId 为 'actionModal'
const modal = useModal({ page: 'actionModal' });

modal.confirm('只会显示在 actionModal 组件上');
</script>
```

在页面中使用带有 pageId 的 Modal 组件：

```vue
<template>
    <view>
        <!-- 普通页面级 Modal -->
        <u-modal page />

        <!-- 指定 pageId 的 Modal，只会响应 useModal({ page: 'actionModal' }) 的调用 -->
        <u-modal page="actionModal" />

        <!-- 另一个指定 pageId 的 Modal -->
        <u-modal page="confirmModal" />
    </view>
</template>
```

**pageId 的作用机制：**

| useModal 调用方式                   | Modal 组件                       | 是否响应 | 说明                        |
| ----------------------------------- | -------------------------------- | -------- | --------------------------- |
| `useModal({ page: 'actionModal' })` | `<u-modal page="actionModal" />` | ✅        | 精确匹配                    |
| `useModal({ page: 'actionModal' })` | `<u-modal page />`               | ❌        | 未指定 pageId，不匹配       |
| `useModal({ page: true })`          | `<u-modal page />`               | ✅        | 使用当前页面路由作为 pageId |
| `useModal(true)` 或 `useModal()`    | `<u-modal global />`             | ✅        | 全局模式                    |

**适用场景：**

1. **子组件中调用**：在子组件中指定父页面的 Modal 组件响应
   ```typescript
   // 子组件中
   const modal = useModal({ page: 'parentModal' });
   modal.confirm('通过子组件触发父页面的 Modal');
   ```

2. **页面中多个 Modal**：不同操作使用不同的 Modal
   ```vue
   <template>
       <view>
           <!-- 普通确认 Modal -->
           <u-modal page />
           <!-- 删除确认 Modal -->
           <u-modal page="deleteConfirm" />
           <!-- 登录过期 Modal -->
           <u-modal page="loginExpired" />
       </view>
   </template>
   ```

   ```typescript
   // 删除操作
   const deleteModal = useModal({ page: 'deleteConfirm' });
   deleteModal.confirm({
       title: '确认删除',
       content: '确定要删除吗？',
       confirmColor: '#ff4d4f'
   });

   // 登录过期处理
   const loginModal = useModal({ page: 'loginExpired' });
   loginModal.confirm({
       title: '登录已过期',
       content: '请重新登录',
       showCancelButton: false
   });
   ```

### 结合实际业务场景

#### 删除确认

```typescript
<script setup lang="ts">
import { useToast } from 'uview-pro';

const modal = useModal();
const toast = useToast();

const handleDelete = (item: any) => {
    modal.confirm({
        title: '确认删除',
        content: `确定要删除「${item.name}」吗？`,
        confirmColor: '#ff4d4f',
        onConfirm: async () => {
            try {
                await deleteItem(item.id);
                toast.success('删除成功');
            } catch (error) {
                toast.error('删除失败');
            }
        },
        onCancel: () => {
            console.log('取消删除');
        }
    });
};
</script>
```

#### 登录过期提示

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

const showLoginExpired = () => {
    modal.confirm({
        title: '登录已过期',
        content: '您的登录状态已过期，请重新登录。',
        confirmText: '重新登录',
        cancelText: '暂不登录',
        onConfirm: () => {
            uni.removeStorageSync('token');
            uni.reLaunch({ url: '/pages/login/index' });
        },
        onCancel: () => {
            uni.switchTab({ url: '/pages/home/index' });
        }
    });
};
```

#### 版本更新提示

```typescript
<script setup lang="ts">
import { useModal } from 'uview-pro';

const modal = useModal();

const checkVersionUpdate = (versionInfo: any) => {
    if (versionInfo.forceUpdate) {
        // 强制更新
        modal.confirm({
            title: '版本更新',
            content: `发现新版本 v${versionInfo.version}，请立即更新以获得更好的体验。`,
            showCancelButton: false, // 隐藏取消按钮
            confirmText: '立即更新',
            onConfirm: () => {
                // 跳转应用商店
                plus.runtime.openURL(versionInfo.downloadUrl);
            }
        });
    } else {
        // 可选更新
        modal.confirm({
            title: '版本更新',
            content: `发现新版本 v${versionInfo.version}，是否更新？`,
            onConfirm: () => {
                plus.runtime.openURL(versionInfo.downloadUrl);
            }
        });
    }
};
```

## 最佳实践

### 封装确认弹窗工具

```typescript
// utils/confirm.ts
import { useModal } from 'uview-pro';

const modal = useModal();

interface ConfirmOptions {
    title?: string;
    content: string;
    confirmText?: string;
    cancelText?: string;
    confirmColor?: string;
    onConfirm?: () => void;
    onCancel?: () => void;
}

export const confirm = (options: ConfirmOptions) => {
    const { title = '确认提示', content, confirmText = '确认', cancelText = '取消', confirmColor, onConfirm, onCancel } = options;
    
    return modal.confirm({
        title,
        content,
        confirmText,
        cancelText,
        confirmColor,
        onConfirm,
        onCancel
    });
};

export const alert = (content: string, title = '提示') => {
    return modal.show({ title, content });
};
```

### 封装删除确认

```typescript
// utils/deleteConfirm.ts
import { useModal } from 'uview-pro';

const modal = useModal();

export const deleteConfirm = (itemName: string, onConfirm: () => void) => {
    return modal.confirm({
        title: '确认删除',
        content: `确定要删除「${itemName}」吗？`,
        confirmColor: '#ff4d4f',
        onConfirm
    });
};
```

## 注意事项

1. **全局模式 vs 局部模式**：
   - 全局模式：使用根目录的 `<u-modal global />`，通常放在全局根组件中
   - 局部模式：需要在当前页面添加 `<u-modal page />`
   - 需要页面/应用中至少存在一个 `<u-modal global />` 或 `<u-modal page />` 实例用于承接事件

2. **show vs confirm**：
   - `show`：显示单按钮弹窗，只有确认按钮
   - `confirm`：显示双按钮弹窗，包含确认和取消按钮

3. **异步关闭**：
   - 使用 `asyncClose: true` 时，需要在 `onConfirm` 回调中手动调用 `modal.close()` 关闭弹窗
   - 适用于需要等待异步操作（如网络请求）完成后才关闭的场景

4. **事件回调**：
   - `onConfirm`：用户点击确认按钮时触发
   - `onCancel`：用户点击取消按钮时触发
   - 点击遮罩关闭不会触发这两个回调

5. **参数兼容**：
   - 支持直接传入字符串作为 `content`
   - 支持传入对象配置所有属性

## 对比其他组件

| 特性     | useModal     | u-modal 组件    |
| -------- | ------------ | --------------- |
| 调用方式 | 函数式调用   | ref 引用调用    |
| 适用场景 | 快速弹窗提示 | 复杂交互/自定义 |
| 全局支持 | ✅            | ✅               |
| 局部支持 | ✅            | ✅               |
| 学习成本 | 低           | 中              |

<ArticleRecommend :articleLinks="['https://mp.weixin.qq.com/s/pkAZ96qITcdsbf7M73gJ-A']" />