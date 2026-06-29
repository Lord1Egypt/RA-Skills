---
name: Smart Home Orchestrator
slug: smart-home-orchestrator
description: 统一编排智能家居设备，支持米家/HomeKit/Alexa/Google Home等多品牌协议，实现灯光、空调、窗帘、安防的跨平台场景自动化。一句话创建起床模式、离家模式、观影模式，让AI管家替你打理全屋智能。
version: 1.0.0
author: ai-gaoqian
tags:
  - smart-home
  - iot
  - automation
  - home-automation
  - scene-orchestration
metadata:
  openclaw:
    requires: []
    pricing:
      amount: 0.50
      currency: CNY
      interval: per-use
---

# Smart Home Orchestrator

AI驱动的跨品牌智能家居统一编排技能。解决多品牌设备无法联动、场景配置繁琐、自动化规则难维护的痛点。

## 使用场景

- 创建/修改智能家居场景（起床模式、离家模式、观影模式、晚安模式）
- 查询和控制单个设备状态（灯光开关/亮度、空调温度/模式、窗帘开合、传感器读数）
- 基于条件的自动化规则（如"当PM2.5>75且窗户打开时，关闭窗户并开启空气净化器"）
- 批量设备巡检与健康诊断

## 支持协议

| 协议 | 覆盖品牌 |
|------|----------|
| Mi Home (米家) | 小米、Aqara、Yeelight、智米 |
| HomeKit | Apple 生态配件 |
| Alexa Smart Home | Amazon Echo 生态 |
| Google Home | Google Nest 生态 |
| MQTT / Zigbee2MQTT | 通用开源协议 |

## 工作流程

1. **设备发现**：扫描局域网内可连接的智能家居网关（米家网关、Homebridge、Home Assistant 等）
2. **场景编排**：用户用自然语言描述场景需求，Skill 自动拆解为设备指令序列
3. **规则引擎**：支持 if-this-then-that 条件触发，支持时间/传感器/设备状态多条件组合
4. **模拟执行**：高危操作（如关闭所有门锁）先模拟预览，经确认后执行

## 配置

在 openclaw.yaml 中配置设备网关地址和认证凭据：

```yaml
skills:
  smart-home-orchestrator:
    gateways:
      - type: homeassistant
        url: http://192.168.1.100:8123
        token: ${HA_LONG_LIVED_TOKEN}
      - type: mihome
        username: ${MI_USERNAME}
        password: ${MI_PASSWORD}
    default_region: cn
```

## 示例指令

- "设置离家模式：关闭所有灯和空调，启动安防摄像头，关闭窗帘"
- "客厅温度超过28度自动开空调制冷26度"
- "列出所有在线的传感器"
- "睡前场景：主灯调暖光20%亮度，播放白噪音，关闭窗帘"
