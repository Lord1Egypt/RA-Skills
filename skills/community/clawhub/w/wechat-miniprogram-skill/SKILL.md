---
name: wechat-miniprogram-skill
version: 1.0.0
description: 微信小程序开发指南 - 从入门到精通。当用户提到微信小程序、小程序开发、WeChat Mini Program、wx API、微信小程序框架时使用此技能。
---

# 微信小程序开发 Skill

> 微信小程序开发指南 - 从入门到精通

## 官方文档

- 开发文档: https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/
- 框架参考: https://developers.weixin.qq.com/miniprogram/dev/reference/
- 组件文档: https://developers.weixin.qq.com/miniprogram/dev/component/
- API 文档: https://developers.weixin.qq.com/miniprogram/dev/api/

---

## 小程序简介

小程序是一种全新的连接用户与服务的方式，可以在微信内被便捷地获取和传播。

### 技术特点

- **快速加载**：从微信本地加载资源
- **原生体验**：流畅的页面切换和操作反馈
- **强大能力**：拍摄、录音、支付、分享等
- **易开发**：类似 Web 开发，学习成本低

### 与 Web 开发的区别

| 特性 | 小程序 | Web |
|------|--------|-----|
| 渲染线程 | 双线程 | 单线程 |
| DOM API | 不可用 | 可用 |
| jQuery/Zepto | 不可用 | 可用 |
| 运行环境 | iOS/Android 微信客户端 | 浏览器 |

---

## 项目结构

```
miniprogram/
├── app.js              # 小程序入口文件
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── pages/              # 页面目录
│   └── index/
│       ├── index.js
│       ├── index.json
│       ├── index.wxml
│       └── index.wxss
├── components/         # 自定义组件
└── utils/              # 工具函数
```

---

## 全局配置 (app.json)

```json
{
  "pages": ["pages/index/index"],
  "window": {
    "navigationBarBackgroundColor": "#000000",
    "navigationBarTextStyle": "white",
    "navigationBarTitleText": "小程序标题"
  },
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#007AFF",
    "list": [
      {"pagePath": "pages/index/index", "text": "首页"}
    ]
  }
}
```

---

## 页面注册 (Page)

```javascript
Page({
  data: {
    text: "Hello World"
  },

  onLoad: function(options) {
    // 页面创建时执行
  },

  onShow: function() {
    // 页面出现在前台
  },

  onPullDownRefresh: function() {
    // 下拉刷新
  },

  handleTap: function() {
    this.setData({ text: '点击了' });
  }
});
```

---

## 模板语法 (WXML)

```xml
<!-- 数据绑定 -->
<view>{{message}}</view>

<!-- 列表渲染 -->
<view wx:for="{{array}}" wx:key="id">{{item.name}}</view>

<!-- 条件渲染 -->
<view wx:if="{{condition}}">显示</view>

<!-- 事件处理 -->
<view bindtap="handleTap">点击</view>
```

---

## 常用 API

### 网络请求

```javascript
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  success: function(res) {
    console.log(res.data);
  }
});
```

### 路由跳转

```javascript
wx.navigateTo({ url: '/pages/detail/detail?id=1' });
wx.redirectTo({ url: '/pages/index/index' });
wx.switchTab({ url: '/pages/index/index' });
wx.navigateBack({ delta: 1 });
```

### 数据缓存

```javascript
wx.setStorageSync('key', 'value');
const value = wx.getStorageSync('key');
```

---

## 自定义组件

```javascript
Component({
  properties: {
    title: { type: String, value: '默认标题' }
  },
  data: { count: 0 },
  methods: {
    increment: function() {
      this.setData({ count: this.data.count + 1 });
      this.triggerEvent('change', { count: this.data.count });
    }
  }
});
```

---

## 注意事项

1. **域名配置**：request 域名需在小程序后台配置
2. **HTTPS 要求**：所有网络请求必须使用 HTTPS
3. **代码包大小**：主包限制 2MB，总分包限制 20MB
4. **用户隐私**：使用地理位置等敏感接口需声明

---

## 参考资源

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/)
- [小程序组件参考](https://developers.weixin.qq.com/miniprogram/dev/component/)
- [小程序 API 参考](https://developers.weixin.qq.com/miniprogram/dev/api/)

## 参考资料

更多小程序文档请参考 `references/` 目录下的文档文件。