## Description:

Web scraping using Chrome + WebMCP. Primary method for all web crawling tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweihub](https://clawhub.ai/user/sweihub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape JavaScript-rendered web pages through Chrome and WebMCP, especially finance and news pages that may require browser interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a live Chrome session and interact with pages under the user's browser profile.

Mitigation: Use a dedicated Chrome profile without sensitive logins before invoking the skill.

Risk: Cleanup instructions may close browser tabs during broad scraping or search tasks.

Mitigation: Constrain the agent to tabs it opened and review tab-cleanup actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sweihub/skills/spider)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown guidance with inline commands and browser-action request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Chrome/WebMCP browser actions, scraping URLs, interaction steps, and cleanup steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
