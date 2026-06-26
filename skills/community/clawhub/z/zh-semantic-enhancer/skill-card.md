## Description: <br>
Enhances Chinese semantic understanding by analyzing wording, cultural context, dialect-sensitive expressions, ambiguity, idioms, slang, and domain terminology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andyxcg](https://clawhub.ai/user/Andyxcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to normalize and enrich Chinese user input before intent handling, especially when idioms, slang, ambiguous phrasing, or culturally implicit language affect interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes billing-related code and local trial or credit records under ~/.openclaw. <br>
Mitigation: Review billing behavior and local state paths before installation, and disclose or disable billing paths when they are not required. <br>
Risk: An executable revenue optimization helper can rewrite installed skill files if run. <br>
Mitigation: Avoid running scripts/revenue_optimize.py unless those modifications are intentional and can be reviewed or rolled back. <br>
Risk: The server security verdict is suspicious because monetization and self-modifying code are under-scoped relative to the semantic analysis use case. <br>
Mitigation: Install only after reviewing the security summary and limiting execution to the semantic analysis entry points needed by the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Andyxcg/zh-semantic-enhancer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Andyxcg) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, guidance] <br>
**Output Format:** [JSON object with normalized text, tokens, entities, expressions, confidence, and suggested actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local trial or credit state under ~/.openclaw when billing-related paths are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
