---
name: vue3-antd-commons-skill
description: Vue3全家桶+Ant Design+publish-commons开发技能总结，包含核心特性、TypeScript集成、主题定制、网络请求等内容
---

# Vue3全家桶 + Ant Design 技能总结

## 前言

本技能总结涵盖Vue3全家桶与Ant Design结合开发的核心知识，包括Vue3核心特性、TypeScript集成、Ant Design组件库使用、主题定制、网络请求、状态管理等内容，帮助开发者快速掌握Vue3+Ant Design项目开发技能。

## 第1章 Vue3核心特性

### 1.1 Composition API

```vue
<template>
  <div>
    <p>计数：{{ count }}</p>
    <button @click="increment">+1</button>
    <button @click="decrement">-1</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 响应式数据
const count = ref<number>(0)

// 计算属性
const doubleCount = computed(() => count.value * 2)

// 方法
const increment = () => count.value++
const decrement = () => count.value--

// 生命周期钩子
onMounted(() => {
  console.log('组件挂载完成')
})

onUnmounted(() => {
  console.log('组件卸载完成')
})
</script>
```

### 1.2 响应式系统

#### 1.2.1 ref vs reactive

```typescript
import { ref, reactive } from 'vue'

// ref - 用于基本类型和对象
const count = ref<number>(0)
const user = ref<User>({ name: '张三', age: 25 })

// reactive - 用于对象
const state = reactive({
  count: 0,
  user: { name: '张三', age: 25 }
})

// 访问方式
console.log(count.value) // ref需要.value
console.log(state.count) // reactive直接访问
```

#### 1.2.2 响应式API

```typescript
import { ref, reactive, shallowRef, readonly, toRef, toRefs } from 'vue'

// shallowRef - 浅层响应式
const shallowState = shallowRef({ count: 0 })

// readonly - 只读响应式
const readonlyState = readonly(reactive({ count: 0 }))

// toRef - 创建单个ref
const state = reactive({ count: 0 })
const countRef = toRef(state, 'count')

// toRefs - 创建多个ref
const { count } = toRefs(state)
```

### 1.3 生命周期钩子

```typescript
import { onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

onBeforeMount(() => {
  console.log('组件挂载前')
})

onMounted(() => {
  console.log('组件挂载完成')
})

onBeforeUpdate(() => {
  console.log('组件更新前')
})

onUpdated(() => {
  console.log('组件更新完成')
})

onBeforeUnmount(() => {
  console.log('组件卸载前')
})

onUnmounted(() => {
  console.log('组件卸载完成')
})
```

## 第2章 TypeScript集成

### 2.1 组件类型定义

#### 2.1.1 Props类型定义

```vue
<script setup lang="ts">
// 基本类型
interface Props {
  title: string
  count?: number
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  disabled: false
})
</script>
```

#### 2.1.2 Emits类型定义

```vue
<script setup lang="ts">
interface Emits {
  (e: 'update', value: number): void
  (e: 'submit', data: FormData): void
  (e: 'cancel'): void
}

const emit = defineEmits<Emits>()

const handleUpdate = (value: number) => {
  emit('update', value)
}
</script>
```

#### 2.1.3 组件暴露类型定义

```vue
<script setup lang="ts">
const count = ref(0
const increment = () => count.value++

defineExpose({
  count,
  increment
})
</script>
```

### 2.2 路由类型定义

```typescript
import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/user/:id',
    name: 'User',
    component: () => import('@/views/User.vue'),
    props: true
  }
]
```

### 2.3 Pinia类型定义

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => !!user.value)

  const setUser = (userData: User) => {
    user.value = userData
  }

  const clearUser = () => {
    user.value = null
  }

  return {
    user,
    isLoggedIn,
    setUser,
    clearUser
  }
})
```

## 第3章 Ant Design Vue组件库

### 3.1 基础组件使用

```vue
<template>
  <a-space direction="vertical">
    <a-button type="primary" @click="handleClick">主要按钮</a-button>
    <a-button type="default">默认按钮</a-button>
    <a-button type="dashed">虚线按钮</a-button>
    <a-button type="text">文本按钮</a-button>
    <a-button type="link">链接按钮</a-button>
  </a-space>
</template>

<script setup lang="ts">
const handleClick = () => {
  console.log('按钮被点击')
}
</script>
```

### 3.2 表单组件

```vue
<template>
  <a-form
    :model="formData"
    :rules="rules"
    @finish="handleSubmit"
  >
    <a-form-item label="用户名" name="username">
      <a-input v-model:value="formData.username" />
    </a-form-item>

    <a-form-item label="密码" name="password">
      <a-input-password v-model:value="formData.password" />
    </a-form-item>

    <a-form-item label="邮箱" name="email">
      <a-input v-model:value="formData.email" />
    </a-form-item>

    <a-form-item>
      <a-button type="primary" html-type="submit">提交</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { Rule } from 'ant-design-vue/es/form'

interface FormData {
  username: string
  password: string
  email: string
}

const formData = reactive<FormData>({
  username: '',
  password: '',
  email: ''
})

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, message: '请输入用户名' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { min: 6, message: '密码长度不能少于6位' }
  ],
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '请输入有效的邮箱地址' }
  ]
}

const handleSubmit = (values: FormData) => {
  console.log('表单提交', values)
}
</script>
```

### 3.3 表格组件

```vue
<template>
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :loading="loading"
    :pagination="pagination"
    @change="handleTableChange"
  />
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { TableProps, ColumnType } from 'ant-design-vue'

interface User {
  id: number
  name: string
  age: number
  email: string
}

const columns: ColumnType<User>[] = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id'
  },
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '年龄',
    dataIndex: 'age',
    key: 'age'
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    key: 'email'
  }
]

const dataSource = ref<User[]>([
  { id: 1, name: '张三', age: 25, email: 'zhangsan@example.com' },
  { id: 2, name: '李四', age: 30, email: 'lisi@example.com' }
])

const loading = ref(false)

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0
})

const handleTableChange: TableProps['onChange'] = (pag, filters, sorter) => {
  console.log('表格变化', pag, filters, sorter)
}
</script>
```

## 第4章 Vue Router路由管理

### 4.1 路由配置

```typescript
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue')
  },
  {
    path: '/user/:id',
    name: 'User',
    component: () => import('@/views/User.vue'),
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

### 4.2 路由守卫

```typescript
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  console.log('路由跳转', to, from)
  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  console.log('路由跳转完成', to, from)
})

export default router
```

### 4.3 编程式导航

```typescript
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 导航到指定路由
const navigateToHome = () => {
  router.push('/')
}

// 导航到命名路由
const navigateToUser = (id: number) => {
  router.push({ name: 'User', params: { id } })
}

// 导航到带查询参数的路由
const navigateToSearch = (query: string) => {
  router.push({ path: '/search', query: { q: query } })
}

// 替换当前路由
const replaceRoute = () => {
  router.replace('/')
}

// 后退
const goBack = () => {
  router.go(-1)
}
```

## 第5章 Pinia状态管理

### 5.1 Store定义

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)

  const increment = () => {
    count.value++
  }

  const decrement = () => {
    count.value--
  }

  const reset = () => {
    count.value = 0
  }

  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset
  }
})
```

### 5.2 Store使用

```vue
<template>
  <div>
    <p>计数：{{ counterStore.count }}</p>
    <p>双倍计数：{{ counterStore.doubleCount }}</p>
    <button @click="counterStore.increment()">+1</button>
    <button @click="counterStore.decrement()">-1</button>
    <button @click="counterStore.reset()">重置</button>
  </div>
</template>

<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const counterStore = useCounterStore()
</script>
```

## 第6章 网络请求与API

### 6.1 Fetch封装

```typescript
interface RequestConfig extends RequestInit {
  timeout?: number
  token?: string
}

interface ResponseData<T = any> {
  code: number
  data: T
  message: string
}

class HttpClient {
  private baseURL: string
  private timeout: number
  private token: string | null

  constructor(baseURL: string = '', timeout: number = 5000) {
    this.baseURL = baseURL
    this.timeout = timeout
    this.token = localStorage.getItem('token')
  }

  private async request<T>(url: string, config: RequestConfig = {}): Promise<ResponseData<T>> {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), config.timeout || this.timeout)

    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...config.headers
      }

      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`
      }

      const response = await fetch(`${this.baseURL}${url}`, {
        ...config,
        headers,
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      clearTimeout(timeoutId)
      throw error
    }
  }

  get<T>(url: string, config?: RequestConfig): Promise<ResponseData<T>> {
    return this.request<T>(url, { ...config, method: 'GET' })
  }

  post<T>(url: string, data?: any, config?: RequestConfig): Promise<ResponseData<T>> {
    return this.request<T>(url, {
      ...config,
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  put<T>(url: string, data?: any, config?: RequestConfig): Promise<ResponseData<T>> {
    return this.request<T>(url, {
      ...config,
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  delete<T>(url: string, config?: RequestConfig): Promise<ResponseData<T>> {
    return this.request<T>(url, { ...config, method: 'DELETE' })
  }

  setToken(token: string) {
    this.token = token
    localStorage.setItem('token', token)
  }

  clearToken() {
    this.token = null
    localStorage.removeItem('token')
  }
}

export const http = new HttpClient('https://api.example.com')
```

### 6.2 API调用示例

```typescript
import { http } from '@/utils/http'

interface User {
  id: number
  name: string
  email: string
}

// 获取用户列表
export const getUsers = () => {
  return http.get<User[]>('/users')
}

// 获取用户详情
export const getUser = (id: number) => {
  return http.get<User>(`/users/${id}`)
}

// 创建用户
export const createUser = (data: Partial<User>) => {
  return http.post<User>('/users', data)
}

// 更新用户
export const updateUser = (id: number, data: Partial<User>) => {
  return http.put<User>(`/users/${id}`, data)
}

// 删除用户
export const deleteUser = (id: number) => {
  return http.delete(`/users/${id}`)
}
```

## 第7章 项目构建与优化

### 7.1 Vite配置

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'antd-vendor': ['ant-design-vue']
        }
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://api.example.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### 7.2 性能优化

```typescript
// 路由懒加载
const routes = [
  {
    path: '/',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/about',
    component: () => import('@/views/About.vue')
  }
]

// 组件懒加载
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() =>
  import('@/components/AsyncComponent.vue')
)
```

### 7.3 代码格式化

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 100
}
```

## 第8章 publish-commons组件库

### 8.1 组件库概览

publish-commons是一个基于Vue3和Ant Design Vue的组件库，提供了丰富的业务组件和工具函数，帮助开发者快速构建企业级应用。

### 8.2 安装与配置

```bash
# 安装组件库
npm install publish-commons
```

```typescript
// main.ts
import { createApp } from 'vue'
import App from './App.vue'
import PublishCommons from 'publish-commons'
import 'publish-commons/dist/style.css'

const app = createApp(App)
app.use(PublishCommons)
app.mount('#app')
```

### 8.3 组件使用

```vue
<template>
  <div>
    <!-- 使用publish-commons组件 -->
    <pc-button type="primary">主要按钮</pc-button>
    <pc-table :columns="columns" :data-source="dataSource" />
    <pc-form :model="formData" @submit="handleSubmit" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const columns = [
  { title: '姓名', dataIndex: 'name' },
  { title: '年龄', dataIndex: 'age' }
]

const dataSource = ref([
  { name: '张三', age: 25 },
  { name: '李四', age: 30 }
])

const formData = ref({
  name: '',
  age: 0
})

const handleSubmit = (data: any) => {
  console.log('表单提交', data)
}
</script>
```

### 8.4 类型定义

```typescript
import type { PcButtonProps, PcTableProps } from 'publish-commons'

// 按钮组件类型
const buttonProps: PcButtonProps = {
  type: 'primary',
  size: 'large',
  disabled: false
}

// 表格组件类型
const tableProps: PcTableProps = {
  columns: [
    { title: '姓名', dataIndex: 'name' },
    { title: '年龄', dataIndex: 'age' }
  ],
  dataSource: [
    { name: '张三', age: 25 },
    { name: '李四', age: 30 }
  ],
  loading: false
}
```

## 第9章 最佳实践

### 9.1 代码组织

```
src/
├── assets/          # 静态资源
├── components/      # 公共组件
├── composables/     # 组合式函数
├── router/          # 路由配置
├── stores/          # Pinia状态管理
├── utils/           # 工具函数
├── views/           # 页面组件
└── App.vue          # 根组件
```

### 9.2 组件设计

```vue
<template>
  <div class="user-card">
    <h3>{{ user.name }}</h3>
    <p>{{ user.email }}</p>
    <button @click="handleEdit">编辑</button>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

interface Props {
  user: User
}

interface Emits {
  (e: 'edit', user: User): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const handleEdit = () => {
  emit('edit', props.user)
}
</script>

<style scoped>
.user-card {
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style>
```

### 9.3 测试

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Counter from '@/components/Counter.vue'

describe('Counter', () => {
  it('renders count', () => {
    const wrapper = mount(Counter)
    expect(wrapper.text()).toContain('计数：0')
  })

  it('increments count', async () => {
    const wrapper = mount(Counter)
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.text()).toContain('计数：1')
  })
})
```

### 9.4 开发规范

1. **命名规范**
   - 组件名使用PascalCase
   - 文件名使用kebab-case
   - 变量名使用camelCase
   - 常量名使用UPPER_SNAKE_CASE

2. **代码风格**
   - 使用TypeScript类型注解
   - 遵循ESLint规则
   - 使用Prettier格式化代码

3. **注释规范**
   - 为复杂逻辑添加注释
   - 为公共API添加JSDoc注释
   - 保持注释与代码同步

## 总结

本技能总结涵盖了Vue3全家桶与Ant Design结合开发的核心知识，包括：

1. Vue3核心特性：Composition API、响应式系统、生命周期钩子
2. TypeScript集成：组件类型定义、路由类型定义、Pinia类型定义
3. Ant Design Vue组件库：基础组件、表单组件、表格组件
4. Vue Router路由管理：路由配置、路由守卫、编程式导航
5. Pinia状态管理：Store定义、Store使用
6. 网络请求与API：Fetch封装、API调用示例
7. 项目构建与优化：Vite配置、性能优化、代码格式化
8. publish-commons组件库：组件库概览、安装与配置、组件使用、类型定义
9. 最佳实践：代码组织、组件设计、测试、开发规范

通过学习这些内容，开发者可以快速掌握Vue3+Ant Design+publish-commons项目开发技能，构建高质量的企业级应用。