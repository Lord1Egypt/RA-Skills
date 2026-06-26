---
name: skill-advisor
description: Evaluate OpenClaw skills before installation. Use when user wants to check a skill's safety, dependencies, popularity, or get an installation recommendation. 安装前评估skill安全性、依赖、流行度。
version: 1.2.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": [], "env": []}}}
---

# Skill Advisor

Pre-install assessment tool for OpenClaw skills.

## Features

- 🔒 **Security Status**: Check ClawHub official scan results
- 📊 **Popularity Metrics**: Downloads, stars, install count
- 🔄 **Maintenance Status**: Last update time, activity level
- 📦 **Dependency Analysis**: Required tools, libraries, complexity
- 💰 **API Cost Assessment**: Free/paid API requirements
- 🎯 **Installation Recommendation**: Clear go/no-go guidance

## Trigger Conditions

- "Check this skill before installing" / "安装前检查这个skill"
- "Is {skill-name} safe?" / "{skill-name}安全吗"
- "Evaluate skill {skill-name}" / "评估skill {skill-name}"
- "What does {skill-name} need?" / "{skill-name}需要什么依赖"
- "Should I install {skill-name}?" / "要不要安装{skill-name}"
- "skill-advisor {skill-name}"
- "帮我看看这个skill怎么样"

---

## Language Support

- 中文 (Chinese)
- English

Output language automatically matches user's input language.

---

## Step 1: Get Skill Information

When user provides a skill name, fetch its metadata:

```
Use clawhub CLI to inspect the skill:
- clawhub inspect {skill-name}
```

---

## Step 2: Fetch SKILL.md Content

Get the actual SKILL.md to analyze dependencies and functionality.

---

## Step 3: Analyze and Generate Report

### Analysis Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| Security | 30% | ClawHub official scan results |
| Popularity | 25% | Downloads, stars |
| Maintenance | 20% | Last update time |
| Dependencies | 15% | Required tools, packages |
| API Cost | 10% | External API requirements |

### Scoring

- **A级 (80-100)**: ✅ Recommended
- **B级 (60-79)**: ⚠️ Install with caution
- **C级 (<60)**: ❌ Not recommended

### Report Structure

```
🎯 Conclusion: {recommendation}
Score: {X}/100 ({grade}) | Security: {status} | Dependencies: {level}

📋 Skill Assessment Report: {skill-name}

📊 Metrics
├─ 🔒 Official Security: {status}
├─ 📈 Popularity: {downloads} downloads | {stars} stars
├─ 🔄 Maintenance: {days} days ago
├─ 📦 Dependencies: {list}
└─ 💰 API Cost: {status}

📝 Description
{description}

⚙️ Requirements
├─ CLI Tools: {tools}
├─ Python Packages: {packages}
├─ Node Packages: {packages}
└─ API Keys: {keys}

⚠️ Usage Notes
├─ {warning}

💡 Installation Advice
{advice}

ℹ️ Metadata
├─ Author: {author}
├─ Version: {version}
├─ License: {license}
└─ Scored at: {datetime}
```

---

## Step 4: Output Report

Display the report directly to user. No files created.

---

## Error Handling

```
Skill not found        → "❌ 未找到该skill，请检查名称"
ClawHub API error      → "❌ 无法连接ClawHub，请稍后重试"
Parse error            → "⚠️ 部分信息解析失败，报告可能不完整"
```

---

## Notes

- No files generated (pure text output)
- Report shows conclusion first, then details
- Security status uses ClawHub's official scan results
- Scores calculated dynamically based on multiple factors
- All data fetched in real-time from ClawHub