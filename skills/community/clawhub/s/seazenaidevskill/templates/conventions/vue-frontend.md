# Vue 3 前端编码规范

> 本规范适用于 Vue 3 + TypeScript 项目，AI 编码时必须遵守。如有与项目 `docs/architecture/coding-convention.md` 冲突之处，以项目文档为准。

## 一、项目结构

```
src/
├── views/              ← 页面级组件（路由对应）
├── components/         ← 公共组件（可复用）
│   └── common/         ← 通用基础组件（按钮、表格、弹窗等）
├── composables/        ← 组合式函数（useXxx）
├── api/                ← 接口请求封装（按模块分文件）
├── router/             ← 路由配置
├── store/              ← Pinia Store（状态管理）
│   └── modules/        ← 按模块拆分
├── utils/              ← 工具函数
├── hooks/              ← 自定义 Hook
├── directives/         ← 自定义指令
├── constants/          ← 常量定义
├── types/              ← TypeScript 类型定义
├── styles/             ← 全局样式
└── assets/             ← 静态资源（图片、字体等）
```

### 职责边界
| 层 | 职责 | 禁止 |
|----|------|------|
| views | 页面布局、组装组件 | 直接调 API（通过 composable） |
| components | UI 渲染和交互 | 包含复杂业务逻辑 |
| composables | 业务逻辑、API 调用 | 操作 DOM |
| store | 全局状态管理 | 直接用 localStorage（用插件） |
| api | HTTP 请求封装 | UI 逻辑 |

## 二、命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserTable.vue`, `OrderDialog.vue` |
| 页面文件 | kebab-case 或 PascalCase | `user-list.vue`, `UserProfile.vue` |
| 组件名 | PascalCase（多单词） | `UserTable`, `OrderForm` |
| Props | camelCase | `userName`, `isVisible` |
| Events | kebab-case | `@update:model-value`, `@item-click` |
| 变量/方法 | camelCase | `userList`, `handleSubmit` |
| 常量 | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| 目录名 | kebab-case | `user-management/`, `order-list/` |
| CSS class | kebab-case / BEM | `.user-table__header`, `.btn--primary` |

### Composable 命名
- 以 `use` 开头：`useUserList`, `useFormValidation`
- 返回 ref/reactive，调用方 `.value` 访问

## 三、组件规范

### 组件定义（必须）
```vue
<script setup lang="ts">
// 1. 导入
import { ref, computed, onMounted } from 'vue'
import type { UserInfo } from '@/types/user'

// 2. Props（必须带类型和默认值）
interface Props {
  userId: string
  disabled?: boolean
}
const props = withDefaults(defineProps<Props>(), {
  disabled: false,
})

// 3. Emits
const emit = defineEmits<{
  'update': [value: UserInfo]
  'close': []
}>()

// 4. 响应式数据 & 计算属性
const loading = ref(false)
const data = ref<UserInfo | null>(null)

// 5. 方法
async function fetchData() { /* ... */ }

// 6. 生命周期
onMounted(() => fetchData())
</script>
```

### 必须遵守
- 组件必须有明确的 Props 类型定义，不允许用 `any`
- 每个组件必须包含 `name`（用于 Vue DevTools 调试）
- 大组件拆分为多个小组件，单个组件不超过 300 行
- 公共组件放到 `components/common/`，业务组件放对应模块目录

## 四、状态管理（Pinia）

```typescript
// store/modules/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!currentUser.value)

  async function login(credentials: LoginDto) {
    const res = await api.login(credentials)
    currentUser.value = res.data
  }

  return { currentUser, isLoggedIn, login }
})
```

- 使用 Composition API 风格（setup store）
- 每个 Store 职责单一，按领域拆分
- 禁止在 Store 中直接操作 DOM 或路由

## 五、API 请求规范

```typescript
// api/user.ts
import request from '@/utils/request'
import type { UserInfo, UserQuery } from '@/types/user'

export const userApi = {
  getList(params: UserQuery) {
    return request.get<PageResult<UserInfo>>('/api/users', { params })
  },
  getById(id: string) {
    return request.get<UserInfo>(`/api/users/${id}`)
  },
  create(data: CreateUserDto) {
    return request.post('/api/users', data)
  }
}
```

- 所有 API 调用统一通过 `api/` 目录封装，禁止在页面中直接 `axios.get`
- 请求拦截器统一处理：Token 注入、Loading 状态
- 响应拦截器统一处理：错误提示、登录过期跳转
- **禁止**在请求拦截器或参数中暴露密码/Token 到日志

## 六、样式规范

- 优先使用 `<style scoped>`，避免样式污染
- 全局样式放 `styles/` 目录
- 使用 CSS 变量管理主题色（定义在 `:root`）
- 禁止使用 `!important`（除非覆盖第三方库）
- 响应式断点：`768px`（平板）、`1024px`（桌面）、`1440px`（大屏）

## 七、路由规范

```typescript
{
  path: '/user-management',
  name: 'UserManagement',
  component: () => import('@/views/user-management/index.vue'),
  meta: {
    title: '用户管理',
    requiresAuth: true,
    permissions: ['user:view']
  }
}
```

- 页面组件必须懒加载（`() => import(...)`）
- 路由 meta 必须包含 `title`
- 权限控制放在 `meta.permissions`，路由守卫统一校验

## 八、安全规范

- 用户输入显示时必须处理 XSS（v-html 仅在可信内容时使用）
- 敏感数据不在 URL 参数中传递
- Token 存储在 httpOnly cookie 或安全存储中，不在 localStorage 明文存放
- 前端校验只是辅助，不可替代后端校验

## 九、测试规范

- 组件测试使用 Vitest + @vue/test-utils
- 测试文件与组件同目录或 `__tests__/` 子目录，命名 `Xxx.test.ts`
- 必须覆盖：正常渲染、Props 变化响应、事件触发、异步数据加载
