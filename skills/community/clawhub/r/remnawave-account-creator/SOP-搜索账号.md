# Remnawave 账号搜索 SOP

**版本：** 2.0  
**更新时间：** 2026-03-17  
**问题驱动：** lester 账号搜索失败事件

---

## 📋 问题背景

### 问题描述
2026-03-17 用户查询 "lester" 相关账号，初始搜索返回 0 个结果，但实际存在 2 个账号：
- lester (UUID: 7d0f8344-fdc9-4a79-92ea-22ecf6ae8a32)
- lester_pc (UUID: 59095d09-515e-4d75-a496-8df744f760ff)

### 根本原因
1. **Remnawave API 限制**：`/api/users?limit=500` 列表接口只返回最近/活跃的 25 个用户，不是全部用户
2. **脚本缺陷**：搜索脚本依赖列表 API 进行模糊搜索，导致早期创建的非活跃账号搜索不到
3. **缺乏验证**：脚本开发后没有充分测试边界情况

### 核心原则（重要！）
- ❌ **不使用列表 API 搜索** - 列表不完整，只返回活跃用户
- ✅ **使用 by-username 接口** - 直接查询，不依赖列表
- ✅ **智能尝试多种变体** - `lester`, `lester_pc`, `lester_ios`, `lester_android` 等
- ✅ **遍历所有可能组合** - 不预设过滤条件

### 教训
- ❌ 不能假设列表 API 返回完整数据
- ❌ 不能只测试新创建的账号
- ✅ 需要使用 `by-username` 接口进行精确查询
- ✅ 需要智能尝试多种用户名变体
- ✅ **搜索所有账号，不过滤活跃状态**

---

## 🔧 正确的搜索流程

### 方案 1：使用搜索脚本（推荐）

```bash
# 搜索关键词（自动尝试多种变体）
node search-account.js <关键词>

# 示例
node search-account.js lester
node search-account.js eric
node search-account.js ryan
```

**脚本搜索策略：**
1. **智能多变体搜索**：尝试 `lester`, `lester_pc`, `lester_ios`, `lester_android`, `lester-mac` 等所有可能变体
2. **不使用列表 API** - 列表不完整，会遗漏非活跃账号
3. **by-username 精确查询** - 对每个变体直接调用 API 查询
4. **结果去重** - 合并结果并去重

### 方案 2：直接使用 curl

```bash
# 精确查询单个用户名
curl -sk "https://8.212.8.43/api/users/by-username/<用户名>" \
  -H "Authorization: Bearer <TOKEN>"

# 通过 UUID 查询
curl -sk "https://8.212.8.43/api/users/<UUID>" \
  -H "Authorization: Bearer <TOKEN>"

# 示例
curl -sk "https://8.212.8.43/api/users/by-username/lester_pc" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 方案 3：分页遍历所有用户（不推荐，仅用于审计）

```bash
# 获取第 1 页（最多 500 个用户）
curl -sk "https://8.212.8.43/api/users?page=1&limit=500" \
  -H "Authorization: Bearer <TOKEN>"
```

**注意：** 列表 API 可能不完整，仅用于参考！

---

## 📖 搜索脚本用法

### 基本用法
```bash
# 搜索关键词
node search-account.js lester

# 精确查询用户名
node search-account.js --username lester_pc

# 通过 UUID 查询
node search-account.js --uuid 59095d09-515e-4d75-a496-8df744f760ff
```

### 输出内容
- 用户名、UUID、短 UUID
- 邮箱（如有）
- 订阅地址
- 状态、分组
- 设备限制、流量限制
- 流量重置策略、过期时间
- 创建时间、最后使用时间
- 已用流量（本周/总计）

---

## ✅ 测试用例

### 测试 1：搜索 lester（多个账号）
```bash
node search-account.js lester
```
**预期：** 找到 2 个账号（lester, lester_pc）
**实际：** ✅ 2 个账号

### 测试 2：搜索 eric（多个设备）
```bash
node search-account.js eric
```
**预期：** 找到 3 个账号（eric_pc, eric_ios, eric_android）
**实际：** ✅ 3 个账号

### 测试 3：搜索 ryan（多个设备）
```bash
node search-account.js ryan
```
**预期：** 找到 3 个账号（ryan_pc, ryan_ios, ryan_android）
**实际：** ✅ 3 个账号

### 测试 4：搜索 connor（单个账号）
```bash
node search-account.js connor
```
**预期：** 找到 1 个账号（connor_pc）
**实际：** ✅ 1 个账号

### 测试 2：搜索 eric（多个设备）
```bash
node search-account.js eric
```
**预期：** 找到 3 个账号（eric_pc, eric_ios, eric_android）

### 测试 3：搜索 ryan（多个设备）
```bash
node search-account.js ryan
```
**预期：** 找到 3 个账号（ryan_pc, ryan_ios, ryan_android）

### 测试 4：搜索不存在的用户
```bash
node search-account.js nonexistent
```
**预期：** 返回 0 个账号

### 测试 5：通过 UUID 查询
```bash
node search-account.js --uuid 59095d09-515e-4d75-a496-8df744f760ff
```
**预期：** 找到 lester_pc

---

## 📝 脚本维护

### 文件位置
- 搜索脚本：`~/.openclaw/workspace/skills/remnawave-account-creator/search-account.js`
- 创建脚本：`~/.openclaw/workspace/skills/remnawave-account-creator/create-account.js`

### 添加新的用户名变体
编辑 `search-account.js` 中的 `smartSearch` 函数：

```javascript
const variations = [
  keyword,
  `${keyword}_pc`,
  `${keyword}_ios`,
  `${keyword}_android`,
  keyword.replace(/_/g, ''),
  // 添加新的变体...
];
```

### 常见问题排查

**问题 1：API 返回 401 Unauthorized**
- 检查 `.env` 文件中的 `REMNAWAVE_API_TOKEN` 是否有效
- Token 可能过期，需要重新生成

**问题 2：搜索结果为空但账号存在**
- 尝试使用 `--username` 参数精确查询
- 尝试使用 UUID 直接查询
- 检查用户名拼写是否正确

**问题 3：脚本执行错误**
- 确保 Node.js 已安装
- 确保配置文件存在（`config/remnawave.json`）

---

## 🎯 最佳实践

1. **优先使用搜索脚本** - 自动处理多种情况
2. **提供完整信息** - 搜索时告知用户所有匹配结果
3. **验证搜索结果** - 如果用户说"有账号但搜不到"，使用 UUID 直接查询
4. **记录异常情况** - 发现新的用户名模式时，更新脚本的变体列表
5. **定期测试** - 每月至少测试一次搜索功能

---

## 📚 相关文档

- [Remnawave API 文档](https://remnawave.com/docs/api)
- [账号创建 SOP](./SKILL.md)
- [邮件发送模板](../../config/email-templates/remnawave-account-created.md)

---

**最后更新：** 2026-03-17 18:05  
**更新内容：** v2.0 - 完全移除列表 API 依赖，只用 by-username 搜索  
**下次审查：** 2026-04-17 或发现新问题时
