## Description:

Typecho Publisher lets an agent manage Typecho blog posts with typecho-cli, including creating, listing, updating, deleting, and querying categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolingrabbit](https://clawhub.ai/user/coolingrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, blog operators, and external agents use this skill to publish and maintain Typecho blog content through a configured CLI while respecting existing categories and account-bound update/delete permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or permanently delete live blog content.

Mitigation: Require explicit confirmation before update or delete actions, verify article ownership and cid, and fetch the existing article before full-replacement updates.

Risk: Token handling can expose credentials if misconfigured.

Mitigation: Use only HTTPS Typecho URLs you control, avoid passing the token with --token, store configuration with restrictive permissions, and rotate the token if it may have been exposed.

Risk: Publishing can fail or target an unsuitable category when categories are assumed.

Mitigation: Run the categories command before publishing and select only an existing category, asking the user to create one manually when none fits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolingrabbit/skills/typecho-publisher)
- [CoolingRabbit Publisher Profile](https://clawhub.ai/user/coolingrabbit)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured HTTPS Typecho domain and an API token; CLI actions return JSON success or error results.]

## Skill Version(s):

4.1.1 (source: ClawHub release metadata; artifact SKILL.md reports 4.1.0 and plugin.json reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
