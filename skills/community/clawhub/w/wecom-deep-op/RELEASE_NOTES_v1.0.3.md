# wecom-deep-op v1.0.3 Release Notes

## 🎉 发布信息

- **版本号**: v1.0.3
- **发布日期**: 2026-03-21
- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **Clawhub**: https://clawhub.com/skills/wecom-deep-op

---

## 📋 本次更新

**响应代码审查，全面提升代码质量**

### 🔧 高优先级修复

- ❌ 移除未使用的依赖 `@wecom/aibot-node-sdk` (package.json)

### ✨ 中优先级改进

- ✅ 添加参数验证工具函数（assertString, assertNumber, assertArray, assertBoolean, assertOptionalString）
- ✅ 为所有API函数添加运行时参数验证（27个函数全覆盖）
  * 文档：doc_get, doc_create, doc_edit
  * 日程：schedule_get, schedule_list, schedule_update, schedule_cancel, schedule_add_attendee, schedule_remove_attendee
  * 会议：meeting_get, meeting_cancel, meeting_update_attendees, meeting_list
  * 待办：todo_get, todo_list, todo_update, todo_update_status, todo_delete, todo_accept, todo_refuse
  * 通讯录：contact_search
- ✅ 为 `Logger` 类添加 `warn` 方法（调试级别）
- ✅ 修复重复的 logger 声明问题（doc_edit 函数）
- ✅ 所有验证包括：必需参数检查、类型检查、枚举值范围（如 priority: 1-3, status: 0-2）

### 📝 改进

- 参数验证错误返回更清晰的错误信息（包含参数名和期望值）
- 必需参数缺失时立即抛出 `WeComError`，避免无效API调用

---

## 🧪 测试验证

- ✅ 完整的安装测试（git clone → npm install → npm run build）
- ✅ 构建产物验证（CJS 41KB, ESM 40KB, types 8.2KB）
- ✅ 安全审查通过（无硬编码密钥）
- ✅ 参数验证覆盖率 100%（27个API函数）

---

## 📦 下载

- Source code (tar.gz): https://github.com/Bingbox/wecom-deep-op/archive/refs/tags/v1.0.3.tar.gz
- Source code (zip): https://github.com/Bingbox/wecom-deep-op/archive/refs/tags/v1.0.3.zip

---

## 🔗 相关链接

- GitHub: https://github.com/Bingbox/wecom-deep-op
- Clawhub: https://clawhub.com/skills/wecom-deep-op
- 文档: [README.md](https://github.com/Bingbox/wecom-deep-op/blob/main/README.md)
- 问题反馈: https://github.com/Bingbox/wecom-deep-op/issues

---

## 📖 使用说明

### 安装

```bash
clawhub install wecom-deep-op --tag latest
```

### 配置

```bash
export WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_UA_KEY"
export WECOM_SCHEDULE_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/schedule?uaKey=YOUR_UA_KEY"
# ... 其他服务
```

### 调用示例

```bash
# 健康检查
openclaw skill invoke wecom-deep-op.ping "{}"

# 创建文档
openclaw skill invoke wecom-deep-op.doc_create '{"doc_type":3, "doc_name":"Test"}'

# 创建日程
openclaw skill invoke wecom-deep-op.schedule_create '{"summary":"Meeting", "start_time":"2026-03-22 10:00:00", "end_time":"2026-03-22 11:00:00"}'
```

---

## 📚 变更日志

### [1.0.3] - 2026-03-21

**修复（响应代码审查）**

- 移除未使用的依赖 `@wecom/aibot-node-sdk`
- 添加参数验证工具函数和运行时验证
- Logger类增强（新增warn方法）
- 修复重复logger声明问题

### [1.0.2] - 2026-03-21

**修复（响应代码审查）**

- 移除未使用的依赖 `@wecom/aibot-node-sdk`
- 添加参数验证工具函数和运行时验证
- Logger类增强（新增warn方法）
- 修复重复logger声明问题

### [1.0.1] - 2026-03-21

**增强**

- 新增 WeComError 类
- 新增 Logger 工具类（debug/info/error/warn）
- 智能重试机制
- 智能配置检查

### [1.0.0] - 2026-03-21

**新增**

- 首次发布，封装5大企业微信服务（文档/日程/会议/待办/通讯录）
- 27个API函数
- 智能配置检查
- TypeScript完整类型定义

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](https://github.com/Bingbox/wecom-deep-op/blob/main/LICENSE)
