## Description:

Detect config drift between required local env keys and a Render service before deploy; fails when required keys are missing remotely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and deployment engineers use this skill before deploying a Render service to compare required local environment keys against the keys configured remotely and block deploys when required keys are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Render API key could be sent to an arbitrary API base URL if RENDER_API_BASE_URL is set.

Mitigation: Run the skill only in trusted environments, keep RENDER_API_BASE_URL unset or pinned to Render's real API endpoint, and use a narrowly scoped Render token where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/render-deploy-diff)
- [Render API endpoint used by the skill](https://api.render.com/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal output with drift summaries and exit status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 0 when all required keys exist on Render and exit code 1 when required keys are missing or inputs are invalid.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
