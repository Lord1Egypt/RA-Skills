## Description:

Helps agent users, skill authors, maintainers, and teams create practical proactive-agent workflows, checklists, analysis, and implementation support for bug fixing, safety hardening, reliability work, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn requests about proactive-agent workflows into concrete plans, templates, checklists, code changes, or decision support. It is intended for practical productivity work such as bug fixing, setup hardening, reliability improvement, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit-invocation wording may cause the skill to activate for generic productivity or implementation requests.

Mitigation: Use explicit invocation or narrower trigger wording when tighter routing is needed.

Risk: Generated plans, workflow changes, code snippets, or shell commands may be incomplete or incorrect for a user's environment.

Mitigation: Review outputs against the stated assumptions and validation checks before applying them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Proactive Agent demand signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [Ontology demand signal](https://clawhub.ai/skills/ontology)
- [Ask HN workflow demand signal](https://news.ycombinator.com/item?id=48979474)
- [Coding skills development demand signal](https://news.ycombinator.com/item?id=48974093)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, constraints, validation checks, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
