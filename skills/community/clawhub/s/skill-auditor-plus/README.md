# Skill Auditor Plus

## Overview

Skill Auditor Plus 是一个综合性的 AgentSkill 审计工具，提供安全、性能和质量三个维度的自动化检查。

## 特性

- 🔒 **安全审计**：扫描危险操作、凭证泄露、可疑模式
- ⚡ **性能审计**：分析 token 使用、context 优化、脚本效率
- 📊 **质量审计**：检查最佳实践合规性、文档完整性

## 快速开始

### 安装

```bash
# 克隆或下载技能
git clone <repository-url>
cd skill-auditor-plus
```

### 使用

```bash
# 审计单个技能
python3 scripts/security_audit.py /path/to/skill
python3 scripts/performance_audit.py /path/to/skill

# 批量审计
for skill in /path/to/skills/*; do
    echo "Auditing $skill"
    python3 scripts/security_audit.py "$skill"
    python3 scripts/performance_audit.py "$skill"
done
```

## 审计报告

### 安全审计报告

```json
{
  "total_issues": 5,
  "high_severity": 1,
  "medium_severity": 2,
  "low_severity": 2,
  "issues": [...]
}
```

### 性能审计报告

```json
{
  "skill_md_stats": {
    "frontmatter_tokens": 85,
    "body_tokens": 1800,
    "total_tokens": 1885,
    "line_count": 240
  },
  "issues": [...]
}
```

## 最佳实践

详见 [references/best-practices.md](references/best-practices.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
