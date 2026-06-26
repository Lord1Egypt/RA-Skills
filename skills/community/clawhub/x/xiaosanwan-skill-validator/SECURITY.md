# skill-validator 安全加固方案

## 🔴 高风险问题

### 1. 执行外部脚本
**位置**: `scripts/validate.sh:195`

**问题代码**:
```bash
output=$(bash "$SKILL_PATH/scripts/diagnose.sh" 2>&1 | head -5)
```

**风险**: 验证的 skill 可能包含恶意脚本，执行后可能：
- 删除文件
- 窃取数据
- 植入后门

**修复方案**:
```bash
# 方案 A: 使用沙箱容器
run_in_sandbox() {
    local script=$1
    # 使用 firejail 或 docker 隔离执行
    firejail --noprofile --private --timeout=10s bash "$script" 2>&1
}

# 方案 B: 静态分析而非执行
analyze_script() {
    local script=$1
    echo "=== 静态分析 $script ==="
    
    # 检查危险命令
    if grep -E "rm -rf|dd if=|mkfs|:(){ :|:& };:" "$script"; then
        echo "⚠ 发现危险命令"
    fi
    
    # 检查网络请求
    if grep -E "curl|wget|nc " "$script"; then
        echo "⚠ 发现网络请求"
    fi
    
    # 检查权限提升
    if grep -E "sudo|chmod 777|chown root" "$script"; then
        echo "⚠ 发现权限提升"
    fi
}

# 方案 C: 只读模式执行
output=$(bash -n "$SKILL_PATH/scripts/diagnose.sh" 2>&1)  # 语法检查，不执行
```

---

## 🟡 中风险问题

### 2. 空参数测试
**位置**: `scripts/validate.sh:160-170`

**问题**: 执行未知脚本可能触发意外行为

**修复方案**:
```bash
# 添加超时和资源限制
test_empty_params() {
    local script=$1
    
    # 限制执行时间和资源
    ulimit -t 5  # CPU 时间限制 5 秒
    ulimit -f 10000  # 文件大小限制
    
    timeout 3 bash "$script" 2>&1 || {
        local exit_code=$?
        case $exit_code in
            124) echo "⚠ 超时" ;;
            *) echo "退出码: $exit_code" ;;
        esac
    }
}
```

---

## 🛡️ 安全验证增强

### 添加恶意代码检测

```bash
# 在 validate.sh 中添加
check_security() {
    local skill_path=$1
    
    echo "🔒 安全检查..."
    
    # 检查危险模式
    local patterns=(
        "rm -rf /"
        "dd if=/dev/zero"
        ":(){ :|:& };:"  # Fork bomb
        "curl.*|.*bash"
        "wget.*|.*sh"
        "eval.*\\$"
        "base64 -d.*|.*bash"
    )
    
    local found=0
    for pattern in "${patterns[@]}"; do
        if grep -rqE "$pattern" "$skill_path" 2>/dev/null; then
            echo "❌ 发现危险模式: $pattern"
            ((found++))
        fi
    done
    
    if [ $found -gt 0 ]; then
        echo "⚠ 发现 $found 个安全问题，建议人工审核"
        return 1
    else
        echo "✅ 未发现明显安全问题"
        return 0
    fi
}
```

---

## 📋 安全检查清单

- [ ] 使用沙箱/容器隔离执行
- [ ] 添加恶意代码静态分析
- [ ] 设置执行超时限制
- [ ] 限制资源使用（CPU、内存、文件）
- [ ] 记录审计日志
- [ ] 添加用户确认提示

---

## ⚠️ 用户须知

**使用 skill-validator 验证未知 skill 时**：

1. **不要直接执行** - 先静态分析
2. **使用沙箱** - 隔离环境测试
3. **人工审核** - 检查可疑代码
4. **备份数据** - 以防意外

---

*生成时间: 2026-03-19*
