# 友盟推送助手 - Cookie 获取方式更新说明

## 📋 更新概述

已将友盟推送助手的 Cookie 获取逻辑从**手动输入**改为**浏览器自动读取**。

## 🔄 主要变更

### 之前的流程（手动）
1. 用户手动访问友盟后台
2. 打开开发者工具
3. 查找并复制 Cookie
4. 将 Cookie 提供给助手保存

### 现在的流程（自动）⭐
1. 助手自动打开浏览器访问友盟后台
2. 自动读取页面 Cookie
3. 自动验证 Cookie 是否包含 `ctoken` 字段
4. 自动保存有效的 Cookie

## 📁 新增文件

### 1. `scripts/auto_get_cookie.py`
主脚本，实现完整的自动化流程：
- 使用 MCP 浏览器工具访问页面
- 执行 JavaScript 读取 Cookie
- 验证 Cookie 有效性
- 保存 Cookie 到本地文件

### 2. `scripts/browser_cookie.py`
Cookie 验证工具：
- 验证 Cookie 格式
- 检查 `ctoken` 字段
- 提取 ctoken 值

### 3. 更新 `scripts/manage_cookie.py`
增强 Cookie 管理功能：
- 添加 `validate` 命令 - 验证 Cookie
- 添加 `extract-ctoken` 命令 - 提取 ctoken
- 改进 `save` 命令 - 保存前自动验证

## 📖 更新的文档

### 1. `SKILL.md`
- 重写 Cookie 管理章节
- 添加自动获取步骤说明
- 保留手动获取作为备用方案
- 更新相关文件列表

### 2. `README.md`
- 添加自动获取方法说明
- 标注为推荐方式
- 更新目录结构
- 添加常见问题解答

## 🔧 使用方法

### 自动获取 Cookie（推荐）

```bash
cd ~/.qoderwork/skills/umeng-push-helper
python scripts/auto_get_cookie.py
```

脚本会：
1. ✅ 打开浏览器访问 https://upush.umeng.com/apps/list
2. ✅ 等待页面加载完成
3. ✅ 执行 `document.cookie` 读取 Cookie
4. ✅ 检查是否包含 `ctoken=` 字段
5. ✅ 验证通过后保存到 `cookie.txt`

### 手动管理 Cookie

```bash
# 保存 Cookie（自动验证）
python scripts/manage_cookie.py save "<cookie_value>"

# 验证 Cookie
python scripts/manage_cookie.py validate "<cookie_value>"

# 提取 ctoken
python scripts/manage_cookie.py extract-ctoken "<cookie_value>"

# 加载已保存的 Cookie
python scripts/manage_cookie.py load

# 检查 Cookie 是否存在
python scripts/manage_cookie.py check
```

## ✨ 优势对比

| 特性 | 旧方式（手动） | 新方式（自动） |
|------|--------------|--------------|
| **操作步骤** | 4+ 步手动操作 | 0 步，全自动 |
| **技术门槛** | 需要了解开发者工具 | 无需任何技术知识 |
| **错误率** | 容易复制错误 | 自动验证，零错误 |
| **ctoken 检查** | 不检查 | 自动检查 |
| **用户体验** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🔒 安全特性

1. **自动验证**：保存前验证 Cookie 有效性
2. **ctoken 检查**：确保包含必需的 CSRF 令牌
3. **长度验证**：检查 ctoken 长度 >= 10
4. **本地存储**：Cookie 仅保存在本地文件

## 🐛 错误处理

### Cookie 无效
```
✗ 验证失败：Cookie 中未找到 ctoken 字段，可能未登录或已过期
```
解决方案：提示用户重新登录

### Cookie 损坏
```
✗ 验证失败：ctoken 长度异常，可能已损坏
```
解决方案：提示用户重新获取

### 浏览器访问失败
```
✗ 失败：操作超时，请重试
```
解决方案：检查网络连接后重试

## 📝 示例输出

### 成功获取
```
============================================================
友盟推送助手 - Cookie 自动获取工具
============================================================

正在打开浏览器访问友盟推送后台...
✓ 页面已加载
正在读取浏览器 Cookie...
正在验证 Cookie...
✓ Cookie 验证通过 (ctoken: pIhBS27dsy...)
✓ Cookie 已保存到：/Users/xxx/.qoderwork/skills/umeng-push-helper/cookie.txt

============================================================
✓ 成功：Cookie 已成功获取并保存

Cookie 已保存到：/Users/xxx/.qoderwork/skills/umeng-push-helper/cookie.txt

您现在可以使用以下命令：
  python scripts/get_app_list.py     - 获取应用列表
  python scripts/query_app_data.py <appkey> - 查询应用数据
============================================================
```

### 失败情况
```
============================================================
✗ 失败：Cookie 验证失败：Cookie 中未找到 ctoken 字段，可能未登录或已过期

您可以尝试：
1. 手动登录 https://upush.umeng.com
2. 在浏览器控制台执行：document.cookie
3. 复制输出结果并使用以下命令保存：
   python scripts/manage_cookie.py save "<cookie_value>"
============================================================
```

## 🎯 后续计划

1. **定期自动刷新**：检测 Cookie 过期时间，提前提醒
2. **多账号支持**：支持保存多个账号的 Cookie
3. **Cookie 加密**：对保存的 Cookie 进行加密存储
4. **图形界面**：提供简单的 GUI 界面

## 📞 技术支持

如有问题，请查看：
- 技能文档：`~/.qoderwork/skills/umeng-push-helper/SKILL.md`
- 使用说明：`~/.qoderwork/skills/umeng-push-helper/README.md`
- 友盟官方文档：https://developer.umeng.com

---

*更新时间：2026-03-31*
