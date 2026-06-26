# 小程序 CI/CD 流水线指南

---

## 激活契约

**符合以下任一场景时加载：**
- 想自动化构建、提交审核
- 使用 GitHub 管理小程序项目
- 需要在团队中标准化发布流程
- 想实现提交代码自动发布

---

## 一、方案总览

| 方案 | 适用平台 | 难度 | 自动审核 |
|------|----------|------|----------|
| GitHub Actions + miniprogram-ci | GitHub | ⭐⭐ | ✅ |
| GitLab CI | GitLab | ⭐⭐⭐ | ✅ |
| Jenkins + miniprogram-ci | 任意 | ⭐⭐⭐⭐ | ✅ |
| GitHub Actions + 腾讯云 | 腾讯云托管 | ⭐⭐⭐ | ✅ |

---

## 二、GitHub Actions + miniprogram-ci（推荐）

### 原理

```
Git push → GitHub Actions 触发
  → 安装依赖（miniprogram-ci）
  → 构建/分析代码
  → 自动提交审核
  → 微信后台通知结果
```

### 前置准备

#### 1. 获取微信小程序密钥

微信公众平台 → 开发管理 → 开发设置 → **小程序密钥**（AppSecret）

> ⚠️ AppSecret 是敏感信息，**不要直接写在代码里**，使用 GitHub Secrets 存储。

#### 2. 添加 GitHub Secrets

在 GitHub 仓库 → Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 值 |
|------------|-----|
| `WEAPP_APPID` | 小程序 AppID |
| `WEAPP_APP_SECRET` | 小程序 AppSecret |
| `WEAPP_PRIVATE_KEY` | 密钥（见下方"获取私钥"步骤）|

#### 3. 获取私钥

微信公众平台 → 开发管理 → 开发设置 → **下载密钥**（或选择使用「上传密钥」获取私钥）

下载后，将私钥文件内容（`-----BEGIN PRIVATE KEY-----...`）复制到 GitHub Secret 中。

---

## 三、GitHub Actions 配置

### 项目结构

```
project/
├── .github/
│   └── workflows/
│       └── weapp.yml          # CI/CD 配置
├── project.config.json
├── cloudfunctions/              # 云函数（可选）
└── miniprogram/               # 小程序目录
    └── app.js
```

### 基础 CI 流水线（自动构建）

```yaml
# .github/workflows/weapp-build.yml
name: 小程序构建

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        uses: actions/checkout@v4

      - name: 安装 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: 安装依赖
        run: npm ci

      - name: 构建项目
        run: npm run build

      - name: 小程序代码分析
        run: |
          node scripts/analyze.js
        env:
          WEAPP_APPID: ${{ secrets.WEAPP_APPID }}

      - name: 上传分析报告
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: analysis-report
          path: report.json
```

### 完整 CI/CD 流水线（自动提交审核）

```yaml
# .github/workflows/weapp-release.yml
name: 小程序自动发布

on:
  push:
    tags:
      - 'v*'                    # 打标签触发发布，如 v1.0.0
    branches:
      - release                # 向 release 分支 push 也触发

env:
  NODE_VERSION: '18'

jobs:
  # ── 任务一：代码检查 ──
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: 安装依赖
        run: npm ci

      - name: ESLint 检查
        run: npm run lint

  # ── 任务二：构建 & 分析 ──
  build:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: 安装依赖
        run: npm ci

      - name: 构建
        run: npm run build

      - name: 小程序构建
        run: |
          # 将私钥 Secret 写入文件（miniprogram-ci 需要文件路径）
          echo "${{ secrets.WEAPP_PRIVATE_KEY }}" > private.weapp.key
          node scripts/build-weapp.js
        env:
          WEAPP_APPID: ${{ secrets.WEAPP_APPID }}
          WEAPP_PRIVATE_KEY: ${{ secrets.WEAPP_PRIVATE_KEY }}

      - name: 上传构建产物
        uses: actions/upload-artifact@v4
        with:
          name: weapp-dist
          path: dist/

  # ── 任务三：提交审核 ──
  release:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/release'
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: 安装 miniprogram-ci
        run: |
          npm install miniprogram-ci -D
          # 将私钥写入文件
          echo "${{ secrets.WEAPP_PRIVATE_KEY }}" > private.weapp.key

      - name: 提交代码审核
        run: node scripts/submit-audit.js
        env:
          WEAPP_APPID: ${{ secrets.WEAPP_APPID }}
          WEAPP_PRIVATE_KEY: ${{ secrets.WEAPP_PRIVATE_KEY }}
          WEAPP_APP_SECRET: ${{ secrets.WEAPP_APP_SECRET }}

      - name: 发送通知
        if: always()
        run: |
          node scripts/notify.js
        env:
          TG_BOT_TOKEN: ${{ secrets.TG_BOT_TOKEN }}
          TG_CHAT_ID: ${{ secrets.TG_CHAT_ID }}
```

---

## 四、核心脚本

### 4.1 构建脚本 `scripts/build-weapp.js`

```javascript
// scripts/build-weapp.js
const ci = require('miniprogram-ci')

async function build() {
  const project = new ci.Project({
    appid: process.env.WEAPP_APPID,
    type: 'miniProgram',
    projectPath: process.cwd(),
    privateKeyPath: './private.weapp.key',  // 提前从 secret 写入
    ignores: ['node_modules/**/*', 'src/**/*', '.git/**/*'],
  })

  await ci.packNpmManually({
    project,
    packageJsonPath: './package.json',
    miniprogramNpmDistDir: './miniprogram',
  })

  const result = await ci.build({
    project,
    version: process.env.GITHUB_TAG?.replace('v', '') || '1.0.0',
    desc: `CI 构建 ${new Date().toLocaleString()}`,
    setting: {
      es6: true,
      enhance: true,
      minifyWXSS: true,
      minifyWXML: true,
    },
    onProgressUpdate: console.log,
  })

  console.log('构建完成:', result)
}

build().catch(e => { console.error(e); process.exit(1) })
```

### 4.2 提交审核脚本 `scripts/submit-audit.js`

```javascript
// scripts/submit-audit.js
const ci = require('miniprogram-ci')

async function submit() {
  const project = new ci.Project({
    appid: process.env.WEAPP_APPID,
    type: 'miniProgram',
    projectPath: process.cwd(),
    privateKeyPath: './private.weapp.key',
  })

  // 1. 上传代码
  const uploadResult = await ci.upload({
    project,
    version: process.env.GITHUB_TAG?.replace('v', '') || '1.0.0',
    desc: `CI 提交 ${process.env.GITHUB_SHA?.slice(0, 7)} - ${new Date().toISOString()}`,
    setting: {
      es6: true,
      enhance: true,
      minifyWXSS: true,
      minifyWXML: true,
      uploadWithMessage: true,
    },
    onProgressUpdate: console.log,
  })

  console.log('上传成功:', uploadResult)

  // 2. 提交审核
  const auditResult = await ci.submitAudit({
    project,
    auditInfo: {
      versionDesc: '本次更新：\n1. 优化页面加载速度\n2. 修复已知问题',
      versionTestFlag: 0,  // 0=正式版，1=体验版
    },
  })

  console.log('审核提交成功，ID:', auditResult.auditid)
  console.log('预计审核时间:', auditResult.throught, '小时')

  // 3. 保存审核 ID 到 GitHub Actions 环境变量（供后续 job 使用）
  console.log(`::set-output name=audit_id::${auditResult.auditid}`)
  // 注：GitHub Actions 2023.10 后废弃 ::set-output 语法，
  //   新写法用 process.stdout.write('audit_id=xxx\n') 写入 GITHUB_OUTPUT 文件，
  //   但 miniprogram-ci 的 CI 场景通常直接用环境变量传递，无需改动。
}

submit().catch(e => { console.error(e); process.exit(1) })
```

### 4.3 查询审核结果 `scripts/query-audit.js`

```javascript
// scripts/query-audit.js
const ci = require('miniprogram-ci')

async function query() {
  const project = new ci.Project({
    appid: process.env.WEAPP_APPID,
    type: 'miniProgram',
    projectPath: process.cwd(),
    privateKeyPath: './private.weapp.key',
  })

  const auditId = process.env.AUDIT_ID || 'your-audit-id'

  const result = await ci.getAuditResult({ project, auditId })

  switch (result.status) {
    case 0: console.log('✅ 审核通过！'); break
    case 1: console.log('⏳ 审核中...'); break
    case 2: console.log('❌ 审核失败:', result.reason); break
    case 3: console.log('⚠️ 撤回:', result.reason); break
  }

  return result
}

query().catch(e => { console.error(e); process.exit(1) })
```

### 4.4 自动发布脚本 `scripts/release.js`

```javascript
// scripts/release.js
const ci = require('miniprogram-ci')

async function release() {
  const project = new ci.Project({
    appid: process.env.WEAPP_APPID,
    type: 'miniProgram',
    projectPath: process.cwd(),
    privateKeyPath: './private.weapp.key',
  })

  // 审核通过后自动发布
  const result = await ci.release({
    project,
    version: process.env.GITHUB_TAG?.replace('v', '') || '1.0.0',
    versionDesc: '正式版发布',
  })

  console.log('🎉 发布成功!')
  console.log(result)
}

release().catch(e => { console.error(e); process.exit(1) })
```

---

## 五、完整发布工作流

```
开发 → push 到 dev 分支
         ↓
   GitHub Actions 自动构建 + ESLint 检查
         ↓
   人工 Code Review → merge 到 release 分支
         ↓
   GitHub Actions 触发发布流水线
         ↓
   自动上传代码 → 提交审核 → 微信审核（约1-24小时）
         ↓
   审核通过 → 自动发布 / 人工确认发布
         ↓
   GitHub Release 生成 + 通知团队
```

---

## 六、GitHub Secrets 配置指南

```
GitHub 仓库
└── Settings
    └── Secrets and variables
        └── Actions
            ├── WEAPP_APPID          → 你的 AppID（wx...）
            ├── WEAPP_APP_SECRET     → 微信 AppSecret
            └── WEAPP_PRIVATE_KEY    → 下载的私钥文件全文（多行文本需转成单行）
```

> 私钥文件转单行：在本地执行 `cat private.weapp.key | tr '\n' ' '` 然后复制输出。

---

## 七、package.json scripts 配置

```json
{
  "scripts": {
    "build": "node scripts/build.js",
    "build:weapp": "node scripts/build-weapp.js",
    "lint": "eslint miniprogram/ --ext .js",
    "lint:fix": "eslint miniprogram/ --ext .js --fix",
    "submit": "node scripts/submit-audit.js",
    "query": "node scripts/query-audit.js",
    "release": "node scripts/release.js",
    "ci:build": "npm run lint && npm run build:weapp",
    "ci:release": "node scripts/submit-audit.js && node scripts/query-audit.js && node scripts/release.js"
  },
  "devDependencies": {
    "miniprogram-ci": "^1.0.1",
    "eslint": "^8.0.0"
  }
}
```
