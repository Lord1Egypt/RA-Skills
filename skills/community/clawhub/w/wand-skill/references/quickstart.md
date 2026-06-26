# Wand UI 快速入门指南

## 安装

```bash
npm install @weiyi/wand-ui
# 或
yarn add @weiyi/wand-ui
```

## 完整引入

在 main.js 中引入所有组件：

```js
import Vue from 'vue'
import WandUI from '@weiyi/wand-ui'
import '@weiyi/wand-ui/lib/wand-ui.css'

Vue.use(WandUI)
```

## 按需引入

### 方式一：手动按需引入

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

### 方式二：使用 babel-plugin-component (推荐)

1. 安装插件：
```bash
npm install babel-plugin-component -D
```

2. 修改 .babelrc 或 babel.config.js：
```js
{
  "plugins": [
    [
      "component",
      {
        "libraryName": "@weiyi/wand-ui",
        "styleLibraryName": "theme-chalk"
      }
    ]
  ]
}
```

3. 直接引入组件即可，样式会自动引入：
```js
import { WandButton, WandInput } from '@weiyi/wand-ui'

export default {
  components: {
    WandButton,
    WandInput
  }
}
```

## TypeScript 支持

Wand UI 提供完整的 TypeScript 类型定义文件：

```typescript
import { WandButton } from '@weiyi/wand-ui'
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: {
    WandButton
  }
})
export default class MyComponent extends Vue {
  // TypeScript 支持
}
```

## 组件命名规则

所有组件使用 `Wand` 前缀 + 组件名称的驼峰命名法：

| 原始名称 | 组件名 | 使用示例 |
|-|-|-|
| button | WandButton | `<wand-button>` |
| input | WandInput | `<wand-input>` |
| nav-bar | WandNavBar | `<wand-nav-bar>` |
| tab-bar | WandTabBar | `<wand-tab-bar>` |
| action-sheet | WandActionSheet | `<wand-action-sheet>` |

## 常见使用场景

### 场景 1: 创建表单页面

```vue
<template>
  <div class="form-page">
    <wand-form :model="formData" :rules="rules" ref="form">
      <wand-form-item label="用户名" prop="username" required>
        <wand-input v-model="formData.username" placeholder="请输入用户名" />
      </wand-form-item>

      <wand-form-item label="密码" prop="password" required>
        <wand-input
          v-model="formData.password"
          type="password"
          placeholder="请输入密码"
        />
      </wand-form-item>

      <wand-button type="primary" size="large" @click="handleSubmit">
        提交
      </wand-button>
    </wand-form>
  </div>
</template>

<script>
import { WandForm, WandFormItem, WandInput, WandButton } from '@weiyi/wand-ui'

export default {
  components: {
    WandForm,
    WandFormItem,
    WandInput,
    WandButton
  },
  data() {
    return {
      formData: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名' }
        ],
        password: [
          { required: true, message: '请输入密码' },
          { min: 6, message: '密码至少6位' }
        ]
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // 提交表单
          console.log('表单数据:', this.formData)
        }
      })
    }
  }
}
</script>
```

### 场景 2: 创建列表页面

```vue
<template>
  <div class="list-page">
    <wand-nav-bar title="列表页" left-arrow @click-left="$router.back()" />

    <wand-list
      :loading="loading"
      :finished="finished"
      @load="onLoad"
    >
      <div v-for="item in list" :key="item.id" class="list-item">
        {{ item.title }}
      </div>
    </wand-list>
  </div>
</template>

<script>
import { WandNavBar, WandList } from '@weiyi/wand-ui'

export default {
  components: {
    WandNavBar,
    WandList
  },
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
      // 加载数据
      const data = await this.fetchData(this.page)
      this.list.push(...data)
      this.loading = false
      this.page++

      if (data.length < 10) {
        this.finished = true
      }
    },
    async fetchData(page) {
      // 模拟 API 调用
      return []
    }
  }
}
</script>
```

### 场景 3: 使用弹窗组件

```vue
<template>
  <div>
    <wand-button @click="showDialog">显示对话框</wand-button>
    <wand-button @click="showActionSheet">显示动作面板</wand-button>
    <wand-button @click="showToast">显示提示</wand-button>

    <wand-dialog
      v-model="dialogVisible"
      title="提示"
      message="这是一条消息"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />

    <wand-action-sheet
      v-model="actionSheetVisible"
      :actions="actions"
      @select="onSelect"
    />
  </div>
</template>

<script>
import { WandButton, WandDialog, WandActionSheet } from '@weiyi/wand-ui'

export default {
  components: {
    WandButton,
    WandDialog,
    WandActionSheet
  },
  data() {
    return {
      dialogVisible: false,
      actionSheetVisible: false,
      actions: [
        { name: '选项1' },
        { name: '选项2' },
        { name: '选项3' }
      ]
    }
  },
  methods: {
    showDialog() {
      this.dialogVisible = true
    },
    showActionSheet() {
      this.actionSheetVisible = true
    },
    showToast() {
      this.$toast('这是一条提示')
    },
    handleConfirm() {
      console.log('确认')
    },
    handleCancel() {
      console.log('取消')
    },
    onSelect(action, index) {
      this.$toast(`选择了: ${action.name}`)
    }
  }
}
</script>
```

### 场景 4: 选择器使用

```vue
<template>
  <div>
    <!-- 日期选择 -->
    <wand-popup-picker
      v-model="datePickerVisible"
      title="选择日期"
    >
      <wand-datetime
        v-model="selectedDate"
        type="date"
        @confirm="onDateConfirm"
      />
    </wand-popup-picker>

    <!-- 级联选择 -->
    <wand-popup-picker
      v-model="cascadePickerVisible"
      title="选择地区"
    >
      <wand-cascade
        v-model="selectedArea"
        :options="areaOptions"
        @confirm="onAreaConfirm"
      />
    </wand-popup-picker>

    <!-- 普通选择器 -->
    <wand-popup-picker
      v-model="pickerVisible"
      title="选择选项"
    >
      <wand-picker
        v-model="selectedOption"
        :columns="options"
        @confirm="onOptionConfirm"
      />
    </wand-popup-picker>
  </div>
</template>

<script>
import {
  WandPopupPicker,
  WandDatetime,
  WandCascade,
  WandPicker
} from '@weiyi/wand-ui'

export default {
  components: {
    WandPopupPicker,
    WandDatetime,
    WandCascade,
    WandPicker
  },
  data() {
    return {
      datePickerVisible: false,
      cascadePickerVisible: false,
      pickerVisible: false,
      selectedDate: new Date(),
      selectedArea: [],
      selectedOption: [],
      areaOptions: [],
      options: ['选项1', '选项2', '选项3']
    }
  },
  methods: {
    onDateConfirm(value) {
      console.log('选择的日期:', value)
      this.datePickerVisible = false
    },
    onAreaConfirm(value) {
      console.log('选择的地区:', value)
      this.cascadePickerVisible = false
    },
    onOptionConfirm(value) {
      console.log('选择的选项:', value)
      this.pickerVisible = false
    }
  }
}
</script>
```

## 浏览器支持

- Android 4.0+
- iOS 8+
- 现代浏览器

## SSR 支持

Wand UI 支持服务端渲染（SSR），可以在 Nuxt.js 等框架中使用。

## 常见问题

### 1. 样式没有加载？

确保引入了组件的样式文件：
```js
import '@weiyi/wand-ui/lib/wand-ui.css'
```

### 2. 按需引入时样式加载失败？

使用 babel-plugin-component 插件可以自动引入样式。

### 3. TypeScript 类型提示不工作？

确保 package.json 中的 types 字段正确指向类型定义文件。

### 4. 组件在移动端显示异常？

确保在 HTML head 中添加了 viewport meta 标签：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
