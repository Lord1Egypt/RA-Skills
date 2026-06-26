# wecom-deep-op 变更日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [2.0.2] - 2026-03-22

### 🛠️ User-Requested Documentation Updates

**更新来源**: 根据用户实际使用反馈和 review 修订

- 📝 **中文文档优化**: 
  - 增强快速开始指南，添加更多实际示例
  - 补充故障排除表格，覆盖常见问题
  - 优化 API 调用示例，添加错误处理建议
  - 完善安全配置说明

- 🌍 **英文文档同步**:
  - README.en.md, SKILL.en.md, QUICKSTART.en.md 同步更新
  - 保持中英文内容一致性
  - 改进技术术语翻译准确性

- 📚 **整体改进**:
  - 统一文档结构和格式
  - 补充贡献指南链接
  - 更新支持联系方式

---

## [2.0.1] - 2026-03-22

### 🌍 Internationalization & Documentation Overhaul

**新增内容**:
- 📚 **Full English Documentation**: Created complete English versions of all docs
  - `README.en.md` - Full project intro, installation, configuration, FAQ
  - `SKILL.en.md` - Complete API reference (27 functions)
  - `QUICKSTART.en.md` - 5-minute quick start with code samples
- 🔗 Updated Chinese `README.md` with link to English docs
- 📝 Updated `QUICKSTART.md` with improved examples

**中文本地化增强**:
- 🛡️ **Security Audit Chapter** - Detailed security analysis and compliance (5/5 rating)
- 🌐 **Data Flow & Security Boundaries** - Explains network patterns and data handling
- 🐛 **Expanded Troubleshooting** - More common issues and solutions
- 📖 **Improved API Examples** - Realistic use cases and error handling

**技术改进**:
- All documentation validated and tested
- Consistent version (v2.0.1) across all files
- Maintained MIT license

---

## [2.0.0] - 2026-03-22

### 🎉 正式发布

**核心特性**:
- ✅ 基于企业微信官方插件 `@wecom/wecom-openclaw-plugin` v1.0.13+
- ✅ 一站式企业微信自动化解决方案
- ✅ 统一封装 5 大服务：文档、日历、会议、待办、通讯录
- ✅ 完整的 OpenClaw MCP 集成：`wecom_mcp call wecom-deep-op.<function>`
- ✅ 智能配置引导：每个 API 自动返回配置步骤
- ✅ 生产就绪：参数验证、错误重试、日志系统
- ✅ 安全设计：无数据存储、用户可控凭证、最小权限原则

**支持的 API** (27个接口):
- 📄 文档管理：`doc_get`, `doc_create`, `doc_edit`
- 📅 日程管理：`schedule_create`, `schedule_list`, `schedule_get`, `schedule_update`, `schedule_cancel`, `schedule_add_attendee`, `schedule_remove_attendee`
- 📹 会议管理：`meeting_create`, `meeting_list`, `meeting_get`, `meeting_cancel`, `meeting_update_attendees`
- ✅ 待办管理：`todo_create`, `todo_list`, `todo_get`, `todo_update_status`, `todo_update`, `todo_delete`, `todo_accept`, `todo_refuse`
- 👥 通讯录：`contact_get_userlist`, `contact_search`
- 🔧 系统：`ping`, `preflight_check`

**技术细节**:
- TypeScript 开发，Rollup 构建（CJS + ESM）
- 完整类型定义（.d.ts）
- 环境变量 + mcporter.json 双配置源
- 异步任务轮询（文档导出）
- 指数退避重试（网络错误）
- MIT 协议开源

**安全与合规**:
- 🔒 不存储任何企业微信凭证
- 📝 清晰的日志分级（debug/info/error）
- 🌐 数据流向透明：用户控制端点、用户提供文件
- ⚠️ 通讯录权限限制提示（仅返回可见范围成员）
- 📊 通过 OpenClaw 安全审计（5/5 生产就绪）
- 📄 **MIT 协议**开源

**文档**:
- 完整的 `SKILL.md` 技能说明
- 详细的 `README.md`（含快速开始、故障排除）
- 示例代码和调用指南
- 贡献指南和 MIT 协议

---

## [历史版本]

> **注意**: 本版本之前的开发版本（1.0.1 - 1.0.5）已被重置，历史记录已清理。
> 这些版本包含的功能已全部整合到当前 v1.0.0 中。
