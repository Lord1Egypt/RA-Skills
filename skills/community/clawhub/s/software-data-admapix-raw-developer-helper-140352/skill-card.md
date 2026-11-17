## Description:

Helps agent users, skill authors, maintainers, and teams adapt AdMapix-style workflows for bug fixing, setup hardening, reliability improvements, safety review, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn AdMapix-style workflow demand into practical implementation help, checklists, analysis, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger keywords such as data, raw, and layer may cause the skill to activate for unrelated software tasks.

Mitigation: Review or narrow trigger keywords before relying on implicit invocation.

Risk: The skill provides workflow, analysis, code, and command guidance that may be incorrect or unsuitable for a specific project context.

Mitigation: Review proposed changes and run the included verification steps before applying outputs in production.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-admapix-raw-developer-helper-140352)
- [AdMapix Demand Signal](https://clawhub.ai/skills/admapix)
- [Ontology Demand Signal](https://clawhub.ai/skills/ontology)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Airlock Service Issue](https://github.com/fips-agents/agent-template/issues/230)
- [MFA Setup and Status Panel Issue](https://github.com/peterrichards-lr/lfr-tunnel/issues/401)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, required inputs, remaining risks, and follow-up work when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
