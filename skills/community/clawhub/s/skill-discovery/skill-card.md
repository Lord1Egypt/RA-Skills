## Description:

Discovers and recommends skills from user intent, searches skills.sh and ClawHub, validates candidates, and returns a user-confirmed installation recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caocong1](https://clawhub.ai/user/caocong1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to discover relevant agent skills for natural-language task requests, compare candidate quality, and receive an installation command or dry-run recommendation for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and remove global skills.

Mitigation: Use dry-run or recommendation mode unless you explicitly intend global modifications, and review the proposed installation or removal before approving it.

Risk: Registry or installer tooling may introduce unreviewed third-party skill content.

Mitigation: Prefer pinned and reviewed installer tooling, review the recommended skill before deployment, and scan skills before installing them.

Risk: Discovery logs and backup files may retain local information.

Mitigation: Avoid putting secrets in discovery prompts, review log and backup paths, and do not set TRASH_DIR to a directory containing data you cannot afford to lose.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caocong1/skills/skill-discovery)
- [Project Homepage](https://github.com/caocong1/skill-discovery)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown-style recommendation text and JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate skills, selected skill metadata, outcome fields, and installation commands.]

## Skill Version(s):

2.2.1 (source: CHANGELOG, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
