## Description: <br>
Routes agent tasks between cheap, default, pro, and ultra model tiers and can suggest sub-agent briefing for heavier work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarAtheris](https://clawhub.ai/user/StarAtheris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route everyday requests to lower-cost models while escalating heavier analysis, debugging, legal, security, or long-context tasks to stronger model tiers. It can emit routing decisions, response-policy hints, and compact briefs for sub-agent handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs may include secrets or highly private context if sensitive material is present in the input. <br>
Mitigation: Review or redact context before briefing, and only pass briefs to sub-agents or models when that sharing is intended. <br>
Risk: Routing decisions may select a stronger or costlier model tier than the operator wants for a specific task. <br>
Mitigation: Review rules.json thresholds and model names, and use router auto off or @cheap, @default, @pro, and @ultra overrides when manual control is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/StarAtheris/staratheris-arya-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON decision records and plain-text briefs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Router output includes model tier, model name, score, reasons, actions, response policy, and helper-script hints; brief output is capped plain text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
