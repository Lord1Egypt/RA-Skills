## Description:

Helps developers prepare, publish, and check skills on SkillHub and ClawHub, including troubleshooting rejected uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and publish skills to SkillHub and ClawHub, inspect release status, and diagnose upload failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or deletion can change public marketplace listings using locally stored credentials without an enforced confirmation step.

Mitigation: Review a dry run and require explicit approval before publishing, removing listings, pushing to GitHub, or running ClawHub commands.

Risk: Upload troubleshooting includes WAF probing that could be used to preserve content a platform blocks.

Mitigation: Do not use WAF bisect results to evade platform security controls; remove blocked content or seek platform review.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/skillhub-publish-skill)
- [SkillHub publishing and CLI setup](artifact/references/cli-install.md)
- [ClawHub categories and topics](artifact/references/clawhub-catalog.md)
- [Upload rejection troubleshooting](artifact/references/waf-details.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Status reports]

**Output Format:** [Markdown with shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing actions may change public marketplace listings.]

## Skill Version(s):

1.7.6 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
