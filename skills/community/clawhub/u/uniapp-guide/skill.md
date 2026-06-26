# Uni-app 跨平台应用开发专家

> 一站式 uni-app 跨平台应用开发指导，助您快速掌握从环境配置到项目发布的全流程。

## 核心能力

- **环境配置**：Node.js、HBuilderX、微信开发者工具等开发环境搭建
- **项目创建**：Vue 3/Vite 和 Vue 2 两种版本的项目初始化
- **开发指导**：页面生命周期、组件开发、样式编写、API 调用
- **运行调试**：Web、小程序、iOS、Android 多平台调试
- **打包发布**：H5、Android APK、iOS IPA 及各小程序平台发布

## uni-app 简介

uni-app 是 DCloud（数字天堂）推出的基于 Vue.js 的跨平台开发框架，实现**一套代码，多端发布**：

- **移动端**：iOS、Android、鸿蒙OS
- **小程序**：微信、支付宝、百度、抖音、QQ、京东小程序
- **Web端**：H5、移动端H5
- **其他**：快应用

## 环境配置

### 1. Node.js 安装

```bash
# 推荐安装 v16 或 v18 LTS 版本
# Windows: 下载安装包 https://nodejs.org/
# macOS: 使用 Homebrew
brew install node@18

# 验证安装
node -v    # v18.x.x
npm -v     # 9.x.x
```

### 2. HBuilderX 安装（推荐IDE）

下载地址：https://www.dcloud.io/hbuilderx.html

配置项：
- 打开 `工具 -> 设置 -> 运行配置`
- 配置 Node.js 路径
- 配置微信开发者工具路径

### 3. 微信开发者工具

下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

安装后配置：
1. 启动微信开发者工具
2. 设置 -> 安全设置 -> 开启服务端口

## 项目创建

### 方法1：HBuilderX 可视化创建

步骤：
1. 打开 HBuilderX
2. 文件 -> 新建 -> 项目
3. 选择模板：Hello uni-app（基础模板）或 uni-ui 项目
4. 输入项目名称
5. 选择 Vue 版本（2 或 3）
6. 点击创建

### 方法2：CLI 命令行创建

```bash
# Vue 3 + Vite 版本（推荐）
npx degit dcloudio/uni-present-vue#vite my-project
cd my-project
npm install

# Vue 2 版本
npx degit dcloudio/uni-preset-vue#v2 my-project-vue2
cd my-project-vue2
npm install
```

### Vue 3 vs Vue 2 版本选择

| 场景 | 推荐版本 | 原因 |
|------|---------|------|
| 新项目 | Vue 3 | 性能更好，Composition API 更灵活 |
| 老项目维护 | Vue 2 | 稳定性高，插件生态丰富 |
| 需要更好性能 | Vue 3 | Vite 编译更快，产物更小 |
| 使用 uni-ui 最新版 | Vue 3 | uni-ui 主要支持 Vue 3 |

## 项目结构

```
my-project/
├── pages/                      # 页面目录
│   ├── index/
│   │   ├── index.vue          # 页面组件
│   │   └── index.json         # 页面配置
│   └── mine/
│       └── mine.vue
├── components/                 # 公共组件
│   └── my-component/
│       └── my-component.vue
├── static/                     # 静态资源
├── utils/                      # 工具函数
│   └── request.js
├── App.vue                     # 应用实例
├── main.js                     # 应用入口
├── manifest.json               # 应用配置
├── pages.json                  # 页面路由配置
└── uni.scss                    # 全局样式变量
```

## 核心配置

### pages.json - 页面路由配置

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页",
        "enablePullDownRefresh": true
      }
    }
  ],
  "tabBar": {
    "color": "#7A7E83",
    "selectedColor": "#007AFF",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "static/tabbar/home.png",
        "selectedIconPath": "static/tabbar/home-active.png"
      },
      {
        "pagePath": "pages/mine/mine",
        "text": "我的",
        "iconPath": "static/tabbar/mine.png",
        "selectedIconPath": "static/tabbar/mine-active.png"
      }
    ]
  }
}
```

### manifest.json - 应用配置

```json
{
  "name": "my-app",
  "appid": "__UNI__XXXXXX",
  "description": "应用描述",
  "versionName": "1.0.0",
  "versionCode": "100",
  "app-plus": {
    "usingComponents": true,
    "splashscreen": {
      "alwaysShowBeforeRender": true,
      "autoclose": true
    }
  },
  "mp-weixin": {
    "appid": "wx1234567890",
    "setting": {
      "urlCheck": false
    }
  },
  "h5": {
    "router": {
      "mode": "hash",
      "base": "./"
    }
  }
}
```

## 生命周期

### 页面生命周期（Vue 3 Composition API）

```javascript
import {
  onLoad,           // 页面加载（只调用一次）
  onShow,           // 页面显示
  onReady,          // 页面渲染完成
  onHide,           // 页面隐藏
  onUnload,         // 页面卸载
  onPullDownRefresh, // 下拉刷新
  onReachBottom     // 上拉加载
} from '@dcloudio/uni-app'

export default {
  setup() {
    // 页面加载时调用（只调用一次）
    onLoad((options) => {
      console.log('页面参数:', options)
      const id = options.id
    })

    // 下拉刷新
    onPullDownRefresh(() => {
      console.log('下拉刷新')
      setTimeout(() => {
        uni.stopPullDownRefresh()
      }, 1000)
    })

    // 上拉加载更多
    onReachBottom(() => {
      console.log('触底加载更多')
    })
  }
}
```

### Vue 2 页面生命周期

```javascript
export default {
  data() {
    return {
      title: 'Hello'
    }
  },
  onLoad(options) {
    console.log('onLoad', options)
  },
  onShow() {
    console.log('页面显示')
  },
  onReady() {
    console.log('页面渲染完成')
  },
  onPullDownRefresh() {
    setTimeout(() => {
      uni.stopPullDownRefresh()
    }, 1000)
  },
  methods: {
    fetchData() {
      // 获取数据
    }
  }
}
```

## 组件开发

### 基础组件示例

```vue
<!-- components/my-button/my-button.vue -->
<template>
  <view
    class="my-button"
    :class="[`my-button--${type}`, { 'is-disabled': disabled }]"
    @click="handleClick"
  >
    <slot></slot>
  </view>
</template>

<script>
export default {
  name: 'MyButton',
  props: {
    type: {
      type: String,
      default: 'default' // default, primary, success, warning, error
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  setup(props, { emit }) {
    const handleClick = () => {
      if (!props.disabled) {
        emit('click')
      }
    }
    return { handleClick }
  }
}
</script>

<style scoped>
.my-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
}

.my-button--primary {
  background-color: #007aff;
  color: #fff;
}

.is-disabled {
  opacity: 0.6;
  pointer-events: none;
}
</style>
```

### 使用组件

```vue
<!-- pages/index/index.vue -->
<template>
  <view class="container">
    <my-button type="primary" @click="handleClick">
      提交按钮
    </my-button>
  </view>
</template>

<script>
import MyButton from '@/components/my-button/my-button.vue'

export default {
  components: {
    MyButton
  },
  methods: {
    handleClick() {
      uni.showToast({
        title: '点击成功',
        icon: 'success'
      })
    }
  }
}
</script>
```

## API 调用

### 请求封装

```javascript
// utils/request.js
const BASE_URL = 'https://api.example.com'

const request = (options) => {
  return new Promise((resolve, reject) => {
    uni.showLoading({ title: '加载中...' })

    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': uni.getStorageSync('token') || ''
      },
      success: (res) => {
        uni.hideLoading()
        if (res.statusCode === 200 && res.data.code === 0) {
          resolve(res.data.data)
        } else {
          uni.showToast({ title: res.data.message || '请求失败', icon: 'none' })
          reject(res.data)
        }
      },
      fail: (err) => {
        uni.hideLoading()
        uni.showToast({ title: '网络请求失败', icon: 'none' })
        reject(err)
      }
    })
  })
}

export default {
  get: (url, data) => request({ url, method: 'GET', data }),
  post: (url, data) => request({ url, method: 'POST', data })
}
```

### 在页面中使用

```javascript
import request from '@/utils/request.js'

export default {
  data() {
    return {
      list: [],
      page: 1
    }
  },
  onLoad() {
    this.fetchList()
  },
  methods: {
    async fetchList() {
      try {
        const data = await request.get('/api/list', { page: this.page })
        this.list = data.list
      } catch (e) {
        console.error('获取数据失败', e)
      }
    }
  }
}
```

## 导航路由

```javascript
// 跳转到新页面（非TabBar页面）
uni.navigateTo({
  url: '/pages/detail/detail?id=123'
})

// 跳转到 TabBar 页面
uni.switchTab({
  url: '/pages/index/index'
})

// 关闭当前页面，跳转到新页面
uni.redirectTo({
  url: '/pages/detail/detail?id=123'
})

// 返回上一页面
uni.navigateBack({
  delta: 1
})
```

## 条件编译

条件编译允许针对不同平台编写特定代码：

```javascript
methods: {
  doSomething() {
    // #ifdef H5
    console.log('仅在 H5 平台执行')
    // #endif

    // #ifdef MP-WEIXIN
    console.log('仅在微信小程序执行')
    // #endif

    // #ifdef APP-PLUS
    console.log('仅在 App 端执行')
    // #endif
  }
}
```

### 条件编译平台标识

| 平台 | 标识 |
|------|------|
| 微信小程序 | MP-WEIXIN |
| 支付宝小程序 | MP-ALIPAY |
| H5 | H5 |
| App (iOS/Android) | APP-PLUS |

## 运行与调试

### HBuilderX 运行

```
1. 打开项目
2. 在工具栏选择运行目标：
   - Chrome（Web）
   - 微信开发者工具（微信小程序）
   - HBuilderX 内置基座（真机调试）
3. 点击运行按钮或使用快捷键 Ctrl+R / Cmd+R
```

### CLI 命令

```bash
npm run dev:h5         # Web开发
npm run dev:mp-weixin # 微信小程序
npm run build:h5       # Web打包
npm run build:mp-weixin # 小程序打包
```

## 常用组件库

### uni-ui（官方推荐）

```bash
npm install @dcloudio/uni-ui
```

```vue
<uni-card title="卡片标题">卡片内容</uni-card>
<uni-button type="primary">按钮</uni-button>
<uni-list>
  <uni-list-item title="列表项1" :show-arrow="true" />
</uni-list>
```

### uView UI

```bash
npm i uview-ui
```

```vue
<u-button type="primary" @click="handleClick">提交</u-button>
<u-input v-model="value" placeholder="请输入" />
```

## 最佳实践

### 项目架构建议

```
├── api/                      # API 接口定义
├── components/               # 公共组件
├── pages/                    # 页面
├── static/                   # 静态资源
├── stores/                   # Pinia stores
├── styles/                   # 全局样式
├── utils/                    # 工具函数
├── App.vue
├── main.js
└── manifest.json
```

### 性能优化建议

```javascript
// 1. 列表渲染使用唯一 key
<view v-for="(item, index) in list" :key="item.id">
  {{ item.name }}
</view>

// 2. 图片懒加载
<image lazy-load />

// 3. 合理使用分包加载
```

## 学习资源

- **官方文档**：https://uniapp.dcloud.net.cn/
- **uni-ui 组件**：https://uniapp.dcloud.net.cn/component/uniui/
- **DCloud 社区**：https://ask.dcloud.net.cn/
- **插件市场**：https://ext.dcloud.net.cn/

## 使用示例

当用户询问 uni-app 相关问题时，根据用户需求提供针对性的指导：

- **入门问题**：提供环境配置和项目创建指导
- **开发问题**：提供组件、生命周期、API 等具体代码示例
- **发布问题**：提供各平台的打包和发布流程
- **调试问题**：提供多平台调试技巧和方法

---

**版本**：v1.0.0
**作者**：MiniMax Agent
**标签**：uni-app, 跨平台, Vue, 小程序, 移动开发
