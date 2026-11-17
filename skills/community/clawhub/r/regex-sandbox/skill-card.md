## Description:

Tests regular expressions against supplied text or a file, showing matches, captured groups, and optional replacement previews in text or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0 (release listing); MIT (code only); documentation all rights reserved

## Use Case:

Developers and other users can test and refine regex patterns, inspect captured groups, and preview substitutions without editing their application code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared Write access exceeds the needs of the local regex tester.

Mitigation: Review before installing and remove or justify Write access.

Risk: Documentation claims file-changing --apply behavior that the bundled tester does not support.

Mitigation: Correct the documentation and permissions to match the actual tool; do not rely on the claimed file-management safeguards.

## Reference(s):

- [Regex Sandbox on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/regex-sandbox)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Match spans and captured groups, with an optional replacement preview; exit status 0 for matches, 1 for no matches, and 2 for invalid patterns or arguments.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; bundled files say 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
