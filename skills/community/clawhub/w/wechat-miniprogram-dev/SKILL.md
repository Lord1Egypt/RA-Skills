---
name: wechat-miniprogram-dev
description: 微信小程序云开发完整指南。包含项目结构、云函数开发、miniprogram-ci 部署命令、常见问题处理。适用于需要开发、部署微信小程序的场景。
---

# 微信小程序云开发指南

## 项目结构

```
weapp-project/
├── miniprogram/           # 小程序前端代码
│   ├── app.js
│   ├── app.json
│   ├── app.wxss
│   ├── pages/
│   │   ├── index/        # 页面目录
│   │   │   ├── index.js
│   │   │   ├── index.wxml
│   │   │   ├── index.wxss
│   │   │   └── index.json
│   │   └── ...
│   ├── components/
│   ├── utils/
│   └── images/
├── cloudfunctions/        # 云函数目录
│   ├── getTaskProgress/
│   │   ├── index.js
│   │   └── package.json
│   └── ...
├── cloudbaserc           # 云开发配置
├── project.config.json   # 小程序项目配置
└── key/
    └── private.key        # 微信公众号密钥
```

## 关键配置文件

### project.config.json
```json
{
  "appid": "your-appid",
  "cloudfunctionRoot": "cloudfunctions/",
  "setting": {
    "urlCheck": false,
    "es6": true,
    "enhance": true
  }
}
```

### 云函数 package.json
```json
{
  "name": "function-name",
  "version": "1.0.0",
  "dependencies": {
    "wx-server-sdk": "~2.6.3"
  }
}
```

## miniprogram-ci 常用命令

### 部署云函数
```bash
npx miniprogram-ci cloud functions upload \
  --pp ./ \
  --pkp ./key/private.key \
  -r 1 \
  -e cloudbase-环境ID \
  -n 函数名 \
  -p ./cloudfunctions/函数名 \
  --rnpm
```

参数说明：
- `--pp`: 项目路径
- `--pkp`: 私钥路径
- `-r`: 机器人编号 (1-30)
- `-e`: 云开发环境ID
- `-n`: 云函数名称
- `-p`: 云函数代码路径
- `--rnpm`: 远程安装依赖

### 预览小程序
```bash
npx miniprogram-ci preview \
  --pp ./miniprogram \
  --pkp ./key/private.key \
  --qr-dest ./preview-qrcode.png \
  --qr-format image \
  --appid your-appid \
  -r 1 \
  --enable-qrcode true \
  --uv "1.0.0" \
  --threads 0 \
  --use-cos false
```

### 上传小程序
```bash
npx miniprogram-ci upload \
  --pp ./miniprogram \
  --pkp ./key/private.key \
  --appid your-appid \
  -r 1 \
  --uv "1.0.0" \
  --ud "更新描述"
```

## 云函数开发要点

### 初始化云开发
```javascript
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const db = cloud.database()
```

### 获取用户信息
```javascript
const { OPENID } = cloud.getWXContext()
```

### 获取临时文件URL
```javascript
async function getTempFileURL(fileID) {
  if (!fileID) return null
  try {
    const result = await cloud.getTempFileURL({
      fileList: [fileID]
    })
    if (result.fileList && result.fileList[0]) {
      return result.fileList[0].tempFileURL
    }
  } catch (e) {
    console.error('获取临时URL失败:', e)
  }
  return null
}
```

### 调用其他云函数
```javascript
const result = await cloud.callFunction({
  name: '函数名',
  data: { /* 参数 */ }
})
```

## 图像处理扩展

### 安装扩展
在云开发控制台 → 扩展能力 → 安装「图像处理」

### 使用示例
```javascript
const extCi = require('@cloudbase/extension-ci')
cloud.registerExtension(extCi)

// 添加水印
const res = await cloud.invokeExtension('CloudInfinite', {
  action: 'WaterMark',
  cloudPath: 'target.jpg',
  fileContent: imageBuffer,
  operations: {
    rules: [{
      fileid: 'output.jpg',
      rule: {
        mode: 3,
        type: 2,
        text: '水印文字',
        gravity: 'SouthEast'
      }
    }]
  }
})
```

## 常见问题

### ⚠️ 重要：wx.requestSubscribeMessage 调用规范

**微信规定**：订阅消息授权必须在**用户点击事件的回调函数中同步触发**，否则会失败。

**正确做法**：
```javascript
// ❌ 错误：在异步回调中调用（云函数返回后才调用）
async submit() {
  await wx.cloud.callFunction({ name: 'xxx' })
  wx.requestSubscribeMessage({ tmplIds: [...] }) // 太晚了！
}

// ✅ 正确：在点击事件第一时间同步调用
async submit() {
  wx.requestSubscribeMessage({ tmplIds: [...] }) // 立即调用
  await wx.cloud.callFunction({ name: 'xxx' })   // 然后再做其他事
}
```

**关键点**：
1. 必须在 `bindtap` 或 `catchtap` 回调的**同步流程**中调用
2. 不能放在 `setTimeout`、异步 `await`、或任何回调链的后面
3. 推荐在 `onLoad` 时预获取模板ID，存入 `data`，点击时直接从 `data` 读取

---

### Q: 云函数上传失败 "ResourceNotFound.Function"
A: 需要先在微信开发者工具中手动创建云函数一次，然后再用 ci 上传更新

### Q: 预览二维码失效
A: 尝试更换版本号 --uv "1.0.X"，多次尝试

### Q: getTempFileURL 返回 undefined
A: 检查 fileID 是否为云存储的 fileID，外部URL不需要转换

### Q: cloud.init 报错
A: 确保在云函数中初始化，客户端使用 wx.cloud

### Q: 云函数依赖安装失败
A: 使用 --rnpm 参数让云端安装依赖，或检查 package.json