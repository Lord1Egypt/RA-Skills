# Skill Development Guide / Skill 开发指南

A comprehensive guide to creating Skills for ClawHub and OpenClaw.

一份完整的 Skill 开发教程，适用于 ClawHub 和 OpenClaw 平台。

---

## Quick Start / 快速开始

A Skill is a reusable prompt template that extends AI capabilities. Every Skill needs a `SKILL.md` file.

Skill 是一个可复用的提示词模板，用于扩展 AI 能力。每个 Skill 都需要一个 `SKILL.md` 文件。

### Minimal Structure / 最小结构

```markdown
# My Skill Name

Short description of what this skill does.

---

instructions: |
  You are a helpful assistant that...

  ## Your Task
  1. Step one
  2. Step two
```

---

## Core Concepts / 核心概念

### 1. Instructions Block / 指令块

The `instructions` field defines AI behavior:

```yaml
instructions: |
  You are an expert at [task].

  ## Guidelines
  - Be concise
  - Focus on accuracy
```

**Tips / 提示**:
- Use clear, specific language / 使用清晰具体的语言
- Break complex tasks into steps / 将复杂任务分解为步骤
- Avoid ambiguous instructions / 避免模糊的指令

### 2. Scripts (Optional) / 脚本（可选）

Add automation with bash scripts:

```yaml
scripts:
  - name: validate
    description: Validate input data
    command: ./scripts/validate.sh
```

**Security Rules / 安全规则**:
- Never use `set -a` (exports all variables) / 禁止使用 `set -a`
- Avoid hardcoded secrets / 避免硬编码密钥
- Use explicit variable exports / 使用显式变量导出

### 3. Allowed Commands / 允许的命令

Declare which commands your skill needs:

```yaml
allowed_commands:
  - curl
  - jq
  - node
```

---

## Best Practices / 最佳实践

### Passing Security Scan / 通过安全扫描

| Do / 推荐 | Don't / 避免 |
|-----------|--------------|
| Explicit variable exports | `set -a` or `export *` |
| Documented API calls | Hidden external requests |
| Clear script descriptions | Vague or missing descriptions |
| User-facing outputs | Silent background operations |

### Writing Good Instructions / 写好指令

1. **Be Specific** / 具体明确
   - Bad: "Help with code"
   - Good: "Review Python code for security vulnerabilities"

2. **Provide Context** / 提供上下文
   - Include relevant background information
   - Define technical terms if needed

3. **Set Boundaries** / 设定边界
   - Specify what the skill should NOT do
   - Define output format expectations

---

## Examples / 示例

### Basic Example / 基础示例

See [examples/minimal.md](examples/minimal.md) for a starter template.

### With Scripts / 带脚本示例

See [examples/with-script.md](examples/with-script.md) for automation patterns.

### Real-World Reference / 实际项目参考

For a complete MCP + Skill implementation example, check out:
- [data-verify-mcp](https://github.com/CCCpan/data-verify-mcp) - A data validation tool with full documentation

---

## Common Mistakes / 常见错误

| Issue | Solution |
|-------|----------|
| Skill not found | Check file is named `SKILL.md` (case-sensitive) |
| Script permission denied | Add `chmod +x` to your script |
| Security scan failed | Review scripts for `set -a`, hardcoded secrets |
| Instructions too long | Break into sections, use bullet points |

---

## FAQ / 常见问题

**Q: How do I test my skill locally?**

A: Use the ClawHub CLI or import directly in OpenClaw.

**Q: Can I use external APIs?**

A: Yes, but document them clearly in your skill description.

**Q: Where can I get help?**

A: Open an issue for discussion and questions:
- https://github.com/CCCpan/data-verify-mcp/issues

---

## Resources / 资源

- [SKILL.md Template](templates/SKILL-template.md) - Ready-to-use template
- [ClawHub Documentation](https://clawhub.ai/docs)
- [OpenClaw Guide](https://openclaw.ai)

---

## Author / 作者

Created by [@CCCpan](https://github.com/CCCpan)

Found this helpful? Star the repo or open an issue to share your feedback!
