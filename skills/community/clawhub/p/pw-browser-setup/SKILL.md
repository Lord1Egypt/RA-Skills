---
name: browser-setup
description: >
  浏览器自动化环境的一键安装、检查和验证工具。
  安装 Playwright + Chromium，支持非头模式（模拟真实用户浏览器）和头模式。
  包含系统兼容性检查（内存、CPU、磁盘）、依赖安装、Xvfb 虚拟显示器配置。
  当用户要求：(1) 安装浏览器自动化环境 (2) 配置 Playwright (3) 检查系统是否支持浏览器
  (4) 安装 Chrome/Chromium 用于自动化 (5) 配置非头浏览器环境 时使用。
---

# Browser Setup

一键安装和验证 Playwright + Chromium 浏览器自动化环境。

## 快速流程

按顺序执行以下三步：

### Step 1: 检查系统兼容性

```bash
bash scripts/check-compat.sh
```

检查项：操作系统、内存（≥2GB，推荐 4GB+）、CPU（≥2核）、磁盘（≥1GB）、Node.js（≥18）、Xvfb 状态。

如果 `FAIL > 0`，先解决问题再继续。

### Step 2: 安装浏览器环境

```bash
bash scripts/install-browser.sh <工作目录路径>
```

自动完成：
- 安装 Xvfb 虚拟显示器（Linux）+ Chrome 系统依赖
- 安装 Playwright npm 包（全局 + 项目内）
- 下载 Chromium + Chrome Headless Shell
- 创建 `scripts/start-xvfb.sh` 辅助脚本

### Step 3: 验证

```bash
# 头模式（适合服务器）
bash scripts/verify-browser.sh <工作目录> /tmp/browser-verify.png headless

# 非头模式（模拟真实用户，需先启动 Xvfb）
bash scripts/verify-browser.sh <工作目录> /tmp/browser-verify.png headed
```

验证脚本会：打开百度 → 截取屏幕 → 输出标题和热搜第一 → 返回截图路径。

## 非头模式说明

服务器环境没有物理显示器，需要 Xvfb 创建虚拟显示器：

```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1280x900x24 -ac &
```

之后 Playwright 设置 `headless: false`，浏览器在虚拟显示器中运行，行为与真实用户完全一致（加载所有扩展、渲染 WebGL、触发真实 DOM 事件）。

## Playwright 代码示例

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({
  headless: false,          // 非头模式
  args: ['--no-sandbox']    // 服务器环境必需
});
const page = await browser.newPage();
await page.goto('https://www.baidu.com');
await page.screenshot({ path: '/tmp/screenshot.png' });
await browser.close();
```

## 截图发送到飞书

验证脚本生成截图后，可通过飞书 API 上传并发送：

```bash
# 1. 上传图片获取 image_key
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -F "image_type=message" \
  -F "image=@/tmp/browser-verify.png" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['image_key'])")

# 2. 发送图片消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"<open_id>","msg_type":"image","content":"{\"image_key\":\"'"$IMAGE_KEY"'\"}"}'
```
