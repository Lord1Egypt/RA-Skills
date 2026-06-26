---
name: uni-app-wechat-cicd
description: uni-app 项目微信小程序全流程开发、构建与 CI/CD 发布。当用户提到：开发 uni-app 小程序、用 uni-app 开发微信小程序、uni-app 小程序 CI/CD 发布、小程序上传体验版、自动发布微信小程序、miniprogram-ci 配置、微信小程序自动化发布、GitHub Actions / GitLab CI 部署微信小程序等场景时触发本技能。
---

# uni-app 微信小程序开发与 CI/CD 发布

## 技能概述

本技能提供 uni-app 开发微信小程序的全流程支持，包括：项目初始化、微信开发者工具配置、`miniprogram-ci` CLI 集成、GitHub Actions / GitLab CI 自动化发布流水线。

---

## 目录结构

```
uni-app-wechat-cicd/
├── SKILL.md                  ← 主入口（本文件）
├── references/
│   ├── miniprogram-ci.md     ← miniprogram-ci 完整配置与 API 参考
│   ├── cicd-templates.md     ← GitHub Actions / GitLab CI 模板配置
│   └── wechat-devtools.md    ← 微信开发者工具 CLI 操作指南
└── scripts/
    ├── build-uni.js          ← uni-app 构建 + miniprogram-ci 上传脚本
    └── ci-publish.sh         ← CI 环境一键发布脚本
```

> 详细参考文档见 `references/` 目录下各文件，按需加载。

---

## 核心工作流

### 1. uni-app 项目初始化（微信小程序）

**目标平台：** H5 / 小程序双模式开发，最终发布到微信小程序。

**关键配置 `manifest.json`：**

```json
{
  "mp-weixin": {
    "appid": "wx0123456789abcdef",
    "setting": {
      "urlCheck": false,
      "es6": true,
      "postcss": true,
      "minified": true
    },
    "usingComponents": true
  }
}
```

**构建命令：**

```bash
# 安装依赖
npm install

# 开发模式（热重载）
npm run dev:mp-weixin

# 生产构建
npm run build:mp-weixin
# 输出目录：dist/build/mp-weixin/
```

---

### 2. 配置微信开发者工具 CLI

微信开发者工具必须开启 CLI 调用功能：

```
微信开发者工具 → 设置 → 安全设置 → 开启服务端口
```

获取 CLI 路径（通常在）：

```
Windows: C:\Program Files (x86)\Tencent\微信web开发者工具\WechatDevTools\1.0.0\cli.bat
macOS:   /Applications/wechat devtools/Contents/MacOS/cli
```

---

### 3. miniprogram-ci 发布流程

`miniprogram-ci` 是微信官方提供的命令行发布工具，支持代码上传、体验版发布、提交审核。

**安装：**

```bash
npm install --save-dev miniprogram-ci
```

**基础上传脚本 `scripts/build-uni.js`：**

详细 API 参数见 [references/miniprogram-ci.md](references/miniprogram-ci.md)

```javascript
const ci = require('miniprogram-ci')

async function upload() {
  const project = new ci.Project({
    appid: 'wx0123456789abcdef',
    type: 'miniProgram',
    projectPath: 'dist/build/mp-weixin',
    privateKeyPath: 'keys/private.wx0123456789abcdef.key',  // 密钥路径
    ignores: ['node_modules/**/*'],
  })

  // ① 上传代码
  const uploadResult = await ci.upload({
    project,
    version: '1.0.0',        // 语义化版本号
    desc: 'CI 自动发布 v1.0.0', // 上传描述
    setting: {
      es6: true,
      minify: true,
      codeProtect: false,
      autoPrefixWXSS: true,
    },
    onProgressUpdate: console.log,
  })
  console.log('上传成功:', uploadResult.subPackageInfo)

  // ② 提交体验版
  await ci Experience.createTestVersion({
    project,
    version: '1.0.0',
    desc: 'CI 自动发布体验版',
  })
  console.log('体验版发布成功')
}

upload().catch(console.error)
```

---

### 4. CI/CD 流水线配置

#### GitHub Actions（推荐）

完整配置模板见 [references/cicd-templates.md](references/cicd-templates.md)

```yaml
# .github/workflows/deploy-wechat.yml
name: Deploy WeChat MiniProgram

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      version:
        description: '版本号'
        required: true
        default: '1.0.0'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build uni-app
        run: npm run build:mp-weixin
        env:
          NODE_ENV: production

      - name: Download private key
        uses: actions/download-artifact@v4
        with:
          name: wechat-private-key
          path: keys/

      - name: Upload to WeChat
        run: node scripts/build-uni.js
        env:
          VERSION: ${{ github.event.inputs.version || '1.0.0' }}
```

**需要的 Secrets（Settings → Secrets）：**

| Secret Name | 说明 |
|---|---|
| `WEAPP_PRIVATE_KEY` | 微信密钥（`.key` 文件内容） |
| `WEAPP_APPID` | 小程序 AppID |
| `WEAPP_PRIVATE_KEY_PATH` | 密钥保存路径 |

#### GitLab CI

见 [references/cicd-templates.md](references/cicd-templates.md)

---

### 5. 自动生成密钥并配置权限

**Step 1：** 登录 [微信公众平台](https://mp.weixin.qq.com) → 开发管理 → 开发设置 → 小程序代码上传密钥 → 生成密钥并下载。

**Step 2：** 将公钥填入平台，私钥妥善保管（不要提交到 Git）。

**Step 3：** 将私钥文件通过 CI Secret 或 artifact 方式安全传入流水线。

---

## 常用命令速查

| 场景 | 命令 |
|---|---|
| 开发调试 | `npm run dev:mp-weixin` |
| 生产构建 | `npm run build:mp-weixin` |
| 本地预览（需微信开发者工具） | `cli.bat open --project <path>` |
| CLI 上传 | `node scripts/build-uni.js` |
| 预览二维码（CI） | 见 `references/miniprogram-ci.md` |

---

## 故障排查

| 问题 | 解决方案 |
|---|---|
| `invalid signature` | 私钥路径错误或格式不对，检查 `privateKeyPath` |
| `40013 appid 不合法` | 检查 `manifest.json` 中的 appid 是否与私钥对应 |
| 微信开发者工具端口不通 | 确认已开启「服务端口」|
| CI 找不到私钥文件 | 检查 artifact 下载路径和 `WEAPP_PRIVATE_KEY_PATH` |
| `plugin not found` | `project.config.json` 中 `compileType` 需为 `miniprogram` |

详细故障排除见 [references/miniprogram-ci.md](references/miniprogram-dev.md)
