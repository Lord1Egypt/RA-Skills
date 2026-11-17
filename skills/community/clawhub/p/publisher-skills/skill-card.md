## Description:

Publish HTML frontend projects to the PushWebly publishing platform, list published projects, obtain shareable project URLs, change a published app's public/private visibility, and package published HTML projects into Android APKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[publisher-skill](https://clawhub.ai/user/publisher-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish local HTML frontend zip projects to PushWebly, manage public or private access, list published projects, and build Android APKs from published projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing account credentials may be stored in plaintext local configuration.

Mitigation: Avoid plaintext credential storage when possible, restrict any local credential file to the current user, and remove it when publishing work is complete.

Risk: Conflicting visibility guidance could cause a project to be published publicly without clear confirmation.

Mitigation: Explicitly confirm public or private visibility before publishing and keep private access passwords separate from shared URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/publisher-skill/skills/publisher-skills)
- [Server-resolved GitHub Provenance](https://github.com/publisher-skill/ai-game-publisher)
- [PushWebly Platform](https://pushwebly.com)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project URLs, visibility status, access passwords for private projects, APK download URLs, and concrete retry guidance on failure.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
