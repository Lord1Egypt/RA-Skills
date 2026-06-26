# wecom-deep-op v1.0.5 Release Notes

## 🎉 发布信息

- **版本号**: v1.0.5
- **发布日期**: 2026-03-21
- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **Clawhub**: https://clawhub.com/skills/wecom-deep-op
- **Tag**: https://github.com/Bingbox/wecom-deep-op/releases/tag/v1.0.5

---

## 🛡️ 安全合规强化（响应 ClawHub Security 扫描）

### 背景

ClawHub Security 扫描器检测到以下模式并标记为可疑：
1. `src/index.ts:52` - "Environment variable access combined with network send"
2. `src/index.ts:1260` - "File read combined with network send (possible exfiltration)"

**本版本通过详细文档解释这些模式的安全边界，证明其为预期功能行为。**

---

### 新增文档：🌐 数据流向与安全边界

README 新增完整章节，说明：

#### 模式1：环境变量 + 网络发送
```typescript
const baseUrl = process.env.WECOM_DOC_BASE_URL;
fetch(`${baseUrl}&method=...`, { ... });
```
**用途**: 调用用户配置的企业微信 MCP 接口  
**安全边界**: URL 完全由用户控制，Skill 不硬编码任何端点

#### 模式2：文件读取 + 网络发送
```typescript
const content = fs.readFileSync(filePath, 'utf-8'); // 用户提供的文件
fetch(url, { body: JSON.stringify({ content }) }); // 发送到用户配置的接口
```
**用途**: 用户上传文档内容到企业微信（`doc_edit` 函数）  
**安全边界**: 文件路径由用户参数指定，网络目标为用户配置的官方 MCP 接口

---

### 安全审计要点

- ✅ **用户控制**: 所有网络端点由 `WECOM_*_BASE_URL` 环境变量决定
- ✅ **用户触发**: 文件读取仅在用户调用特定 API（如 `doc_edit`）时发生
- ✅ **无自主外联**: Skill 无后台任务，无第三方域名访问
- ✅ **审计建议**:
  - 验证 `WECOM_*_BASE_URL` 指向 `qyapi.weixin.qq.com`
  - 在隔离环境测试，使用非敏感文件
  - 检查 dist/ 产物确认无意外硬编码

---

## 📦 版本信息

- **版本**: 1.0.5
- **类型**: 安全合规增强
- **影响范围**: 无代码变更，仅文档增强
- **升级建议**: 所有用户推荐升级（提升透明度）

---

## 🔗 链接

- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **Clawhub**: https://clawhub.com/skills/wecom-deep-op
- **数据流向章节**: https://github.com/Bingbox/wecom-deep-op/blob/main/README.md#-数据流向与安全边界
- **安全审计章节**: https://github.com/Bingbox/wecom-deep-op/blob/main/README.md#-安全审计

---

## 🚀 快速验证

```bash
# 安装 v1.0.5
clawhub install wecom-deep-op --tag latest

# 查看安全文档
openclaw skill read wecom-deep-op | grep -A 20 "数据流向与安全边界"
```

---

## 📊 版本历史

### [1.0.5] - 2026-03-21

**安全合规强化（响应 ClawHub Security 扫描）**

- 新增 "🌐 数据流向与安全边界" 章节
- 解释 "env + network" 和 "file read + network" 模式的安全边界
- 提供审计建议：验证官方域名、隔离环境测试
- 无代码变更，纯文档增强

### [1.0.4] - 2026-03-21

**安全增强（响应 OpenClaw 安全审计）**

- skill.yml 新增 `env` 块，声明5个必需环境变量
- README 新增完整"🔍 安全审计"章节，安全评级 5/5

### [1.0.3] - 2026-03-21

**首次 Clawhub 发布**（修复版）

- 移除未使用依赖
- 参数验证全覆盖
- Logger 增强

### [1.0.2] - 2026-03-21

**代码审查修复**

### [1.0.1] - 2026-03-21

**错误处理与智能配置**

### [1.0.0] - 2026-03-21

**初始版本**

---

## 📄 许可证

MIT License - 详见 [LICENSE](https://github.com/Bingbox/wecom-deep-op/blob/main/LICENSE)
