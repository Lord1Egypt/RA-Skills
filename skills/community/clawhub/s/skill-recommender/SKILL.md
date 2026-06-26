---
name: skill-recommender
description: "Agent skill recommender. Input a user need, task description, or existing skill list; output best matching skills, install rationale, duplicate/merge candidates, and gaps for new skill briefs. Runtime-neutral and not tied to one agent platform."
---
# Skill Recommender

Use this skill to recommend the best matching skills from an existing skill collection.

## Default workflow

1. Identify the user's target intent:
   - exact function
   - adjacent use case
   - duplicate/overlap check
   - best skill recommendation
2. Scan available skills from a given directory.
3. Match by:
   - name
   - description
   - keywords
   - domain words
4. Group similar skills into clusters when needed.
5. Return a ranked recommendation with reasons.

## Use the bundled scripts

### 1. Recommend similar skills
Use `scripts/recommend_skills.js` when the user gives a query such as:
- “找同类 skill”
- “有没有类似的 skill”
- “这些 skill 哪个更适合”
- “帮我筛选同功能的 skills”

Example:

```bash
node scripts/recommend_skills.js '{
  "query": "家庭采购 库存 提醒",
  "skills_dir": "/Users/jianghaidong/.openclaw/workspace/skills",
  "limit": 8
}'
```

### 2. Cluster related skills
Use `scripts/cluster_skills.js` when the user wants a grouped view of similar skills, duplicates, or overlapping categories.

### 3. Avoid duplicate skill development
Use `scripts/check_skill_dedup.js` when the user is about to build a new skill and wants to know:
- whether similar skills already exist
- whether the request should reuse an existing skill
- whether it is better to extend or merge current skills instead of building a new one

Typical triggers:
- “这个 skill 会不会重复开发”
- “帮我查重一下 skill”
- “我想做一个新 skill，先看看有没有类似的”
- “这是不是应该复用现有 skill”

## Output contract

Default output sections:
- 目标功能理解
- 推荐 skill
- 推荐理由
- 相近但次优 skill
- 可合并/避免重复开发的 skill
- 下一步建议

## Recommendation rules

- Prefer concrete task fit over keyword overlap.
- Distinguish “direct match” from “adjacent match”.
- If several skills overlap heavily, say so explicitly.
- If a new skill request is already covered by existing skills, recommend reuse before new development.
- If confidence is low, surface the ambiguity.

## Read references as needed

- Read `references/recommendation-rules.md` for ranking heuristics.
- Read `references/output-schema.md` for the output schema.
- Read `references/dedup-mode.md` when the user wants to avoid duplicate skill development.
