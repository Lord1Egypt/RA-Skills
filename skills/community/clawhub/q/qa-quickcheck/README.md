# QA QuickCheck - AI 驱动的日常测试助手

> ⚡ 2 分钟上手 | 一句话完成日常 PR 测试

[![版本](https://img.shields.io/badge/version-1.0.3-blue)](https://clawhub.ai/houyang995/skills/qa-quickcheck)
[![许可证](https://img.shields.io/badge/license-MIT--0-green)](https://clawhub.ai/houyang995/skills/qa-quickcheck)
[![分类](https://img.shields.io/badge/分类-测试%20%7C%20代码质量%20%7C%20DevOps-orange)](https://clawhub.ai/houyang995/skills/qa-quickcheck)

## 这是什么？

QA QuickCheck 是一个 **AI 驱动的自动化测试 Skill**，帮你把日常 PR 检查从"手动跑测试"变成"一句话搞定"。

你只需要在聊天框里说 `按 Quick 测试` 或 `按 Standard 测试`，AI 就会自动完成静态代码扫描、动态功能测试、配置检查，并生成一份结构化的测试报告。

## 为什么需要它？

| 没有 QuickCheck | 有 QuickCheck |
|:---|:---|
| 手动检查硬编码密钥，容易漏 | AI 自动扫描所有源码，正则匹配 |
| PR 前要跑各种测试，忘记步骤 | 一句话 `按 Standard 测试`，全自动 |
| 测试报告格式不统一 | 自动生成 PM/Dev 双视角结构化报告 |
| 不知道回归范围 | Git diff 自动识别变更模块，只测必要的 |

## 快速开始

### 安装

```bash
clawhub install qa-quickcheck
```

### 使用

```
# 改了个小功能 → 2 分钟快速扫描
@qa-quickcheck 按 Quick 测试

# 提 PR 前 → 静态 + 动态 + 回归检查
@qa-quickcheck 按 Standard 测试
```

## 两种模式

| 模式 | 做什么 | 耗时 | 场景 |
|:---|:---|:---|:---|
| **Quick** | 极速静态扫描（硬编码密钥 + 危险 API + 配置检查） | 2-5 分钟 | 小改动、日常检查 |
| **Standard** | 静态审计 + 动态功能测试 + Git diff 回归 | 5-15 分钟 | PR / 合并前检查 |

## 能力一览

### ✅ 能做的
- 🔍 **静态代码审计**：硬编码密钥扫描、危险 API 检测、依赖 CVE 审计、许可证合规
- 🧪 **动态功能测试**：自动启动项目 → 冒烟测试 → 核心链路 → 边界异常
- 🛡️ **配置合规检查**：HTTP 头部基础配置审查（CSP、HSTS、CORS 等）
- 🔄 **智能回归**：Git diff 自动识别变更范围，只测变更模块
- 📝 **结构化报告**：PM/Dev 双视角缺陷描述 + 双向追溯映射表 + 门禁结论

### 🚧 Roadmap（持续迭代中）
- 浏览器 E2E 测试（Playwright/Cypress）
- API 契约动态验证（OpenAPI CDC）
- 性能压测（PP0~PP4 五级递进）
- 深度安全合规检测（OWASP Top 10 全覆盖）

## 技术栈支持

| 语言 | 静态审计 | 依赖审计 | 动态测试 |
|:---|:---:|:---:|:---:|
| JavaScript / TypeScript | ✅ | npm audit | ✅ |
| Python | ✅ | pip-audit / safety | ✅ |
| Java (Maven/Gradle) | ✅ | dependency-check | ✅ |
| Go | ✅ | govulncheck | ✅ |
| Rust | ✅ | cargo audit | ✅ |
| Ruby | ✅ | bundle audit | ✅ |
| PHP | ✅ | composer audit | ✅ |
| .NET / C# | ✅ | dotnet list package | ✅ |

## 报告示例

```
📊 测试报告：test-report.md

## 执行摘要
- 执行模式：Standard
- 结论：⚠️ 有条件通过
- 发现：2 个 Medium 缺陷，1 个 High 配置问题

## 缺陷总览
### PM 视角
- **SEC-001**：用户登录接口的 Token 未设置 HttpOnly 标志，
  可能导致用户会话信息被意外获取。
- **DEF-001**：商品列表分页在翻到第 100 页时返回空数据，
  但实际仍有商品，用户会误以为没有更多商品。

## Dev 视角
- **SEC-001 [静态]**：src/middleware/auth.js#L42
  Cookie 设置缺少 HttpOnly 属性
- **DEF-001 [动态]**：GET /api/products?page=100
  返回空数组，但 total 显示 1200 条记录
```

## 配置

可选配置项（`openclaw.json`）：

```json
{
  "skills": {
    "qa-quickcheck": {
      "default_mode": "standard",
      "base_url": "http://localhost:3000",
      "test_timeout": 30000
    }
  }
}
```

## 安装要求

- OpenClaw 2026.1.0+
- Node.js 22+（用于运行测试脚本）
- 项目可启动（Standard 模式需要）

## 安全声明

- ✅ **只读不写**：不会修改任何业务代码
- ✅ **测试隔离**：所有脚本仅在 `tests/` 或 `.ai_test_tmp/` 下运行
- ✅ **自动清理**：测试结束后自动删除临时文件
- ✅ **非侵入性**：所有检测均为只读请求，不发送任何非预期内容至目标服务

## 反馈与贡献

- 🐛 报告 Bug：[GitHub Issues](https://github.com/your-username/qa-quickcheck/issues)
- 💬 讨论：[OpenClaw Discord](https://discord.gg/openclaw)
- 📧 联系：your-email@example.com

---

**Made with ❤️ for the OpenClaw community. MIT Licensed.**
