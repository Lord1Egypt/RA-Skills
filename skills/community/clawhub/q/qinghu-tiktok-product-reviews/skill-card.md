## Description:

Helps agents retrieve collected TikTok Shop product reviews by product ID and summarize buyer feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to review collected TikTok Shop buyer comments for a specified product, including negative feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can install software globally or change the local shell environment.

Mitigation: Review setup steps before execution; prefer a preinstalled, pinned qhkit version and avoid automatic global installs or shell-profile changes.

Risk: The skill requires a Qinghu API token.

Mitigation: Provide the token only after confirming the vendor account and keep it out of shared outputs.

Risk: Review lookups consume paid credits, with charges varying by returned results.

Mitigation: Check the current estimate and obtain user consent before paid calls or large queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-reviews)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise review summaries with optional tabular exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review coverage depends on the vendor's collected data.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
