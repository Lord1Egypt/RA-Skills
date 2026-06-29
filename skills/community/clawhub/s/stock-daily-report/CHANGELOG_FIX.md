# stock-daily-report v1.0.5 修复说明

## 修复的问题

### 1. 首次安装流程跑不通 ❌ → ✅

**问题原因：**
- 没有自动安装依赖的步骤
- 用户不知道需要安装 matplotlib、pyppeteer
- 中文字体路径硬编码，系统没有该字体时报错

**解决方案：**
- 新增 `install.sh` 自动安装脚本
- 一键安装所有 Python 依赖（matplotlib、pyppeteer）
- 自动检测并安装中文字体（支持 Debian/Ubuntu/CentOS/Arch/macOS）
- 预下载 pyppeteer 所需的 Chromium

**使用方法：**
```bash
cd ~/.openclaw/workspace/skills/stock-daily-report-publish
bash install.sh
```

### 2. 没有输出图片 ❌ → ✅

**问题原因：**
- 默认 `output_format` 是 `"html"` 而不是 `"both"`
- pyppeteer 是可选依赖，首次安装不会自动安装

**解决方案：**
- `config.json` 默认值改为 `"output_format": "both"`
- `install.sh` 自动安装 pyppeteer
- SKILL.md 和 README.md 明确说明如何生成图片

### 3. 没有按照要求的内容输出 ❌ → ✅

**问题原因：**
- 文档不够清晰，用户不知道完整功能

**解决方案：**
- 完善 SKILL.md 和 README.md
- 添加详细的故障排查指南
- 明确说明输出内容包含：
  - 📰 国际新闻 + 国内新闻
  - 🌍 地缘政治风险提示
  - 📊 市场影响概览（油价、黄金、美元指数、人民币）
  - 🎯 个股深度分析（K 线图 + 技术指标 + 操作建议）

## 其他改进

### 字体加载优化
- 支持多个常见字体路径
- 自动检测系统字体
- 如果找不到中文字体，给出明确的安装提示

### 文档完善
- SKILL.md：添加详细的安装步骤和故障排查
- README.md：添加快速开始指南
- 新增 `install.sh`：一键安装所有依赖

## 用户更新步骤

### 已安装用户
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/stock-daily-report-publish

# 拉取最新代码（如果是 git 安装）
git pull

# 或者重新安装
clawhub install stock-daily-report

# 运行安装脚本
bash install.sh
```

### 新用户
```bash
# 安装技能
clawhub install stock-daily-report

# 进入目录并运行安装脚本
cd ~/.openclaw/workspace/skills/stock-daily-report-publish
bash install.sh

# 生成报告
python3 generate_report.py --format both
```

## 测试验证

✅ Python 语法检查通过
✅ 中文字体检测正常
✅ HTML 报告生成正常
✅ 包含所有必需内容（股票数据、技术指标、K 线图、新闻等）

## 版本信息

- **修复版本**: v1.0.5
- **修复日期**: 2026-03-05
- **修复者**: OpenClaw Assistant
