#!/usr/bin/env node

/**
 * 云函数生成器
 */

const fs = require('fs');
const path = require('path');

// 云函数模板
const templates = {
  login: `// 登录云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const db = cloud.database()

  // 查询用户是否存在
  const userResult = await db.collection('users').where({
    openid: wxContext.OPENID
  }).get()

  if (userResult.data.length === 0) {
    // 创建新用户
    await db.collection('users').add({
      data: {
        openid: wxContext.OPENID,
        createdAt: new Date(),
        ...event.userInfo
      }
    })
  }

  return {
    openid: wxContext.OPENID,
    appid: wxContext.APPID,
    isNew: userResult.data.length === 0
  }
}`,

  payment: `// 支付云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { orderId, totalFee } = event
  const wxContext = cloud.getWXContext()

  // 调用微信支付
  const res = await cloud.cloudPay.unifiedOrder({
    body: '商品支付',
    outTradeNo: orderId,
    spbillCreateIp: '127.0.0.1',
    totalFee: totalFee * 100, // 单位：分
    envId: cloud.DYNAMIC_CURRENT_ENV,
    functionName: 'payCallback',
    nonceStr: Math.random().toString(36).substr(2),
    tradeType: 'JSAPI'
  })

  return res
}`,

  subscribe: `// 订阅消息云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { touser, templateId, page, data } = event

  const res = await cloud.openapi.subscribeMessage.send({
    touser,
    templateId,
    page,
    data
  })

  return res
}`,

  upload: `// 文件上传云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { cloudPath, fileContent } = event

  const res = await cloud.uploadFile({
    cloudPath,
    fileContent: Buffer.from(fileContent, 'base64')
  })

  return res
}`,

  crud: `// CRUD 云函数
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { action, collection, data, id, where } = event

  switch (action) {
    case 'create':
      return await db.collection(collection).add({ data })

    case 'read':
      if (id) {
        return await db.collection(collection).doc(id).get()
      }
      return await db.collection(collection).where(where || {}).get()

    case 'update':
      return await db.collection(collection).doc(id).update({ data })

    case 'delete':
      return await db.collection(collection).doc(id).remove()

    default:
      return { error: 'Invalid action' }
  }
}`
};

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(`
📖 云函数生成器

用法:
  node generate-function.js <类型> [--collection 表名]

类型:
  login      登录
  payment    支付
  subscribe  订阅消息
  upload     文件上传
  crud       通用 CRUD

示例:
  node generate-function.js login
  node generate-function.js crud --collection products
`);
  process.exit(0);
}

const funcType = args[0];
const collectionIndex = args.indexOf('--collection');
const collection = collectionIndex !== -1 ? args[collectionIndex + 1] : 'items';

if (!templates[funcType]) {
  console.error(`❌ 不支持的类型: ${funcType}`);
  console.log(`支持的类型: ${Object.keys(templates).join(', ')}`);
  process.exit(1);
}

// 创建云函数目录
const funcDir = path.join(process.cwd(), funcType);
if (fs.existsSync(funcDir)) {
  console.error(`❌ 云函数已存在: ${funcType}`);
  process.exit(1);
}

fs.mkdirSync(funcDir, { recursive: true });

// 写入云函数代码
let code = templates[funcType];
if (funcType === 'crud') {
  code = code.replace(/collection/g, `'${collection}'`);
}

fs.writeFileSync(path.join(funcDir, 'index.js'), code);

// 写入 package.json
const packageJson = {
  name: funcType,
  version: '1.0.0',
  main: 'index.js',
  dependencies: {
    'wx-server-sdk': '~2.6.3'
  }
};
fs.writeFileSync(path.join(funcDir, 'package.json'), JSON.stringify(packageJson, null, 2));

console.log(`\n✅ 云函数已创建: ${funcType}/
📁 位置: ${funcDir}

下一步:
1. cd ${funcType} && npm install
2. 在微信开发者工具中上传并部署
`);
