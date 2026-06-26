# CI/CD 流水线配置模板

## GitHub Actions（推荐）

### 完整配置：`.github/workflows/deploy-wechat.yml`

```yaml
name: WeChat MiniProgram CI/CD

on:
  push:
    branches: [main, master]
  workflow_dispatch:
    inputs:
      version:
        description: '发布版本号 (semver)'
        required: true
        default: '1.0.0'
      mode:
        description: '发布模式'
        required: true
        default: 'experience'
        type: choice
        options:
          - experience   # 体验版
          - review       # 提交审核
          - release      # 直接发布（需审核通过）

concurrency:
  group: wechat-deploy-${{ github.ref }}
  cancel-in-progress: true

jobs:
  deploy:
    name: Build & Deploy
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      # 1. 拉取代码
      - name: Checkout
        uses: actions/checkout@v4

      # 2. 安装 Node.js
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      # 3. 安装依赖
      - name: Install dependencies
        run: npm ci

      # 4. 写入微信私钥
      - name: Prepare private key
        run: |
          mkdir -p keys
          echo "${{ secrets.WEAPP_PRIVATE_KEY }}" > keys/private.key
          chmod 400 keys/private.key

      # 5. 构建 uni-app
      - name: Build uni-app
        run: npm run build:mp-weixin
        env:
          NODE_ENV: production

      # 6. 上传并发布
      - name: Upload to WeChat
        run: node scripts/build-uni.js
        env:
          VERSION: ${{ github.event.inputs.version || '1.0.0' }}
          WEAPP_APPID: ${{ secrets.WEAPP_APPID }}
          WEAPP_PRIVATE_KEY_PATH: keys/private.key

      # 7. 通知（可选：飞书/钉钉/Slack）
      - name: Notify (optional)
        if: always()
        run: |
          echo "Deploy completed: ${{ job.status }}"
```

### 配置 Secrets（必须）

在 GitHub 仓库 → **Settings → Secrets and variables → Actions** 中添加：

| Secret 名称 | 说明 | 获取方式 |
|---|---|---|
| `WEAPP_APPID` | 小程序 AppID | 微信公众平台 → 开发管理 → 开发设置 |
| `WEAPP_PRIVATE_KEY` | 私钥文件全文 | 下载的 `.key` 文件内容（注意换行符）|

> ⚠️ Windows 生成 secret 时，私钥内容中的换行需保留 `\n`，不要转成空格。

### 多环境配置示例

```yaml
env:
  NODE_ENV: production
  WEAPP_APPID: ${{ secrets.WEAPP_APPID_QA }}    # QA 环境
  # WEAPP_APPID: ${{ secrets.WEAPP_APPID_PROD }} # 正式环境
```

---

## GitLab CI

### 完整配置：`.gitlab-ci.yml`

```yaml
stages:
  - build
  - deploy
  - notify

variables:
  NODE_VERSION: "18"
  UNI_BUILD_CMD: "npm run build:mp-weixin"

.build_node:
  image: node:${NODE_VERSION}-alpine
  before_script:
    - npm ci --prefer-offline

build:
  stage: build
  extends: .build_node
  script:
    - npm run build:mp-weixin
  artifacts:
    name: "dist-wechat"
    paths:
      - dist/build/mp-weixin/
    expire_in: 1 hour

deploy:experience:
  stage: deploy
  extends: .build_node
  image: node:18-alpine
  script:
    - npm install --save-dev miniprogram-ci
    - mkdir -p keys
    - echo "$WEAPP_PRIVATE_KEY" > keys/private.key
    - node scripts/build-uni.js
  artifacts:
    name: "wechat-artifacts"
    paths:
      - dist/build/mp-weixin/
  variables:
    VERSION: "${CI_COMMIT_TAG:-1.0.0}"
    WEAPP_APPID: ${WEAPP_APPID}
    WEAPP_PRIVATE_KEY_PATH: keys/private.key
  only:
    - main
    - master
  needs:
    - build
```

### GitLab CI/CD 变量配置

在 GitLab → **Settings → CI/CD → Variables** 中配置：

| 变量名 | 值 | 选项 |
|---|---|---|
| `WEAPP_APPID` | `wx0123456789abcdef` | Protected + Masked |
| `WEAPP_PRIVATE_KEY` | `.key` 文件全文内容 | Protected + Masked |

---

## Jenkins（可选）

```groovy
pipeline {
  agent any

  environment {
    WEAPP_APPID = credentials('weapp-appid')
    WEAPP_PRIVATE_KEY_PATH = credentials('weapp-private-key-path')
    VERSION = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Build') {
      steps {
        sh 'npm ci'
        sh 'npm run build:mp-weixin'
      }
    }

    stage('Deploy') {
      steps {
        sh 'node scripts/build-uni.js'
      }
    }
  }

  post {
    always {
      deleteDir()
    }
  }
}
```

---

## 常见问题

### Q: `40013 invalid appid`
→ `WEAPP_APPID` 与私钥不匹配，确认 Secrets 中的 appid 与私钥来源一致。

### Q: GitHub Actions 私钥换行符问题
Windows 写入 secret 时换行符可能丢失。用以下命令验证：
```bash
# 验证密钥格式正确
openssl rsa -in keys/private.key -check
```

### Q: 多分支发布不同环境
用 GitHub Environments 实现：

```yaml
environment:
  name: production
  url: https://example.com
```
