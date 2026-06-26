---
name: wechat-miniprogram-toolkit
version: 1.6.0
description: 微信小程序全栈开发 skill，支持项目初始化、云开发（数据库/存储/云函数/聚合查询/事务）、用户登录鉴权、微信支付（JSAPI/统一下单/支付通知/退款）、直播/实时音视频（TRTC）、数据分析/埋点、分享海报/朋友圈分享、TypeScript 泛型封装、云托管（容器化后端）、客服消息、订阅消息、客服自动回复、内容安全（文本/图片/音视频审核）、小程序互跳（APP↔小程序/URL Scheme/扫码）、硬件能力（蓝牙/GPS/NFC/Wi-Fi/扫码）、Skyline 高性能渲染、WXS 脚本、性能优化、CI/CD 流水线、代码分包（每个包小于 2MB）。
author: OpenClaw Agent
license: MIT
tags: [微信, 小程序, 云开发, 微信支付, 直播, TRTC, 数据分析, 埋点, 分享, TypeScript, 云托管, 容器, 客服, 订阅消息, 内容安全, 审核, 互跳, APP跳转, URL Scheme, 蓝牙, GPS, NFC, Wi-Fi, 扫码, 分包, Skyline, Worklet]
---

# 微信小程序全栈开发 Skill

> 整合腾讯云官方认证最佳实践 + Skyline 官方 Worklet 动画规范 + 工程化 CI/CD 配置，一站式覆盖从项目初始化到生产发布的全链路。

---

## 📋 元信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.6.0 |
| 更新日期 | 2026-04-12 |
| 适用基础库 | ≥ 2.2.3（云开发）/ ≥ 3.0（Skyline）|
| 许可证 | MIT |
| 官方文档 | https://developers.weixin.qq.com/miniprogram/dev/framework/ |

---

## 🚀 快速上手

**Step 1：安装**
```
skillhub install wechat-miniprogram-toolkit
```
> SkillHub CLI 未安装时，告诉 AI「安装 SkillHub」即可自动完成。

**Step 2：初始化项目（AI 帮你生成）**
```
告诉 AI："帮我创建一个微信小程序项目，包含云开发、分包、登录功能"
AI 将参照 references/project-init.md 自动生成完整项目结构
```

**Step 3：运行分包分析（上线前必做）**
```
告诉 AI："分析我的小程序分包，给我最优分包方案"
AI 运行 scripts/analyze_subpackages.py，输出 app.json 配置
```

**Step 4：配置 CI/CD（可选）**
```
告诉 AI："配置 GitHub Actions 自动发布"
AI 参照 references/ci-cd.md 生成完整流水线
```

---

## 📦 前置依赖

> 本 skill 大部分能力开箱即用，无需额外安装。以下为可选场景所需的额外工具，按需安装：

### Skill 工具依赖

| 工具 | 用途 | 状态 | 说明 |
|------|------|------|------|
| Python ≥ 3.7 | 运行 `analyze_subpackages.py` 分包分析 | ✅ 通常已内置 | AI 内置，无需手动安装 |
| Node.js ≥ 16 | CI/CD GitHub Actions | ✅ 通常已内置 | GitHub Actions 环境自带，无需本地安装 |

### 项目可选 npm 包

> 以下是**小程序项目**开发时可能用到的 npm 依赖（通过 `npm install` 安装到项目目录）：

| 依赖 | 用途 | 安装命令 |
|------|------|----------|
| miniprogram-ci | 自动构建/上传/提交审核 | `npm install miniprogram-ci -D` |
| ESLint | 代码规范检查 | `npm install eslint -D` |
| eslint-plugin-wxmp | 微信小程序专用 ESLint 规则 | `npm install eslint-plugin-wxmp -D` |

### 其他可选依赖

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| matplotlib | 公式渲染（LaTeX → PNG） | `pip install matplotlib` |

> **提示**：如果环境中没有安装这些工具，告诉 AI「帮我安装 miniprogram-ci」即可自动处理。

---

## 🛠 开发环境准备

> 上线前需要在微信公众平台和本地完成以下账号/工具配置：

| 准备项 | 用途 | 获取/操作方式 |
|--------|------|--------------|
| 微信开发者工具 | 预览、调试、上传代码 | 下载：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html |
| 微信小程序 AppID | 小程序唯一标识，创建项目必需 | 登录 https://mp.weixin.qq.com → 设置 → 基本设置 → AppID |
| 云开发环境 | 数据库/存储/云函数 | 开发者工具内点击「云开发」按钮开通，创建生产/测试两个环境 |
|商户号（微信支付）| JSAPI 调起支付（可选，支付场景必需）| https://pay.weixin.qq.com → 申请商户号并完成认证 |
| GitHub 账号 + 仓库 | CI/CD 流水线（可选）| https://github.com → 创建私有仓库存放小程序代码 |
| miniprogram-ci | 自动构建上传（可选）| `npm install miniprogram-ci -D` |
| Node.js ≥ 16 | CI/CD 构建环境（可选）| GitHub Actions 已内置，无需本地安装 |

> **提示**：以上大部分为微信官方平台操作，AI 可以帮你完成代码层面的所有工作，但账号注册/认证需要你本人操作。

---

## 📖 使用方法

### 第一次使用

1. **安装**：运行 `skillhub install wechat-miniprogram-toolkit`
2. **初始化项目**：告诉 AI「帮我创建一个微信小程序项目，包含云开发、分包、登录功能」，AI 参照 `references/project-init.md` 生成完整项目结构
3. **按需开发**：根据任务类型，先查阅上方「写代码前先读」表，对应加载 reference 文档

### 日常使用

| 需求 | 操作 |
|------|------|
| 新增功能页面 | 告诉 AI「参照 project-init.md 在项目中新增一个 XX 页面」|
| 分析分包是否合理 | 告诉 AI「运行 analyze_subpackages.py 分析分包，输出 app.json 配置」|
| 配置微信支付 | 告诉 AI「参照 payment.md 配置 JSAPI 支付，商户号为 XXX」|
| 遇到报错 | 告诉 AI「运行时报错：[错误信息]，查看常见错误处理表」|
| 查看能力清单 | 告诉 AI「列出这个 skill 支持的全部能力」|

### 遇到问题

1. 查上方「常见错误处理」表
2. 查对应 reference 文档的 Common Mistakes
3. 告诉 AI「查看这个 skill 的错误台账」查看历史问题记录
4. 以上均无法解决 → 描述具体问题，AI 将生成定制解答

### 需要的能力不在列表中

告诉 AI：「这个 skill 支持 XX 能力吗？」，AI 将判断：
- **已支持**：直接加载对应 reference 文档
- **部分支持**：告知当前覆盖范围 + 缺失部分
- **未支持**：记录到错误台账，等待后续版本扩展

---

## 📂 文件结构

```
wechat-miniprogram-toolkit/
│
├── SKILL.md                        # 本文件（入口）
│
├── scripts/
│   └── analyze_subpackages.py      # 自动分包分析工具（Python）
│
└── references/
    ├── project-init.md             # 项目初始化模板（必读）
    ├── cloud-dev.md                # 云开发全指南（含聚合/事务/安全）
    ├── auth.md                     # 登录鉴权指南（含手机号/UnionID）
    ├── payment.md                  # 微信支付全流程（JSAPI/退款/通知）
    ├── live-stream.md              # 直播 & 实时音视频（TRTC）
    ├── analytics.md                # 数据分析 & 用户行为埋点
    ├── share.md                    # 分享能力（朋友圈/海报/卡片）
    ├── typescript.md               # TypeScript 类型定义 & 泛型封装
    ├── cloudhosting.md             # 云托管（容器化后端/Docker）
    ├── messaging.md               # 客服消息 & 订阅消息推送
    ├── content-safety.md          # 内容安全（文本/图片/音视频审核）
    ├── miniapp-handoff.md         # 小程序互跳（APP↔小程序/URL Scheme）
    ├── hardware.md                # 硬件能力（蓝牙/GPS/NFC/Wi-Fi/扫码）
    ├── subpackage.md               # 分包策略（必读）
    ├── advanced-render.md           # Skyline/公式/表格（按需）
    ├── wxs-performance.md          # WXS & 性能优化（按需）
    ├── ci-cd.md                    # CI/CD 流水线（按需）
    └── error-log.md               # 错误台账 & 进化记录
```

---

## 激活契约（必须先读）

### ✅ 首次激活时

**符合以下任一场景，立即加载本 skill：**
- 提及"微信小程序"、"小程序"、"wxml"、"wxss"、"miniprogram"
- 需要分包、限制 2MB、subpackage
- 需要云开发、wx.cloud、cloudbase、聚合查询、事务
- 需要登录、openid、unionid、鉴权、手机号登录
- 需要微信支付、JSAPI、下单、支付通知、退款
- 需要直播、live-player、live-pusher、TRTC、实时音视频
- 需要数据分析、埋点、DAU/MAU、行为追踪、转化漏斗
- 需要分享、onShareAppMessage、onShareTimeline、分享海报
- 需要 TypeScript、TS 类型、泛型封装
- 需要云托管、容器化部署、Docker、后端服务
- 需要客服消息、订阅消息、自动回复、机器人
- 需要内容安全、文本审核、图片审核、msgSecCheck、imgSecCheck
- 需要小程序互跳、跳转APP、URL Scheme、扫一扫、deeplink
- 需要蓝牙、GPS、NFC、Wi-Fi、硬件设备
- 需要 Skyline、worklet、动画
- 需要 WXS、过滤器、性能优化
- 需要小程序 CI/CD、GitHub Actions、自动化发布

### ✅ 写代码前先读

| 任务 | 先读文档 |
|------|----------|
| 云开发（CRUD/聚合/事务/权限）| `references/cloud-dev.md` |
| 用户登录鉴权 | `references/auth.md` |
| 微信支付（JSAPI/下单/退款）| `references/payment.md` |
| 直播 / 实时音视频 | `references/live-stream.md` |
| 数据分析 / 埋点 | `references/analytics.md` |
| 分享 / 朋友圈 / 海报 | `references/share.md` |
| TypeScript 泛型封装 | `references/typescript.md` |
| 云托管 / 容器化后端 | `references/cloudhosting.md` |
| 客服消息 / 订阅消息 | `references/messaging.md` |
| 内容安全 / 内容审核 | `references/content-safety.md` |
| 小程序互跳 / URL Scheme | `references/miniapp-handoff.md` |
| 硬件能力 / 蓝牙/GPS/NFC | `references/hardware.md` |
| 分包策略/分包分析 | `references/subpackage.md` |
| Skyline / 动画 | `references/advanced-render.md` |
| 性能优化 / WXS | `references/wxs-performance.md` |
| 项目初始化配置 | `references/project-init.md` |

### ❌ 不适用场景

- Web 端微信登录（用 auth-web skill）
- 非微信小程序（如抖音/支付宝小程序）
- 需要商户后台直连（非云开发）的场景（需服务端 SDK）

---

## 能力总览

| 能力模块 | 参考文档 | 优先级 | 说明 |
|----------|----------|--------|------|
| 项目初始化 & 规范 | `project-init.md` | 🔴 必读 | 目录结构、project.config.json、app.json |
| 云开发（DB/存储/函数）| `cloud-dev.md` | 🔴 必读 | CRUD、聚合查询、事务、权限规则 |
| 登录鉴权（openid/unionid）| `auth.md` | 🔴 必读 | 静默登录、按钮授权、手机号、权限守卫 |
| 微信支付（JSAPI/下单/退款）| `payment.md` | 🔴 必读 | 统一下单、支付通知、订单查询、退款、安全规范 |
| 直播 & 实时音视频 | `live-stream.md` | 🟡 按需 | live-player、TRTC、视频通话、直播带货 |
| 数据分析 & 埋点 | `analytics.md` | 🟡 按需 | DAU/MAU、行为追踪、转化漏斗、错误监控 |
| 分享能力 | `share.md` | 🟡 按需 | onShareAppMessage、朋友圈分享、海报生成 |
| TypeScript 泛型封装 | `typescript.md` | 🟡 按需 | 类型定义、泛型封装、云函数 TS、项目配置 |
| 云托管（容器化后端）| `cloudhosting.md` | 🟡 按需 | Docker 部署、HTTP API、定时任务、自动扩缩 |
| 客服消息 & 订阅消息 | `messaging.md` | 🟡 按需 | 订阅消息、客服组件、自动回复、AccessToken 缓存 |
| 内容安全（文本/图片审核）| `content-safety.md` | 🟡 按需 | msgSecCheck、imgSecCheck、昵称审核、配额管理 |
| 小程序互跳（APP↔小程序）| `miniapp-handoff.md` | 🟡 按需 | 跳转APP、URL Scheme、开放标签、扫一扫太阳码 |
| 硬件能力（蓝牙/GPS/NFC/Wi-Fi）| `hardware.md` | 🟡 按需 | BLE、iBeacon、室内定位、NFC、Wi-Fi 配网 |
| 分包策略（≤ 2MB）| `subpackage.md` | 🔴 必读 | 分包结构、预加载、跨包通信 |
| Skyline Worklet 动画 | `advanced-render.md` | 🟡 按需 | Worklet API、SharedValue、组合动画 |
| 数学公式 & 表格 | `advanced-render.md` | 🟡 按需 | Unicode/KaTeX/WebView 三方案 |
| WXS 脚本 & 性能优化 | `wxs-performance.md` | 🟡 按需 | 过滤器、setData 优化、内存管理 |
| CI/CD 流水线 | `ci-cd.md` | 🟢 可选 | GitHub Actions、自动审核、通知 |
| 自动分包分析工具 | `analyze_subpackages.py` | 🔴 工具 | 贪心算法，自动生成 app.json 分包配置 |
| 错误台账 & 进化记录 | `references/error-log.md` | 🟢 自动 | 用户反馈/报错自动记录，≥3次自动提升 |

---

## 场景速查（快速导航）

### 场景 A：项目初始化（从零开始）

```
1. 参照 project-init.md 生成目录结构
2. 配置 project.config.json（注意 cloudfunctionRoot 路径）
3. 配置 app.json（pages + subpackages + tabBar + usingComponents）
4. 在 app.js 中初始化云开发 + 静默登录
```

### 场景 B：用户登录鉴权

```javascript
// app.js 全局初始化
wx.cloud.init({ env: 'your-env-id', traceUser: true })  // 或 wx.cloud.DYNAMIC_CURRENT_ENV

// 云函数内自动获取 openid（无需前端传参）
// cloudfunctions/login/index.js
const openid = cloud.getWXContext().OPENID  // 微信自动注入

// 页面按钮授权
<!-- 头像选择按钮 -->
<button open-type="chooseAvatar" bindchooseavatar="onChooseAvatar">
  <image src="{{avatarUrl}}" />
</button>
<!-- 昵称输入（唤起微信昵称键盘）-->
<input type="nickname" bindinput="onNicknameInput" />
```

### 场景 C：云数据库 CRUD

```javascript
const db = wx.cloud.database()
// 增
await db.collection('posts').add({ data: { title: '标题', _openid, createdAt: db.serverDate() } })
// 查
await db.collection('posts').where({ _openid: wx.getStorageSync('openid') }).get()
// 改
await db.collection('posts').doc(id).update({ data: { title: '新标题' } })
// 删
await db.collection('posts').doc(id).remove()
```

### 场景 D：分包配置（上线前必做）

```bash
python scripts/analyze_subpackages.py <项目目录> --main-max 2 --pkg-max 2
# 工具输出 app.json 分包配置片段，直接复制使用
```

### 场景 E：Skyline Worklet 动画

```javascript
// onReady 中绑定一次样式（只绑定一次）
onReady() {
  const { shared, spring } = wx.worklet
  this._scale = shared(1)

  this.applyAnimatedStyle('#box', () => {
    'worklet'
    return { transform: `scale(${this._scale.value})` }
  })
},

// 触发动画（只更新 SharedValue）
handleTap() {
  'worklet'
  const { spring } = wx.worklet
  // spring(toValue, options)：toValue=目标值，options=弹簧参数
  this._scale.value = spring(1.2, { damping: 15, stiffness: 200 })
}
```

### 场景 F：WXS 性能优化

```xml
<!-- WXS 过滤器（无需 JS 线程通信，零延迟） -->
<wxs module="utils" src="./utils.wxs"></wxs>
<view>{{utils.formatPrice(price)}}</view>
<view>{{utils.timeAgo(timestamp)}}</view>
```

---

## 不要这样做（Common Mistakes）

| ❌ 不要这样做 | ✅ 正确做法 |
|---|---|
| 在小程序里做 Web 风格登录页 | 用按钮 `open-type="chooseAvatar"` + `input type="nickname"` + 云函数自动鉴权 |
| 把 openid 从云函数返回给前端再传回来 | openid 在云函数内通过 `cloud.getWXContext()` 自动获取，无需传输 |
| 在云函数内写死 env ID | 用 `cloud.DYNAMIC_CURRENT_ENV` 自动匹配当前环境 |
| 解构 `this.data` 后修改值 | 直接修改 `this.data.xxx`，然后 `setData()` |
| 在 Worklet 中直接调用 wx API | 通过 `runOnJS()` 回调到 JS 线程再调用 |
| Worklet 函数缺少 `'worklet'` 声明 | 所有 worklet 函数第一行必须是 `'worklet'` |
| 跨分包 require 组件 | 改用 `wx.cloud.callFunction` 或 eventBus |
| 主包引用分包内的组件 | 分包组件只能分包内使用 |
| 大量小图超过 2MB | 合并雪碧图、压缩图片、移动到云存储 |
| 使用 wx.getUserInfo / getUserProfile（已废弃）| 改用 `button open-type="chooseAvatar"` + `input type="nickname"` 组合 |
| setData 传整个列表 | 用 `this.setData({ 'list[' + index + '].field': value })` 精准更新 |

---

## 开发流程（推荐）

```
阶段一：初始化
  1. 参照 project-init.md 生成完整目录
  2. 配置 project.config.json（cloudfunctionRoot + miniprogramRoot）
  3. 配置 app.json（pages + subpackages 骨架）

阶段二：开发
  4. 开发主包页面 + 组件（保持在 1.5MB 以内）
  5. 按需引入云开发能力（cloud-dev.md）
  6. 实现登录鉴权（auth.md）

阶段三：分包优化（上线前必须）
  7. 运行 python scripts/analyze_subpackages.py
  8. 根据报告创建 subpackages/ 目录结构
  9. 移动页面 + 更新 app.json 分包配置
 10. 验证包大小（微信开发者工具 → 详情 → 包大小分析）

阶段四：发布
 11. 配置 CI/CD 流水线（references/ci-cd.md）
 12. GitHub Actions 自动构建 + 提交审核
```

---

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `app.json not found` | 工作目录不对 | 确保在项目根目录，project.config.json 的 `miniprogramRoot` 指向正确 |
| 分包页面 404 | root 路径不匹配 | 检查 app.json root 与实际目录一致，路径不带前缀 `/` |
| 云函数 500 | 权限不足 / env 未初始化 | 云函数内用 `cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })` ✅；小程序端用字符串环境 ID `wx.cloud.init({ env: 'your-env-id' })` ✅，`cloud.DYNAMIC_CURRENT_ENV` 在小程序端是 **undefined** ❌ |
| 包超 2MB 警告 | 资源过大 | 压缩图片、移动到分包、使用 CDN 链接 |
| require 失败（跨分包）| 分包 A 引用了主包模块 | 用 `wx.cloud.callFunction` 或 eventBus 解耦 |
| wx.getUserInfo / wx.getUserProfile 失效 | 微信已废弃这些 API（2021 年起逐步停用）| 改用 `button open-type="chooseAvatar"` + `input type="nickname"` 组合（2024+ 标准方案）|
| Worklet 动画无效 | 缺少 `'worklet'` 声明 | 函数第一行必须写 `'worklet'` |
| SharedValue 替换失效 | `offset = 100` 替换了整个对象 | 用 `offset.value = 100` |
| 分包图片加载 404 | 分包内相对路径错误 | 用绝对路径或云存储 CDN |
| setData 卡顿 | 在滚动/手势回调中频繁 setData | 用 Worklet SharedValue 替代 |

### 运行时错误（高频）

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `errMsg: "invalid credential"` | access_token 过期 | 重新获取（有效期 2 小时，存 storage 需加缓存逻辑）|
| `errMsg: "cloud.callFunction:fail"` | 云函数超时/未部署/入口文件报错 | 检查云函数是否已上传，确认入口文件名（通常是 `index.js`）|
| `errMsg: "chooseImage:fail auth deny"` | 用户拒绝相册/相机权限 | 引导用户在设置页开启权限，或提供降级方案 |
| `errMsg: "request payment:fail"` | 支付参数签名错误 | 检查 prepay_id / 时间戳 / 随机串 / 签名算法是否与文档一致 |
| `errMsg: "database:permission denied"` | 数据库权限规则拒绝读写 | 检查 `database permission` 规则，确认用户身份字段（`_openid`）|
| `errMsg: "chooseAvatar:fail cancel"` | 用户取消头像选择 | 引导选择头像或允许使用默认头像 |
| setData 后视图不更新 | 在 Worklet 中直接修改 this.data | Worklet 只修 SharedValue，setData 须在 JS 线程调用 |
| 订阅消息发送失败 | 用户未授权 / 模板 ID 错误 | 确认 `tmplIds` 存在、用户在授权弹窗点了允许 |
| 云存储上传失败 | 文件超过 50MB | 分片上传（云托管）或改用 CDN 直传 |
| 云函数返回 500 但本地正常 | 云端环境 env 不一致 | 确认云函数部署的环境与小程序 init 的 env ID 一致 |

---

## 常用官方文档链接

| 文档 | 链接 |
|------|------|
| 官方开发文档 | https://developers.weixin.qq.com/miniprogram/dev/framework/ |
| 云开发指南 | https://developers.weixin.qq.com/miniprogram/dev/wxcloud/basis/ |
| 分包加载 | https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages/ |
| Skyline 渲染 | https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/skyline/ |
| Worklet 动画 | https://developers.weixin.qq.com/miniprogram/dev/framework/view/skyline/worklet-animation.html |
| WXS 参考 | https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxs/ |
| miniprogram-ci | https://www.npmjs.com/package/miniprogram-ci |

---

## 🧠 自我进化机制

> 本 skill 具有自我进化能力。当用户反馈错误、或发现更好的方案时，AI 会自动记录并改进。

### 触发条件

当出现以下任一情况时，AI 自动记录到 skill 的错误台账：

| 触发场景 | 记录内容 |
|----------|----------|
| 用户说"不对"、"错了"、"应该..." | 用户纠正的错误内容 |
| AI 生成的代码运行报错 | 错误信息 + 报错场景 |
| 微信官方 API 变更 | 变更内容 + 更新后的正确写法 |
| 用户提出 skill 没有覆盖的能力 | 需求描述 + 优先级 |

### 进化记录格式

```markdown
## 进化记录

### LRN-YYYYMMDD-NNNN
**时间**: YYYY-MM-DD
**触发场景**: <用户反馈/报错/新需求>
**错误内容**: <AI 给出的错误答案>
**正确内容**: <正确的做法>
**修复文件**: <修改了哪个文件>
```

### 进化流程

```
用户反馈 / 发现错误
    ↓
立即修复当前答案（本次回答正确）
    ↓
记录到 `references/error-log.md`（永久积累）
    ↓
若同一错误出现 ≥ 3 次 → 自动更新到 SKILL.md / 对应 reference 文件
    ↓
下次遇到相同场景 → 直接从 skill 文件中读取正确答案
```

### 查看进化记录

告诉 AI：「查看这个 skill 的错误台账」即可查看所有历史记录。

### 当前进化记录

> 暂无记录（每次反馈都会自动追加）

---

*版本历史：v1.0.0（初始版本）→ v1.1.0（新增 WXS / CI-CD / 激活契约 / 自我进化机制）→ v1.5.0（新增内容安全/互跳/硬件能力）→ v1.6.0（修复废弃 API、全面支持 2024+ 登录方案、修复支付 MCH_ID 错误）*
