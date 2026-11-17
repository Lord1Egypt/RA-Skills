## Description:

Security scanner for ClawHub skills from Gen Digital that looks up skill safety via the scan API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexshang](https://clawhub.ai/user/rexshang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to check the safety status of a ClawHub skill URL before recommending installation or use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill URLs are sent to Gen Digital's scan API for lookup.

Mitigation: Use the skill only when sharing the scanned ClawHub skill URL with that external API is acceptable.

Risk: The scan API verdict is advisory and may not catch obfuscated or novel threats.

Mitigation: Combine the result with sandboxing, least privilege, and manual review before using a skill.

## Reference(s):

- [Skillscanner on ClawHub](https://clawhub.ai/rexshang/skills/skillscanner)
- [rexshang ClawHub profile](https://clawhub.ai/user/rexshang)
- [Agent Trust Hub](https://ai.gendigital.com)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and status interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses scan API status and severity fields as advisory input.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
