---
name: storm-research
description: STORM-style pre-research for content creation. Use to break a topic, trend, external article, product question, or learning area into perspectives, contradiction maps, research briefs, confidence reviews, and evidence plans before writing. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/storm-research
---

# STORM Research

This skill turns a loose topic into a research structure. It prepares writing; it does not write the article.

## Scope

Do:

- scan multiple perspectives
- identify conflicts, consensus, and blind spots
- write a research brief
- score confidence
- create an evidence plan for `wenchang-research`
- update `content_state` and `handoff`

Do not:

- write a final article
- treat simulated perspectives as facts
- replace source-backed fact checking
- make medical, legal, financial, or high-stakes decisions
- use unsupported social screenshots as primary evidence

## Process

1. Run five default perspectives:
   - practitioner
   - researcher
   - skeptic
   - economic observer
   - historical observer
2. Build a contradiction map:
   - direct conflicts
   - shared assumptions
   - strongest evidence
   - weakest evidence
   - blind spots
3. Write a research brief:
   - one-paragraph summary
   - 5 key findings
   - hidden connection
   - actionable insight
   - frontier question
4. Review confidence:
   - score each finding
   - identify weakest claim
   - list missing perspectives
   - list facts requiring verification
5. Produce an evidence plan for `wenchang-research`.

## Output Format

```md
## Research Decision
- Fit for next stage:
- Recommended next step:
- Main reason:

## Perspectives
| Perspective | Core concern | Supports | Challenges | Unique information | Needs verification |
| --- | --- | --- | --- | --- | --- |

## Contradiction Map
- Conflicts:
- Consensus:
- Strongest evidence:
- Weakest evidence:
- Blind spots:

## Research Brief
- Summary:
- Key findings:
- Hidden connection:
- Actionable insight:
- Frontier question:

## Confidence Review
- Scores:
- Weakest claim:
- Bias check:
- Missing perspectives:
- Must verify:

## Evidence Plan
1. <question>: <suggested primary sources>

## content_state Update
```yaml
content_state:
  storm_research:
    topic:
    perspectives: []
    contradiction_map:
      conflicts: []
      consensus: []
      blind_spots: []
    confidence_review:
      verification_needed: []
    evidence_plan: []
  next_step:
    skill: wenchang-research
    reason:
    user_decision_needed:
  handoff:
    from_stage: storm-research
    to_stage:
    accepted_inputs: []
    ignored_context: []
    stop_condition:
```
```

## Stop Conditions

Pause if there are more than three equally strong angles, if the topic involves high-stakes advice, or if core claims cannot be verified with primary sources.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
