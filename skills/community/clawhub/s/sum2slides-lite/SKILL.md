---
name: sum2slides-lite
description: 对话总结成专业PPT，支持纯本地处理和可选飞书上传 (v1.1.6)
metadata:
  openclaw:
    requires:
      env: []  # 基础功能不需要环境变量，飞书凭证是可选的
---

# Sum2Slides Lite v1.1.6 - 对话总结成PPT

## 🎯 简介

**Sum2Slides Lite v1.1.6** 是一个智能对话总结成PPT工具，支持纯本地处理和可选飞书上传。

## 🔒 安全使用指南 (ClawHub审查建议整合)

### **📋 安装前必须做:**
1. **检查代码** - 如果可以，审查所有代码文件
2. **运行验证** - 运行 `INSTALL_VERIFICATION.py` 和 `quick_permission_check.py`
3. **安全测试** - 在安全目录运行 `simple_sum2slides_test.py`

### **🔑 飞书凭证安全:**
- **仅设置可信应用** - 只为你信任的飞书应用设置 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- **凭证权限** - 这些凭证允许上传到你的飞书租户
- **谨慎使用** - 如果不信任技能作者，不要设置飞书凭证

### **🌐 网络活动控制:**
- **纯本地模式** - 保持 `feishu.enabled=false` 且不设置 `FEISHU_*` 环境变量
- **无网络活动** - 这样技能将完全在本地运行
- **用户选择** - 你可以选择是否启用飞书上传功能

### **📁 安全安装方法:**
- **手动复制** - 如果不完全信任包作者，使用手动复制/符号链接方法
- **用户控制** - 这样你可以控制何时将文件添加到技能文件夹
- **逐步验证** - 在启用上传功能前逐步验证所有操作

## ✨ 核心功能

### **纯本地处理:**
- ✅ 智能对话分析
- ✅ 专业PPT生成 (PowerPoint/WPS)
- ✅ 多种模板支持
- ✅ 标准 .pptx 格式

### **可选飞书上传:**
- ⚠️ 需要设置 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- ⚠️ 数据会上传到你的飞书租户
- ⚠️ 需要网络连接

## 🚀 快速开始

### **🎯 版本: v1.1.5 (安全审查整合版)**

### **方式A: 纯本地使用 (推荐，最安全)**
```bash
# 1. 解压文件
unzip sum2slides-lite-v1.1.6.zip
cd sum2slides-lite-v1.1.6

# 2. 不设置任何环境变量 (保持纯本地)
# FEISHU_APP_ID 和 FEISHU_APP_SECRET 是可选的，不设置即可禁用网络功能
# 保持 feishu.enabled=false (默认)

# 3. 运行安全验证
python INSTALL_VERIFICATION.py
python quick_permission_check.py

# 4. 测试功能
python simple_sum2slides_test.py

# 5. 安装
mkdir -p ~/.openclaw/skills/sum2slides-lite
cp -r * ~/.openclaw/skills/sum2slides-lite/
```

### **方式B: 飞书上传模式 (需要凭证)**
```bash
# 1. 解压文件
unzip sum2slides-lite-v1.1.6.zip
cd sum2slides-lite-v1.1.6

# 2. 设置可选飞书凭证 (仅当信任时)
export FEISHU_APP_ID="your_trusted_app_id"
export FEISHU_APP_SECRET="your_trusted_app_secret"

# 3. 启用飞书功能
# 编辑 config/config.yaml 设置 feishu.enabled=true

# 4. 运行完整验证
python INSTALL_VERIFICATION.py --full
python quick_permission_check.py
python simple_sum2slides_test.py --feishu-test

# 5. 安装
mkdir -p ~/.openclaw/skills/sum2slides-lite
cp -r * ~/.openclaw/skills/sum2slides-lite/
```

### **方式C: 符号链接 (开发者)**
```bash
# 保持源文件位置，便于更新和审查
ln -s "$(pwd)" ~/.openclaw/skills/sum2slides-lite
```

## ⚙️ 配置说明

### **config/config.yaml 关键设置:**
```yaml
basic:
  output_dir: "~/Desktop/Sum2Slides"  # 输出目录
  default_software: "powerpoint"       # powerpoint 或 wps

feishu:
  enabled: false  # ⚠️ 设置为 true 启用飞书上传
  app_id: ""      # 从环境变量读取
  app_secret: ""  # 从环境变量读取
```

### **🔑 环境变量说明 (重要澄清)**

#### **注册表元数据澄清:**
- **SKILL.md元数据**: 正确标记为 `requires: env: []` (基础功能不需要环境变量)
- **实际使用**: `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是可选的
- **修复问题**: v1.1.6修复了之前版本元数据不一致的问题

#### **环境变量使用:**
```bash
# ⚠️ FEISHU_APP_ID 和 FEISHU_APP_SECRET 是可选的
# 仅当使用飞书上传功能时需要设置
export FEISHU_APP_ID="your_app_id"        # 可选
export FEISHU_APP_SECRET="your_app_secret" # 可选

# 输出目录 (可选)
export OUTPUT_DIR="~/Desktop/Sum2Slides"   # 可选
```

#### **纯本地模式 (推荐):**
```
✅ 不设置 FEISHU_* 环境变量
✅ 保持 feishu.enabled=false
✅ 完全无网络活动
✅ 数据100%在本地
```

## 📊 使用模式

### **模式1: 完全本地 (最安全)**
```
输入 → 本地处理 → 本地PPT文件
```
- ❌ 无网络连接
- ✅ 数据完全在本地
- ✅ 无需API凭证

### **模式2: 飞书上传 (需要信任)**
```
输入 → 本地处理 → 飞书云盘
```
- ✅ 网络连接 (飞书API)
- ⚠️ 数据上传到飞书
- ⚠️ 需要API凭证

## 🔧 验证工具

### **安全验证:**
```bash
# 1. 安装验证
python INSTALL_VERIFICATION.py

# 2. 权限检查
python quick_permission_check.py

# 3. 功能测试
python simple_sum2slides_test.py

# 4. 网络检查 (可选)
grep -r "requests\|urllib" . --include="*.py"
```

### **飞书功能验证:**
```bash
# 仅当启用飞书时运行
python examples/basic_usage.py --feishu-test
```

## 📁 文件说明

### **核心文件:**
- `sum2slides.py` - 主程序
- `core/` - PPT生成核心
- `platforms/feishu/` - 飞书平台集成 (可选)

### **验证工具:**
- `INSTALL_VERIFICATION.py` - 安装验证 (必须运行)
- `quick_permission_check.py` - 权限检查
- `simple_sum2slides_test.py` - 功能测试

### **安全文档:**
- `SECURE_INSTALLATION_GUIDE.md` - 安全使用指南
- `docs/SECURITY_GUIDE.md` - 完整安全指南

## 🤝 支持与反馈

### **安全报告:**
- 发现安全问题立即报告
- 通过官方渠道反馈

### **使用帮助:**
- 参考 `docs/USER_GUIDE.md`
- 查看 `examples/` 目录

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

**Sum2Slides Lite v1.1.5** - 智能对话总结，安全可控

**重要提醒:** 本技能提供两种使用模式，用户可以根据安全需求选择。建议首次使用时选择纯本地模式，熟悉后再考虑是否启用飞书上传功能。
