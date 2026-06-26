# miniprogram-ci 完整参考

## 安装与初始化

```bash
npm install --save-dev miniprogram-ci
```

## Project 初始化

```javascript
const ci = require('miniprogram-ci')

const project = new ci.Project({
  appid: 'wxyourappid',            // 小程序 AppID
  type: 'miniProgram',             // 固定值
  projectPath: 'dist/build/mp-weixin', // uni-app 构建产物路径
  privateKeyPath: 'keys/private.wxyourappid.key',
  ignores: [
    'node_modules/**/*',
    '.git/**/*',
    '*.md',
  ],
})
```

## API 列表

### ci.upload() — 上传代码

```javascript
const uploadResult = await ci.upload({
  project,
  version: '1.2.3',           // 版本号（语义化，推荐 semver）
  desc: 'feat: 新增用户中心页面\nfix: 修复登录闪退',  // 上传描述
  setting: {
    es6: true,
    minify: true,             // 压缩
    codeProtect: false,        // 代码保护（付费）
    autoPrefixWXSS: true,
    minifyWXML: true,
    minifyWXSS: true,
    minifyJS: true,
  },
  onProgressUpdate: (info) => {
    // info: { status, message, total, current }
    console.log(`[${info.status}] ${info.message}`)
  },
})
console.log(uploadResult)  // { subPackageInfo, pluginInfo, ...
```

### ci.Experience.createTestVersion() — 发布体验版

```javascript
const { expireType, testUrl } = await ci.Experience.createTestVersion({
  project,
  version: '1.2.3',
  desc: 'CI 自动发布 - 体验版',
})
console.log('体验版二维码:', testUrl)
```

### ci.Code.commitVersion() — 提交审核

```javascript
await ci.Code.commitVersion({
  project,
  version: '1.2.3',
  desc: 'feat: 新增用户中心\nfix: 修复登录问题',
})
```

### ci.Code.audit() — 提交审核后查询状态

```javascript
const auditResult = await ci.Code.audit({
  project,
  auditId: 'audit_id_string',
})
console.log(auditResult.status)  // 0=成功, 1=待审核, 2=被驳回
```

### ci.Code.getAuditResult() — 获取审核结果

```javascript
const result = await ci.Code.getAuditResult({
  project,
  auditId: 'audit_id_string',
})
```

### ci.Code.release() — 发布已审核版本（需先通过审核）

```javascript
await ci.Code.release({
  project,
  version: '1.2.3',
})
```

### ci.Code.rollback() — 回滚

```javascript
await ci.Code.rollback({
  project,
  version: '1.2.3',  // 要回滚到的目标版本
})
```

### ci.Code.getVersionInfo() — 获取版本信息

```javascript
const info = await ci.Code.getVersionInfo({ project })
console.log(info)
```

## 完整 CI 发布脚本（build-uni.js）

```javascript
const ci = require('miniprogram-ci')
const path = require('path')
const fs = require('fs')

const VERSION = process.env.VERSION || '1.0.0'
const APP_ID = process.env.WEAPP_APPID
const PRIVATE_KEY_PATH = process.env.WEAPP_PRIVATE_KEY_PATH || 'keys/private.key'

async function main() {
  const project = new ci.Project({
    appid: APP_ID,
    type: 'miniProgram',
    projectPath: path.resolve(__dirname, '../dist/build/mp-weixin'),
    privateKeyPath: PRIVATE_KEY_PATH,
    ignores: ['node_modules/**/*', '*.md', '.git/**/*'],
  })

  console.log(`🚀 开始发布 v${VERSION}`)

  // 1. 上传代码
  const uploadResult = await ci.upload({
    project,
    version: VERSION,
    desc: `CI 自动构建发布 v${VERSION} - ${new Date().toISOString()}`,
    setting: {
      es6: true,
      minify: true,
      codeProtect: false,
      autoPrefixWXSS: true,
      minifyWXML: true,
      minifyWXSS: true,
      minifyJS: true,
    },
    onProgressUpdate: (info) => {
      if (info.status === 'building' || info.status === 'uploading') {
        process.stdout.write(`\r  ${info.message} ${info.current}/${info.total}`)
      }
    },
  })
  console.log('\n✅ 代码上传成功')
  console.log('  插件信息:', uploadResult.pluginInfo)
  console.log('  分包信息:', uploadResult.subPackageInfo)

  // 2. 发布体验版
  const { testUrl } = await ci.Experience.createTestVersion({
    project,
    version: VERSION,
    desc: `CI 自动构建 v${VERSION}`,
  })
  console.log('\n✅ 体验版发布成功')
  console.log('  体验二维码:', testUrl)

  // 3. 自动提交审核（可选，取消注释即可启用）
  // await ci.Code.commitVersion({
  //   project,
  //   version: VERSION,
  //   desc: `CI 自动提交审核 v${VERSION}`,
  // })
  // console.log('\n✅ 已提交审核')
  //
  // const auditResult = await ci.Code.audit({ project })
  // console.log('  审核 ID:', auditResult.auditid)
}

main().catch((err) => {
  console.error('\n❌ 发布失败:', err.message)
  process.exit(1)
})
```

## 环境变量

| 变量名 | 说明 | 示例 |
|---|---|---|
| `WEAPP_APPID` | 小程序 AppID | `wx0123456789abcdef` |
| `WEAPP_PRIVATE_KEY_PATH` | 私钥文件路径 | `keys/private.wx012345.key` |
| `WEAPP_PRIVATE_KEY` | 私钥内容（直接传入）| `-----BEGIN RSA PRIVATE KEY-----\n...` |
| `VERSION` | 发布版本号 | `1.2.3` |
| `NODE_ENV` | 环境 | `production` |

## 密钥安全管理

### 推荐：通过 Secrets 注入文件内容

```yaml
# GitHub Actions
- name: Prepare private key
  run: |
    mkdir -p keys
    echo "${{ secrets.WEAPP_PRIVATE_KEY }}" > keys/private.key
    chmod 600 keys/private.key

env:
  WEAPP_APPID: ${{ secrets.WEAPP_APPID }}
  WEAPP_PRIVATE_KEY_PATH: keys/private.key
```

### 注意：不要提交 `.key` 文件到 Git！
