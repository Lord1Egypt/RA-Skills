# Vela Docs Map

## Official doc entry points

- 项目结构: https://iot.mi.com/vela/quickapp/zh/guide/start/project-overview.html
- 框架总览: https://iot.mi.com/vela/quickapp/zh/guide/framework/
- 组件总览: https://iot.mi.com/vela/quickapp/zh/components/
- 接口总览: https://iot.mi.com/vela/quickapp/zh/features/
- 传感器接口: https://iot.mi.com/vela/quickapp/zh/features/system/sensor.html
- AIoT IDE / 快速开始: https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html

## What each section is good for

### 项目结构
Use when you need to confirm required files/folders such as:
- `manifest.json`
- `app.ux`
- page `.ux`
- `common/`

### 框架总览
Use when reasoning about:
- routing
- data binding
- page lifecycle
- template/script/style structure

### 组件总览
Use when choosing UI building blocks such as:
- `div`
- `text`
- `image`
- `list`
- `input`
- `textarea`
- other native UI components

### 接口总览
Use when the app needs capabilities like:
- storage
- vibrator
- network
- battery
- brightness
- sensor

### 传感器接口
Use when the user asks about motion / pressure / sensor-triggered app ideas.
Confirmed from current work:
- Xiaomi Band 10 supports accelerometer and pressure APIs in Vela sensor docs
- Heart-rate reading is not exposed through the public Vela sensor API page we checked

## Practical search strategy

When stuck:
1. Start from the nearest official overview page above
2. Open the specific component/feature page
3. Keep project fixes minimal and rebuild immediately

## Notes from fetched docs

- Vela apps are built from `manifest.json` + page `.ux` files
- A `.ux` page typically contains `template`, `style`, and `script`
- Framework provides native components and feature APIs
- `manifest.json` declares app info, feature usage, and page routing
