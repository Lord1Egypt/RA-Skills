# 微信小程序全局配置 app.json

小程序根目录下的 app.json 文件用来对微信小程序进行全局配置。文件内容为一个 JSON 对象。

## 配置项

| 属性 | 类型 | 必填 | 描述 |
|------|------|------|------|
| entryPagePath | string | 否 | 小程序默认启动首页 |
| pages | string[] | 是 | 页面路径列表 |
| window | Object | 否 | 全局的默认窗口表现 |
| tabBar | Object | 否 | 底部 tab 栏的表现 |
| networkTimeout | Object | 否 | 网络超时时间 |
| debug | boolean | 否 | 是否开启 debug 模式 |
| functionalPages | boolean | 否 | 是否启用插件功能页 |
| subpackages | Object[] | 否 | 分包结构配置 |
| workers | string | 否 | Worker 代码放置的目录 |
| requiredBackgroundModes | string[] | 否 | 需要在后台使用的能力 |
| requiredPrivateInfos | string[] | 否 | 调用的地理位置相关隐私接口 |
| plugins | Object | 否 | 使用到的插件 |
| preloadRule | Object | 否 | 分包预下载规则 |
| resizable | boolean | 否 | PC/iPad 小程序窗口调整 |
| usingComponents | Object | 否 | 全局自定义组件配置 |
| permission | Object | 否 | 小程序接口权限相关设置 |
| sitemapLocation | string | 是 | 指明 sitemap.json 的位置 |
| style | string | 否 | 指定使用升级后的 weui 样式 |
| useExtendedLib | Object | 否 | 指定需要引用的扩展库 |
| darkmode | boolean | 否 | 小程序支持 DarkMode |
| themeLocation | string | 否 | 指明 theme.json 的位置 |
| lazyCodeLoading | string | 否 | 配置自定义组件代码按需注入 |

## window 配置

用于设置小程序的状态栏、导航条、标题、窗口背景色。

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| navigationBarBackgroundColor | HexColor | #000000 | 导航栏背景颜色 |
| navigationBarTextStyle | string | white | 导航栏标题颜色，black/white |
| navigationBarTitleText | string | - | 导航栏标题文字内容 |
| navigationStyle | string | default | 导航栏样式，default/custom |
| backgroundColor | HexColor | #ffffff | 窗口的背景色 |
| backgroundTextStyle | string | dark | 下拉 loading 样式，dark/light |
| enablePullDownRefresh | boolean | false | 是否开启全局下拉刷新 |
| onReachBottomDistance | number | 50 | 页面上拉触底事件触发距离(px) |
| pageOrientation | string | portrait | 屏幕旋转设置 |

## tabBar 配置

如果小程序是一个多 tab 应用，可以通过 tabBar 配置项指定 tab 栏的表现。

| 属性 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| color | HexColor | 是 | - | tab 上文字默认颜色 |
| selectedColor | HexColor | 是 | - | tab 上文字选中时颜色 |
| backgroundColor | HexColor | 是 | - | tab 的背景色 |
| borderStyle | string | 否 | black | tabbar 上边框颜色 |
| list | Array | 是 | - | tab 列表，最少2个最多5个 |
| position | string | 否 | bottom | tabBar 位置，bottom/top |
| custom | boolean | 否 | false | 自定义 tabBar |

## networkTimeout 配置

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| request | number | 60000 | wx.request 超时时间(ms) |
| connectSocket | number | 60000 | wx.connectSocket 超时时间(ms) |
| uploadFile | number | 60000 | wx.uploadFile 超时时间(ms) |
| downloadFile | number | 60000 | wx.downloadFile 超时时间(ms) |

## 示例

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "navigationBarBackgroundColor": "#000000",
    "navigationBarTextStyle": "white",
    "navigationBarTitleText": "小程序标题",
    "backgroundColor": "#ffffff"
  },
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#007AFF",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "icons/home.png",
        "selectedIconPath": "icons/home-active.png"
      }
    ]
  },
  "debug": true
}
```