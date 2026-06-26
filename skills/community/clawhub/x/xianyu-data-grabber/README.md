# 🐾 闲鱼数据抓取技能

使用 Playwright + OCR 技术突破闲鱼反爬虫，自动上传数据到 Gitee 仓库。

## 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip3 install pillow pytesseract --break-system-packages

# Tesseract OCR
apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Node 依赖（已有）
npm install playwright
```

### 2. 配置 Gitee

创建 `~/.openclaw/workspace/.xianyu-grabber-config.json`:

```json
{
  "gitee": {
    "token": "你的 Gitee 个人访问令牌",
    "owner": "你的 Gitee 用户名",
    "repo": "xianyu-data"
  },
  "xianyu": {
    "cookie": "你的闲鱼 Cookie（可选）"
  },
  "grabber": {
    "keywords": ["Magisk", "KernelSU", "手机维修"],
    "uploadToGitee": true
  }
}
```

**获取 Gitee Token**:
1. 登录 https://gitee.com
2. 设置 → 个人访问令牌
3. 创建新令牌（勾选 `projects` 权限）

### 3. 使用技能

```bash
# 抓取单个关键词
node skills/xianyu-data-grabber/grabber.js "Magisk"

# 抓取多个关键词
node skills/xianyu-data-grabber/grabber.js "Magisk" "KernelSU" "root"

# 使用配置文件
node skills/xianyu-data-grabber/grabber.js --config
```

### 4. 查看结果

- 截图：`legion/screenshots/xianyu-{keyword}.png`
- 数据：`legion/data/xianyu-full-data.json`
- 报告：`legion/data/xianyu-summary.md`
- Gitee: https://gitee.com/{owner}/{repo}

## 文件说明

| 文件 | 功能 |
|------|------|
| `SKILL.md` | 技能文档 |
| `grabber.js` | 主抓取脚本 |
| `ocr.py` | OCR 识别脚本 |
| `uploader.sh` | Gitee 上传脚本 |
| `README.md` | 使用说明 |

## 已有数据

当前仓库已有 283 个商品数据（15 个关键词）：

- `legion/xianyu-full-data.json` - 完整数据
- `legion/xianyu-final-report.md` - 分析报告
- `legion/screenshots/` - 截图文件

可以直接上传到 Gitee：

```bash
bash skills/xianyu-data-grabber/uploader.sh legion/data legion/xianyu-final-report.md
```

## 注意事项

1. **Cookie 有效期**: 闲鱼 Cookie 约 7 天，需定期更新
2. **请求频率**: 默认 5 秒间隔，避免被封
3. **Gitee 仓库**: 需要提前创建（公开或私有均可）
4. **磁盘空间**: 截图较大，注意清理

## 扩展功能

- [ ] 支持更多电商平台（淘宝/拼多多）
- [ ] 自动价格监控
- [ ] 竞品对比分析
- [ ] 定时自动抓取

---

**作者**: 爪爪 🐾  
**版本**: 1.0.0  
**日期**: 2026-03-20
