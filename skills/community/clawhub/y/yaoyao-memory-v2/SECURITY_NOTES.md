# 安全说明

## 功能概述

### 本地存储
- 记忆存储在 `~/.openclaw/workspace/memory/`
- 向量数据库在 `~/.openclaw/memory-tdai/vectors.db`

### 可选功能
- 云同步（需配置凭证）
- HTTP API（需认证）
- 自动更新（默认禁用）

## 安全设计

### 凭证处理
- 凭证由用户管理
- 存储在用户指定位置
- 不自动获取

### 代码执行
- Shell 执行用于文件管理
- 不执行用户提供的外部命令

---

## 扫描误报说明

### 检测代码说明

部分杀软和平台扫描会检测到以下代码：

**1. 提示注入检测正则**
```python
# skills_guard.py - 安全检测模块
(r'ignore\s+(previous|all|above|prior)\s+instructions', 'prompt_injection'),
```

**2. 危险命令检测列表**
```python
# governance.py - 内容安全检测
DANGER_KEYWORDS = ['rm -rf', 'eval(', 'exec(', ...]
```

**3. 脚本安全扫描**
```python
# install_modules.py - 安装前扫描
dangerous_patterns = ['eval(', 'exec(', 'subprocess.run', ...]
```

这些是**安全检测代码**，不是真正的危险代码：

| 类型 | 用途 | 是否危险 |
|------|------|----------|
| 正则表达式 | 检测提示注入 | ❌ 安全 |
| 关键词列表 | 扫描恶意内容 | ❌ 安全 |
| 模式匹配 | 验证脚本安全 | ❌ 安全 |

### 为什么会被标记？

杀软的静态分析基于字符串匹配，无法区分：
- ❌ `eval(user_input)` - 真正执行
- ✅ `'eval('` - 检测模式字符串

### 如何验证安全？

审查方法：
1. 检查这些代码是否在**执行**敏感操作
2. 还是在**检测/扫描**危险模式

**执行代码示例**（危险）：
```python
eval(user_input)  # 执行用户输入
```

**检测代码示例**（安全）：
```python
if 'eval(' in user_input:  # 检测危险模式
    block()
```

---

## 审核建议

如需完全确认安全，请检查：

1. **skills_guard.py** - 是否只检测不执行
2. **governance.py** - 是否是模式列表而非执行代码
3. **install_modules.py** - 是否在安装前扫描而非直接执行

---

*最后更新：2026-04-12*
