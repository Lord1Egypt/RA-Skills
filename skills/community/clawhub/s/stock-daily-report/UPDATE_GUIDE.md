# 📢 stock-daily-report v1.0.5 更新公告

## ⚠️ 重要修复

v1.0.5 版本修复了以下严重问题：

1. **首次安装流程跑不通** - 新增自动安装脚本
2. **没有输出图片** - 默认改为 HTML+ 图片双输出
3. **文档不完善** - 完善安装说明和故障排查

## 🔧 已安装用户如何更新

### 方式 1：手动更新（推荐）

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/stock-daily-report-publish

# 2. 备份配置文件（如果已自定义）
cp config.json config.json.bak

# 3. 从 ClawHub 重新安装
clawhub install stock-daily-report --force

# 4. 恢复配置文件
cp config.json.bak config.json

# 5. 运行安装脚本
bash install.sh
```

### 方式 2：Git 更新（如果是 git 安装）

```bash
cd ~/.openclaw/workspace/skills/stock-daily-report-publish
git pull
bash install.sh
```

## 🎯 新用户如何安装

```bash
# 1. 安装技能
clawhub install stock-daily-report

# 2. 进入目录
cd ~/.openclaw/workspace/skills/stock-daily-report-publish

# 3. 运行自动安装脚本（一键安装所有依赖）
bash install.sh

# 4. 生成报告
python3 generate_report.py --format both
```

## ✨ v1.0.5 新增功能

### 1. 自动安装脚本 `install.sh`

一键安装所有依赖：
- ✅ Python 依赖：matplotlib、pyppeteer
- ✅ 系统字体：Noto Sans CJK
- ✅ 预下载 Chromium（用于图片生成）

**使用方法：**
```bash
bash install.sh
```

### 2. 智能字体检测

支持多个常见字体路径，自动检测系统字体：
- `/usr/share/fonts/google-noto-cjk/`
- `/usr/share/fonts/noto-cjk/`
- `/usr/share/fonts/opentype/noto-cjk/`
- macOS 系统字体
- Windows 系统字体

如果未找到中文字体，会给出明确的安装提示。

### 3. 默认输出 HTML + 图片

`config.json` 默认配置改为：
```json
{
  "output_format": "both"
}
```

现在默认同时生成 HTML 和 PNG 长图。

### 4. 完善文档

- SKILL.md：详细安装步骤 + 故障排查
- README.md：快速开始指南
- CHANGELOG_FIX.md：修复说明

## 📋 输出内容说明

生成的报告包含：

### 市场概览
- 📰 国际新闻（2 条）
- 📋 国内新闻（2 条）
- 🌍 地缘政治风险提示
- 📊 市场影响（油价、黄金、美元指数、人民币）

### 个股分析（每只股票）
- 📈 K 线图（蜡烛图 + 均线 + 支撑/压力位）
- 📊 技术指标（KDJ、MACD、量比、换手率、振幅）
- 🔍 K 线形态分析
- 💡 操作建议（评级、目标价、止损价、仓位）

## 🐛 常见问题

### Q: 更新后还是旧版本？
A: 使用 `--force` 参数强制重新安装：
```bash
clawhub install stock-daily-report --force
```

### Q: install.sh 执行失败？
A: 确保脚本有执行权限：
```bash
chmod +x install.sh
bash install.sh
```

### Q: 图片生成失败？
A: 检查是否安装了 pyppeteer 和中文字体：
```bash
pip3 install pyppeteer --user
sudo apt install fonts-noto-cjk  # Debian/Ubuntu
```

### Q: 如何验证版本？
A: 查看 _meta.json：
```bash
cat ~/.openclaw/workspace/skills/stock-daily-report-publish/_meta.json | grep version
```

应该显示 `"version": "1.0.5"`

## 📞 反馈

如有问题，请在 ClawHub 上联系作者 **bo170814** 或提交 issue。

---

**版本**: v1.0.5  
**发布日期**: 2026-03-05  
**作者**: bo170814
