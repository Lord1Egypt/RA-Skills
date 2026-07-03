# Device Knowledge Base (2026 Refresh)

> 以 `智能家居设备型号清单_2026.md` 为主，保留可用于规划/选型的高频型号与落地提示。

## 1. Gateways / Hubs

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Xiaomi | 米家多模网关2 | Zigbee + BLE Mesh + Wi-Fi | 199 | ✅ | ✅ | ❌ | 小户型首选，性价比高 |
| Xiaomi | 米家中枢网关 | Zigbee + BLE Mesh + Wi-Fi | 399 | ✅ | ✅ | ❌ | 适合大户型/复式/别墅 |
| Aqara | M3 | Zigbee 3.0 + Thread + Matter | 499 | ✅ | ✅ | ✅ | 旗舰级，带警笛和 Thread 边界路由 |
| Aqara | M100 | Zigbee 3.0 | 299 | ✅ | ✅ | ✅ | 入门级 HomeKit 网关 |
| Tuya | 涂鸦 Zigbee 网关 | Zigbee 3.0 | 99-199 | ✅ | ✅ | ❌ | 涂鸦生态入门 |
| Huawei | 华为智慧中枢 | PLC + Wi-Fi 6+ | 999+ | ❌ | ❌ | ❌ | 华为生态核心 |

### Gateway Notes
- 优先选支持本地联动、Thread 或 Matter 的网关。
- 想要跨平台和未来兼容性，优先 Aqara M3。
- Xiaomi 网关适合纯米家生态。

---

## 2. Lighting

### Ceiling / Main Lights

| Brand | Model | Feature | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|---------|-------------|-----|------|---------|-------|
| Yeelight | 灵犀智能吸顶灯 Pro | 双面出光，Ra95 | 599-899 | ✅ | ✅ | ✅ | 客厅主灯优先 |
| Yeelight | Pro M20 Ceiling Light | 局域网本地控制 | 799-1099 | ✅ | ✅ | ✅ | 方/圆可选 |
| Yeelight | 皓石 LED 吸顶灯 Pro | 大尺寸客厅灯 | 799 | ✅ | ✅ | ✅ | 免费安装卖点 |
| Xiaomi | 米家吸顶灯套系 | 全光谱灯珠 | 199+ | ✅ | ✅ | ❌ | 入门款 |
| Legrand/领普 | LX1 人体存在吸顶灯 | 雷达感应 | 299 | ✅ | ❌ | ❌ | 人来亮灯人走灭 |
| Aqara | 繁星系列无主灯 | Thread/Matter | 399+ | ✅ | ✅ | ✅ | 本地响应更好 |

### Bulbs / Ambient Lights

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Yeelight | Smart Bulb 1S | WiFi | 79-99 | ✅ | ✅ | ✅ | 性价比高，色温可调 |
| Philips | Hue White | Zigbee | 149-199 | ✅ | ❌ | ✅ | 高端，需 Hue Bridge |
| Aqara | Smart Bulb T1 | Zigbee | 69-89 | ✅ | ✅ | ✅ | 需网关 |
| Xiaomi | Mesh Bulb | BLE Mesh | 49-69 | ✅ | ✅ | ❌ | 低价，需网关 |
| Xiaomi | 烛光灯泡 | WiFi/BLE | 79 | ✅ | ✅ | ❌ | 氛围灯 |
| Philips | Hue 彩光版 | Zigbee | 299/个 | ✅ | ❌ | ✅ | 彩灯推荐 |

### Switches / Modules

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Xiaomi | 米家智能开关（零火版） | Zigbee/BLE | 69+ | ✅ | ✅ | ❌ | 新房优先，稳定不闪灯 |
| Aqara | 墙壁开关（中性版） | Zigbee | 89-139 | ✅ | ✅ | ✅ | 本地响应快 |
| Aqara | 繁星妙控开关 V1 | Zigbee | 299 | ✅ | ✅ | ✅ | 旗舰触控开关 |
| 领普 | T1 超薄智能开关 | BLE Mesh 2.0 | 29+ | ✅ | ✅ | ❌ | 6.9mm 超薄 |
| 领普 | E3S 超薄四键开关 | BLE Mesh 2.0 | 89 | ✅ | ✅ | ❌ | 多键控制 |
| 领普 | E3S 单火版 | BLE Mesh 2.0 | 89 | ✅ | ✅ | ❌ | 老房无零线专用 |
| 领普 | E3 Pro 玻璃面板开关 | BLE Mesh 2.0 | 119 | ✅ | ✅ | ❌ | 质感更好 |
| 领普 | E2 Pro 带屏开关 | BLE Mesh 2.0 | 179 | ✅ | ✅ | ❌ | 可自定义名称 |
| Sonoff | MINI Extreme (MINIR4) | WiFi | 59 | ✅ | ❌ | ❌ | HA 友好，可刷 ESPHome |
| Sonoff | BASICR4 | WiFi | 49 | ✅ | ❌ | ❌ | 10A/16A 通断器 |
| Sonoff | ZBMINI-L2 | Zigbee | 49-69 | ✅ | ❌ | ❌ | 玄关/后装模块 |

### Light Strips

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Yeelight | Light Strip 1S | WiFi | 129-179 | ✅ | ✅ | ✅ | RGB + white |
| Aqara | LED Strip T1 | Zigbee | 129-169 | ✅ | ✅ | ✅ | 需网关 |
| Govee | RGBIC Strip | WiFi/BLE | 79-149 | ✅ | ❌ | ❌ | 可寻址 RGB |

### Lighting Notes
- 新房装修优先零火版开关，稳定性最好。
- 老房无零线，优先领普 E3S 单火版或后装模块。
- 主灯选吸顶灯，氛围灯选灯泡/灯带。

---

## 3. Curtains

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Xiaomi | 米家智能窗帘电机（Zigbee版） | Zigbee | 399 | ✅ | ✅ | ❌ | 断网可用，本地联动 |
| Xiaomi | 米家窗帘伴侣（电池款） | BLE/WiFi | 299 | ✅ | ✅ | ❌ | 租房友好 |
| Aqara | Curtain Controller E1 | Zigbee | 399-499 | ✅ | ✅ | ✅ | 兼容性好 |
| Aqara | Roller Shade Driver E1 | Zigbee | 299-399 | ✅ | ✅ | ✅ | 卷帘专用 |
| Aqara | 智能隐形窗帘电机 C200 | Thread/Matter | 799 | ✅ | ✅ | ✅ | 隐形安装 |
| Dooya | M7 / DT82TN | Zigbee | 349-599 | ✅ | ✅ | ❌ | 专业安装更稳 |
| Tuya | 涂鸦三代智能窗帘电机 | WiFi + Zigbee | 199-399 | ✅ | ✅ | ❌ | 双模方案 |
| 领普 | CE1 隐藏式窗帘电机 | BLE Mesh | 79 | ✅ | ✅ | ❌ | 低价卷王 |

### Curtain Notes
- 先确认轨道类型：U 轨、I 轨、罗马杆。
- 优先看承重、静音和断电手动能力。

---

## 4. Smart Locks

| Brand | Model | Unlock | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|--------|-------------|-----|------|---------|-------|
| Xiaomi | E10 | 指纹 + 密码 + NFC | 619 | ✅ | ✅ | ❌ | 入门款 |
| Xiaomi | E30 | HomeKit 认证 | 999 | ✅ | ✅ | ✅ | 千元级 |
| Xiaomi | M30 Pro | 3D 人脸 + 指纹 + 密码 + NFC + 猫眼 | 2499 | ✅ | ✅ | ❌ | 功能全面 |
| Xiaomi | M40 | AI 双摄全景猫眼 + 屏幕 | 3299 | ✅ | ✅ | ❌ | 高配 |
| Xiaomi | M40 Pro | 3D 人脸 + 掌静脉 + AI 双摄 | 3229 | ✅ | ✅ | ❌ | 旗舰 |
| Xiaomi | 智能门锁2 人脸识别版 | 3D 结构光 + 160° 摄像头 | 1799 | ✅ | ✅ | ❌ | 人脸识别 |
| Aqara | U100 / U300 | 指纹 + NFC + Home Key | 1299+ | ✅ | ✅ | ✅ | Apple 家庭钥匙 |
| Aqara | D100 | 指纹 + 密码 + NFC | 899-1099 | ✅ | ✅ | ✅ | 性价比 Aqara |
| Haier | CFA-X70-CA | 多方式解锁 | 2599 | ❌ | ❌ | ❌ | 海尔生态 |
| Schlage | Encode Plus | WiFi + Home Key | 1999-2499 | ✅ | ❌ | ✅ | Apple 用户优先 |

### Lock Notes
- 门厚、背距、锁体孔位要先量。
- 必须保留机械钥匙/应急供电方案。

---

## 5. Sensors

### Presence / Motion

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Xiaomi | 人体存在传感器 | BLE | 119 | ✅ | ✅ | ❌ | 静止存在检测 |
| Aqara | 高精度人体传感器 / FP2 | WiFi | 299-399 | ✅ | ✅ | ✅ | mmWave，分区检测 |
| Aqara | Motion Sensor P1 | Zigbee | 79-99 | ✅ | ✅ | ✅ | PIR，灵敏度可调 |
| Xiaomi | Motion Sensor 2 | BLE | 49-69 | ✅ | ✅ | ❌ | 低价 |
| Tuya | Tuya HX-MP01 | Zigbee | 59 | ✅ | ✅ | ❌ | 120° 广角 |
| 领普 | ES5 顶装传感器 | Zigbee/BLE | 149 | ✅ | ✅ | ❌ | 雷达 + 红外融合 |

### Environment

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Aqara | Temp & Humidity Sensor T1 | Zigbee | 59-79 | ✅ | ✅ | ✅ | 准确，常用 |
| Xiaomi | Temp & Humidity 2 | BLE | 29-49 | ✅ | ✅ | ❌ | 入门款 |
| Xiaomi | 米家温湿度传感器 | BLE Mesh | 39+ | ✅ | ✅ | ❌ | 2026 常见款 |
| Xiaomi | 小米空气检测仪 | BLE/WiFi | 价格不一 | ✅ | ✅ | ❌ | PM2.5 + TVOC |
| Aqara | TVOC 空气传感器 | Zigbee | 价格不一 | ✅ | ✅ | ✅ | HomeKit 原生 |
| 领普 | K2S 温湿度传感无线开关 | BLE Mesh | 20 | ✅ | ✅ | ❌ | 二合一 |
| Sonoff | TH Origin | WiFi | 价格不一 | ✅ | ❌ | ❌ | 带开关功能 |
| Aqara | 光照传感器 T1 | Zigbee | 179 | ✅ | ✅ | ✅ | 自动调光 |

### Security

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Aqara | Door Sensor T1 | Zigbee | 49-69 | ✅ | ✅ | ✅ | 门窗监测 |
| Xiaomi | Door Sensor 2 | BLE | 29-39 | ✅ | ✅ | ❌ | 低价 |
| Aqara | Door/Window Sensor Thread 版 | Thread | 价格不一 | ✅ | ✅ | ✅ | 未来兼容性好 |
| Xiaomi | 烟雾报警器 | BLE/Zigbee | 129 | ✅ | ✅ | ❌ | 安防场景必备 |
| Xiaomi | 燃气卫士 | BLE/Zigbee | 119 | ✅ | ✅ | ❌ | 厨房安全 |
| Xiaomi | 水浸卫士 | BLE/Zigbee | 79 | ✅ | ✅ | ❌ | 漏水联动 |
| Aqara | 水浸传感器 | Zigbee | 99 | ✅ | ✅ | ✅ | 可靠 |
| 领普 | 水浸传感器 | Zigbee/BLE | 49 | ✅ | ✅ | ❌ | 低价备选 |

### Sensor Notes
- 人体传感器建议 2-2.5m 高度，放角落更容易覆盖。
- FP2 适合静态存在检测，普通 PIR 只适合“动了才触发”。
- 温湿度传感器远离空调出风口和阳光。

---

## 6. Cameras & Security

| Brand | Model | Protocol | Price (CNY) | HA | 米家 | HomeKit | Notes |
|-------|-------|----------|-------------|-----|------|---------|-------|
| Xiaomi | 摄像头 云台版 2K | WiFi | 199 | ✅ | ✅ | ❌ | 入门首选 |
| Xiaomi | 摄像头 云台版 Pro | WiFi | 299 | ✅ | ✅ | ❌ | 2.5K + AI 人形侦测 |
| Aqara | G5 Pro | WiFi | 599 | ✅ | ✅ | ✅ | 本地处理，夜视强 |
| Aqara | Camera E1 | WiFi | 199-299 | ✅ | ✅ | ✅ | HomeKit Secure Video |
| Arlo | Essential Indoor | WiFi | 399-499 | ✅ | ❌ | ✅ | 隐私遮罩 |
| Xiaomi | Smart Doorbell 3 | WiFi | 249-349 | ✅ | ✅ | ❌ | 双向语音 |
| Aqara | G4 Doorbell | WiFi | 499-699 | ✅ | ✅ | ✅ | HomeKit Secure Video |
| Arlo | Essential Doorbell | WiFi | 599-799 | ✅ | ❌ | ✅ | 无线门铃 |
| Tuya | 涂鸦太阳能摄像头 | WiFi | 299 | ✅ | ✅ | ❌ | 免插电，续航长 |

### Camera Notes
- 室内摄像头优先选带物理遮挡的型号。
- 存储方案优先本地 SD / NAS，其次云端。

---

## 7. Robot Vacuums

| Brand | Model | Notes | Price (CNY) | HA | 米家 | HomeKit |
|-------|-------|-------|-------------|-----|------|---------|
| Xiaomi | 扫拖机器人 1S | 基础款 | 1299 | ✅ | ✅ | ❌ |
| Xiaomi | 扫拖机器人 M30 | 自清洁基站 | 1999 | ✅ | ✅ | ❌ |
| Xiaomi | 扫拖机器人 Ultra | 旗舰款 | 2999 | ✅ | ✅ | ❌ |
| Roborock | 石头 G/P 系列 | 生态兼容较好 | 3000-5000 | ✅ | ✅ | ❌ |
| Narwal | 云鲸 J 系列 | 拖布清洁强 | 3000-4500 | ✅ | ❌ | ❌ |
| iRobot | Roomba 系列 | HA 原生支持 | 2500+ | ✅ | ❌ | ❌ |
| Dreame | 追觅 X 系列 | HA 可接入 | 3000+ | ✅ | ❌ | ❌ |

---

## 8. Air Conditioning & Environment

| Brand | Model | Notes | HA | 米家 | HomeKit |
|-------|-------|-------|-----|------|---------|
| Xiaomi | 米家空调伴侣 | 传统空调转接，语音 + 远程控制 | ✅ | ✅ | ❌ |
| Xiaomi | 米家空调 | 小爱同学直连 | ✅ | ✅ | ❌ |
| Sensibo | Sky | 通用空调控制器 | ✅ | ❌ | ✅ |
| Haier | 卡萨帝 CAP7226G10(81)VU1 | AI 人感送风 | ❌ | ❌ | ❌ |
| Haier | 安睡新风柜式 KFR-72LW/B700-1 | 新风 + 恒温 | ❌ | ❌ | ❌ |
| Huawei | 华为全屋智能空调联动 | PLC 控制 | ❌ | ❌ | ❌ |

---

## 9. Control Panels / Voice Assistants

| Brand | Model | Notes | Price (CNY) |
|-------|-------|-------|-------------|
| Xiaomi | 小爱音箱 Pro | 主力语音 + 红外遥控 | 299 |
| Xiaomi | 小爱触屏音箱 | 床头/门口中控 | 399 |
| Xiaomi | 小爱音箱 Play | 入门级 | 99 |
| Aqara | 集悦妙控屏 S1 Plus | 墙面中控屏 | 999 |
| Tuya | TuyaGo 智慧中控屏 Mini | 可定制界面 | 299 |

---

## 10. Tuya Ecosystem Snapshot

| Category | Typical Model / Solution | Notes |
|----------|--------------------------|-------|
| Smart plug | 涂鸦 WiFi 智能插座 10A/16A | 电量统计，29-59 |
| Smart switch | 涂鸦 Zigbee 智能开关 | 三开/双开/单开 |
| Motion sensor | Tuya HX-MP01 | 12m 探测 |
| Smoke alarm | 涂鸦烟感报警器 | Zigbee |
| Curtain motor | 涂鸦三代智能窗帘电机 | WiFi+Zigbee 双模 |
| Control panel | TuyaGo 智慧中控屏 Mini | 墙面安装 |
| Camera | 涂鸦太阳能摄像头 | 免插电，续航长 |

---

## 11. Home Assistant Best Combos

| Use Case | Recommended Combination | Integration |
|----------|-------------------------|-------------|
| Gateway + sensors | Aqara M3 + Aqara sensors | Zigbee / Thread / Matter |
| Xiaomi family | Xiaomi devices + hass-xiaomi-miot | Local / cloud |
| Tuya devices | Tuya Zigbee devices | Tuya integration |
| Smart switches | Sonoff MINIR4 | WiFi / ESPHome |
| Smart plugs | Sonoff S31 Lite zb | ZHA |
| Curtains | 米家 Zigbee 窗帘电机 | Low latency |
| Air conditioning | 米家空调伴侣 | Local control |

---

## 12. Budget Quick Reference (120-150 sqm, 3BR)

| Plan | Budget | Core Stack |
|------|--------|------------|
| Economy | 1200-2200 | 米家多模网关2 + 领普 T1 开关 x6 + 米家门锁 E10 + 窗帘伴侣 + 传感器套装 |
| Comfort | 8000-12000 | Aqara M3 + Aqara 开关面板 + 小米 M30 门锁 + Yeelight 吸顶灯 + 米家空调伴侣 |
| High-end | 25000-45000 | Aqara 全系 + Yeelight Pro + 全屋传感器 + 摄像头/门铃 |
| Geek | 60000+ | Home Assistant 服务器 + Aqara 全系 + 米家家电 + Tuya 补位 + 多中控屏 |

---

## 13. Compatibility Quick Reference

### Works with All 3 Platforms
- Aqara M3 / M100 ecosystem
- Yeelight WiFi bulbs and strips
- Aqara FP2 presence sensor

### HA + 米家 Only
- Xiaomi / Mijia BLE devices via gateway
- Xiaomi cameras
- Most budget Xiaomi sensors

### HA + HomeKit Only
- Philips Hue (via Hue Bridge)
- Arlo cameras
- Some Matter devices

### Platform Exclusive / Mostly Exclusive
- HomeKit-only: Schlage Encode Plus (Apple Home Key)
- 米家-only: XiaoAi speaker ecosystem
- HA-only: Z-Wave devices, Zigbee2MQTT devices

---

## 14. Selection Rules

- 新房装修优先：网关 + Zigbee/Thread 设备 + 零火开关 + 门窗/人体传感器。
- 老房改造优先：后装模块、免布线窗帘、电池传感器。
- Apple 用户优先：Aqara M3 / M100 + HomeKit 原生设备。
- 纯米家优先：米家多模网关2 + 米家开关/窗帘/传感器。
- 想要长期兼容性：优先 Thread / Matter / 本地联动。
