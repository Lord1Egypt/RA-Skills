## Description:

Make a SaaS demo or explainer video with Pexo by relaying a software description, app URL, or screenshot to Pexo so it can write the script, generate visuals, select models, add narration and captions, and return a publish-ready video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create SaaS demo, explainer, onboarding, landing-page, or sales videos through Pexo's hosted video agent. The agent creates projects, uploads approved assets, sends the user's request, polls status, and returns project or final asset links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Pexo API keys and local configuration.

Mitigation: Keep PEXO_BASE_URL set to https://pexo.ai, protect ~/.pexo/config with user-only permissions or a safer secret store, and run setup diagnostics before use.

Risk: The skill can upload SaaS descriptions, screenshots, and local files to Pexo.

Mitigation: Use it only for SaaS material approved for sharing with Pexo, and avoid uploading files or screenshots that contain secrets or sensitive data.

Risk: Generated projects, asset downloads, and project state are handled by an external hosted service.

Mitigation: Review Pexo output before publication, monitor long-running jobs, and avoid exposing signed asset URLs beyond the intended recipient.

## Reference(s):

- [Pexo](https://pexo.ai)
- [ClawHub Skill Page](https://clawhub.ai/pexo/skills/saas-video)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON script responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return project IDs, asset IDs, project links, status JSON, signed asset URLs, and local downloaded asset paths.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
