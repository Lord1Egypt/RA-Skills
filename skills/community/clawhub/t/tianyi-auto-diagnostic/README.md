# Auto-Diagnostic 技能

[![ClawHub](https://img.shields.io/badge/ClawHub-auto--diagnostic-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.com)

> 🔧 自动诊断 OpenClaw 运行时问题并驱动修复

---

## 📋 功能特性

- **自动诊断** - 分析日志、识别根因、匹配解决方案
- **问题检测** - 网关/浏览器/技能/配置异常自动发现
- **修复建议** - 提供具体修复步骤和命令
- **自动修复** - 低风险问题自动执行修复（需授权）
- **预防建议** - 避免问题再次发生的最佳实践

---

## 🚀 安装

```bash
clawhub install tianyi-auto-diagnostic
```

---

## 📖 使用说明

### 运行诊断

```powershell
.\scripts\diagnose.ps1 -Category "gateway"
```

### 支持的诊断类别

| 类别 | 检查项 |
|------|--------|
| **gateway** | 网关服务状态、端口占用、令牌配置 |
| **browser** | 扩展连接、标签页状态、浏览器进程 |
| **skills** | 技能加载、依赖安装、权限配置 |
| **config** | 配置文件语法、路径有效性、权限检查 |
| **all** | 完整系统诊断 |

---

## 🔍 诊断示例

### 问题：网关连接失败

```
【诊断结果】
问题：网关连接失败（unauthorized: gateway token mismatch）
根因：gateway.auth.token 与 gateway.remote.token 不匹配

【已执行】
✓ 读取配置文件 ~/.openclaw/openclaw.json
✓ 比对 gateway.auth.token 和 gateway.remote.token
✓ 识别差异

【建议修复】
1. 统一令牌值：
   - gateway.auth.token: "abc123"
   - gateway.remote.token: "" (空)

2. 执行修复命令：
   openclaw gateway restart

【预防建议】
令牌变更后需同步更新所有配置位置
```

---

## ⚙️ 自动修复规则

### 可自动执行（低风险）
- ✅ 日志读取分析
- ✅ 状态检查
- ✅ 配置比对
- ✅ 建议生成

### 需授权执行（中风险）
- ⚠️ 配置文件修改
- ⚠️ 服务重启
- ⚠️ 依赖安装

### 禁止自动执行（高风险）
- ❌ 文件删除
- ❌ 系统配置修改
- ❌ 凭证重置

---

## 📊 诊断流程

```
1. 问题报告/检测
       ↓
2. 收集上下文（日志/配置/状态）
       ↓
3. AI 分析根因
       ↓
4. 匹配解决方案
       ↓
5. 执行修复（或建议）
       ↓
6. 验证修复结果
       ↓
7. 记录诊断历史
```

---

## 📝 更新日志

### v1.0.0 (2026-03-01)
- 初始发布
- 网关诊断
- 浏览器诊断
- 技能系统诊断
- 配置诊断
- 自动修复建议

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 链接

- [ClawHub](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub Repo](https://github.com/openclaw_ceo/skills/auto-diagnostic)
