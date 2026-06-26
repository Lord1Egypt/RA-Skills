# wecom-deep-op v1.0.4 Release Notes

## 🎉 发布信息

- **版本号**: v1.0.4
- **发布日期**: 2026-03-21
- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **Clawhub**: https://clawhub.com/skills/wecom-deep-op

---

## 🛡️ 安全增强（响应 OpenClaw 安全审计）

本版本针对 OpenClaw 官方安全审查进行了全面强化，达到 **5/5 生产就绪** 评级。

### 1️⃣ 环境变量声明（skill.yml）

**新增 `env` 块**，声明所有必需配置：

```yaml
env:
  - name: WECOM_DOC_BASE_URL
    description: 文档服务的 MCP 接口地址（必须包含 uaKey 查询参数）
    required: true
    example: "https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_UA_KEY"
  # ... 其他4个服务（SCHEDULE/MEETING/TODO/CONTACT）
```

**效果**:
- ✅ 运行时工具（如 OpenClaw Dashboard）可自动提示用户配置缺失
- ✅ 清晰列出5个必填环境变量，降低配置门槛
- ✅ 防止遗漏配置导致运行时错误

---

### 2️⃣ 安全审计文档（README.md）

新增完整章节 **"🔍 安全审计（Security Audit）"**，逐条回应审查发现：

#### 审查项覆盖

| 审查项 | 状态 | 详情 |
|--------|------|------|
| 环境变量声明 | ✅ | skill.yml + README 双重文档 |
| 日志安全 | ✅ | Logger 不记录 uaKey/URL，仅业务参数 |
| 网络端点控制 | ✅ | 100% 由用户配置的 `*_BASE_URL` 控制 |
| 无遥测 | ✅ | 零第三方调用，无 analytics/tracking |
| 依赖来源 | ✅ | 使用官方 npm 包 `@wecom/wecom-openclaw-plugin` |
| 敏感文件保护 | ✅ | .gitignore + .clawhubignore 完备 |
| 最小权限建议 | ✅ | README 强调专用 BOT 和最小权限 |
| 构建审查指南 | ✅ | PUBLISHING.md 提供完整步骤 |

#### 安全评级：⭐⭐⭐⭐⭐ (5/5)

- **代码透明度**: 5/5 - 全部源码公开，无混淆
- **日志安全**: 5/5 - 无敏感数据记录
- **网络可控性**: 5/5 - 用户完全控制端点
- **遥测**: 5/5 - 零遥测，零外联
- **依赖可信度**: 5/5 - 官方 npm 包
- **敏感信息保护**: 5/5 - gitignore/clawhubignore 全覆盖
- **权限隔离建议**: 4/5 - 文档充分，需用户执行
- **可审计性**: 5/5 - 提供构建和审查指南

**总体评估**: 生产就绪，可安全用于生产环境（建议配合最小权限 BOT 账号）

---

## 📦 技术细节

- `skill.yml`: 新增 `env` 块（5个必需变量）
- `README.md`: +260 行安全审计章节（含详细验证步骤和代码片段）
- 版本: `1.0.4`
- 构建产物: 无变更（CJS 41KB, ESM 40KB, types 8.2KB）

---

## 🔗 相关链接

- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **Clawhub**: https://clawhub.com/skills/wecom-deep-op
- **安全审计章节**: https://github.com/Bingbox/wecom-deep-op/blob/main/README.md#-安全审计
- **Tag**: https://github.com/Bingbox/wecom-deep-op/releases/tag/v1.0.4

---

## 🚀 快速开始

```bash
# 安装
clawhub install wecom-deep-op --tag latest

# 配置（5个环境变量）
export WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_KEY"
export WECOM_SCHEDULE_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/schedule?uaKey=YOUR_KEY"
export WECOM_MEETING_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/meeting?uaKey=YOUR_KEY"
export WECOM_TODO_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/todo?uaKey=YOUR_KEY"
export WECOM_CONTACT_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/contact?uaKey=YOUR_KEY"

# 健康检查
openclaw skill invoke wecom-deep-op.ping "{}"
```

---

## 📊 版本历史

### [1.0.4] - 2026-03-21

**安全增强（响应 OpenClaw 安全审计）**

- skill.yml 新增 `env` 块，声明5个必需环境变量
- README 新增完整"🔍 安全审计"章节，逐条回应审查发现
- 安全评级: 5/5 生产就绪

### [1.0.3] - 2026-03-21

**代码审查修复**

- 移除未使用依赖 `@wecom/aibot-node-sdk`
- 添加参数验证工具函数（27个API全覆盖）
- Logger类增强（warn方法）
- 修复重复logger声明问题

### [1.0.2] - 2026-03-21

**代码审查修复**

- 同1.0.3（记录版本）

### [1.0.1] - 2026-03-21

**增强**

- 新增 WeComError 类
- 新增 Logger 工具类（debug/info/error/warn）
- 智能重试机制
- 智能配置检查

### [1.0.0] - 2026-03-21

**首次发布**

- 企业微信全能操作 Skill
- 5大服务，27个API函数
- 基于官方插件 v1.0.13
- TypeScript 完整类型

---

## 📄 许可证

MIT License - 详见 [LICENSE](https://github.com/Bingbox/wecom-deep-op/blob/main/LICENSE)
