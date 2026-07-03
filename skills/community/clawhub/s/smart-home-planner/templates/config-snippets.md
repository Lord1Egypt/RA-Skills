# Platform Config Snippets

## Home Assistant

### Home Mode (回家模式)
```yaml
automation:
  - alias: "Home Mode"
    trigger:
      - platform: state
        entity_id: device_tracker.phone
        to: "home"
    condition: []
    action:
      - service: light.turn_on
        target:
          area_id: hallway
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room
        data:
          temperature: 24
```

### Away Mode (离家模式)
```yaml
automation:
  - alias: "Away Mode"
    trigger:
      - platform: state
        entity_id: group.all_devices
        to: "not_home"
        for: "00:05:00"
    action:
      - service: light.turn_off
        target:
          area_id: all
      - service: climate.turn_off
        target:
          area_id: all
      - service: alarm_control_panel.alarm_arm_away
        target:
          entity_id: alarm_control_panel.home
```

### Sleep Mode (睡眠模式)
```yaml
automation:
  - alias: "Sleep Mode"
    trigger:
      - platform: event
        event_type: call_service
        event_data:
          domain: scene
          service: turn_on
          service_data:
            entity_id: scene.sleep
    action:
      - service: light.turn_off
        target:
          area_id:
            - living_room
            - kitchen
      - service: light.turn_on
        target:
          entity_id: light.bedroom
        data:
          brightness_pct: 10
          color_temp_kelvin: 2700
      - service: cover.close_cover
        target:
          area_id: all
      - service: lock.lock
        target:
          entity_id: lock.front_door
```

### Security Mode (安防模式)
```yaml
automation:
  - alias: "Security Alert"
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.door_sensor
          - binary_sensor.window_sensor
        to: "on"
    condition:
      - condition: state
        entity_id: alarm_control_panel.home
        state: "armed_away"
    action:
      - service: notify.mobile_app
        data:
          title: "安全警报"
          message: "{{ trigger.to_state.attributes.friendly_name }} 被打开"
      - service: camera.record
        target:
          entity_id: camera.indoor
        data:
          duration: 30
```

---

## 米家

### Home Mode (回家模式)
```
米家 App → 智能 → 添加场景
  触发条件：当 [手机] 到达 [家]
  执行动作：
    → 打开 [玄关灯]
    → 打开 [客厅窗帘]
    → 设置 [空调] 为 24°C
```

### Away Mode (离家模式)
```
米家 App → 智能 → 添加场景
  触发条件：当所有家庭成员离开 [家]
  执行动作：
    → 关闭所有灯
    → 关闭所有空调
    → 关闭所有窗帘
    → 启动 [扫地机器人]
```

### Sleep Mode (睡眠模式)
```
米家 App → 智能 → 添加场景
  触发条件：手动触发 / 语音"小爱同学，晚安"
  执行动作：
    → 关闭 [客厅灯]
    → 设置 [卧室灯] 亮度 10%
    → 关闭所有窗帘
    → 设置 [空调] 睡眠模式 26°C
    → 上锁 [门锁]
```

### Security Mode (安防模式)
```
米家 App → 智能 → 添加场景
  触发条件：当 [门窗传感器] 检测到打开
  条件：[手机] 不在家
  执行动作：
    → 发送手机通知
    → 开启 [摄像头] 录像
    → [警报器] 响铃
```

---

## Apple HomeKit

### Home Mode (回家模式)
```
家庭 App → 自动化 → 创建个人自动化
  触发：我到家时
  配件：
    → 玄关灯：打开
    → 客厅窗帘：打开
    → 恒温器：设为 24°C
```

### Away Mode (离家模式)
```
家庭 App → 自动化 → 创建个人自动化
  触发：最后一个人离开时
  配件：
    → 所有灯：关闭
    → 所有窗帘：关闭
    → 恒温器：关闭
```

### Sleep Mode (睡眠模式)
```
家庭 App → 场景 → 创建场景
  名称：晚安
  配件：
    → 客厅灯：关闭
    → 卧室灯：亮度 10%，暖色
    → 所有窗帘：关闭
    → 门锁：上锁
  然后创建自动化 → 触发：每天 23:00
```

### HomeKit Secure Video
```
家庭 App → 摄像头设置 → 录制选项
  → 检测到运动时录制
  → 有人在家时关闭
  → 存储到 iCloud（加密）
```
