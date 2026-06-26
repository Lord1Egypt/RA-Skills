# 页面开发参考

## 页面结构规范

每个页面必须包含以下4个文件：

```
pages/<name>/index.tsx   # 页面逻辑 (React Component)
pages/<name>/index.scss   # 页面样式 (SCSS)
pages/<name>/index.config.js  # 页面配置（可选，覆盖全局 window 配置）
```

## 路由与跳转

```typescript
// 声明式跳转（保留当前页，可返回）
import { navigateTo } from '@tarojs/taro'
navigateTo({ url: '/pages/home/index' })

// 替换当前页（不可返回）
import { redirectTo } from '@tarojs/taro'
redirectTo({ url: '/pages/home/index' })

// 跳转到 TabBar 页面
import { switchTab } from '@tarojs/taro'
switchTab({ url: '/pages/home/index' })

// 关闭所有页面，跳转
import { reLaunch } from '@tarojs/taro'
reLaunch({ url: '/pages/home/index' })
```

## TabBar 注意事项

TabBar 页面必须在 `app.config.js` 的 `tabBar.list` 中注册，且使用 `switchTab` 跳转，不能用 `navigateTo`。

## 状态管理

```typescript
// 推荐：组件内 useState
state = { data: null, loading: true }

// 推荐：页面参数获取
const taskId = (this as any).$router?.params?.taskId
```

## 生命周期

| 生命周期 | 说明 |
|---------|------|
| `componentDidMount()` | 组件挂载完成（替代 onLoad）|
| `componentDidShow()` | 页面显示 |
| `componentDidHide()` | 页面隐藏 |
| `componentWillUnmount()` | 组件卸载 |

## 存储

```typescript
// 存
wx.setStorageSync('key', value)

// 取
const value = wx.getStorageSync('key')

// 清除
wx.clearStorageSync()
```

## 下拉刷新

```typescript
// 页面配置
config/index.js 或 page.config.js:
{
  enablePullDownRefresh: true,
  backgroundTextStyle: 'dark'
}

// 监听
onPullDownRefresh() {
  // fetch data
  wx.stopPullDownRefresh()
}
```

## 上拉加载

```typescript
onReachBottom() {
  // load more
}
```
