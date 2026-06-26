---
name: wechat-quick-setup
description: 微信小程序快速启动模板。一键创建云函数、配置后端、生成代码。10分钟搭建完整微信小程序。
version: 1.0.0
author: OpenClaw CN
tags:
  - wechat
  - miniprogram
  - tencent-cloud
  - quick-start
---

# 微信小程序快速启动

专为微信小程序开发者设计。10 分钟搭建完整小程序，包含云函数、用户系统、数据存储。

## 功能

- ⚡ **快速初始化** - 一键生成项目结构
- ☁️ **云函数模板** - 登录/支付/存储常用云函数
- 👤 **用户系统** - 完整的登录/授权/用户信息管理
- 💾 **数据存储** - 云数据库 CRUD 操作封装
- 🎨 **UI 组件** - 常用页面模板

## 安装

```bash
npx clawhub@latest install wechat-quick-setup
```

## 使用方法

### 1. 初始化项目

```bash
node ~/.openclaw/skills/wechat-quick-setup/init.js --name "我的小程序"
```

生成项目结构：
```
my-miniprogram/
├── cloudfunctions/      # 云函数
│   ├── login/          # 登录
│   ├── getProducts/    # 获取商品
│   ├── createOrder/    # 创建订单
│   └── initDB/         # 初始化数据库
├── miniprogram/        # 小程序前端
│   ├── pages/          # 页面
│   ├── components/     # 组件
│   └── utils/          # 工具函数
├── project.config.json # 配置
└── README.md
```

### 2. 生成云函数

```bash
# 生成登录云函数
node ~/.openclaw/skills/wechat-quick-setup/generate-function.js login

# 生成 CRUD 云函数
node ~/.openclaw/skills/wechat-quick-setup/generate-function.js crud --collection products
```

### 3. 生成页面

```bash
# 生成商品列表页
node ~/.openclaw/skills/wechat-quick-setup/generate-page.js product-list

# 生成订单页
node ~/.openclaw/skills/wechat-quick-setup/generate-page.js order
```

### 4. 配置云开发

```bash
# 初始化云开发环境
node ~/.openclaw/skills/wechat-quick-setup/setup-cloud.js --env your-env-id
```

## 包含的模板

### 云函数模板
- **login** - 用户登录
- **getOpenId** - 获取用户 OpenID
- **getProducts** - 获取商品列表
- **createOrder** - 创建订单
- **initDB** - 初始化数据库
- **uploadFile** - 文件上传

### 页面模板
- **首页** - 轮播图 + 商品列表
- **商品详情** - 商品信息 + 购买按钮
- **订单列表** - 订单状态展示
- **用户中心** - 用户信息 + 设置

### UI 组件
- **product-card** - 商品卡片
- **order-item** - 订单项
- **loading** - 加载状态
- **empty** - 空状态

## 完整示例

### 创建电商小程序

```bash
# 1. 初始化
node ~/.openclaw/skills/wechat-quick-setup/init.js --name "商城"

# 2. 生成云函数
node ~/.openclaw/skills/wechat-quick-setup/generate-function.js login
node ~/.openclaw/skills/wechat-quick-setup/generate-function.js getProducts
node ~/.openclaw/skills/wechat-quick-setup/generate-function.js createOrder

# 3. 生成页面
node ~/.openclaw/skills/wechat-quick-setup/generate-page.js home
node ~/.openclaw/skills/wechat-quick-setup/generate-page.js product-detail
node ~/.openclaw/skills/wechat-quick-setup/generate-page.js order

# 4. 用微信开发者工具打开
# 导入项目 → 选择目录 → 填入 AppID
```

## 技术栈

- **前端**: 微信小程序原生框架
- **后端**: 腾讯云开发（云函数 + 云数据库 + 云存储）
- **语言**: JavaScript/TypeScript

## 常见问题

### Q: 需要服务器吗？
A: 不需要。使用腾讯云开发，免费额度足够小型应用使用。

### Q: 如何获取 AppID？
A: 访问 https://mp.weixin.qq.com → 开发 → 开发设置 → AppID

### Q: 云开发免费吗？
A: 有免费额度：
- 云函数：10 万次调用/月
- 数据库：2GB 存储
- 云存储：5GB 存储

## 配置

编辑 `~/.openclaw/skills/wechat-quick-setup/config.json`：

```json
{
  "appid": "your-appid",
  "envId": "your-env-id",
  "projectName": "我的小程序"
}
```

---

## 💬 Pro 版本（¥299）

### 免费版（当前）
- 基础云函数模板
- 基础页面模板
- 项目初始化

### Pro 版（¥299）
- ✅ 20+ 高级云函数（支付/订阅/消息推送）
- ✅ 10+ 完整页面模板
- ✅ 数据库设计模板
- ✅ 后台管理系统
- ✅ 1对1 远程配置支持
- ✅ 1年更新支持

### 联系方式
- **QQ**: 1002378395（中国用户）
- **Telegram**: `待注册`（海外用户）

> 添加 QQ 1002378395，发送"微信小程序"获取 Pro 版信息

---

## License

MIT（免费版）
Pro 版：付费后可用
