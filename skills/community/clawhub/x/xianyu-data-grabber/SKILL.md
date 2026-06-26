---
name: xianyu-data-grabber
description: 闲鱼数据抓取技能。使用 Playwright + OCR 技术突破反爬虫，抓取闲鱼商品数据（标题、价格、想要人数等），自动上传截图和数据到 Gitee 仓库。支持批量关键词搜索、竞品分析、市场调研。
version: 1.0.0
author: 爪爪
tags:
  - 闲鱼
  - 数据抓取
  - 竞品分析
  - 市场调研
  - Playwright
  - OCR
requires:
  env:
    - GITEE_TOKEN: Gitee 个人访问令牌
    - GITEE_OWNER: Gitee 用户名/组织名
    - GITEE_REPO: Gitee 仓库名
    - XIANFU_COOKIE: 闲鱼登录 Cookie（可选，提高成功率）
  bins:
    - node: JavaScript 运行时
    - python3: Python 运行时
    - tesseract: OCR 文字识别
    - playwright: 浏览器自动化
---

# 闲鱼数据抓取技能 (xianyu-data-grabber)

## 功能描述

使用 Playwright + OCR 技术突破闲鱼反爬虫，抓取商品数据并自动上传到 Gitee 仓库。

**核心能力**:
- 批量关键词搜索（支持 15+ 关键词）
- 自动截图保存（PNG 格式）
- OCR 文字识别（中文 + 英文）
- 商品信息提取（标题、价格、想要人数）
- 自动生成分析报告（Markdown + JSON）
- 自动上传到 Gitee 仓库

## 什么时候使用

当用户提到以下场景时，激活此技能：

1. 「帮我抓取闲鱼上的竞品数据」
2. 「调研闲鱼上某某类目的商品」
3. 「分析闲鱼头部卖家的定价策略」
4. 「闲鱼市场调研」
5. 「抓取闲鱼商品价格和销量」
6. 「xianyu research」/「闲鱼数据抓取」
7. 「看看闲鱼上这个东西卖得怎么样」
8. 「闲鱼竞品分析」

## 配置文件

### 1. 基础配置

创建 `~/.openclaw/workspace/.xianyu-grabber-config.json`:

```json
{
  "gitee": {
    "token": "your_gitee_token",
    "owner": "your_username",
    "repo": "xianyu-data"
  },
  "xianyu": {
    "cookie": "your_xianyu_cookie"
  },
  "grabber": {
    "keywords": ["Magisk", "KernelSU", "手机维修"],
    "screenshotDir": "legion/screenshots",
    "dataDir": "legion/data",
    "uploadToGitee": true,
    "ocrLanguage": "chi_sim+eng"
  }
}
```

### 2. Gitee 个人访问令牌

获取方式：
1. 登录 https://gitee.com
2. 设置 → 个人访问令牌
3. 创建新令牌（勾选 `projects` 权限）
4. 复制令牌到配置文件

### 3. 闲鱼 Cookie（可选）

获取方式：
1. 浏览器登录闲鱼
2. F12 开发者工具 → Network
3. 刷新页面 → 复制 Cookie 字段

## 使用方法

### 基础用法

```bash
# 抓取单个关键词
xianyu-data-grabber search "Magisk"

# 抓取多个关键词
xianyu-data-grabber search "Magisk" "KernelSU" "root"

# 使用配置文件中的关键词列表
xianyu-data-grabber search --config
```

### 高级用法

```bash
# 指定输出目录
xianyu-data-grabber search "Magisk" --output ./my-research

# 不上传 Gitee
xianyu-data-grabber search "Magisk" --no-upload

# 仅 OCR 不抓取（已有截图）
xianyu-data-grabber ocr --input ./screenshots

# 生成汇总报告
xianyu-data-grabber report --input ./data

# 上传到 Gitee
xianyu-data-grabber upload --all
```

### 通过消息技能调用

```
帮我抓取闲鱼上"Magisk"相关的商品数据
调研闲鱼手机维修类目的竞品
分析闲鱼 root 服务的定价策略
```

## 输出文件

### 截图文件

- `legion/screenshots/xianyu-{keyword}.png`
- 全页面截图（高度可能超过 10000px）

### 数据文件

| 文件 | 格式 | 内容 |
|------|------|------|
| `xianyu-{keyword}.json` | JSON | 单个关键词原始数据 |
| `xianyu-full-data.json` | JSON | 所有关键词汇总 |
| `xianyu-summary.md` | Markdown | 汇总报告 |
| `xianyu-analysis.md` | Markdown | 深度分析报告 |

### Gitee 仓库结构

```
xianyu-data/
├── README.md              # 自动生成的说明
├── data/
│   ├── xianyu-full-data.json
│   └── xianyu-{keyword}.json
├── screenshots/
│   └── xianyu-{keyword}.png
├── reports/
│   ├── xianyu-summary.md
│   └── xianyu-analysis.md
└── upload-{timestamp}.md  # 上传记录
```

## 核心脚本

### grabber.js - 主抓取脚本

```javascript
// 1. 启动 Playwright 浏览器（Headless + 伪装）
// 2. 加载 Cookie（如有）
// 3. 遍历关键词搜索
// 4. 截图保存
// 5. 调用 OCR 识别
// 6. 提取商品信息
// 7. 保存 JSON 数据
```

### ocr.py - OCR 识别脚本

```python
# 1. 读取截图
# 2. Tesseract OCR 识别
# 3. 提取价格/想要人数等
# 4. 输出结构化数据
```

### uploader.sh - Gitee 上传脚本

```bash
# 1. 调用 Gitee API
# 2. 创建/更新文件
# 3. 提交 commit
# 4. 返回上传结果
```

## 数据格式

### 单个商品数据

```json
{
  "keyword": "Magisk",
  "products": [
    {
      "title": "Magisk 模块合集 17G 资源",
      "price": "1.00",
      "wants": "628 人想要",
      "seller": "卖家信用优秀",
      "tags": ["24h 自动发货", "包邮"]
    }
  ],
  "timestamp": "2026-03-20T06:00:00+08:00",
  "screenshot": "screenshots/xianyu-Magisk.png"
}
```

### 汇总报告结构

```markdown
# 闲鱼数据调研报告

## 关键词：Magisk
- 商品数：19 个
- 价格区间：¥1-50 元
- 热门商品：...

## 关键词：KernelSU
...

## 价格分析
...

## 竞品分析
...
```

## DEBUG 指引

### 日志位置

| 日志 | 文件 |
|------|------|
| 抓取日志 | `logs/xianyu-grabber.log` |
| OCR 日志 | `logs/xianyu-ocr.log` |
| 上传日志 | `logs/xianyu-upload.log` |
| 错误日志 | `logs/xianyu-error.log` |

### 常见问题

#### 1. 截图显示「非法访问」

**原因**: 反爬虫检测到自动化

**解决**:
```bash
# 1. 更新 Cookie
# 2. 降低抓取速度（增加延迟）
# 3. 减少并发关键词数量
```

#### 2. OCR 识别结果为空

**原因**: Tesseract 未安装或语言包缺失

**解决**:
```bash
# 安装 Tesseract
apt-get install tesseract-ocr tesseract-ocr-chi-sim

# 验证安装
tesseract --version
tesseract --list-langs
```

#### 3. Gitee 上传失败

**原因**: Token 无效或权限不足

**解决**:
```bash
# 1. 检查 Token 是否有效
curl -H "Authorization: Bearer YOUR_TOKEN" https://gitee.com/api/v5/user

# 2. 检查仓库权限
# 确保 Token 有 projects 权限
```

#### 4. Playwright 浏览器启动失败

**原因**: 缺少依赖或浏览器未安装

**解决**:
```bash
# 安装 Playwright 浏览器
npx playwright install chromium

# 安装系统依赖
apt-get install libnss3 libnspr4 libatk1.0-0 \
  libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
  libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libgbm1 libasound2 libpango-1.0-0 libcairo2
```

### 测试命令

```bash
# 测试配置
xianyu-data-grabber test-config

# 测试 OCR
xianyu-data-grabber test-ocr --image test.png

# 测试 Gitee 上传
xianyu-data-grabber test-upload --file test.txt

# 完整测试
xianyu-data-grabber test --all
```

## 定时任务

### 每日自动抓取

```bash
# crontab -e
0 9 * * * cd ~/.openclaw/workspace && node skills/xianyu-data-grabber/grabber.js --config --upload >> logs/xianyu-cron.log 2>&1
```

### 每周生成报告

```bash
0 10 * * 1 cd ~/.openclaw/workspace && node skills/xianyu-data-grabber/report.js >> logs/xianyu-report.log 2>&1
```

## 安全与隐私

### 敏感数据保护

- **Cookie**: 存储在配置文件，权限 600
- **Gitee Token**: 存储在配置文件，权限 600
- **数据文件**: 本地存储，不上传第三方

### 平台合规

- **请求频率**: 默认 5 秒间隔/关键词
- **User-Agent**: 真实浏览器标识
- **数据使用**: 仅用于个人研究

## 性能优化

### 批量抓取

```bash
# 并行抓取（更快但可能被检测）
xianyu-data-grabber search --parallel 3

# 串行抓取（更慢但更安全）
xianyu-data-grabber search --sequential
```

### 缓存机制

- 截图缓存：避免重复抓取
- OCR 缓存：避免重复识别
- 数据缓存：5 分钟有效期

## 相关文件

- 技能文件：`skills/xianyu-data-grabber/SKILL.md`
- 主脚本：`skills/xianyu-data-grabber/grabber.js`
- OCR 脚本：`skills/xianyu-data-grabber/ocr.py`
- 上传脚本：`skills/xianyu-data-grabber/uploader.sh`
- 配置文件：`.xianyu-grabber-config.json`

## Changelog

### v1.0.0 (2026-03-20)
- 🎉 初始版本
- Playwright + OCR 抓取
- Gitee 自动上传
- 批量关键词支持
- 自动生成报告
