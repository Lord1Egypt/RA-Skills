# Vue 2 前端编码规范

> 本规范适用于 Vue 2 + JavaScript/TypeScript 项目，AI 编码时必须遵守。如有与项目 `docs/architecture/coding-convention.md` 冲突之处，以项目文档为准。

## 一、项目结构

```
src/
├── views/              ← 页面级组件（路由对应）
├── components/         ← 公共组件（可复用）
│   └── common/         ← 通用基础组件（按钮、表格、弹窗等）
├── api/                ← 接口请求封装（按模块分文件）
├── router/             ← 路由配置
├── store/              ← Vuex Store（状态管理）
│   └── modules/        ← 按模块拆分
├── utils/              ← 工具函数
├── mixins/             ← 混入（公共逻辑复用）
├── directives/         ← 自定义指令
├── filters/            ← 全局过滤器
├── constants/          ← 常量定义
├── styles/             ← 全局样式
└── assets/             ← 静态资源（图片、字体等）
```

### 职责边界
| 层 | 职责 | 禁止 |
|----|------|------|
| views | 页面布局、组装组件 | 直接调 API |
| components | UI 渲染和交互 | 包含复杂业务逻辑 |
| store (Vuex) | 全局状态管理 | 直接用 localStorage |
| api | HTTP 请求封装 | UI 逻辑 |

## 二、命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase 或 kebab-case | `UserTable.vue`, `order-dialog.vue` |
| 页面文件 | kebab-case | `user-list.vue`, `order-detail.vue` |
| 组件 name | PascalCase（多单词） | `name: 'UserTable'` |
| Props | camelCase | `userName`, `isVisible` |
| Events | kebab-case | `this.$emit('item-click')` |
| 变量/方法 | camelCase | `userList`, `handleSubmit` |
| 常量 | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| 目录名 | kebab-case | `user-management/` |
| CSS class | kebab-case / BEM | `.user-table__header` |

### Mixin 命名
- 以 `mixin` 结尾：`paginationMixin`, `formValidateMixin`
- Mixin 内的方法和数据必须带前缀避免冲突，如 `mixin_pageSize`

## 三、组件规范

### 组件定义（必须）
```vue
<template>
  <div class="user-table">
    <el-table :data="list" :loading="loading">
      <!-- ... -->
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'UserTable',

  // Props 必须定义类型和默认值
  props: {
    userId: {
      type: [String, Number],
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

  // 数据
  data() {
    return {
      loading: false,
      list: []
    }
  },

  // 计算属性
  computed: {
    hasData() {
      return this.list.length > 0
    }
  },

  // 侦听器
  watch: {
    userId: {
      immediate: true,
      handler(val) {
        if (val) this.fetchData()
      }
    }
  },

  // 生命周期
  created() {
    this.fetchData()
  },

  // 方法
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await userApi.getList({ userId: this.userId })
        this.list = res.data
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### 必须遵守
- Props 必须定义 `type`，禁止用空对象 `props: {}`
- 每个组件必须有 `name` 属性
- 单个组件不超过 300 行，超长必须拆分
- `data` 必须是函数（返回新对象），不能是对象字面量
- 禁止在 `methods` 中使用箭头函数（this 指向问题）

## 四、状态管理（Vuex）

```javascript
// store/modules/user.js
const state = {
  currentUser: null,
  token: ''
}

const getters = {
  isLoggedIn: state => !!state.currentUser
}

const mutations = {
  SET_USER(state, user) {
    state.currentUser = user
  },
  SET_TOKEN(state, token) {
    state.token = token
  }
}

const actions = {
  async login({ commit }, credentials) {
    const res = await userApi.login(credentials)
    commit('SET_USER', res.data.user)
    commit('SET_TOKEN', res.data.token)
  },
  logout({ commit }) {
    commit('SET_USER', null)
    commit('SET_TOKEN', '')
  }
}

export default {
  namespaced: true,  // 必须开启命名空间
  state,
  getters,
  mutations,
  actions
}
```

### 必须遵守
- 所有模块必须 `namespaced: true`
- 组件中通过 `mapState`/`mapGetters`/`mapActions` 访问，不直接操作 `this.$store.state`
- Mutation 大写蛇形命名（`SET_XXX`），Action 驼峰命名（`fetchXxx`）
- 禁止在 Mutation 中做异步操作（异步放 Action）
- Store 模块按领域拆分，单个模块不超过 200 行

## 五、API 请求规范

```javascript
// api/user.js
import request from '@/utils/request'

export const userApi = {
  getList(params) {
    return request.get('/api/users', { params })
  },
  getById(id) {
    return request.get(`/api/users/${id}`)
  },
  create(data) {
    return request.post('/api/users', data)
  }
}
```

- 所有 API 调用统一通过 `api/` 目录封装，禁止在页面中直接 `axios.get`
- 请求拦截器统一处理：Token 注入、Loading 状态
- 响应拦截器统一处理：错误提示、登录过期跳转（401 统一跳登录页）
- **禁止**在请求拦截器或参数中暴露密码/Token 到 console

## 六、样式规范

- 必须使用 `<style scoped>`，避免样式污染
- Element UI 覆盖样式使用 `/deep/` 或 `::v-deep`
- 全局样式放 `styles/` 目录
- 禁止使用 `!important`（除非覆盖第三方库）
- 响应式断点：`768px`（平板）、`1024px`（桌面）

## 七、路由规范

```javascript
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
- `meta` 必须包含 `title`
- 权限控制放 `meta.permissions`，路由守卫统一校验
- 路由守卫使用 `router.beforeEach`，不放各页面重复校验

## 八、安全规范

- 用户输入显示时禁止直接 `v-html`（除非内容已经过 XSS 处理且可信）
- 敏感数据不在 URL 参数中传递
- Token 存储在 httpOnly cookie 或加密存储中，不在 localStorage 明文存放
- 前端校验只是辅助，不可替代后端校验
- 不在 console.log 中打印敏感信息

## 九、Element UI 使用规范

- 表单统一使用 `el-form` + `rules` 校验
- 表格统一使用 `el-table`，列宽使用 `min-width` 而非固定 `width`
- 弹窗统一使用 `el-dialog`，关闭前必须重置数据
- 分页统一使用 `el-pagination`，配合 `@size-change` 和 `@current-change`
- 消息提示使用 `this.$message` / `this.$confirm` 等全局方法

## 十、测试规范

- 组件测试使用 Jest + @vue/test-utils
- 测试文件与组件同目录或 `__tests__/` 子目录，命名 `Xxx.spec.js`
- 必须覆盖：Props 渲染、事件触发、异步数据加载、v-model 双向绑定
