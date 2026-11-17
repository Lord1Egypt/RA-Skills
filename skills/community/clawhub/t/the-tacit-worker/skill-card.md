## Description:

A unified AI Engineering Operating System that helps agents extract tacit knowledge, structure an Agent OS, and run pre-deployment governance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to interview domain experts, turn the resulting tacit knowledge into structured agent operating files, and review the agent before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verification workflow can read and reveal snippets from local files when pointed at arbitrary paths.

Mitigation: Run verification only inside a dedicated output workspace and restrict reviewed paths to expected agent artifacts.

Risk: The self-improving loop proposes persistent updates to frameworks, templates, and governance checklists.

Mitigation: Require human review before persisting template, framework, or checklist changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielfoojunwei/skills/the-tacit-worker)
- [SECI Externalization Interview Framework](references/extraction_framework.md)
- [Agent OS Architecture Guide](references/os_architecture_guide.md)
- [Pre-Deployment Governance Checklist](references/governance_checklist.md)
- [Verify Action Protocol](scripts/verify_action.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tacit knowledge profiles, Agent OS files, audit reports, and verification guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
