---
name: query-policy-deepseek
description: >
  This skill should be used when the user asks to query or search for
  "科技特长生升学政策" (technology/specialty student admission policies),
  batch query education policies by region, or execute the query_policy_v2.py
  script. It provides the core DeepSeek API integration for fetching
  programming/technology specialty student policies for primary and secondary
  school admissions in China.
agent_created: true
---

# Query Policy DeepSeek Skill

批量查询各地科技特长生升学政策的 Skill，基于 DeepSeek API 实现。

## Core Script

The main execution script is located at:
```
scripts/query_policy_v2.py
```

This script performs the following:
1. Reads region list from `地区.txt`
2. Calls DeepSeek API to query technology specialty student admission policies
3. Parses CSV-formatted responses
4. Writes results to `政策.csv` with UTF-8-sig encoding (Excel compatible)
5. Tracks progress in `进度.txt`

## Key Configuration

| Setting | Value |
|---------|-------|
| API Key | `sk-134d7a53ebab42e4ac5af93ea28e5f13` |
| API Endpoint | `https://api.deepseek.com/chat/completions` |
| Model | `deepseek-chat` |
| Temperature | 0 (deterministic output) |

## File Paths

Default paths (configured in the script):
- Input: `C:\Users\zhufangming\Desktop\zfm_demo_02\地区.txt`
- Output: `C:\Users\zhufangming\Desktop\zfm_demo_02\政策.csv`
- Progress: `C:\Users\zhufangming\Desktop\zfm_demo_02\进度.txt`

**Important**: Before running, verify these paths exist and are correct.

## Output Format

CSV with 5 columns:
1. 学段 (Education stage: 小升初/初升高)
2. 地区 (Region)
3. 学校名称 (School name)
4. 赛事/项目名称 (Competition/project name)
5. 对升学的具体帮助 (Specific admission benefits)

## Policy Rules

### Allowed Competitions
- Python编程赛/Python创意编程赛
- 全国青少年Python编程竞赛
- 中国电子学会青少年Python编程等级测试
- NOC大赛Python赛项
- 全国青少年科技创新大赛（科技创新成果类）
- 青少年机器人竞赛（不含图形化编程类）
- 青少年电子信息智能创新大赛
- 人工智能相关竞赛（创意编程、算法类）

### Prohibited Competitions (Must NOT appear)
- Scratch/图形化编程类
- 蓝桥杯/BlueCloud
- NOI系列 (NOIP, CSP-J/S, IOI, etc.)
- C++信息学奥赛相关

### Description Requirements

Each policy description MUST include:
- 年份 (Year): Which year's admission policy
- 招生人数 (Quota): Specific numbers (e.g., 招收3人, 招收5人)
- 报名条件 (Conditions): Award level requirements
- 招生对象 (Target): Which students can apply
- 过程/方式 (Process): How admission works

## Execution

To run the policy query:

```bash
python "C:\Users\zhufangming\.workbuddy\skills\query-policy-deepseek\scripts\query_policy_v2.py"
```

Or copy the script to the target directory and run from there.

## Version History

- v2: Base version with 5 columns
- v3: Added 信息来源 (information source) column - not yet integrated in main script

For updates or modifications, edit `scripts/query_policy_v2.py` directly.
