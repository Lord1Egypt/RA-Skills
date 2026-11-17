## Description:

Regex-based routing sends simple tasks to local AI, moderate tasks to mid-tier models, and complex tasks to premium models to reduce API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to classify prompts by complexity and select local, mid-tier, or premium models before dispatch. It supports cost-aware routing while allowing custom regex rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When connected to cloud models, regex routing may send sensitive prompts, confidential business data, regulated advice, or cost-sensitive requests to an unintended model tier.

Mitigation: Review and extend the routing rules before deployment, and require explicit handling for sensitive, confidential, regulated, and cost-sensitive prompts.

Risk: Routing decisions are heuristic and should not be treated as a complete privacy, safety, or cost-control system.

Mitigation: Use the router as one control in a broader review and dispatch process, with human or policy checks for high-impact workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/task-complexity-router)
- [README](artifact/README.md)
- [TaskRouter source](artifact/src/task-router.js)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [JavaScript module output object with model, reason, confidence, and matched rule names; documentation examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic regex-based routing; local processing unless the user connects the routing decision to external model services]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
