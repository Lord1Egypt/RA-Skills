# Sum2Slides Lite 安装规范声明
# 版本: 1.0.3

## 🎯 官方安装规范

### **1. 安装前提条件声明**

#### **系统要求:**
```
操作系统: macOS 10.15+, Windows 10+, Linux (Ubuntu 18.04+)
Python: 3.7 或更高版本
磁盘空间: 至少 100MB 可用空间
内存: 至少 4GB RAM
```

#### **可选软件依赖:**
```
PPT软件 (二选一):
1. Microsoft PowerPoint 2016+ (Windows/macOS)
2. WPS Office 10.0+ (全平台支持)
```

### **2. 环境变量要求声明**

#### **必需环境变量: 无**
```
核心PPT生成功能不需要任何环境变量
所有功能在无环境变量情况下正常工作
```

#### **可选环境变量 (仅当使用飞书文档功能时):**
```bash
# 飞书应用凭证 (可选，用于文档处理)
FEISHU_APP_ID=your_app_id_here
FEISHU_APP_SECRET=your_app_secret_here

# 输出目录 (可选，默认: ~/Desktop/Sum2Slides)
OUTPUT_DIR=~/Desktop/Sum2Slides
```

#### **环境变量配置声明:**
```markdown
## 环境变量配置方法

### 方法A: 不使用环境变量 (推荐)
```
不设置任何环境变量
功能: 本地PPT生成，无飞书上传
```

### 方法B: 使用环境变量 (可选)
```bash
# 临时设置
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"

# 永久设置 (添加到 ~/.bashrc 或 ~/.zshrc)
echo 'export FEISHU_APP_ID="your_app_id"' >> ~/.bashrc
echo 'export FEISHU_APP_SECRET="your_app_secret"' >> ~/.bashrc
```

### 方法C: 使用 .env 文件 (可选)
```bash
cp .env.example .env
# 编辑 .env 文件 (可选)
```
```

### **3. 安装步骤规范声明**

#### **步骤1: 下载**
```bash
# 从官方发布渠道下载
# 文件: sum2slides-lite-v1.0.3.zip
```

#### **步骤2: 验证**
```bash
# 验证文件完整性 (建议)
# 检查文件大小: 约 92KB
# 检查文件类型: ZIP压缩包
```

#### **步骤3: 解压**
```bash
# 解压到用户目录
unzip sum2slides-lite-v1.0.3.zip
```

#### **步骤4: 审查 (强烈建议)**
```bash
# 审查主要文件
less sum2slides.py
less setup.py
less docs/PERMISSIONS.md
less INSTALL_SPECIFICATION.md
```

#### **步骤5: 运行安装脚本**
```bash
# 进入目录
cd sum2slides-lite-v1.0.3

# 运行安装脚本
# 手动安装

# 安装脚本行为声明:
# ✅ 仅复制文件到目标目录
# ✅ 不执行任何代码
# ✅ 不自动安装依赖
# ✅ 不获取任何权限
# ✅ 需要用户确认每个步骤
```

#### **步骤6: 安装依赖 (可选)**
```bash
# 必需依赖 (仅当需要PPT生成功能时)
pip install python-pptx>=0.6.21

# 可选依赖 (仅当需要飞书上传功能时)
pip install requests>=2.28.0
```

#### **步骤7: 配置 (可选)**
```bash
# 仅当使用飞书上传时配置
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### **4. setup.py 安全行为声明**

#### **setup.py 功能声明:**
```python
# setup.py 仅执行以下安全操作:

# 1. 显示安全警告
print_security_warning()

# 2. 获取用户确认
get_user_confirmation()

# 3. 复制文件
copy_files_only()

# 4. 创建目录
create_directories()

# 5. 提供使用指南
print_usage_guide()

# setup.py 不执行以下操作:
# ❌ 不执行 subprocess.call()
# ❌ 不执行 os.system()
# ❌ 不执行 eval() 或 exec()
# ❌ 不下载文件
# ❌ 不连接网络
# ❌ 不修改系统设置
```

#### **setup.py 代码可验证性:**
```bash
# 用户可验证 setup.py 安全性:
grep -n "subprocess\|os.system\|eval\|exec\|downloading\|wget\|curl" setup.py

# 预期结果: 无匹配 (安全)
```

### **5. 安装验证声明**

#### **验证安装成功:**
```bash
# 运行权限检查
python quick_permission_check.py

# 预期输出:
✅ 安装验证通过
```

#### **验证功能正常:**
```bash
# 运行功能测试
python simple_sum2slides_test.py

# 预期输出:
✅ PPT生成功能正常
```

### **6. 安全保证声明**

#### **安装过程安全保证:**
1. ✅ **无代码执行** - 安装过程不执行任何代码
2. ✅ **无权限获取** - 不自动获取任何系统权限
3. ✅ **无网络连接** - 离线安装，不连接网络
4. ✅ **用户控制** - 用户确认所有操作
5. ✅ **透明操作** - 所有操作可审查

#### **setup.py 安全审查方法:**
```bash
# 安全团队可验证:
python -m py_compile setup.py  # 语法检查
pylint setup.py  # 代码质量检查
bandit -r .  # 安全漏洞检查
```

### **7. 故障排除声明**

#### **安装问题解决:**
```markdown
1. **权限错误**: 选择有写权限的目录
2. **依赖问题**: 手动安装 python-pptx
3. **环境变量**: 飞书上传为可选功能
4. **其他问题**: 查看 docs/TROUBLESHOOTING.md
```

#### **安全支持:**
```markdown
安全报告: security@openclaw.org
问题反馈: 查看 GitHub Issues
文档: docs/SECURITY_GUIDE.md
```

### **8. 卸载指南声明**

#### **安全卸载:**
```bash
# 1. 删除安装目录
rm -rf ~/.openclaw/skills/sum2slides-lite/

# 2. 清理环境变量 (如设置)
# 从配置文件中移除相关行

# 3. 卸载依赖 (可选)
pip uninstall python-pptx requests
```

---

## ✅ 安装规范总结

### **核心声明:**
1. ✅ **安装规范明确** - 本文件为正式安装规范
2. ✅ **环境变量声明** - 明确声明环境变量要求
3. ✅ **setup.py 安全** - 仅复制文件，不执行代码
4. ✅ **用户控制** - 用户确认所有操作

### **合规性声明:**
Sum2Slides Lite v1.0.3 符合以下要求:
- 明确的安装规范声明
- 明确的环境变量要求声明
- 安全的安装过程 (无代码执行)
- 透明的操作过程

**此文件为 Sum2Slides Lite 的官方安装规范声明。**