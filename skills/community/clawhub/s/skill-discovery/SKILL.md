---
name: skill-discovery
description: 基于用户意图发现并推荐 skill。分析用户输入，搜索匹配 skill，验证质量后推荐最佳匹配，由用户确认后安装。
metadata:
  openclaw:
    install:
      type: bundled
      entrypoint: index.js
    requires:
      bins:
        - npx
      anyBins:
        - clawhub
    homepage: https://github.com/caocong1/skill-discovery
---

# Skill Discovery

根据用户意图发现并推荐匹配的 skill。默认仅推荐，需用户确认后才会安装。

## 何时使用

适用场景：

- 用户请求帮助完成某个任务，且可能已有现成的 skill 方案
- 用户表达了扩展能力的需求（如"怎么部署"、"帮我写测试"）
- 用户提到了特定领域的工具需求（设计、测试、部署等）
- 用户明确询问"有没有 skill 可以..."、"找个工具帮我..."

## 工作流程

1. **分析用户输入** — 理解意图，识别目标领域
2. **搜索 skills.sh + ClawHub** — 并行搜索两个注册表，合并去重结果
3. **质量验证** — 检查安装量和来源可信度
4. **推荐最佳匹配** — 返回推荐结果和安装命令，由用户确认后执行安装

> **安全说明**: 默认运行在推荐模式（dry-run），不会自动安装任何 skill。
> 只有调用方显式传入 `{ dryRun: false }` 时才会执行实际安装。
> OpenClaw hook 始终使用推荐模式。

## 输入/输出

**输入**: 用户自然语言文本（中文或英文）

**输出**（统一结构）:
```javascript
{
  success: boolean,
  stage: 'analyze' | 'search' | 'select' | 'install',
  outcome: 'installed' | 'already_installed' | 'dry_run' | 'skipped' | 'failed',
  errorCode: string | null,   // 如 'NO_RESULTS'、'INSTALL_FAILED'
  skill: object | null,
  candidates: array,
  message: string
}
```

## 触发示例

**中文:**
- "帮我部署到 Vercel"
- "有什么工具可以优化性能"
- "怎么写测试"
- "推荐一个数据处理工具"

**英文:**
- "find a skill for deploying"
- "help me with testing"
- "is there a skill for PDF parsing"
- "I need a tool for React optimization"

## 安全特性

- **推荐模式默认**: 默认 dry-run，不自动安装，需用户确认
- **Shell 转义**: 所有 CLI 参数转义防止命令注入
- **日志脱敏**: `sanitize()` 递归遮蔽敏感字段（字段名匹配 `token/secret/password/api_key/credential/authorization`）和敏感值（`Bearer`/`sk-`/`ghp_` 等模式），业务字段（installs/confidence/domain）保持原值。日志写入 `$OPENCLAW_DIR/logs/skill-discovery-v3.json`，可通过 `OPENCLAW_DIR` 环境变量自定义路径
- **卸载备份**: 卸载的 skill 备份到 `.trash/`，保留 7 天
- **来源验证**: 校验 skill 来源是否在可信 owner 列表中

## 支持语言

- 中文：触发词 + 领域关键词（含负面模式排除避免误触发）
- 英文：触发词 + 领域关键词

## 覆盖领域

DevOps、测试、设计、文档、代码质量、数据处理、图片处理、视频处理、性能优化、API/网络、数据库、AI/ML、安全、移动端、游戏

## 依赖

- Node.js >= 18
- `npx skills` CLI（来自 skills.sh）
- `clawhub` CLI（可选，来自 clawhub.ai）

## 许可证

MIT-0
