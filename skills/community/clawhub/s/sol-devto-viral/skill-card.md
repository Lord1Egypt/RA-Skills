## Description:

Dev.to viral engine for mining trending AI stories, preparing contextual promotional comments, and cross-posting blog content to dev.to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to support dev.to growth workflows by finding trending AI articles, preparing contextual outreach copy, and publishing adapted Jekyll blog posts through the dev.to API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes automated public publishing to dev.to.

Mitigation: Use a dedicated dev.to API key, confirm the posting account, and require preview plus explicit approval before publishing.

Risk: The skill describes a daily launchd schedule.

Mitigation: Install scheduling only after review and document clear disable steps before enabling recurring execution.

Risk: The setup references API keys and source-level secret handling.

Mitigation: Keep API keys outside source code and use environment or secret-store injection with least-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-devto-viral)
- [Publisher profile](https://clawhub.ai/user/amrree)
- [sol-skills-bundle source link from artifact](https://github.com/TheSolAI/sol-skills-bundle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and text guidance with code, shell commands, configuration details, and log file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates dev.to trend, advertising, and cross-post tracking logs when executed in the expected environment.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
