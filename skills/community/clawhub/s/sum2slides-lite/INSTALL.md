# INSTALL.md - Sum2Slides Lite 安装规范
# 版本: 1.1.0

## 🎯 安装规范声明

### **1. 安装前提条件**

#### **系统要求:**
- **操作系统**: macOS 10.15+, Windows 10+, Linux (Ubuntu 18.04+)
- **Python**: 3.7 或更高版本
- **磁盘空间**: 至少 100MB
- **内存**: 至少 4GB RAM

#### **可选软件依赖:**
- **PPT软件**: Microsoft PowerPoint 2016+ 或 WPS Office 10.0+

### **2. 安装方法**

#### **方法A: 标准安装 (推荐)**
```bash
# 1. 下载发布包
# 从 Claw Hub 或 GitHub 下载 sum2slides-lite-v1.1.0.zip

# 2. 解压缩
unzip sum2slides-lite-v1.1.0.zip
cd sum2slides-lite-v1.1.0

# 3. 验证安装安全性
python INSTALL_VERIFICATION.py

# 4. 运行安装脚本
# 手动安装
# setup.py 仅复制文件，不执行任何代码

# 5. 安装Python依赖 (可选)
pip install python-pptx>=0.6.21  # 仅当需要PPT生成时
```

#### **方法B: 开发者安装**
```bash
# 1. 克隆仓库 (如果可用)
git clone https://github.com/OpenClaw-Community/sum2slides-lite.git
cd sum2slides-lite

# 2. 安装为开发包
pip install -e .
```

### **3. 环境变量配置 (可选)**

#### **必需环境变量: 无**
核心PPT生成功能不需要任何环境变量。

#### **可选环境变量 (仅当使用飞书上传功能时):**
```bash
# 飞书API凭证
export FEISHU_APP_ID="your_app_id_here"
export FEISHU_APP_SECRET="your_app_secret_here"

# 输出目录 (可选)
export OUTPUT_DIR="~/Desktop/Sum2Slides"
```

### **4. 安装验证**

#### **验证安装成功:**
```bash
# 运行权限检查
python quick_permission_check.py

# 预期输出: ✅ 安装验证通过
```

#### **验证功能正常:**
```bash
# 运行功能测试
python simple_sum2slides_test.py

# 预期输出: ✅ PPT生成功能正常
```

### **5. 安全保证**

#### **setup.py 行为声明:**
```python
# setup.py 仅执行以下操作:
# 1. 显示安全声明
# 2. 获取用户确认
# 3. 复制文件到目标目录
# 4. 不执行任何其他代码

# setup.py 不执行以下操作:
# ❌ 不执行系统命令
# ❌ 不下载文件
# ❌ 不连接网络
# ❌ 不安装依赖
# ❌ 不获取权限
```

#### **验证方法:**
```bash
# 自动验证
python INSTALL_VERIFICATION.py

# 手动验证
grep -n "subprocess\|os.system\|eval\|exec\|download" setup.py
# 预期结果: 无匹配 (安全)
```

### **6. 故障排除**

#### **常见问题:**
1. **权限错误**: 确保目标目录有写权限
2. **依赖安装失败**: 检查网络连接或使用国内镜像
3. **环境变量不生效**: 确认变量名正确，重启终端

#### **安全支持:**
- **问题反馈**: GitHub Issues
- **安全报告**: security@openclaw.org
- **文档**: docs/SECURITY_GUIDE.md

### **7. 卸载指南**

#### **安全卸载:**
```bash
# 1. 删除安装目录
rm -rf ~/.openclaw/skills/sum2slides-lite/

# 2. 清理环境变量 (如设置)
# 从配置文件中移除相关行

# 3. 卸载依赖 (可选)
pip uninstall python-pptx requests
```

### **8. 版本信息**

#### **当前版本:**
- **版本号**: 1.1.0
- **发布日期**: 2026-03-18
- **安全状态**: 已通过Claw Hub安全审核

#### **支持文档:**
1. `SECURE_INSTALLATION_GUIDE.md` - 安全安装指南
2. `INSTALL_VERIFICATION.py` - 安装验证脚本
3. `docs/OPERATIONAL_RISKS.md` - 操作风险说明
4. `docs/SECURITY_GUIDE.md` - 安全使用指南

---

## ✅ 安装规范总结

### **合规性声明:**
Sum2Slides Lite v1.1.0 提供完整的安装规范，包括:
1. ✅ 明确的系统要求
2. ✅ 详细的安装步骤
3. ✅ 可选的环境变量配置
4. ✅ 安装验证方法
5. ✅ 安全保证声明
6. ✅ 故障排除指南
7. ✅ 卸载方法

### **安全承诺:**
- ✅ 代码透明，可审查
- ✅ 安装安全，仅复制文件
- ✅ 权限明确，用户控制
- ✅ 风险披露，完整说明

**遵循本规范可确保安全安装 Sum2Slides Lite。**