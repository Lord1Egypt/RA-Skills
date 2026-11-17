## Description:

VolcEngine Video lets agents submit text-to-video generation requests to VolcEngine and query task status and result URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzbpaq123](https://clawhub.ai/user/zzbpaq123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create AI videos from text prompts through VolcEngine and to check submitted generation tasks for completion and output URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts and task IDs to an external paid VolcEngine API.

Mitigation: Review prompts before use and avoid sending private, proprietary, or personal information unless VolcEngine processing is intended.

Risk: The skill asks users to store VolcEngine API credentials in a local config.json file.

Mitigation: Use a dedicated low-privilege VolcEngine key with quotas, keep secrets out of the skill directory where possible, and do not commit or share config.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzbpaq123/skills/volcengine-video)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command-line usage and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task IDs for submitted videos and task status or video URLs for completed jobs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
