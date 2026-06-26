# 友盟推送助手 - 使用示例

## 首次使用流程

### 1. 检查登录状态

```bash
cd ~/.qoderwork/skills/umeng-push-helper
python scripts/check_auth.py
```

**输出示例（未登录）：**
```
❌ 未检测到登录信息

📝 请先登录并保存 Cookie:
   1. 访问 https://upush.umeng.com 并登录
   2. 按 F12 打开开发者工具，在 Console 中输入：document.cookie
   3. 复制完整的 Cookie 字符串
   4. 运行：python save_cookie.py "你的 Cookie"
```

### 2. 登录友盟后台

1. 打开浏览器访问：https://upush.umeng.com
2. 输入账号密码登录
3. 登录成功后，按 `F12` 打开开发者工具
4. 切换到 **Console** 标签
5. 输入并执行：`document.cookie`
6. 复制输出的完整 Cookie 字符串

### 3. 保存 Cookie

```bash
python scripts/save_cookie.py "粘贴你复制的 Cookie 字符串"
```

**输出示例（成功）：**
```
✅ Cookie 保存成功!

📦 Cookie (脱敏): UMENG_TOKEN=abcd1234...; PHPSESSID=xyz5678...
🕐 保存时间：2026-03-27T14:30:00.123456
📁 文件路径：/Users/liuxinyuan/.qoderwork/skills/umeng-push-helper/cookie.json
🔒 文件权限：600 (仅所有者可读写)

💡 现在可以使用友盟推送助手功能了
   示例：查询消息详情 uluzms2177451692046001
```

### 4. 验证登录

```bash
python scripts/check_auth.py --verbose
```

**输出示例（已登录）：**
```
✅ 已登录

📦 Cookie (脱敏): UMENG_TOKEN=abcd1234...; PHPSESSID=xyz5678...
🕐 保存时间：2026-03-27T14:30:00.123456
📁 文件路径：/Users/liuxinyuan/.qoderwork/skills/umeng-push-helper/cookie.json
🔒 文件权限：600
```

---

## 日常使用场景

### 场景 1：查询推送消息详情

当用户问："查询消息 uluzms2177451692046001 的内容"

**步骤：**

1. 先检查登录状态
```bash
python scripts/check_auth.py
```

2. 如果已登录，调用 API 查询
```bash
# 注意：实际 API 地址需要根据友盟文档调整
python scripts/api_request.py get_msg_content uluzms2177451692046001
```

或者直接使用 MCP 服务（如已配置）：
```
调用 mcp__test-tool__get_msg_content_by_id 查询消息
```

---

### 场景 2：清除并重新登录

如果 Cookie 过期或需要切换账号：

```bash
# 1. 清除旧 Cookie
python scripts/clear_cookie.py

# 2. 重新登录并保存新 Cookie
python scripts/save_cookie.py "新 Cookie"
```

---

### 场景 3：自定义 API 请求

如果需要调用其他友盟 API：

```bash
# GET 请求
python scripts/api_request.py custom "https://upush.umeng.com/api/stats?date=2026-03-27" GET

# POST 请求
python scripts/api_request.py custom "https://upush.umeng.com/api/send" POST
```

---

## 故障排查

### 问题 1：提示 "Cookie 格式可能不正确"

**原因：** Cookie 字符串不完整或格式错误

**解决：**
1. 确保在登录后立即复制 Cookie
2. 确保复制的是完整的 `document.cookie` 输出
3. 重新登录并保存

### 问题 2：API 返回 401 错误

**原因：** Cookie 已过期

**解决：**
```bash
# 清除旧 Cookie
python scripts/clear_cookie.py

# 重新登录获取新 Cookie
python scripts/save_cookie.py "新 Cookie"
```

### 问题 3：无法访问友盟后台

**原因：** 网络问题或账号权限问题

**解决：**
1. 检查网络连接
2. 确认账号可以正常访问 https://upush.umeng.com
3. 联系管理员确认账号权限

---

## 安全建议

1. **定期更新 Cookie** - 建议每周重新登录一次
2. **不要共享 cookie.json 文件** - 包含敏感认证信息
3. **使用后立即清除** - 在公共电脑上使用后务必运行 `clear_cookie.py`
4. **检查文件权限** - 确保 cookie.json 权限为 600

---

## 脚本说明

| 脚本 | 功能 | 示例 |
|------|------|------|
| `check_auth.py` | 检查登录状态 | `python check_auth.py --verbose` |
| `save_cookie.py` | 保存登录 Cookie | `python save_cookie.py "cookie-string"` |
| `clear_cookie.py` | 清除 Cookie | `python clear_cookie.py` |
| `api_request.py` | 发起 API 请求 | `python api_request.py get_msg_content <id>` |

---

## 注意事项

- Cookie 文件存储在 `~/.qoderwork/skills/umeng-push-helper/cookie.json`
- 所有脚本都需要 Python 3.x 环境
- 首次使用必须先登录并保存 Cookie
- Cookie 有过期时间，过期后需要重新登录
