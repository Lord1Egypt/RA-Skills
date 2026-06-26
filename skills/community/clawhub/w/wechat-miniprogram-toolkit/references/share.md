# 微信小程序分享能力全指南

## 激活契约

**符合以下任一场景时加载：**
- 小程序分享、share、onShareAppMessage、onShareTimeline
- 分享卡片、分享海报、生成海报、shareImage
- 分享朋友圈、shareToTimeline、wx.showShareMenu
- 转发邀请、邀请好友、shareMessage

---

## 一、分享能力矩阵

| 能力 | 触发方式 | 分享位置 |
|------|---------|---------|
| 页面转发 | 点击右上角"···" → 转发 | 微信好友 |
| 小程序分享卡片 | 按钮触发 `wx.showShareMenu` | 微信好友 |
| 朋友圈分享 | `onShareTimeline`（需满足条件） | 朋友圈 |
| 分享海报 | canvas 绘制 + 保存图片 | 生成图片分享 |
| 消息订阅 | `wx.requestSubscribeMessage` | 推送通知 |

---

## 二、好友分享（页面转发）

### 2.1 启用页面转发

```javascript
// pages/index/index.js

// 方式 A：在页面配置中启用（推荐）
Page({
  onShareAppMessage(options) {
    const { from, target } = options

    // 用户点击右上角"···"触发
    if (from === 'menu') {
      return this.getShareConfig()
    }

    // 用户点击页面内按钮触发（button 的 open-type="share"）
    if (from === 'button' && target) {
      return {
        title: '快来一起玩！',
        path: `/pages/index/index?from=${target.dataset.userId}`,
        imageUrl: '/assets/share-cover.png',
      }
    }
  },

  getShareConfig() {
    return {
      title: '小程序名称',              // 分享标题（默认用 app.json 的 title）
      desc: '一句话介绍你的小程序',       // 分享描述（部分场景展示）
      path: '/pages/index/index',       // 分享后打开的页面路径
      imageUrl: '/assets/share-cover.png', // 自定义分享图片（建议比例 5:4）
    }
  },
})
```

### 2.2 全局默认分享配置

> 如果每个页面都写 `onShareAppMessage` 太繁琐，可以用 Component 构造器劫持

```javascript
// components/share-handler/index.js
Component({
  pageLifetimes: {
    show() {
      // 劫持页面 show 重新注入分享配置
      if (this.shareConfig) {
        wx.showShareMenu({ withShareTicket: true })
      }
    }
  },

  methods: {
    // 设置该页面的分享配置
    setShareConfig(config = {}) {
      this.shareConfig = {
        title: config.title || '默认标题',
        path: config.path || getCurrentPages().slice(-1)[0].route,
        imageUrl: config.imageUrl || '',
        ...config,
      }
    },
  }
})

// 在页面 JSON 中引用：
// { "usingComponents": { "share-handler": "/components/share-handler/index" } }
```

---

## 三、朋友圈分享（onShareTimeline）

> ⚠️ **重要条件**：小程序需已发布（不能是体验版/开发版），且类目符合微信开放范围

### 3.1 启用朋友圈分享

```javascript
// pages/index/index.js
Page({
  // ⚠️ 必须返回对象，否则朋友圈分享按钮不显示
  onShareTimeline() {
    return {
      title: '小程序标题',              // 朋友圈分享标题
      query: 'from=timeline',          // 附加参数（打开小程序时可在 onLoad 中获取）
      imageUrl: '/assets/timeline-cover.png',  // 朋友圈分享缩略图（建议正方形 5:5）
    }
  },
})
```

### 3.2 朋友圈分享与好友分享的区别

| 属性 | 好友分享 | 朋友圈分享 |
|------|---------|-----------|
| `title` | ✅ 支持 | ✅ 支持 |
| `desc` | ✅ 支持 | ❌ 不支持 |
| `path` | ✅ 支持 | ❌（用 `query` 替代）|
| `imageUrl` | ✅ 支持 | ✅ 支持 |
| `imageUrl` 建议尺寸 | 5:4 | 1:1（正方形）|

---

## 四、分享海报（Canvas 绘制）

### 4.1 绘制分享海报

```javascript
// pages/share/poster.js
Page({
  data: { posterUrl: '' },

  async onLoad(options) {
    const { goodsId } = options
    const goods = await this.fetchGoods(goodsId)
    const poster = await this.drawPoster(goods)
    this.setData({ posterUrl: poster })
  },

  async drawPoster(goods) {
    return new Promise((resolve) => {
      const ctx = wx.createCanvasContext('share-canvas')

      // 画布尺寸（标准海报比例 750:1000）
      const W = 750
      const H = 1000

      // 1. 白色背景
      ctx.setFillStyle('#ffffff')
      ctx.fillRect(0, 0, W, H)

      // 2. 顶部商品图（先下载到本地再画）
      wx.cloud.getTempFileURL({ fileList: [goods.coverUrl] }).then(res => {
        ctx.drawImage(res.fileList[0].tempFileURL, 0, 0, W, 500)
        ctx.draw()

        // 3. 商品标题
        ctx.setFontSize(36)
        ctx.setFillStyle('#333333')
        ctx.setTextAlign('left')
        ctx.fillText(goods.name, 40, 560, W - 80)

        // 4. 价格
        ctx.setFontSize(48)
        ctx.setFillStyle('#ff4757')
        ctx.fillText(`¥${goods.price}`, 40, 640)

        // 5. 二维码区域（白色卡片）
        ctx.setFillStyle('#f5f5f5')
        ctx.fillRect(W/2 - 140, 720, 280, 280)

        // 6. 小程序码（通过云调用生成）
        this.generateQRCode(goods.id).then(qrUrl => {
          ctx.drawImage(qrUrl, W/2 - 100, 740, 200, 200)
          ctx.draw(true)  // 最后一个参数 true 表示把之前的内容也合并进来

          // 7. 提示文字
          ctx.setFontSize(24)
          ctx.setFillStyle('#999999')
          ctx.setTextAlign('center')
          ctx.fillText('长按识别小程序', W / 2, 980)

          ctx.draw(true)

          // 8. 导出图片
          wx.canvasToTempFilePath({
            canvasId: 'share-canvas',
            x: 0,
            y: 0,
            width: W,
            height: H,
            destWidth: W * 2,   // 建议 2x 清晰度
            destHeight: H * 2,
            success: (res) => resolve(res.tempFilePath),
            fail: (err) => console.error(err),
          })
        })
      })
    })
  },

  // 生成小程序码（云函数）
  async generateQRCode(goodsId) {
    const res = await wx.cloud.callFunction({
      name: 'createQRCode',
      data: {
        scene: `goodsId=${goodsId}`,   // 最多 32 个字符
        page: 'pages/goods/detail',     // 必须已发布的小程序页面
        width: 280,
      },
    })
    // res.result 已经是云存储的 fileID，直接用 getTempFileURL 获取临时链接
    const urlRes = await wx.cloud.getTempFileURL({ fileList: [res.result.fileID] })
    return urlRes.fileList[0].tempFileURL
  },

  // 保存到相册
  async savePoster() {
    const { posterUrl } = this.data

    // 先请求相册权限
    const setting = await wx.getSetting()
    if (!setting.authSetting['scope.writePhotosAlbum']) {
      const res = await wx.authorize({ scope: 'scope.writePhotosAlbum' })
      if (res.errMsg !== 'authorize:ok') {
        wx.showToast({ title: '请允许保存到相册', icon: 'none' })
        return
      }
    }

    wx.saveImageToPhotosAlbum({
      filePath: posterUrl,
      success: () => wx.showToast({ title: '已保存到相册', icon: 'success' }),
      fail: (err) => wx.showToast({ title: '保存失败', icon: 'none' }),
    })
  },
})
```

```xml
<!-- pages/share/poster.wxml -->
<view class="poster-page">
  <!-- 隐藏的 canvas（用于绘制海报） -->
  <canvas
    canvas-id="share-canvas"
    style="width:750px; height:1000px; position:absolute; left:-9999px;"
  />

  <!-- 预览区域 -->
  <image
    wx:if="{{posterUrl}}"
    src="{{posterUrl}}"
    mode="widthFix"
    class="poster-preview"
  />

  <view class="actions">
    <button bindtap="savePoster" type="primary">保存到相册</button>
    <button open-type="share">分享给好友</button>
  </view>
</view>
```

---

## 五、分享数据追踪

```javascript
// utils/shareTracker.js  — 追踪分享效果

// 在页面 onShareAppMessage 中注入追踪
function trackShare(shareType, targetPath) {
  wx.reportEvent('share', {
    share_type: shareType,      // 'friend' | 'timeline' | 'poster'
    share_path: targetPath,
    share_scene: wx.getLaunchOptionsSync().scene,
    timestamp: Date.now(),
  })
}

// 在小程序码/海报的 onLoad 中追踪来源
function trackShareSource(query) {
  if (query.from_share) {
    wx.reportEvent('share_convert', {
      source_path: query.from_share || '',
      target_path: getCurrentPages().slice(-1)[0].route,
    })
  }
}

module.exports = { trackShare, trackShareSource }
```

---

## 六、订阅消息（分享后的通知触达）

> 用户分享后，通过订阅消息通知被分享者

```javascript
// pages/index/index.js
Page({
  // 分享成功后引导用户订阅通知
  onShareAppMessage(options) {
    // 分享后弹窗引导订阅
    setTimeout(() => {
      this.requestSubscribeMessage()
    }, 100)

    return {
      title: '邀请你加入！',
      path: `/pages/invite/accept?from=${wx.getStorageSync('openid')}`,
    }
  },

  // 请求订阅消息权限
  async requestSubscribeMessage() {
    // ⚠️ 需在微信公众平台配置订阅消息模板
    const tmplIds = [
      'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',  // 模板消息 ID（需在后台申请）
    ]

    const res = await wx.requestSubscribeMessage({
      tmplIds,
      success: (r) => {
        if (r[tmplIds[0]] === 'accept') {
          wx.showToast({ title: '已订阅，有更新会通知你', icon: 'success' })
        }
      }
    })
  },
})
```

---

## 七、Common Mistakes（分享高频错误）

| 错误 | 正确做法 |
|------|---------|
| onShareTimeline 返回 undefined | 必须返回 `{title, query, imageUrl}` 三个字段的对象 |
| 朋友圈分享用 `path` | 朋友圈分享应用 `query`，`path` 不生效 |
| canvas 绘制跨域图片不处理 | 必须先 `wx.cloud.getTempFileURL` 转临时链接 |
| canvas 不设置 `destWidth/destHeight` | 2x 分辨率，否则在高清屏上模糊 |
| 分享海报二维码用 `scene` 超过32字符 | scene 最多32字符，超长需编码 |
| 不请求相册权限直接保存 | 必须先 `wx.authorize({scope:'scope.writePhotosAlbum'})` |
| onShareTimeline 在开发版测试 | onShareTimeline 必须在已发布版本才生效（朋友圈入口）|
| 分享卡片图片太大 | 建议不超过 128KB，否则可能被压缩 |

---

## 八、官方文档链接

- 页面分享：https://developers.weixin.qq.com/miniprogram/dev/component/form/button.html（button share）
- onShareAppMessage：https://developers.weixin.qq.com/miniprogram/dev/reference/api/Page.html#onshareappmessageoptions
- onShareTimeline：https://developers.weixin.qq.com/miniprogram/dev/reference/api/Page.html#onsharetimeline
- canvas 绘制：https://developers.weixin.qq.com/miniprogram/dev/component/canvas.html
- 小程序码：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/qr-code/createQRCode.html
