# Sum2Slides Lite 安装机制说明
# 版本: 1.0.2

## 🎯 安装机制设计原则

### **核心原则:**
```
1. 最小权限 - 安装过程不需要特殊权限
2. 透明操作 - 所有操作对用户可见
3. 用户控制 - 用户控制每个步骤
4. 安全审查 - 安装前可审查所有代码
```

## 📋 安装流程详细说明

### **步骤1: 文件解压 (用户操作)**
```bash
# 用户手动解压
unzip sum2slides-lite-v1.0.2.zip

# 安全特性:
✅ 用户控制解压位置
✅ 可审查所有文件
✅ 无自动执行
```

### **步骤2: 代码审查 (建议)**
```bash
# 用户可审查代码
cat sum2slides.py
cat setup.py
cat config/config.yaml

# 安全特性:
✅ 鼓励安装前审查
✅ 所有代码可读
✅ 无隐藏文件
```

### **步骤3: 运行安装脚本**
```python
# setup.py 安全设计:
def safe_installation():
    """安全安装流程"""
    # 1. 显示安全警告
    print_security_warning()
    
    # 2. 获取用户确认
    if not get_user_confirmation():
        return False
    
    # 3. 仅复制文件 (不执行代码)
    copy_files_only()
    
    # 4. 提供安全指南
    print_safety_guide()
    
    return True
```

### **步骤4: 手动安装依赖**
```bash
# 用户手动安装依赖
pip install python-pptx>=0.6.21

# 可选依赖 (用户决定)
pip install requests>=2.28.0  # 仅当需要飞书上传时

# 安全特性:
✅ 用户控制依赖安装
✅ 可审查依赖包
✅ 无自动安装
```

### **步骤5: 安全配置**
```bash
# 用户手动配置
cp .env.example .env
# 编辑 .env 文件 (可选)

# 安全特性:
✅ 用户控制配置
✅ 敏感信息不硬编码
✅ 配置可审查
```

## 🔒 安装机制安全特性

### **1. 无代码执行**
```python
# setup.py 关键代码:
def copy_files_only():
    """仅复制文件，不执行任何代码"""
    import shutil
    import os
    
    # 仅文件复制操作
    shutil.copy(source, destination)
    
    # 无以下操作:
    # ❌ subprocess.call() - 不执行系统命令
    # ❌ eval() - 不执行动态代码
    # ❌ exec() - 不执行外部代码
    # ❌ os.system() - 不调用系统命令
```

### **2. 无权限获取**
```python
# 安装过程不请求任何权限:
def no_permission_requests():
    """无权限请求"""
    # 不请求:
    # ❌ 文件系统权限
    # ❌ 网络权限  
    # ❌ AppleScript权限
    # ❌ 系统权限
    
    # 所有权限在运行时按需请求
    # 用户可随时拒绝
```

### **3. 完全透明**
```python
def transparent_operations():
    """透明操作记录"""
    # 记录所有操作
    operations_log = []
    
    # 记录文件复制
    operations_log.append(f"复制: {source} → {destination}")
    
    # 记录目录创建
    operations_log.append(f"创建目录: {dir_path}")
    
    # 保存操作日志
    save_operations_log(operations_log)
```

### **4. 用户确认**
```python
def require_confirmation_for_all_steps():
    """所有步骤都需要用户确认"""
    confirmations = [
        ("安装位置确认", "确认安装目录"),
        ("文件复制确认", "确认复制文件"),
        ("配置确认", "确认配置文件"),
        ("风险确认", "确认了解风险")
    ]
    
    for step, message in confirmations:
        if not get_user_confirmation(step, message):
            return False
    
    return True
```

## 📊 安装机制验证

### **静态代码分析:**
```bash
# 检查setup.py的安全性
grep -n "subprocess\|os.system\|eval\|exec" setup.py

# 预期结果: 无匹配 (安全)
```

### **操作监控验证:**
```bash
# 监控安装过程
strace -f # 手动安装 2>&1 | grep -E "(execve|open|write)"

# 预期结果: 仅文件操作，无代码执行
```

### **权限监控验证:**
```bash
# 监控权限请求
dtruss # 手动安装 2>&1 | grep -E "(sandbox|entitlement|permission)"

# 预期结果: 无权限请求
```

### **网络监控验证:**
```bash
# 监控网络连接
tcpdump -i any -n port not 22 2>&1 | grep -E "(SYN|ACK)"

# 预期结果: 无网络连接 (离线安装)
```

## ⚠️ 安装风险与缓解

### **潜在风险1: 恶意文件替换**
**风险**: 安装过程中文件被恶意替换
**缓解**: 
```python
def verify_file_integrity():
    """验证文件完整性"""
    # 计算文件哈希
    expected_hash = "abc123..."
    actual_hash = calculate_file_hash(file_path)
    
    if expected_hash != actual_hash:
        print("⚠️ 文件完整性验证失败")
        return False
    
    return True
```

### **潜在风险2: 目录遍历攻击**
**风险**: 安装到系统敏感目录
**缓解**: 
```python
def validate_installation_path(path):
    """验证安装路径安全性"""
    sensitive_dirs = [
        "/System", "/etc", "/usr/bin",
        "/bin", "/sbin", "/var"
    ]
    
    for sensitive_dir in sensitive_dirs:
        if path.startswith(sensitive_dir):
            print(f"❌ 禁止安装到系统目录: {sensitive_dir}")
            return False
    
    return True
```

### **潜在风险3: 依赖包风险**
**风险**: 恶意依赖包
**缓解**: 
```python
def verify_dependencies():
    """验证依赖包安全性"""
    safe_dependencies = {
        "python-pptx": "知名PPT生成库",
        "requests": "知名HTTP库"
    }
    
    for dep in dependencies:
        if dep not in safe_dependencies:
            print(f"⚠️ 未知依赖: {dep}")
            return False
    
    return True
```

## 🛡️ 安全安装指南

### **用户应该:**
```markdown
1. 🔍 审查代码 - 安装前查看所有源代码
2. 📁 选择安全目录 - 安装到用户目录
3. 🔒 控制权限 - 只授予必要权限
4. 📊 监控安装 - 注意安装过程中的操作
5. 🧪 测试功能 - 安装后测试基本功能
```

### **开发者承诺:**
```markdown
1. ✅ 无隐藏操作 - 所有代码可审查
2. ✅ 无自动执行 - 不执行任何代码
3. ✅ 无权限请求 - 不自动获取权限
4. ✅ 无网络连接 - 离线安装
5. ✅ 完全透明 - 记录所有操作
```

## 🔍 安全团队验证建议

### **验证方法:**
```bash
# 1. 分析setup.py代码
python -m py_compile setup.py  # 语法检查
pylint setup.py  # 代码质量检查

# 2. 监控安装过程
strace -f -e trace=file,process # 手动安装

# 3. 检查权限请求
codesign -d --entitlements - setup.py

# 4. 验证文件完整性
shasum -a 256 setup.py
```

### **预期结果:**
```
✅ setup.py 仅包含文件复制操作
✅ 无系统命令执行
✅ 无权限请求
✅ 无网络连接
✅ 完全透明可审计
```

---

## ✅ 结论

Sum2Slides Lite 的安装机制:

1. ✅ **安全设计** - 仅复制文件，不执行代码
2. ✅ **权限控制** - 不自动获取任何权限
3. ✅ **透明操作** - 所有操作可审查
4. ✅ **用户控制** - 用户确认每个步骤
5. ✅ **离线安装** - 无需网络连接

安装过程完全安全可控，用户可放心使用。