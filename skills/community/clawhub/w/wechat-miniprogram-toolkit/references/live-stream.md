# 微信小程序直播与实时音视频全指南

## 激活契约

**符合以下任一场景时加载：**
- 小程序直播、直播间、live-player、live-pusher
- 实时音视频通话、TRTC、视频会议、语音聊天室
- 视频上传、视频播放、视频通话、在线教育
- 直播带货、带货主播、连麦 PK

---

## 一、能力矩阵

| 能力 | 组件/API | 适用场景 |
|------|---------|---------|
| 直播推流 | `<live-pusher>` | 主播端：摄像头+麦克风推流 |
| 直播拉流 | `<live-player>` | 观众端：播放直播流 |
| 实时音视频（TRTC）| `trtc-pusher` / `trtc-player` | 双向视频通话、连麦 |
| 视频播放 | `<video>` | 点播、回放 |
| 视频上传 | `wx.chooseVideo` + 云存储 | 用户上传视频 |

---

## 二、直播组件（微信小程序直播）

> 微信小程序自带「小程序直播」插件，适合电商带货等场景。也可使用自主研发的 TRTC 方案。

### 2.1 开通条件

- 已认证的企业/个体工商户小程序
- 类目符合直播开放范围（电商/教育/医疗等）
- 在小程序管理后台 → 直播 → 开通

### 2.2 引入直播组件

```json
// app.json
{
  "plugins": {
    "live-player-plugin": {
      "version": "3.3.2",  // 使用最新版
      "provider": "wx2b03c6e691cd7370"  // 固定 plugin id
    }
  }
}
```

### 2.3 拉取直播间列表

```javascript
// pages/live/room-list.js
Page({
  data: { rooms: [] },

  async onLoad() {
    // ⚠️ 直播列表接口需要在小程序后台配置
    const res = await wx.request({
      url: 'https://api.weixin.qq.com/wxa/business/getliveinfo',
      method: 'GET',
      data: {
        access_token: wx.getStorageSync('access_token'),
        start: 0,
        limit: 10,
      }
    })
    this.setData({ rooms: res.data.room_info || [] })
  },

  // 进入直播间
  enterRoom(roomId) {
    wx.navigateTo({
      url: `plugin://live-player-plugin?room_id=${roomId}`,
    })
  },
})
```

### 2.4 直播间页面

```xml
<!-- pages/live/room.wxml -->
<view class="room">
  <!-- 直播播放器（微信直播插件）-->
  <live-player
    src="{{streamUrl}}"
    mode="live"
    autoplay
    bindstatechange="onPlayerStateChange"
    binderror="onPlayerError"
  />

  <!-- 弹幕层 -->
  <view class="danmu-list">
    <view wx:for="{{danmus}}" wx:key="id">{{item.text}}</view>
  </view>

  <!-- 商品列表 -->
  <view class="goods-list" wx:if="{{showGoods}}">
    <view wx:for="{{goods}}" wx:key="id" class="goods-item">
      <image src="{{item.cover}}" />
      <text>{{item.name}}</text>
      <text class="price">¥{{item.price}}</text>
      <button size="mini" bindtap="buyGoods" data-id="{{item.id}}">购买</button>
    </view>
  </view>

  <!-- 底部互动栏 -->
  <view class="action-bar">
    <input bindinput="onDanmuInput" placeholder="发弹幕..." />
    <button bindtap="sendDanmu">发送</button>
    <button bindtap="toggleGoods">{{showGoods ? '收起' : '商品'}}</button>
  </view>
</view>
```

```javascript
// pages/live/room.js
Page({
  data: {
    streamUrl: '',
    danmus: [],
    goods: [],
    showGoods: false,
  },

  onLoad(options) {
    const { roomId } = options
    this.fetchRoomInfo(roomId)
  },

  async fetchRoomInfo(roomId) {
    // 从自己的服务端获取直播信息
    const res = await wx.cloud.callFunction({
      name: 'getLiveRoom',
      data: { roomId },
    })
    this.setData({
      streamUrl: res.result.pushUrl,  // 推流地址
      goods: res.result.goods || [],
    })
  },

  // 播放器状态变化
  onPlayerStateChange(e) {
    const { code, message } = e.detail
    if (code === 2007) console.log('视频加载中...')
    if (code === 2004) console.log('正在播放')
    if (code === -2301) console.error('网络错误，请检查网络')
  },

  // 播放器错误
  onPlayerError(e) {
    wx.showToast({ title: '直播已结束', icon: 'none' })
  },

  // 发送弹幕（通过云函数广播）
  async sendDanmu() {
    const { danmuText } = this.data
    await wx.cloud.callFunction({
      name: 'broadcastDanmu',
      data: { text: danmuText, roomId: this.data.roomId },
    })
  },

  // 加入/退出商品列表
  toggleGoods() {
    this.setData({ showGoods: !this.data.showGoods })
  },
})
```

---

## 三、实时音视频（TRTC）

> 适合：视频通话、在线会议、互动课堂、连麦 PK、语音聊天室

### 3.1 引入 TRTC 组件

```json
// app.json
{
  "plugins": {
    "trtc-plugin": {
      "version": "1.0.0",  // 使用最新版
      "provider": "wx71e0xxxxxxxxxxx"  // 腾讯云 TRTC plugin id
    }
  }
}
```

### 3.2 TRTC 推流端

```xml
<!-- pages/trtc/pusher.wxml -->
<trtc-pusher
  id="pusher"
  url="{{pushUrl}}"
  mode="RTC"
  enable-camera="{{enableCamera}}"
  enable-microphone="{{enableMic}}"
  beauty="{{beautyLevel}}"
  whiteness="{{whitenessLevel}}"
  bindonerror="onPushError"
  bindonstats="onPushStats"
/>

<view class="control-bar">
  <button bindtap="toggleCamera">{{enableCamera ? '关摄像头' : '开摄像头'}}</button>
  <button bindtap="toggleMic">{{enableMic ? '闭麦' : '开麦'}}</button>
  <button bindtap="switchCamera">切换摄像头</button>
  <button type="warn" bindtap="leaveRoom">离开</button>
</view>
```

```javascript
// pages/trtc/pusher.js
Page({
  data: {
    pushUrl: '',
    enableCamera: true,
    enableMic: true,
    beautyLevel: 5,
    whitenessLevel: 3,
    roomId: '',
    userId: wx.getStorageSync('userId'),
  },

  async onLoad(options) {
    const { roomId } = options
    this.setData({ roomId })

    // 从云函数获取 TRTC 签名
    const res = await wx.cloud.callFunction({
      name: 'getTRTCSig',
      data: {
        roomId,
        userId: this.data.userId,
        role: 'anchor',  // 主播角色
      },
    })

    // 生成推流地址（腾讯云 TRTC 需自行拼接或用云函数生成）
    this.setData({ pushUrl: res.result.pushUrl })
  },

  toggleCamera() {
    const pusher = this.selectComponent('#pusher')
    pusher.setData({ 'enable-camera': !this.data.enableCamera })
    this.setData({ enableCamera: !this.data.enableCamera })
  },

  toggleMic() {
    const pusher = this.selectComponent('#pusher')
    pusher.setData({ 'enable-microphone': !this.data.enableMic })
    this.setData({ enableMic: !this.data.enableMic })
  },

  switchCamera() {
    const pusher = this.selectComponent('#pusher')
    pusher.switchCamera()
  },

  onPushError(e) {
    wx.showToast({ title: '推流失败：' + e.detail.errMsg, icon: 'none' })
  },

  onPushStats(e) {
    // 实时网络状态（可展示给用户）
    console.log('视频码率:', e.detail.videoBitrate)
    console.log('音频码率:', e.detail.audioBitrate)
    console.log('网络质量:', e.detail.networkQuality)  // 0=unknown, 1=好, 2=中等, 3=差
  },

  leaveRoom() {
    wx.navigateBack()
    // 云函数：通知房间内其他用户该用户已离开
    wx.cloud.callFunction({ name: 'leaveTRTCRoom', data: { roomId: this.data.roomId } })
  },
})
```

### 3.3 TRTC 拉流端（观众）

```xml
<!-- pages/trtc/player.wxml -->
<trtc-player
  wx:for="{{remoteUsers}}"
  wx:key="userId"
  id="player-{{item.userId}}"
  url="{{item.url}}"
  mode="RTC"
  object-fit="fillCrop"
  enable-camera="{{item.hasCamera}}"
  enable-microphone="{{item.hasMic}}"
/>

<!-- 本地预览小窗 -->
<trtc-player
  id="local-preview"
  url="{{localUrl}}"
  mode="RTC"
  object-fit="fillCrop"
  style="position:fixed; right:16rpx; bottom:200rpx; width:200rpx; height:300rpx;"
/>
```

```javascript
// pages/trtc/player.js
Page({
  data: {
    roomId: '',
    localUrl: '',
    remoteUsers: [],  // [{userId, url, hasCamera, hasMic}]
  },

  async onLoad(options) {
    const { roomId } = options
    this.setData({ roomId })

    const res = await wx.cloud.callFunction({
      name: 'getTRTCSig',
      data: {
        roomId,
        userId: this.data.userId,
        role: 'user',  // 观众角色
      },
    })

    this.setData({ localUrl: res.result.playUrl })
    // 加入房间（云函数通知房间内所有人）
    await wx.cloud.callFunction({
      name: 'joinTRTCRoom',
      data: { roomId, userId: this.data.userId },
    })
  },

  // 监听新用户加入
  onRemoteUserJoin(userId) {
    const users = this.data.remoteUsers
    users.push({ userId, url: '', hasCamera: true, hasMic: true })
    this.setData({ remoteUsers: users })
  },
})
```

---

## 四、视频上传与点播

### 4.1 用户上传视频

```javascript
// 选择 + 上传到云存储
async function uploadVideo() {
  const { tempFilePath } = await wx.chooseVideo({
    sourceType: ['album', 'camera'],
    maxDuration: 60,      // 最长60秒
    camera: 'back',
  })

  // ⚠️ 视频文件较大，建议先压缩
  const compressed = await wx.compressVideo({
    src: tempFilePath,
    quality: 'medium',    // low / medium / high
    bitrate: 1500,
  })

  // 上传到云存储
  const res = await wx.cloud.uploadFile({
    cloudPath: `videos/${Date.now()}.mp4`,
    filePath: compressed.tempFilePath,
  })

  console.log('视频上传成功，fileID:', res.fileID)
  return res.fileID
}
```

### 4.2 视频播放

```xml
<video
  id="myVideo"
  src="{{videoUrl}}"
  poster="{{coverImage}}"
  controls
  show-fullscreen-btn
  enable-danmu
  danmu-list="{{danmuList}}"
  bindtimeupdate="onTimeUpdate"
  bindended="onVideoEnd"
  object-fit="fill"
/>
```

```javascript
// 分段加载：视频太大时使用云存储临时链接
async function getVideoUrl(fileID) {
  const res = await wx.cloud.getTempFileURL({ fileList: [fileID] })
  return res.fileList[0].tempFileURL
},

// 弹幕列表（从数据库加载）
async function loadDanmu(videoId) {
  const res = await wx.cloud.callFunction({
    name: 'getDanmu',
    data: { videoId },
  })
  return res.result.list
},
```

---

## 五、Common Mistakes（直播/实时音视频高频错误）

| 错误 | 正确做法 |
|------|---------|
| 直播组件不传 `mode="live"` | 实时互动用 `RTC`，直播观看用 `live` |
| 不处理 `binderror` | 必须监听错误，防止用户看到黑屏不知原因 |
| TRTC 不传 `role` 参数 | 主播用 `anchor`，观众用 `user`，影响权限 |
| 视频不压缩直接上传 | 微信要求视频不超过 20MB，超过需压缩 |
| 直播弹幕存在前端内存 | 弹幕应通过 WebSocket/云函数实时广播 |
| TRTC 签名放小程序前端 | 签名必须在云函数内生成，绝不暴露密钥 |
| 房间 ID 直接用数字 | 房间 ID 应为字符串，防止大数精度丢失 |
| 进入直播间不先加入房间 | 先 `joinTRTCRoom` 再拉流，防止卡顿 |

---

## 六、官方文档链接

- 小程序直播组件：https://developers.weixin.qq.com/miniprogram/dev/framework/liveplayer/live-player-plugin.html
- live-player 组件：https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
- live-pusher 组件：https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
- TRTC 小程序 SDK：https://cloud.tencent.com/document/product/647/63716
- 视频上传：https://developers.weixin.qq.com/miniprogram/dev/api/media/video/wx.chooseVideo.html
