## Description:

Make a video for your startup with Pexo by relaying a company, product, vision, or website brief to the hosted Pexo video agent, which writes the script, generates shots, selects models, and returns a publish-ready startup video with music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to help users create startup brand, company intro, homepage, fundraising deck, or social videos through Pexo's hosted video workflow. It is not positioned for paid ad campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Pexo API credentials and a configurable external endpoint.

Mitigation: Keep the config file permission-restricted, do not commit or sync ~/.pexo/config, and keep PEXO_BASE_URL set to https://pexo.ai unless the user intentionally changes it.

Risk: Startup plans, customer media, and generated video assets may be sensitive and can be cached locally.

Mitigation: Review whether uploaded content is appropriate for Pexo before use and remove sensitive cached files from ~/.pexo/tmp or PEXO_TMP_DIR after delivery.

Risk: The workflow can consume paid Pexo credits and may fail when credits or concurrent project limits are exhausted.

Mitigation: Check credit and entitlement errors before retrying, direct users to top up only when needed, and avoid duplicate chat calls while a project is waiting.

## Reference(s):

- [Pexo Homepage](https://pexo.ai)
- [ClawHub Skill Page](https://clawhub.ai/pexo/skills/startup-video)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON status interpretation, project links, and signed asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return project identifiers, preview choices, full signed media URLs, and local cache paths for downloaded assets.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
