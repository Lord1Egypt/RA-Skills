---
name: wand-skill
description: 帮助开发者在项目中快速集成和使用 Wand UI 2.0 移动端组件库。该技能提供完整的组件 API 参考、使用示例和最佳实践。适用于以下场景：(1) 需要在 Vue 2.0 项目中使用 Wand UI 组件；(2) 查询特定组件的属性、事件或插槽；(3) 需要组件使用示例和代码模板；(4) 解决 Wand UI 集成相关问题；(5) 实现表单、列表、导航等常见移动端界面。
---

# Wand UI 技能

## 概述

Wand UI 2.0 是一个基于 Vue 2.0 的移动端 UI 组件库，专为移动端 H5 应用设计。本技能帮助你快速在项目中集成和使用 Wand UI 组件。

**核心特性**
- 36+ 精心设计的移动端组件
- 完整的 TypeScript 支持
- 支持按需引入
- 单元测试覆盖率 90%+
- 支持 SSR（服务端渲染）
- 兼容 Android 4.0+ 和 iOS 8+

## 快速开始

### 安装

```bash
npm install @weiyi/wand-ui
```

### 引入方式

**完整引入**（适合小型项目）
```js
import Vue from 'vue'
import WandUI from '@weiyi/wand-ui'
import '@weiyi/wand-ui/lib/wand-ui.css'

Vue.use(WandUI)
```

**按需引入**（推荐，减小打包体积）
```js
import { WandButton, WandInput } from '@weiyi/wand-ui'
import '@weiyi/wand-ui/lib/button/style.css'
import '@weiyi/wand-ui/lib/input/style.css'

export default {
  components: {
    WandButton,
    WandInput
  }
}
```

## 组件分类

### 表单组件
用于数据输入和表单验证

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| Button | WandButton | 按钮操作 |
| Input | WandInput | 单行文本输入 |
| Textarea | WandTextarea | 多行文本输入 |
| Check | WandCheck | 复选框 |
| Switch | WandSwitch | 开关切换 |
| Form | WandForm | 表单容器和验证 |
| FormItem | WandFormItem | 表单项 |
| Rate | WandRate | 评分 |
| Uploader | WandUploader | 文件上传 |

**示例：创建表单**
```vue
<template>
  <wand-form :model="formData" :rules="rules" ref="form">
    <wand-form-item label="用户名" prop="username" required>
      <wand-input v-model="formData.username" placeholder="请输入用户名" />
    </wand-form-item>

    <wand-button type="primary" @click="submit">提交</wand-button>
  </wand-form>
</template>

<script>
export default {
  data() {
    return {
      formData: { username: '' },
      rules: {
        username: [{ required: true, message: '请输入用户名' }]
      }
    }
  },
  methods: {
    submit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // 提交表单
        }
      })
    }
  }
}
</script>
```

### 选择器组件
用于日期、时间、选项等选择

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| Picker | WandPicker | 基础选择器 |
| PopupPicker | WandPopupPicker | 弹出式选择器 |
| Datetime | WandDatetime | 日期时间选择 |
| Cascade | WandCascade | 级联选择（如省市区） |

**示例：日期选择**
```vue
<template>
  <wand-popup-picker v-model="visible" title="选择日期">
    <wand-datetime
      v-model="selectedDate"
      type="date"
      @confirm="onConfirm"
    />
  </wand-popup-picker>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
      selectedDate: new Date()
    }
  },
  methods: {
    onConfirm(value) {
      console.log('选择的日期:', value)
      this.visible = false
    }
  }
}
</script>
```

### 反馈组件
用于用户操作的反馈提示

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| Toast | WandToast | 轻提示 |
| Loading | WandLoading | 加载状态 |
| Dialog | WandDialog | 对话框 |
| Confirm | WandConfirm | 确认框 |
| Alert | WandAlert | 警告框 |
| ActionSheet | WandActionSheet | 动作面板 |

**示例：Toast 提示**
```js
// 文字提示
this.$toast('操作成功')

// 成功提示
this.$toast.success('保存成功')

// 失败提示
this.$toast.fail('操作失败')

// 加载中
this.$toast.loading('加载中...')
```

**示例：Dialog 对话框**
```vue
<template>
  <div>
    <wand-button @click="showDialog">显示对话框</wand-button>

    <wand-dialog
      v-model="dialogVisible"
      title="提示"
      message="确定要删除吗？"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />
  </div>
</template>
```

### 展示组件
用于内容展示和布局

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| List | WandList | 列表和上拉加载 |
| Swipe | WandSwipe | 轮播图 |
| SwipeItem | WandSwipeItem | 轮播项 |
| Collapse | WandCollapse | 折叠面板 |
| CollapseGroup | WandCollapseGroup | 折叠面板组 |
| NoticeBar | WandNoticeBar | 通知栏 |
| PhotoViewer | WandPhotoViewer | 图片预览 |

**示例：列表加载**
```vue
<template>
  <wand-list
    :loading="loading"
    :finished="finished"
    @load="onLoad"
  >
    <div v-for="item in list" :key="item.id">
      {{ item.title }}
    </div>
  </wand-list>
</template>

<script>
export default {
  data() {
    return {
      list: [],
      loading: false,
      finished: false,
      page: 1
    }
  },
  methods: {
    async onLoad() {
      this.loading = true
      const data = await this.fetchData(this.page)
      this.list.push(...data)
      this.loading = false
      this.page++

      if (data.length === 0) {
        this.finished = true
      }
    }
  }
}
</script>
```

### 导航组件
用于页面导航和路由切换

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| Tab | WandTab | 标签页容器 |
| TabItem | WandTabItem | 标签页项 |
| TabBar | WandTabBar | 底部导航栏 |
| TabBarItem | WandTabBarItem | 底部导航项 |
| NavBar | WandNavBar | 顶部导航栏 |

**示例：底部导航栏**
```vue
<template>
  <wand-tab-bar v-model="active" fixed>
    <wand-tab-bar-item name="home" icon="home">
      首页
    </wand-tab-bar-item>
    <wand-tab-bar-item name="user" icon="user">
      我的
    </wand-tab-bar-item>
  </wand-tab-bar>
</template>

<script>
export default {
  data() {
    return {
      active: 'home'
    }
  }
}
</script>
```

### 其他组件

| 组件 | 引入名称 | 主要用途 |
|-|-|-|
| Popup | WandPopup | 弹出层基础组件 |
| Popover | WandPopover | 气泡弹出框 |
| Search | WandSearch | 搜索框 |
| SwipeCell | WandSwipeCell | 滑动单元格 |
| Affix | WandAffix | 固钉 |

## 组件使用工作流

### 步骤 1: 确定需求

根据用户需求，确定需要使用哪些组件：
- **表单页面** → Form, FormItem, Input, Button 等
- **列表页面** → List, NavBar
- **选择功能** → Picker, Datetime, Cascade
- **反馈提示** → Toast, Dialog, Loading

### 步骤 2: 引入组件

根据项目规模选择引入方式：
- 小型项目：完整引入所有组件
- 大型项目：按需引入需要的组件

### 步骤 3: 查询 API

当需要了解组件的具体属性、事件或插槽时：
1. 查看 `references/components_api.md` 了解组件的完整 API
2. 查看该组件的 Props、Events、Slots 等

### 步骤 4: 编写代码

参考示例代码和最佳实践编写组件代码：
1. 在 template 中使用组件标签
2. 在 script 中引入组件
3. 绑定数据和事件处理器

### 步骤 5: 样式调整

如有需要，通过以下方式自定义样式：
- 使用组件的 `customStyle` 属性（如 Button）
- 通过 CSS 覆盖组件样式
- 使用组件提供的插槽自定义内容

## 常见使用场景

### 场景 1: 创建登录页面

```vue
<template>
  <div class="login-page">
    <wand-nav-bar title="登录" />

    <wand-form :model="formData" :rules="rules" ref="loginForm">
      <wand-form-item label="手机号" prop="mobile" required>
        <wand-input
          v-model="formData.mobile"
          type="tel"
          placeholder="请输入手机号"
          clearable
        />
      </wand-form-item>

      <wand-form-item label="验证码" prop="code" required>
        <wand-input
          v-model="formData.code"
          placeholder="请输入验证码"
        >
          <template #right-slot>
            <wand-button
              size="small"
              type="primary"
              @click="sendCode"
              :disabled="codeSending"
            >
              {{ codeText }}
            </wand-button>
          </template>
        </wand-input>
      </wand-form-item>

      <wand-button
        type="primary"
        size="large"
        @click="handleLogin"
        :disabled="loading"
      >
        {{ loading ? '登录中...' : '登录' }}
      </wand-button>
    </wand-form>
  </div>
</template>

<script>
import {
  WandNavBar,
  WandForm,
  WandFormItem,
  WandInput,
  WandButton
} from '@weiyi/wand-ui'

export default {
  components: {
    WandNavBar,
    WandForm,
    WandFormItem,
    WandInput,
    WandButton
  },
  data() {
    return {
      formData: {
        mobile: '',
        code: ''
      },
      rules: {
        mobile: [
          { required: true, message: '请输入手机号' },
          { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' }
        ],
        code: [
          { required: true, message: '请输入验证码' }
        ]
      },
      loading: false,
      codeSending: false,
      codeText: '发送验证码'
    }
  },
  methods: {
    async sendCode() {
      // 发送验证码逻辑
    },
    async handleLogin() {
      this.$refs.loginForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            // 登录 API 调用
            await this.$api.login(this.formData)
            this.$toast.success('登录成功')
            this.$router.push('/home')
          } catch (error) {
            this.$toast.fail(error.message)
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>
```

### 场景 2: 创建商品列表页

```vue
<template>
  <div class="product-list">
    <wand-nav-bar
      title="商品列表"
      left-arrow
      @click-left="$router.back()"
    />

    <wand-search
      v-model="searchText"
      placeholder="搜索商品"
      show-action
      @search="onSearch"
    />

    <wand-list
      :loading="loading"
      :finished="finished"
      finished-text="没有更多商品了"
      @load="loadMore"
    >
      <div
        v-for="product in productList"
        :key="product.id"
        class="product-item"
        @click="goToDetail(product.id)"
      >
        <img :src="product.image" class="product-image">
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p class="price">¥{{ product.price }}</p>
        </div>
      </div>
    </wand-list>
  </div>
</template>

<script>
import {
  WandNavBar,
  WandSearch,
  WandList
} from '@weiyi/wand-ui'

export default {
  components: {
    WandNavBar,
    WandSearch,
    WandList
  },
  data() {
    return {
      searchText: '',
      productList: [],
      loading: false,
      finished: false,
      page: 1
    }
  },
  methods: {
    async loadMore() {
      this.loading = true
      try {
        const data = await this.$api.getProducts({
          page: this.page,
          keyword: this.searchText
        })

        this.productList.push(...data.list)
        this.page++

        if (data.list.length === 0) {
          this.finished = true
        }
      } catch (error) {
        this.$toast.fail('加载失败')
      } finally {
        this.loading = false
      }
    },
    onSearch() {
      this.productList = []
      this.page = 1
      this.finished = false
      this.loadMore()
    },
    goToDetail(id) {
      this.$router.push(`/product/${id}`)
    }
  }
}
</script>
```

## 最佳实践

### 1. 表单验证

使用 Form 组件的 rules 进行验证，统一在提交时调用 validate 方法：

```js
this.$refs.form.validate((valid) => {
  if (valid) {
    // 表单验证通过，执行提交逻辑
  } else {
    // 表单验证失败
    return false
  }
})
```

### 2. 列表加载

使用 List 组件实现下拉加载时，注意：
- 在 load 事件中设置 `loading = true`
- 加载完成后设置 `loading = false`
- 没有更多数据时设置 `finished = true`
- 重置列表时要重置 `finished = false`

### 3. Toast 提示规范

```js
// 成功操作
this.$toast.success('操作成功')

// 失败操作
this.$toast.fail('操作失败')

// 加载中（需要手动关闭）
const toast = this.$toast.loading('加载中...')
// 请求完成后
toast.clear()

// 普通提示
this.$toast('提示信息')
```

### 4. 组件命名规范

在模板中使用 kebab-case（短横线命名），在 JavaScript 中使用 PascalCase（大驼峰命名）：

```vue
<template>
  <!-- 模板中使用短横线命名 -->
  <wand-button type="primary">按钮</wand-button>
  <wand-nav-bar title="标题" />
</template>

<script>
// JavaScript 中使用大驼峰命名
import { WandButton, WandNavBar } from '@weiyi/wand-ui'

export default {
  components: {
    WandButton,
    WandNavBar
  }
}
</script>
```

## TypeScript 支持

Wand UI 提供完整的 TypeScript 类型定义：

```typescript
import { WandButton } from '@weiyi/wand-ui'
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: {
    WandButton
  }
})
export default class MyComponent extends Vue {
  private message: string = 'Hello'

  private handleClick(): void {
    console.log(this.message)
  }
}
```

## 参考资源

本技能包含以下参考文档，可根据需要查看：

### references/components_api.md
完整的组件 API 参考文档，包含所有组件的：
- Props（属性）
- Events（事件）
- Slots（插槽）
- Methods（方法）
- 使用示例

**何时查看**: 需要了解特定组件的详细 API 时

### references/quickstart.md
快速入门指南，包含：
- 安装和引入方式
- 常见使用场景的完整示例
- 浏览器支持信息
- 常见问题解答

**何时查看**: 初次使用 Wand UI 或需要参考完整的使用示例时

## 故障排查

### 样式没有生效

**问题**: 组件显示不正常或没有样式

**解决方案**:
1. 确保引入了 CSS 文件: `import '@weiyi/wand-ui/lib/wand-ui.css'`
2. 按需引入时，确保引入了对应组件的样式文件
3. 检查是否使用了 babel-plugin-component 插件

### 组件提示未注册

**问题**: 控制台报错"Unknown custom element"

**解决方案**:
1. 确保在 components 中注册了组件
2. 确保组件名称拼写正确
3. 全局引入时确保调用了 `Vue.use(WandUI)`

### Toast 等全局方法不存在

**问题**: `this.$toast is not a function`

**解决方案**:
1. 确保使用了完整引入方式 `Vue.use(WandUI)`
2. 或者手动安装 Toast 组件: `Vue.use(WandToast)`

### 移动端显示异常

**问题**: 在移动设备上显示不正常

**解决方案**:
在 HTML 的 `<head>` 中添加 viewport 标签：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
```
