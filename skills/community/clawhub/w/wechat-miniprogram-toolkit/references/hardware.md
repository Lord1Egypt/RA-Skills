# 微信小程序硬件能力全指南

## 激活契约

**符合以下任一场景时加载：**
- 蓝牙、BLE、iBeacon、设备连接
- GPS、地理位置、坐标、经纬度、location
- NFC、射频、门禁、刷卡、碰一碰
- Wi-Fi 连接、startWifi、连接无线网
- 扫码、scanCode、条形码、二维码
- 设备硬件、传感器、陀螺仪、加速度计

---

## 一、硬件能力矩阵

| 能力 | API | 典型场景 | 权限申请 |
|------|-----|---------|---------|
| 蓝牙低功耗 | `wx.openBluetoothAdapter` 等 | 设备控制、健康数据、定位信标 | 需要申请（个人可申请）|
| GPS 定位 | `wx.getLocation` | 地图、附近功能、导航 | 需要申请（个人可申请）|
| NFC | `wx.getNFCAdapter` | 门禁、支付、标签读取 | 需要企业资质 |
| Wi-Fi | `wx.startWifi` | 智能设备配网 | 需要申请（个人可申请）|
| 扫码 | `wx.scanCode` | 付款、验票、扫码点餐 | 小程序自带权限 |
| 设备信息 | `wx.getDeviceInfo` | 系统信息、设备 ID | 小程序自带权限 |

---

## 二、蓝牙低功耗（BLE）

> ⚠️ 基础库 1.1.0+ 支持。iOS 和 Android 实现有差异，iOS 需使用 CoreBluetooth。

### 2.1 初始化与权限检查

```javascript
// utils/ble.js

class BLEManager {
  constructor() {
    this.deviceId = null
    this.serviceId = null
    this.characteristicId = null
    this.connected = false
    this._listeners = {}
  }

  // 初始化蓝牙模块
  async init() {
    // wx.getBluetoothAdapterState() 已在部分版本废弃，
    // 改用 openBluetoothAdapter 的返回值判断（失败即不可用）
    try {
      await wx.openBluetoothAdapter()
    } catch (err) {
      if (err.errMsg?.includes('not available')) {
        throw new Error('当前设备不支持蓝牙')
      }
      if (!err.errMsg?.includes('already been opened')) {
        throw err
      }
    }

    // 监听蓝牙适配器状态变化（广播，可多次调用）
    wx.onBluetoothAdapterStateChange(res => {
      if (!res.available || !res.discovering) {
        console.warn('[BLE] 蓝牙适配器状态变化', res)
      }
      this._emit('stateChange', res)
    })

    // 监听低功耗蓝牙连接
    wx.onBLEConnectionStateChange(res => {
      console.log(`[BLE] 设备连接状态: ${res.connected ? '已连接' : '已断开'}`)
      this.connected = res.connected
      if (!res.connected) {
        this.deviceId = null
      }
      this._emit('connectionChange', res)
    })
  }

  // 搜索附近 BLE 设备
  async startDiscovery(options = {}) {
    const {
      services = [],    // 服务 UUID 列表，过滤特定设备
      timeout = 10000,   // 搜索超时（ms）
    } = options

    // 开始搜索
    await wx.startBluetoothDevicesDiscovery({
      services,        // 可选，指定服务 UUID 以节省电量
      allowDuplicatesKey: false,  // 是否重复上报同一设备（耗电）
    })

    // 收集发现到的设备（注意：不要在回调里声明同名变量遮蔽此处）
    const foundDevices = []

    return new Promise((resolve, reject) => {
      // ⚠️ 回调参数名不要与外层变量同名，否则闭包引用错误
      wx.onBluetoothDeviceFound(res => {
        // res.devices: 本次新发现设备列表
        res.devices.forEach(d => {
          // 过滤信号强度太弱的设备（RSSI 通常 < -70，-80 即可见范围）
          if (d.RSSI > -80) {
            foundDevices.push({
              name: d.localName || d.name || '未知设备',
              deviceId: d.deviceId,
              RSSI: d.RSSI,
              advertisedData: d.advertisData ? this.ab2hex(d.advertisData) : '',
            })
          }
        })
      })

      setTimeout(() => {
        wx.stopBluetoothDevicesDiscovery()
        resolve(foundDevices)  // ✅ 正确引用外层变量
      }, timeout)
    })
  }

  // 连接设备
  async connect(deviceId) {
    await wx.createBLEConnection({ deviceId, timeout: 10000 })
    this.deviceId = deviceId
    this.connected = true

    // 获取设备服务列表
    const { services } = await wx.getBLEDeviceServices({ deviceId })
    console.log('[BLE] 服务列表:', services)

    // 找到数据通道服务（通常有读和通知特征）
    for (const service of services) {
      const { characteristics } = await wx.getBLEDeviceCharacteristics({
        deviceId,
        serviceId: service.uuid,
      })

      for (const char of characteristics) {
        // 特征属性：0x02=读, 0x04=写, 0x10=通知
        if (char.properties.notify || char.properties.indicate) {
          this.serviceId = service.uuid
          this.characteristicId = char.uuid
          break
        }
      }
      if (this.characteristicId) break
    }

    // 开启通知（监听数据）
    await wx.notifyBLECharacteristicValueChange({
      deviceId,
      serviceId: this.serviceId,
      characteristicId: this.characteristicId,
      state: true,
    })

    // 监听数据变化
    wx.onBLECharacteristicValueChange(res => {
      const data = this.ab2hex(res.value)
      this._emit('data', data)
    })

    return true
  }

  // 发送数据（写入）
  async write(data) {
    if (!this.connected) throw new Error('设备未连接')

    const buffer = this.stringToBuffer(data)
    await wx.writeBLECharacteristicValue({
      deviceId: this.deviceId,
      serviceId: this.serviceId,
      characteristicId: this.characteristicId,
      value: buffer,
    })
  }

  // 断开连接
  async disconnect() {
    if (this.deviceId) {
      await wx.closeBLEConnection({ deviceId: this.deviceId })
    }
    await wx.closeBluetoothAdapter()
    this.connected = false
    this.deviceId = null
  }

  // 工具函数
  ab2hex(buffer) {
    const hexArr = Array.prototype.map.call(
      new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')
    )
    return hexArr.join('')
  }

  stringToBuffer(str) {
    const buffer = new ArrayBuffer(str.length)
    const dataView = new Uint8Array(buffer)
    for (let i = 0; i < str.length; i++) {
      dataView[i] = str.charCodeAt(i)
    }
    return buffer
  }

  // 事件监听
  on(event, cb) {
    if (!this._listeners[event]) this._listeners[event] = []
    this._listeners[event].push(cb)
  }
  _emit(event, data) {
    (this._listeners[event] || []).forEach(cb => cb(data))
  }
}

export { BLEManager }
```

### 2.2 iBeacon 室内定位

```javascript
// utils/ibeacon.js

/**
 * iBeacon 室内定位
 * ⚠️ iBeacon 权限通过 scope.userLocation（地理位置）授权，不需要单独的 scope.beacon
 * app.json 正确写法：
 * "permission": {
 *   "scope.userLocation": { "desc": "获取位置用于室内导航" }
 * }
 */

// 搜索 iBeacon 设备
async function startBeaconDiscovery() {
  // 开始监听 iBeacon 设备
  wx.startBeaconDiscovery([])  // 传空数组表示监听所有 iBeacon

  wx.onBeaconUpdate(res => {
    // res.beacons: iBeacon 列表
    // UUID + major + minor + accuracy + rssi + proximity
    res.beacons.forEach(beacon => {
      if (beacon.rssi > -70) {  // 过滤距离太远的信标
        updateLocation(beacon)
      }
    })
  })
}

// 根据 iBeacon 三角定位估算用户位置
function updateLocation(beacon) {
  // 根据 beacon.major + beacon.minor 查数据库获取实际坐标
  // 再结合多个 beacon 的 RSSI 估算位置
  console.log(`[iBeacon] ${beacon.uuid}/${beacon.major}/${beacon.minor} RSSI=${beacon.rssi}`)
}
```

---

## 三、GPS 定位

### 3.1 获取当前位置

```javascript
// utils/location.js

/**
 * 获取用户位置
 * @param {number} type - gcj02（国测局坐标，地图使用）| wgs84（GPS原始坐标）
 */
async function getLocation(type = 'gcj02') {
  const setting = await wx.getSetting()

  if (!setting.authSetting['scope.userLocation']) {
    // ⚠️ 权限 key 是 'scope.userLocation'，不是 'scope.location'
    // 未授权，弹出授权框让用户主动授权
    const { authSetting } = await wx.openSetting()
    if (!authSetting['scope.userLocation']) {
      throw new Error('用户未授权位置权限')
    }
  }

  const res = await wx.getLocation({ type })

  return {
    latitude: res.latitude,   // 纬度
    longitude: res.longitude, // 经度
    speed: res.speed,         // 速度（m/s）
    accuracy: res.accuracy,    // 精度（m）
    altitude: res.altitude,    // 高度（m）
  }
}

/**
 * 计算两点之间的距离（米）
 * Haversine 公式
 */
function calcDistance(lat1, lon1, lat2, lon2) {
  const R = 6371000  // 地球半径（m）
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat / 2) ** 2
    + Math.cos(lat1 * Math.PI / 180)
    * Math.cos(lat2 * Math.PI / 180)
    * Math.sin(dLon / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}
```

### 3.2 地图展示

```xml
<!-- 展示地图并标记位置 -->
<map
  id="map"
  longitude="{{longitude}}"
  latitude="{{latitude}}"
  scale="16"
  show-location
  markers="{{markers}}"
  circles="{{circles}}"
  bindtap="onMapTap"
>
  <!-- 地图控件 -->
  <cover-view slot="callout">
    <cover-view marker-id="0">
      <cover-view class="callout">距您 {{distance}}m</cover-view>
    </cover-view>
  </cover-view>
</map>
```

```javascript
Page({
  data: {
    latitude: 39.908823,
    longitude: 116.397470,
    markers: [],
    circles: [],
  },

  async onLoad() {
    const { latitude, longitude } = await getLocation()

    // 在地图上标记当前位置
    this.setData({
      latitude,
      longitude,
      markers: [{
        id: 1,
        latitude,
        longitude,
        width: 30,
        height: 30,
        iconPath: '/assets/current-location.png',
        callout: { content: '我的位置', color: '#333', fontSize: 12, padding: 5, borderRadius: 10 },
      }],
      // 周围 500m 范围圈
      circles: [{
        latitude,
        longitude,
        color: '#07c16055',
        fillColor: '#07c16022',
        radius: 500,
        strokeWidth: 1,
      }],
    })
  },

  onMapTap(e) {
    // 点击地图获取经纬度
    const { latitude, longitude } = e.detail
    console.log('[地图点击]', latitude, longitude)
  },
})
```

---

## 四、NFC 能力

### 4.1 读取 NFC 标签

> ⚠️ 仅支持 Android 系统（基础库 1.9.90+）。iOS 不支持小程序 NFC。

```javascript
// utils/nfc.js

async function readNFC() {
  // 获取 NFC 适配器
  const nfc = wx.getNFCAdapter()

  if (!nfc) {
    throw new Error('当前设备不支持 NFC')
  }

  // 监听标签发现
  nfc.onDiscovered(res => {
    const { tech, id, sectors } = res

    // tech: NFC 技术类型（NFC_A / NFC_V / ISO_DEP / MIFARE / NFC_F / NFC_B）
    console.log('[NFC] 发现标签', tech, 'ID:', this.bytesToHex(id))

    // ISO_DEP（MIFAREClassic / DESFire）读取
    if (tech.includes('ISO_DEP')) {
      const data = this.readIsoDep(sectors)
      return data
    }
  })

  // 开始发现（监听 NFC 标签靠近）
  await nfc.startDiscovery({
    purpose: 'NFC',  // 'NFC' | 'HMS_STRENGTH'
  })
}

bytesToHex(bytes) {
  return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('')
}
```

### 4.2 NFC 常见应用场景

| 场景 | 数据格式 | 说明 |
|------|---------|------|
| 门禁卡 | MIFARE Classic | 读取扇区数据 |
| 设备配对 | NDEF | 读取设备标识 |
| 会员卡 | NDEF | 读取卡号 |

> ⚠️ NFC 功能需要**企业主体**小程序，个人主体**不支持** NFC 能力申请。

---

## 五、Wi-Fi 连接

### 5.1 连接已知 Wi-Fi

```javascript
// utils/wifi.js

async function connectWiFi(ssid, password = '') {
  // 初始化 Wi-Fi 模块
  await wx.startWifi()

  // 检查是否已连接到某个 Wi-Fi（返回 Promise，失败时 reject，需 catch）
  let currentWifi = null
  try {
    const info = await wx.getConnectedWifi()
    // info: { SSID, BSSID, secure, signalStrength, ... }
    currentWifi = info.SSID
    console.log('[Wi-Fi] 已连接到', info.SSID, '强度:', info.signalStrength)
  } catch (err) {
    // err.errMsg === 'getConnectedWifi:fail not connected' 表示未连接
    console.log('[Wi-Fi] 当前未连接到 Wi-Fi')
  }

  // 连接 Wi-Fi
  if (password) {
    // 需要密码的 Wi-Fi
    await wx.connectWifi({
      SSID: ssid,
      password,
      // ⚠️ Android 11+ 需要用户手动确认（无法静默连接）
    })
  } else {
    // 无密码 Wi-Fi
    await wx.connectWifi({ SSID: ssid })
  }

  // 获取 Wi-Fi 列表（需用户授权）
  const { wifiList } = await wx.getWifiList()
  console.log('[Wi-Fi] 周围网络:', wifiList.map(w => w.SSID))
}
```

### 5.2 智能设备配网（小程序 + Wi-Fi）

> 典型场景：智能摄像头/灯泡等设备，手机连接设备热点后，小程序将家中 Wi-Fi 信息传给设备

```javascript
// pages/device/add/add.js
Page({
  data: {
    step: 1,
    homeSSID: '',
    homePassword: '',
  },

  async onAddDevice() {
    // Step 1: 连接设备的热点（设备处于配网模式时会发出特定 SSID）
    await wx.showLoading({ title: '正在连接设备热点...' })
    try {
      await wx.connectWifi({ SSID: 'Device_AP_12345', password: '' })
      wx.hideLoading()
      wx.showToast({ title: '已连接设备', icon: 'success' })
      this.setData({ step: 2 })
    } catch (err) {
      wx.hideLoading()
      wx.showModal({ title: '连接失败', content: '请确保设备已进入配网模式', showCancel: false })
    }
  },

  // Step 2: 将家中 Wi-Fi 信息发给设备（通过 TCP/UDP）
  async sendHomeWiFi() {
    const { homeSSID, homePassword } = this.data

    // ⚠️ 通过 HTTP POST 将 Wi-Fi 信息发送到设备本地 IP
    const res = await wx.request({
      url: 'http://192.168.1.1/config',  // 设备热点的 IP
      method: 'POST',
      data: { ssid: homeSSID, password: homePassword },
      timeout: 5000,
    })

    if (res.statusCode === 200) {
      this.setData({ step: 3 })
      wx.showToast({ title: 'Wi-Fi 已发送，请等待设备联网...' })
    }
  },
})
```

---

## 六、Common Mistakes（硬件能力高频错误）

| 错误 | 正确做法 |
|------|---------|
| 蓝牙搜索无结果（iOS）| iOS 搜索蓝牙需要用户打开系统蓝牙，miniprogram 无法静默打开 |
| 蓝牙写入失败 | Android 可直接写入，iOS 需要先开启 notify 再写入（时序要求）|
| GPS 定位返回 -1 | 确认用户已授权 `scope.userLocation`，国内使用 gcj02 坐标系 |
| NFC 仅支持 Android | iOS 小程序不支持 NFC，提前在 iOS 端判断并给出提示 |
| NFC 功能个人主体无法申请 | NFC 需企业主体小程序，个人开发请使用 BLE 替代方案 |
| Wi-Fi 配网在 Android 11+ 失败 | Android 11+ 需要用户在系统设置中手动选择 Wi-Fi，API 无法绕过 |
| 连续调用 startDiscovery 导致蓝牙关闭 | 每次搜索后调用 stopBluetoothDevicesDiscovery 释放资源 |
| BLE 读写中文/二进制数据 | 使用 ArrayBuffer + bytesToHex 转换，不要直接传字符串 |
| 地图 marker 点击事件冲突 | 多个 marker 叠加时，给每个 marker 设置不同的 callout 或 markerId |

---

## 七、官方文档链接

- 蓝牙低功耗：https://developers.weixin.qq.com/miniprogram/dev/device/bluetooth/bluetooth.html
- 蓝牙设备连接：https://developers.weixin.qq.com/miniprogram/dev/api/device/bluetooth-ble/wx.createBLEConnection.html
- GPS 定位：https://developers.weixin.qq.com/miniprogram/dev/api/location/wx.getLocation.html
- NFC：https://developers.weixin.qq.com/miniprogram/dev/device/nfc.html
- Wi-Fi：https://developers.weixin.qq.com/miniprogram/dev/device/wifi.html
- 扫码：https://developers.weixin.qq.com/miniprogram/dev/api/device/scan/wx.scanCode.html
- 地图组件：https://developers.weixin.qq.com/miniprogram/component/map.html
