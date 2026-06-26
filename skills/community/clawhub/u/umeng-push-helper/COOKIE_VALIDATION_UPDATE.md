# Cookie 验证逻辑更新说明

## 📋 更新概述

已将 Cookie 验证逻辑从仅检查 `ctoken` 字段升级为同时检查 `ctoken` 和 `umplus_uc_loginid` 两个字段，确保用户已登录友盟账号。

## 🔄 变更详情

### 之前的验证逻辑
```python
def validate_cookie(cookie_value):
    # 只检查 ctoken 字段
    if 'ctoken=' not in cookie_value:
        return False, "Cookie 中未找到 ctoken 字段，可能未登录或已过期"
    # ... 其他验证
```

### 现在的验证逻辑
```python
def validate_cookie(cookie_value):
    # 1. 检查 Cookie 是否为空
    if not cookie_value:
        return False, "Cookie 为空"
    
    # 2. 检查 ctoken 字段（CSRF 令牌）
    if 'ctoken=' not in cookie_value:
        return False, "Cookie 中未找到 ctoken 字段，可能未登录或已过期"
    
    # 3. 检查 umplus_uc_loginid 字段（登录标识）⭐ 新增
    if 'umplus_uc_loginid=' not in cookie_value:
        return False, "Cookie 中未找到 umplus_uc_loginid 字段，需要登录后才能使用。请访问 https://upush.umeng.com 登录"
    
    # 4. 提取并验证 ctoken 长度
    match = re.search(r'ctoken=([^;]+)', cookie_value)
    if not match or len(match.group(1)) < 10:
        return False, "无法从 Cookie 中提取 ctoken 值" or "ctoken 长度异常"
    
    # 5. 提取并显示登录用户 ID
    login_id_match = re.search(r'umplus_uc_loginid=([^;]+)', cookie_value)
    if login_id_match:
        login_id = unquote(login_id_match.group(1).strip())
    
    return True, f"Cookie 验证通过 (用户：{login_id}, ctoken: {ctoken[:10]}...)"
```

## ✅ 新增功能

### 1. 登录状态检测
- **检查字段**: `umplus_uc_loginid`
- **作用**: 确认用户是否已登录友盟账号
- **失败提示**: "Cookie 中未找到 umplus_uc_loginid 字段，需要登录后才能使用。请访问 https://upush.umeng.com 登录"

### 2. 用户 ID 提取
- **新增函数**: `extract_login_id(cookie_value)`
- **返回**: URL 解码后的用户登录 ID
- **用途**: 显示当前登录的用户名

### 3. 增强的验证信息
验证成功时显示：
```
✓ Cookie 验证通过 (用户：鱼鱼鱼 01, ctoken: pIhBS27dsy...)
```

## 📁 更新的文件

### 1. `scripts/manage_cookie.py`
**变更**:
- ✅ 修改 `validate_cookie()` 函数，添加 `umplus_uc_loginid` 检查
- ✅ 新增 `extract_login_id()` 函数
- ✅ 新增命令行命令 `extract-loginid`
- ✅ 导入 `urllib.parse.unquote` 用于 URL 解码

**新增命令**:
```bash
# 从 Cookie 中提取登录用户 ID
python scripts/manage_cookie.py extract-loginid "<cookie_value>"
```

### 2. `scripts/browser_cookie.py`
**变更**:
- ✅ 修改 `validate_cookie()` 函数，添加 `umplus_uc_loginid` 检查

### 3. `scripts/auto_get_cookie.py`
**变更**:
- ✅ 修改 `get_browser_cookie()` 函数，增强错误提示
- ✅ 特殊处理缺少 `umplus_uc_loginid` 的情况，明确提示用户需要登录

**新的错误提示**:
```
✗ 失败：检测到您尚未登录友盟账号。请先访问 https://upush.umeng.com 完成登录，然后重试。
```

### 4. `SKILL.md`
**变更**:
- ✅ 更新 Cookie 验证步骤说明
- ✅ 添加 `umplus_uc_loginid` 字段检查说明

## 🧪 测试用例

### 测试 1: 完整的 Cookie（包含所有必需字段）
```bash
# 加载并验证已保存的 Cookie
python scripts/manage_cookie.py load
python scripts/manage_cookie.py validate "$(python scripts/manage_cookie.py load)"

# 预期输出:
# VALID: Cookie 验证通过 (用户：鱼鱼鱼 01, ctoken: pIhBS27dsy...)
```

### 测试 2: 缺少 umplus_uc_loginid
```bash
python scripts/manage_cookie.py validate "ctoken=test123456; other=value"

# 预期输出:
# INVALID: Cookie 中未找到 umplus_uc_loginid 字段，需要登录后才能使用。请访问 https://upush.umeng.com 登录
```

### 测试 3: 缺少 ctoken
```bash
python scripts/manage_cookie.py validate "umplus_uc_loginid=用户; other=value"

# 预期输出:
# INVALID: Cookie 中未找到 ctoken 字段，可能未登录或已过期
```

### 测试 4: 提取登录用户 ID
```bash
python scripts/manage_cookie.py extract-loginid "$(python scripts/manage_cookie.py load)"

# 预期输出:
# 鱼鱼鱼 01
```

## 📊 验证流程对比

| 验证项 | 旧逻辑 | 新逻辑 |
|--------|--------|--------|
| **Cookie 为空** | ✅ 检查 | ✅ 检查 |
| **ctoken 存在** | ✅ 检查 | ✅ 检查 |
| **ctoken 长度** | ✅ 检查 | ✅ 检查 |
| **umplus_uc_loginid** | ❌ 不检查 | ✅ 检查 ⭐ |
| **显示用户 ID** | ❌ 不显示 | ✅ 显示 ⭐ |
| **登录状态确认** | ❌ 间接推断 | ✅ 直接确认 |

## 🔒 安全增强

### 之前的问题
- 只检查 `ctoken` 无法完全确认用户登录状态
- 可能存在 Cookie 部分有效但用户实际未登录的情况

### 现在的解决方案
1. **双重验证**: 同时检查 `ctoken` 和 `umplus_uc_loginid`
2. **明确提示**: 清晰告知用户需要登录
3. **用户识别**: 显示当前登录的用户名，便于多账号管理

## 💡 使用示例

### 自动获取 Cookie（带登录检测）
```bash
python scripts/auto_get_cookie.py
```

**输出示例 1 - 成功**:
```
============================================================
友盟推送助手 - Cookie 自动获取工具
============================================================

正在打开浏览器访问友盟推送后台...
✓ 页面已加载
正在读取浏览器 Cookie...
正在验证 Cookie...
✓ Cookie 验证通过 (用户：鱼鱼鱼 01, ctoken: pIhBS27dsy...)
✓ Cookie 已保存到：/Users/xxx/.qoderwork/skills/umeng-push-helper/cookie.txt

============================================================
✓ 成功：Cookie 已成功获取并保存
============================================================
```

**输出示例 2 - 未登录**:
```
============================================================
友盟推送助手 - Cookie 自动获取工具
============================================================

正在打开浏览器访问友盟推送后台...
✓ 页面已加载
正在读取浏览器 Cookie...
正在验证 Cookie...
✗ 失败：检测到您尚未登录友盟账号。请先访问 https://upush.umeng.com 完成登录，然后重试。

您可以尝试：
1. 手动登录 https://upush.umeng.com
2. 在浏览器控制台执行：document.cookie
3. 复制输出结果并使用以下命令保存：
   python scripts/manage_cookie.py save "<cookie_value>"
============================================================
```

### 手动保存 Cookie
```bash
python scripts/manage_cookie.py save "完整 cookie 字符串"
```

**输出**:
```
✓ Cookie 已保存到：/Users/xxx/.qoderwork/skills/umeng-push-helper/cookie.txt
✓ 验证：Cookie 验证通过 (用户：鱼鱼鱼 01, ctoken: pIhBS27dsy...)
```

### 验证 Cookie
```bash
python scripts/manage_cookie.py validate "完整 cookie 字符串"
```

**输出**:
```
VALID: Cookie 验证通过 (用户：鱼鱼鱼 01, ctoken: pIhBS27dsy...)
```

### 提取登录用户 ID
```bash
python scripts/manage_cookie.py extract-loginid "完整 cookie 字符串"
```

**输出**:
```
鱼鱼鱼 01
```

## 🎯 影响范围

### 受影响的脚本
- ✅ `manage_cookie.py` - 核心验证逻辑
- ✅ `browser_cookie.py` - Cookie 验证工具
- ✅ `auto_get_cookie.py` - 自动获取脚本
- ✅ `save_cookie.py` - 保存时调用验证
- ✅ 所有调用 API 的脚本（间接影响）

### 不受影响的功能
- ✅ API 调用逻辑
- ✅ Cookie 存储格式
- ✅ 现有应用列表和数据查询功能

## 📝 向后兼容性

### 兼容情况
- ✅ 已保存的 Cookie 仍然有效（只要包含 `umplus_uc_loginid`）
- ✅ 旧的 Cookie 文件格式无需更改
- ✅ 现有命令仍然可用

### 不兼容情况
- ❌ 不包含 `umplus_uc_loginid` 的旧 Cookie 将被视为无效
- ❌ 需要重新登录并获取完整的 Cookie

## 🚀 升级建议

### 对于已安装用户
1. 运行一次自动获取脚本更新 Cookie：
   ```bash
   python scripts/auto_get_cookie.py
   ```

2. 或手动保存新的 Cookie：
   ```bash
   python scripts/manage_cookie.py save "新的 cookie 值"
   ```

### 对于新用户
直接使用自动获取脚本即可，会自动检测登录状态并引导登录。

---

*更新时间：2026-03-31*  
*版本：v1.1.0*
