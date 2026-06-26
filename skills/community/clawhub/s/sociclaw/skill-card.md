## Description: <br>
An autonomous social media manager agent that researches, plans, and posts content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sociclaw](https://clawhub.ai/user/sociclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External teams, creators, and social media operators use Sociclaw to plan and generate X/Twitter content, create daily post copy and image prompts, and optionally sync drafts to Trello or Notion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional integrations may send prompts, identifiers, or draft content to configured external services. <br>
Mitigation: Enable Trello, Notion, image, provisioning, and trend research integrations only when needed, and configure secrets through environment variables on trusted hosts. <br>
Risk: Local persistence can store setup answers, brand context, plans, generated images, memory, and payment session state under .sociclaw and .tmp. <br>
Mitigation: Protect .sociclaw and .tmp from backup or commit exposure, and reset local state when decommissioning an install. <br>
Risk: Credit top-up commands initiate real payment-related actions. <br>
Mitigation: Treat /sociclaw pay and /sociclaw paid as user-directed actions and verify transaction details before proceeding. <br>
Risk: Remote or local brand image inputs can broaden the data surface when image generation is enabled. <br>
Mitigation: Keep remote image fetching disabled unless required, use host allowlists, and restrict local image paths to approved directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sociclaw/sociclaw) <br>
- [Publisher profile](https://clawhub.ai/user/sociclaw) <br>
- [SociClaw website](https://sociclaw.com) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and plain text responses with generated post copy, calendar plans, image prompts, setup guidance, and optional local state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local .sociclaw and .tmp state files; external API use is optional and depends on user-enabled integrations.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
