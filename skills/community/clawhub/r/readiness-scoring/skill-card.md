## Description:

Build an account readiness score that rises with fresh engagement signals, decays as they age, and alerts a team when an account crosses its threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and revenue operations teams use this skill to adapt an account readiness scoring workflow to their Cargo project and route accounts that cross a chosen threshold to Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes an unpinned command to install another skill.

Mitigation: Verify that skill and pin it to a reviewed version before use.

Risk: Deployment could remove unrelated columns and data from shared models.

Mitigation: Inspect existing shared-model columns and confirm the deployment preserves those still needed before deploying.

## Reference(s):

- [Readiness scoring README](README.md)
- [Run guide](references/run.md)
- [Signal weighting guide](references/weights.md)
- [ClawHub release](https://clawhub.ai/cargo-ai/skills/readiness-scoring)
- [Publisher project homepage](https://github.com/getcargohq/gtm-skills)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Operational guidance]

**Output Format:** [Markdown with TypeScript examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific configuration requires adaptation before deployment.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
