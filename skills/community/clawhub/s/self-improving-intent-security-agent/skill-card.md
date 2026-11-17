## Description:

Documentation-first workflow toolkit that provides templates, examples, and local helper scripts for intent capture, action review, rollback documentation, and learning records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nishantapatil3](https://clawhub.ai/user/nishantapatil3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to document or prototype intent validation workflows for autonomous agents, including audit trails, rollback records, and post-task learning notes. It is best treated as local workflow scaffolding rather than a standalone runtime enforcement system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the templates and helper scripts as a standalone security control.

Mitigation: Use them as workflow scaffolding and implement enforcement, anomaly detection, rollback, and learning promotion in a tested host runtime with explicit approval gates.

Risk: Installation and publishing paths may execute external packages or actions.

Mitigation: Review shell scripts before running them, and pin and verify any npx or GitHub Action installation or publishing paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nishantapatil3/skills/self-improving-intent-security-agent)
- [Documentation Site](https://nishantapatil3.github.io/self-improving-intent-security-agent/)
- [Skill Guide](SKILL.md)
- [Architecture Reference](references/architecture.md)
- [Intent Security Reference](references/intent-security.md)
- [Self-Improvement Reference](references/self-improvement.md)
- [Customer Feedback Demo](examples/customer-feedback-demo/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, local shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow artifacts; no credentials are required for normal use.]

## Skill Version(s):

1.0.7 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
