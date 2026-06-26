---
name: travel-app-toolkit
description: "[user] 旅行目的地必备 App 一键清单生成器，根据目的地国家/城市、旅行风格和偏好，生成分类App推荐清单，附带 iOS App Store 和 Android Google Play 双平台下载直达链接，输出为可直接在浏览器打开的交互式 HTML 页面（支持平台切换、分类过滤、搜索）。当用户提到\"旅行App推荐\"\"出国必备App\"\"当地常用App\"\"下载什么App\"\"travel apps\"\"必备应用\"\"打车App\"\"翻译App\"\"地图App\"\"出行工具包\"\"旅行前准备App\"时使用。"
---

# Travel App Toolkit

根据旅行目的地自动生成分类 App 推荐清单，输出可直接在浏览器打开的交互式 HTML 页面。

## 工作流程

### Step 1: 收集用户信息

如未明确提供，通过 AskUserQuestion 询问：

1. **目的地**：国家或城市（必填）
2. **旅行风格**：自助游 / 亲子 / 商务 / 蜜月（可选，默认自助游）
3. **手机平台**：iOS / Android / 两个都要（可选，默认两个都要）
4. **支付偏好**：是否需要当地支付 App（可选，默认是）

### Step 2: 读取 App 数据库

读取 `app-database.json`（与本文件同目录），该文件包含按国家/地区分组的 App 数据。

数据库路径：在本 SKILL.md 同级目录下的 `app-database.json`。

### Step 3: 匹配与筛选

1. 根据目的地匹配对应国家/地区的 App 列表
2. 加入 `global` 分组下的通用必备 App
3. 如果目的地不在数据库中，使用 `global` 通用推荐 + Agent 自身知识补充当地特色 App
4. 根据旅行风格调整推荐优先级（例如亲子游增加亲子类 App，商务增加通讯类 App）

### Step 4: 生成 HTML 页面

参考 `template.html` 生成 `.html` 文件，核心功能：

- **平台切换 Tab**：iOS / Android 一键切换下载链接
- **分类筛选**：按交通、地图、支付、餐饮、翻译、通讯等分类过滤
- **搜索框**：快速搜索 App 名称
- **优先级标签**：必装 (must-have) / 推荐 (recommended) / 可选 (optional)
- **下载直达**：点击即跳转对应平台商店页面
- **小贴士**：每个 App 附带实用使用建议

### Step 5: 输出

将生成的 `.html` 文件保存到用户工作目录并分享链接。用户可直接在浏览器中打开使用。

## App 分类体系

| 分类 ID | 中文名 | 图标 | 典型 App |
|---------|--------|------|----------|
| transport | 交通出行 | 🚕 | Grab, Uber, 滴滴 |
| maps | 地图导航 | 🗺️ | Google Maps, 高德地图 |
| food | 餐饮外卖 | 🍜 | UberEats, 大众点评 |
| payment | 支付工具 | 💳 | PayPay, Apple Pay |
| translation | 翻译语言 | 🗣️ | Google 翻译, DeepL |
| communication | 通讯社交 | 💬 | WhatsApp, LINE |
| travel | 旅行预订 | ✈️ | Booking, Airbnb |
| essentials | 其他必备 | 🔧 | VPN, eSIM, 天气 |

## 优先级定义

- **must-have**（必装）：到当地几乎无法离开的 App，如日本的 PayPay、泰国的 Grab
- **recommended**（推荐）：显著提升旅行体验的 App
- **optional**（可选）：有则更好，锦上添花

## 设计要求

- 纯 HTML/CSS/JS 单文件，无外部依赖，浏览器直接打开
- 旅行主题配色（蓝/绿/白）
- 卡片式布局，移动端友好
- 每个 App 卡片包含：图标 emoji、名称、一句话描述、优先级标签、下载按钮、使用小贴士
- 顶部显示目的地名称和 App 总数统计
- 底部附"温馨提示"：建议出发前在 WiFi 下提前下载

## 注意事项

- App Store / Play 商店链接使用标准格式：
  - iOS: `https://apps.apple.com/app/{name}/id{id}`
  - Android: `https://play.google.com/store/apps/details?id={package}`
- 如某 App 仅支持单平台，在另一平台显示"该平台暂不可用"
- 部分国家的 App 可能需要当地手机号注册，在 tips 中说明
- 对于中国大陆用户出境，可提醒提前下载 VPN 类工具
