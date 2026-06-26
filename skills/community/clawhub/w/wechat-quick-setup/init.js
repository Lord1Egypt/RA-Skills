#!/usr/bin/env node

/**
 * 微信小程序快速初始化
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const nameIndex = args.indexOf('--name');
const projectName = nameIndex !== -1 ? args[nameIndex + 1] : 'my-miniprogram';

if (args.length === 0 || !nameIndex) {
  console.log(`
📖 微信小程序快速初始化

用法:
  node init.js --name "项目名称"

示例:
  node init.js --name "商城小程序"
`);
  process.exit(0);
}

console.log(`\n🚀 初始化微信小程序: ${projectName}\n`);

// 项目结构
const structure = {
  'cloudfunctions': {
    'login/index.js': `// 登录云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  return {
    openid: wxContext.OPENID,
    appid: wxContext.APPID
  }
}`,
    'getProducts/index.js': `// 获取商品列表
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { page = 1, pageSize = 10 } = event
  const result = await db.collection('products')
    .skip((page - 1) * pageSize)
    .limit(pageSize)
    .get()
  return result
}`,
    'createOrder/index.js': `// 创建订单
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { productId, quantity } = event
  const wxContext = cloud.getWXContext()

  const result = await db.collection('orders').add({
    data: {
      productId,
      quantity,
      openid: wxContext.OPENID,
      status: 'pending',
      createdAt: new Date()
    }
  })
  return result
}`,
    'initDB/index.js': `// 初始化数据库
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  // 创建商品表
  await db.createCollection('products')
  // 创建订单表
  await db.createCollection('orders')
  // 创建用户表
  await db.createCollection('users')
  return { message: '数据库初始化成功' }
}`
  },
  'miniprogram': {
    'pages/index/index.js': `// 首页
Page({
  data: {
    products: []
  },
  onLoad() {
    this.loadProducts()
  },
  async loadProducts() {
    const res = await wx.cloud.callFunction({
      name: 'getProducts'
    })
    this.setData({ products: res.result.data })
  }
})`,
    'pages/index/index.wxml': `<view class="container">
  <view wx:for="{{products}}" wx:key="_id" class="product-card">
    <text>{{item.name}}</text>
    <text>¥{{item.price}}</text>
  </view>
</view>`,
    'pages/index/index.wxss': `.container {
  padding: 20rpx;
}
.product-card {
  padding: 20rpx;
  margin-bottom: 20rpx;
  border-radius: 8rpx;
  background: #fff;
}`,
    'app.js': `App({
  onLaunch() {
    wx.cloud.init({
      env: 'your-env-id',
      traceUser: true
    })
  }
})`,
    'app.json': `{
  "pages": [
    "pages/index/index"
  ],
  "window": {
    "navigationBarTitleText": "${projectName}"
  },
  "cloud": true
}`,
    'app.wxss': `page {
  background: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}`
  },
  'project.config.json': `{
  "miniprogramRoot": "miniprogram/",
  "cloudfunctionRoot": "cloudfunctions/",
  "setting": {
    "es6": true,
    "postcss": true,
    "minified": true
  },
  "appid": "touristappid",
  "projectname": "${projectName}"
}`,
  'README.md': `# ${projectName}

微信小程序项目

## 开发

1. 用微信开发者工具打开此目录
2. 填入你的 AppID
3. 配置云开发环境 ID（在 app.js 中）
4. 上传并部署云函数

## 云函数

- login - 用户登录
- getProducts - 获取商品列表
- createOrder - 创建订单
- initDB - 初始化数据库

## 目录结构

\`\`\`
cloudfunctions/  # 云函数
miniprogram/     # 小程序前端
\`\`\`
`
};

// 创建目录和文件
function createStructure(basePath, obj) {
  for (const [key, value] of Object.entries(obj)) {
    const fullPath = path.join(basePath, key);
    if (typeof value === 'string') {
      // 文件
      const dir = path.dirname(fullPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(fullPath, value);
      console.log(`✅ 创建: ${key}`);
    } else {
      // 目录
      createStructure(fullPath, value);
    }
  }
}

const projectPath = path.join(process.cwd(), projectName);
if (fs.existsSync(projectPath)) {
  console.error(`❌ 目录已存在: ${projectName}`);
  process.exit(1);
}

fs.mkdirSync(projectPath, { recursive: true });
createStructure(projectPath, structure);

console.log(`\n✅ 项目初始化完成: ${projectName}
📖 下一步:
1. 用微信开发者工具打开目录
2. 填入你的 AppID
3. 配置云开发环境
4. 上传并部署云函数
`);
