## Description:

Records post-run outcome events, such as publication status, orders, impressions, clicks, revenue, and notes, for Yufluent Listing, SEO, and related skill runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and ecommerce operators use this skill to register seller-provided outcome metrics against a prior Yufluent run_id for effect tracking and attribution. It is intended for manual outcome recording, not automatic collection from marketplace backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API key and seller metrics, so misconfigured endpoints could expose sensitive operational data.

Mitigation: Use only trusted Yufluent endpoint configuration, keep TOKENAPI_KEY private, and review the outcome payload before submission.

Risk: The skill can load a local shared client path, so a compromised local skills/_shared directory could affect execution.

Mitigation: Install from trusted packages, inspect local shared files before deployment, and avoid running the skill from untrusted workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-record-outcome)
- [Yufluent homepage](https://claw.changzhiai.com)
- [OpenClaw application](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Plain text confirmation or JSON response from the outcome-recording command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; TOKENAPI_BASE_URL is optional and should point only to a trusted Yufluent endpoint.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
