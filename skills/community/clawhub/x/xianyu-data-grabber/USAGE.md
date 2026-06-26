# 🐾 闲鱼数据抓取技能 - 使用说明

## 技能概述

**技能名称**: `xianyu-data-grabber`  
**版本**: 2.0  
**功能**: 自动抓取闲鱼商品数据，OCR 识别，生成报告，上传 Gitee

---

## 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip3 install pillow pytesseract opencv-python-headless --break-system-packages

# 系统依赖
apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Node 依赖（已有）
npm install playwright
npx playwright install chromium
```

### 2. 配置

创建配置文件 `~/.openclaw/workspace/.xianyu-grabber-config.json`:

```bash
cp .xianyu-grabber-config.template.json .xianyu-grabber-config.json
```

编辑配置文件：

```json
{
  "gitee": {
    "token": "你的 Gitee 个人访问令牌",
    "owner": "你的 Gitee 用户名",
    "repo": "xianyu-data"
  },
  "xianyu": {
    "cookie": "你的闲鱼 Cookie（可选，提高成功率）"
  },
  "grabber": {
    "keywords": ["Magisk", "KernelSU"],
    "uploadToGitee": true
  }
}
```

**获取 Gitee Token**:
1. 登录 https://gitee.com
2. 设置 → 个人访问令牌
3. 创建令牌（勾选 `projects` 权限）

**获取闲鱼 Cookie**:
1. 浏览器登录闲鱼
2. F12 → Network → 刷新
3. 复制 Cookie 字段

---

## 使用方法

### 方式 1: 统一入口（推荐）

```bash
cd /root/.openclaw/workspace

# 查看状态
./skills/xianyu-data-grabber/run.sh status

# 抓取指定关键词
./skills/xianyu-data-grabber/run.sh grab "Magisk" "KernelSU"

# 抓取所有 60+ 关键词
./skills/xianyu-data-grabber/run.sh grab-all

# 生成报告
./skills/xianyu-data-grabber/run.sh report

# 上传 Gitee
./skills/xianyu-data-grabber/run.sh upload

# 查看帮助
./skills/xianyu-data-grabber/run.sh help
```

### 方式 2: 直接调用脚本

```bash
# 抓取
node skills/xianyu-data-grabber/grabber-enhanced.js "Magisk" "KernelSU"

# OCR
python3 skills/xianyu-data-grabber/ocr-enhanced.py legion/screenshots/xianyu-Magisk.png

# 上传
bash skills/xianyu-data-grabber/uploader.sh legion/data
```

### 方式 3: 通过消息技能调用

```
帮我抓取闲鱼上"Magisk"的数据
调研闲鱼手机维修类目
上传闲鱼数据到 Gitee
```

---

## 输出文件

### 截图文件

- 位置：`legion/screenshots/xianyu-{keyword}.png`
- 格式：PNG（全页面截图）
- 大小：1-3MB/张

### 数据文件

| 文件 | 格式 | 内容 |
|------|------|------|
| `xianyu-{keyword}-data.json` | JSON | 单个关键词数据 |
| `xianyu-43keywords-data.json` | JSON | 汇总数据 |
| `xianyu-stats.json` | JSON | 统计信息 |

### 报告文件

| 文件 | 格式 | 内容 |
|------|------|------|
| `xianyu-{keyword}-report.md` | Markdown | 单个关键词报告 |
| `xianyu-43keywords-report.md` | Markdown | 汇总报告 |
| `xianyu-enhanced-final-report.md` | Markdown | 最终报告 |

### Gitee 仓库结构

```
xianyu-data/
├── README.md
├── data/
│   ├── xianyu-43keywords-data.json
│   └── xianyu-stats.json
├── screenshots/
│   └── xianyu-{keyword}.png
└── reports/
    └── xianyu-enhanced-final-report.md
```

---

## 配置说明

### 完整配置项

```json
{
  "gitee": {
    "token": "gitee_token",
    "owner": "username",
    "repo": "xianyu-data"
  },
  "xianyu": {
    "cookie": "cookie_string"
  },
  "grabber": {
    "keywords": ["Magisk", "KernelSU"],
    "screenshotDir": "legion/screenshots",
    "dataDir": "legion/data",
    "uploadToGitee": true,
    "ocrLanguage": "chi_sim+eng"
  }
}
```

### 配置项说明

| 配置项 | 必填 | 说明 |
|--------|------|------|
| `gitee.token` | 否 | Gitee 个人访问令牌 |
| `gitee.owner` | 否 | Gitee 用户名 |
| `gitee.repo` | 否 | Gitee 仓库名 |
| `xianyu.cookie` | 否 | 闲鱼 Cookie（可选） |
| `grabber.keywords` | 否 | 关键词列表 |
| `grabber.uploadToGitee` | 否 | 是否自动上传 |

---

## 关键词库

技能内置 60+ 关键词，分为 10 类：

### ROOT 方案（10 个）
Magisk, 面具，KernelSU, APatch, root 权限，超级用户，系统权限，boot 修补，解锁 BL, lineageos

### 环境隐藏（9 个）
Zygisk, Shamiko, 隐藏环境，LSPosed, Xposed, 隐藏 root, 过检测，环境配置，白名单，面具隐藏

### 救砖服务（10 个）
手机不开机，救砖，卡 LOGO, 基带修复，线刷包，系统修复，无法启动，反复重启，官方固件，900 模式

### 刷机服务（10 个）
刷机，刷 ROM, 第三方 ROM, 类原生，MIUI, ColorOS, Flyme, 系统降级，跨区刷机，解锁 Bootloader

### 游戏优化（10 个）
游戏优化，解锁 120 帧，画质修改，GPU 驱动，游戏助手，性能模式，散热优化，帧率解锁，画质增强，游戏插帧

### 其他（10+ 个）
手机维修，数据恢复，账号解锁，网络解锁，配件改装等

---

## 常见问题

### Q1: 截图显示「非法访问」

**原因**: 反爬虫检测到自动化

**解决**:
1. 更新 Cookie
2. 降低抓取频率
3. 使用真实浏览器 User-Agent

### Q2: OCR 识别结果为空

**原因**: Tesseract 未安装或语言包缺失

**解决**:
```bash
apt-get install tesseract-ocr tesseract-ocr-chi-sim
tesseract --list-langs  # 验证安装
```

### Q3: Gitee 上传失败

**原因**: Token 无效或权限不足

**解决**:
1. 检查 Token 是否有效
2. 确保有 `projects` 权限
3. 仓库需要提前创建

### Q4: Playwright 浏览器启动失败

**原因**: 缺少依赖

**解决**:
```bash
npx playwright install chromium
apt-get install libnss3 libnspr4 libatk1.0-0 \
  libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0
```

---

## 性能优化

### 批量抓取

```bash
# 并行抓取（更快但可能被检测）
./skills/xianyu-data-grabber/run.sh grab --parallel 3

# 串行抓取（更慢但更安全）
./skills/xianyu-data-grabber/run.sh grab --sequential
```

### 缓存机制

- 截图缓存：避免重复抓取
- OCR 缓存：避免重复识别
- 数据缓存：5 分钟有效期

---

## 安全与隐私

### 敏感数据保护

- Cookie 存储在配置文件，权限 600
- Gitee Token 存储在配置文件，权限 600
- 数据文件本地存储，不上传第三方

### 平台合规

- 请求频率：默认 2-4 秒间隔/关键词
- User-Agent：真实浏览器标识
- 数据使用：仅用于个人研究

---

## 更新日志

### v2.0 (2026-03-20)
- ✅ 增强 OCR（图像预处理 + 多模式）
- ✅ 结构化数据提取
- ✅ 60+ 关键词库
- ✅ 统一入口脚本
- ✅ Gitee 自动上传

### v1.0 (2026-03-20)
- 🎉 初始版本
- Playwright + OCR 抓取
- 基础关键词支持

---

## 技术支持

- 技能文档：`skills/xianyu-data-grabber/SKILL.md`
- 使用说明：`skills/xianyu-data-grabber/USAGE.md`
- 示例数据：`legion/data/xianyu-43keywords-data.json`

---

**作者**: 爪爪 🐾  
**日期**: 2026-03-20  
**版本**: 2.0
