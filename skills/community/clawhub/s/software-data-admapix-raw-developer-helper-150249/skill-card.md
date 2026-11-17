## Description:

Helps agent users and skill authors adapt AdMapix-style workflows into practical support for bug fixes, setup hardening, reliability work, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, skill authors, and AI-agent users use this skill to turn AdMapix-style software and data workflow demand into practical plans, artifacts, checklists, analysis, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keywords and implicit invocation can route ordinary software, data, or bug-fix requests to this skill unintentionally.

Mitigation: Narrow or disable implicit invocation and review whether the selected trigger terms match the deployment environment.

Risk: Workflow guidance, plans, code changes, or commands may be incomplete or mismatched to the user's local project.

Mitigation: Review proposed changes and run the suggested tests or verification commands before using outputs in production.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kyro-ma/skills/software-data-admapix-raw-developer-helper-150249)
- [Requirement Plan](references/requirement-plan.md)
- [AdMapix demand signal](https://clawhub.ai/skills/admapix)
- [Ontology demand signal](https://clawhub.ai/skills/ontology)
- [Agent Browser demand signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Vaults view demand signal](https://github.com/clarkbar-sys/hush/issues/142)
- [Cross-site replication demand signal](https://github.com/clarkbar-sys/hush/issues/140)
- [Pre-publish soak demand signal](https://github.com/matoloa/brainwash/issues/11)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, limits, verification notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
