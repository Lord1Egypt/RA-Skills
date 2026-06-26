---
name: wechat-miniapp-deploy
description: "Deploy and manage WeChat Mini Programs (微信小程序) using the official miniprogram-ci CLI. Teach AI agents how to upload code, submit for review, manage versions, configure QR codes, and automate the full WeChat Mini Program deployment pipeline. Covers: first-time project setup and CI configuration, code upload with version management, review submission with privacy compliance, automated CI/CD pipeline for mini programs, multi-environment deployment (dev/staging/prod). Triggers on: 微信小程序部署, wechat mini program deploy, 小程序上传, miniapp upload, 小程序审核, mini program review, 小程序CI/CD, miniprogram-ci, 微信小程序发布, wechat miniapp publish, 小程序自动化部署, mini program automation, 小程序版本管理, miniapp version management, 小程序隐私合规, miniapp privacy compliance"
---

# WeChat MiniApp Deploy - 微信小程序部署专家

You are an expert at deploying and managing WeChat Mini Programs using the official `miniprogram-ci` CLI tool. You automate the full deployment pipeline from code upload to review submission.

## Core Philosophy

**WeChat Mini Program deployment is not just `git push`.** It involves code upload → version management → experience QR → review submission → release. Each step has specific requirements and failure modes unique to the WeChat ecosystem.

## Prerequisites

### 1. Install miniprogram-ci
```bash
npm install -g miniprogram-ci
```

### 2. Get CI Key
1. Go to https://mp.weixin.qq.com → Development → Development Settings → Mini Program CI
2. Download the CI key (private key file)
3. Note the AppID from Settings → Basic Information
4. **Whitelist the deploy IP** in the same settings page

### 3. Project Configuration
Ensure `project.config.json` exists in project root:
```json
{
  "appid": "wx1234567890abcdef",
  "projectname": "my-miniapp",
  "compileType": "miniprogram",
  "setting": {
    "es6": true,
    "minify": true,
    "uglifyFileName": true
  }
}
```

## Workflow 1: First-Time Project Setup

**When**: New mini program project, first deployment

```bash
# Step 1: Verify project structure
ls project.config.json app.json app.js 2>/dev/null || echo "❌ Missing required files"

# Step 2: Upload with initial version
miniprogram-ci upload \
  --pp ./ \
  --pkp ./private.wx1234567890abcdef.key \
  --appid wx1234567890abcdef \
  --uv "1.0.0" \
  -r 1 \
  --desc "Initial release" \
  --enable-es6 true

# Step 3: Generate experience QR code
miniprogram-ci preview \
  --pp ./ \
  --pkp ./private.wx1234567890abcdef.key \
  --appid wx1234567890abcdef \
  -q ./preview-qrcode.jpg \
  --desc "Preview v1.0.0"

# Step 4: Verify upload succeeded
miniprogram-ci get-preview-info \
  --pkp ./private.wx1234567890abcdef.key \
  --appid wx1234567890abcdef
```

**Output**: Experience QR code generated, ready for testing before review submission.

## Workflow 2: Code Upload with Version Management

**When**: Regular deployment, new version upload

```bash
# Step 1: Determine version number
# Read current version from project.config.json or package.json
CURRENT_VERSION=$(node -p "require('./package.json').version" 2>/dev/null || echo "1.0.0")

# Step 2: Bump version (patch/minor/major)
# Ask user which bump type, then:
NEW_VERSION=$(node -p "
const v = '$CURRENT_VERSION'.split('.').map(Number);
v[2]++;  // patch bump
v.join('.')
")

# Step 3: Upload with version and changelog
miniprogram-ci upload \
  --pp ./ \
  --pkp ./private.key \
  --appid $APPID \
  --uv "$NEW_VERSION" \
  -r 1 \
  --desc "$(git log --oneline -5 | head -5)" \
  --enable-es6 true \
  --enable-minify true

# Step 4: Generate preview QR
miniprogram-ci preview \
  --pp ./ \
  --pkp ./private.key \
  --appid $APPID \
  -q ./qrcode-v${NEW_VERSION}.jpg
```

**Version Rules**:
- **Patch** (1.0.x): Bug fixes, minor tweaks
- **Minor** (1.x.0): New features, backward compatible
- **Major** (x.0.0): Breaking changes, major redesign

## Workflow 3: Review Submission with Privacy Compliance

**When**: Ready to submit for WeChat review (required before public release)

**⚠️ Critical**: WeChat review is strict. Missing privacy declarations = instant rejection.

### Pre-Submission Checklist
```bash
# Step 1: Verify privacy compliance
# Check __privacy__.json exists and is complete
cat __privacy__.json 2>/dev/null || echo "❌ Missing privacy declaration"

# Required privacy fields:
# - userInfo: if collecting user info
# - location: if using location API
# - album: if accessing photo album
# - camera: if using camera
# - microphone: if recording audio
# - contacts: if accessing contacts
# - phoneNumber: if getting phone number

# Step 2: Verify app.json permissions
node -e "
const app = require('./app.json');
const required = app.permission || {};
console.log('Declared permissions:', JSON.stringify(required, null, 2));
"

# Step 3: Check for banned content
# - No virtual payment for non-virtual goods
# - No user-generated content without moderation
# - No social features without real-name verification
# - No lottery/gambling mechanics
```

### Submit for Review
```bash
# Step 4: Submit via WeChat MP admin API
# Note: miniprogram-ci doesn't directly submit for review
# This must be done via the WeChat MP admin panel or API

# Using WeChat API (requires access_token):
ACCESS_TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$APPID&secret=$APPSECRET" | node -p "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).access_token")

# Submit for review
curl -X POST "https://api.weixin.qq.com/wxa/submit_audit?access_token=$ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_list": [{
      "address": "pages/index/index",
      "tag": "首页",
      "first_class": "工具",
      "second_class": "效率",
      "title": "首页"
    }],
    "feedback_info": "首次提交审核",
    "feedback_stuff": ""
  }'
```

## Workflow 4: Automated CI/CD Pipeline

**When**: Set up automated deployment in GitHub Actions / GitLab CI

### GitHub Actions Example
```yaml
name: MiniApp Deploy
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          npm install
          npm install -g miniprogram-ci

      - name: Upload to WeChat
        env:
          MINI_APPID: ${{ secrets.MINI_APPID }}
          MINI_PRIVATE_KEY: ${{ secrets.MINI_PRIVATE_KEY }}
        run: |
          echo "$MINI_PRIVATE_KEY" > ./private.key
          VERSION=$(node -p "require('./package.json').version")
          miniprogram-ci upload \
            --pp ./ \
            --pkp ./private.key \
            --appid $MINI_APPID \
            --uv "$VERSION" \
            -r 1 \
            --desc "$(git log --oneline -1)" \
            --enable-es6 true \
            --enable-minify true
          rm ./private.key

      - name: Generate Preview QR
        if: github.ref != 'refs/heads/main'
        run: |
          echo "$MINI_PRIVATE_KEY" > ./private.key
          miniprogram-ci preview \
            --pp ./ \
            --pkp ./private.key \
            --appid $MINI_APPID \
            -q ./preview.jpg
          rm ./private.key

      - name: Upload QR artifact
        if: github.ref != 'refs/heads/main'
        uses: actions/upload-artifact@v4
        with:
          name: preview-qrcode
          path: preview.jpg
```

### Required GitHub Secrets
- `MINI_APPID`: WeChat Mini Program AppID
- `MINI_PRIVATE_KEY`: Contents of the CI private key file

## Workflow 5: Multi-Environment Deployment

**When**: Managing dev/staging/prod environments

```bash
# Environment-specific configuration
ENV=$1  # dev | staging | prod

# Map environment to AppID (different mini programs for each env)
case $ENV in
  dev)
    APPID="wx_dev_appid"
    VERSION_SUFFIX="-dev"
    ;;
  staging)
    APPID="wx_staging_appid"
    VERSION_SUFFIX="-rc"
    ;;
  prod)
    APPID="wx_prod_appid"
    VERSION_SUFFIX=""
    ;;
esac

# Build with environment config
npm run build:$ENV

# Upload to corresponding environment
miniprogram-ci upload \
  --pp ./dist/$ENV \
  --pkp ./private.${APPID}.key \
  --appid $APPID \
  --uv "$(node -p "require('./package.json').version")${VERSION_SUFFIX}" \
  -r 1 \
  --desc "Deploy to $ENV environment" \
  --enable-es6 true
```

## Common Rejection Reasons & Fixes

| Rejection Reason | Fix |
|-----------------|-----|
| Missing privacy declaration | Add `__privacy__.json` with all used APIs |
| Virtual payment violation | Remove wx.requestPayment for physical goods |
| User content without moderation | Add content review before display |
| No real-name for social features | Implement real-name verification |
| Misleading UI | Remove fake system dialogs/notifications |
| Unauthorized API usage | Only use documented WeChat APIs |
| Test content in production | Remove all placeholder/test data |
| Missing user agreement | Add terms of service page |

## Safety Rules

1. **Never commit private keys**: CI keys must be in secrets, never in code
2. **IP whitelist**: Always whitelist CI server IPs in WeChat MP settings
3. **Version bump**: Never upload with the same version number twice
4. **Preview before submit**: Always test with experience QR before review submission
5. **Privacy first**: Every API that touches user data needs declaration
6. **Backup before deploy**: Tag the git commit before uploading

## Quick Reference

```bash
# Upload
miniprogram-ci upload --pp ./ --pkp ./key --appid $ID --uv "1.0.0" -r 1 --desc "desc"

# Preview
miniprogram-ci preview --pp ./ --pkp ./key --appid $ID -q ./qr.jpg

# Build npm (if using npm packages)
miniprogram-ci build-npm --pp ./

# Get upload record
miniprogram-ci get-preview-info --pkp ./key --appid $ID
```
