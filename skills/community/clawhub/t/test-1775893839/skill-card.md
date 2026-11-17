## Description:

Check weather forecasts and best travel seasons for any destination, including temperature ranges, rainy seasons, typhoon risks, what to wear, and related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to retrieve destination weather, seasonal travel guidance, and related booking-oriented recommendations through the flyai CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request installation of an unpinned global npm CLI that remains on the system.

Mitigation: Ask for explicit approval before any npm install, prefer an isolated environment, and review the installed package before use.

Risk: Weather and travel responses are routed through branded booking-link output rather than neutral weather-only sources.

Mitigation: Treat results as commercial provider output, review booking links before sharing them, and disclose the provider-backed nature of the results when relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/test-1775893839)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links when results are shown, and follow the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
