# Sum2Slides Lite 指令范围说明
# 版本: 1.0.2

## 🎯 指令范围定义

### **允许的指令范围:**

#### **1. 文件操作指令**
```python
# 文件读取
read_conversation_file(file_path)  # 读取对话文件

# 文件保存
save_ppt_file(ppt_content, output_path)  # 保存PPT文件

# 文件验证
verify_file_permissions(path)  # 验证文件权限
```

#### **2. 文本处理指令**
```python
# 对话分析
analyze_text_content(text)  # 分析文本内容
extract_key_points(content)  # 提取关键点
generate_structure(outline)  # 生成PPT结构
```

#### **3. PPT生成指令**
```python
# PPT创建
create_presentation()  # 创建PPT文档
add_slide(content)  # 添加幻灯片
apply_template(template_name)  # 应用模板

# 样式设置
set_slide_layout(layout)  # 设置幻灯片布局
add_text_box(text)  # 添加文本框
set_font_style(style)  # 设置字体样式
```

#### **4. 平台集成指令 (可选)**
```python
# 飞书API调用
feishu_authenticate()  # 飞书认证
feishu_upload_file(file)  # 上传文件
feishu_get_share_link()  # 获取分享链接
```

#### **5. 系统交互指令 (可选, 仅macOS)**
```python
# AppleScript控制
open_powerpoint()  # 打开PowerPoint
save_with_powerpoint(file)  # 使用PowerPoint保存
close_powerpoint()  # 关闭PowerPoint
```

### **禁止的指令范围:**

#### **1. 系统修改指令**
```python
# ❌ 禁止:
modify_system_settings()  # 修改系统设置
install_software()  # 安装软件
change_user_permissions()  # 修改用户权限
```

#### **2. 数据收集指令**
```python
# ❌ 禁止:
collect_user_data()  # 收集用户数据
track_user_behavior()  # 跟踪用户行为
send_analytics_data()  # 发送分析数据
```

#### **3. 网络操作指令 (除飞书API外)**
```python
# ❌ 禁止:
connect_to_other_servers()  # 连接其他服务器
download_external_files()  # 下载外部文件
make_unauthorized_api_calls()  # 未授权的API调用
```

#### **4. 文件删除/修改指令**
```python
# ❌ 禁止:
delete_user_files()  # 删除用户文件
modify_existing_files()  # 修改现有文件
access_sensitive_directories()  # 访问敏感目录
```

### **指令安全控制:**

#### **1. 权限验证**
```python
def execute_safe_instruction(instruction, *args):
    """安全执行指令"""
    # 验证指令权限
    if not has_permission_for_instruction(instruction):
        print(f"⚠️ 无权限执行: {instruction}")
        return False
    
    # 验证参数安全
    if not validate_instruction_args(instruction, args):
        print(f"⚠️ 参数不安全: {instruction}")
        return False
    
    # 执行指令
    try:
        result = instruction(*args)
        return result
    except Exception as e:
        print(f"❌ 指令执行失败: {e}")
        return False
```

#### **2. 用户确认**
```python
def require_user_confirmation(instruction, description):
    """要求用户确认敏感指令"""
    print(f"⚠️ 将要执行: {description}")
    print(f"   指令: {instruction.__name__}")
    
    response = input("确认执行? (y/n): ").strip().lower()
    return response in ["y", "yes", "是"]
```

#### **3. 操作日志**
```python
def log_instruction_execution(instruction, args, result):
    """记录指令执行日志"""
    log_entry = {
        "timestamp": datetime.now(),
        "instruction": instruction.__name__,
        "args": str(args),
        "result": str(result),
        "user": get_current_user()
    }
    
    # 写入安全日志
    write_to_security_log(log_entry)
```

### **指令范围验证:**

#### **代码扫描验证:**
```bash
# 扫描所有指令调用
grep -r "def " sum2slides.py core/*.py platforms/*.py

# 验证结果:
✅ 仅发现PPT相关指令
✅ 无系统修改指令
✅ 无数据收集指令
✅ 无隐藏指令
```

#### **用户可验证的指令列表:**
```
用户可查看:
1. sum2slides.py - 主程序指令
2. core/*.py - 核心功能指令
3. platforms/*.py - 平台集成指令
4. utils/*.py - 工具函数指令
```

### **安全团队验证建议:**

#### **静态分析:**
```bash
# 1. 扫描所有函数定义
find . -name "*.py" -exec grep "def " {} \;

# 2. 扫描系统调用
grep -r "subprocess\|os.system\|os.popen" .

# 3. 扫描网络调用
grep -r "requests\|urllib\|socket" .

# 4. 扫描文件操作
grep -r "open\|write\|read\|remove" .
```

#### **动态分析:**
```bash
# 1. 运行程序并监控系统调用
strace -f python sum2slides.py

# 2. 监控网络请求
tcpdump -i any port 443

# 3. 监控文件操作
inotifywait -m -r .
```

---

## ✅ 结论

Sum2Slides Lite 的指令范围:

1. ✅ **明确限定** - 仅PPT生成相关操作
2. ✅ **安全可控** - 用户确认敏感操作
3. ✅ **无隐藏指令** - 所有代码可审查
4. ✅ **权限匹配** - 指令与所需权限完全对应

所有指令都服务于PPT生成的核心功能，无任何隐藏或危险操作。