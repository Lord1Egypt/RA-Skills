---
name: skill-router-bzai
version: 1.0.0
description: Cost-effective skill selector for maximizing ROI on AI operations (增收降本版 v1.0.0). Use when the user needs to accomplish a task and wants the optimal skill chosen automatically to minimize costs while maximizing quality. Evaluates skills based on quality (35%), token cost (30%), security/reliability (20%), and speed (15%). Searches both local skills and clawhub.com, presents top recommendations for user confirmation before execution.
metadata:
  purpose: "增收降本 - 智能选择最优技能以最小化Token成本"
---

# Skill Router (增收降本版 v1.0.0)

智能技能选择器 - 用于增收降本的 AI 操作优化工具。

自动选择并执行最优技能，在保证质量的前提下最小化 Token 成本。

## When to Use

- User wants to accomplish something but doesn't know which skill to use
- Multiple skills could solve the same problem - need to pick the best one
- Want to minimize token cost while maximizing quality
- Need to evaluate skills from clawhub.com before installation

## Workflow

### 1. Parse Task

Analyze user request and decompose into atomic subtasks if needed.

### 2. Discover Skills

Search for candidate skills:
- List local installed skills: `openclaw skills list`
- Search clawhub.com: `clawhub search <keywords>`

### 3. Evaluate Candidates

For each candidate skill, score on:

| Dimension | Weight | Evaluation Criteria |
|-----------|--------|---------------------|
| Quality/Utility | 35% | User ratings, downloads, functionality match |
| Token Cost | 30% | Estimated input/output tokens based on skill complexity |
| Security/Reliability | 20% | Code audit, permissions, update frequency, author trust |
| Speed | 15% | API response time, execution efficiency |

**Scoring Algorithm:**
```
final_score = (quality × 0.35) + (token_score × 0.30) + (security × 0.20) + (speed × 0.15)
```

### 4. Generate Recommendations

Present Top-3 ranked options:
- Rank, skill name, final score
- Breakdown by dimension
- Estimated tokens and time
- Reasoning for recommendation
- Security assessment summary

### 5. User Confirmation

Wait for user to:
- Select option (1, 2, or 3)
- Request more details about a skill
- Cancel or modify the task

### 6. Execute

After confirmation:
- If skill not installed: `clawhub install <skill>`
- Execute the skill with original user request
- Record actual metrics vs estimates

## Security Assessment

Before recommending any skill from clawhub:

1. **Code Review**: Check for suspicious patterns (network calls, file system access, credential harvesting)
2. **Permission Analysis**: Verify requested permissions match functionality
3. **Author Verification**: Prefer verified authors, established projects
4. **Update Frequency**: Recently updated skills are preferred
5. **Community Trust**: Ratings, issues, download count

**Red flags that disqualify a skill:**
- Requests excessive permissions for its stated purpose
- Contains obfuscated code
- Makes unexpected network calls
- Has no recent updates and low community engagement

## Token Estimation

Estimate token costs based on:
- Skill description length/complexity
- Historical usage data (if available)
- Number of API calls required
- Output format verbosity

Store actual vs estimated for continuous improvement.

## Scripts

- `scripts/evaluate_skill.py` - Score a skill across all dimensions
- `scripts/search_clawhub.py` - Search and fetch skill metadata from clawhub
- `scripts/calculate_cost.py` - Estimate token and time costs

## References

- `references/evaluation-rubric.md` - Detailed scoring criteria
- `references/security-checklist.md` - Security audit checklist
