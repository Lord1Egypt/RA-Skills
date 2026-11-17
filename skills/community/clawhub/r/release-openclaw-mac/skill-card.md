## Description:

Run or recover OpenClaw macOS release signing, notarization, appcast, and asset promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to validate, sign, notarize, publish, or recover stable OpenClaw macOS releases and their appcast assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release instructions treat an explicit stable or full release request as authorization for macOS publication without separate consent, and the security evidence says some referenced paths were unavailable to the scan.

Mitigation: Confirm the release scope and current environment policy, and review the release instructions and any unavailable referenced files before running signing, notarization, or promotion steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/release-openclaw-mac)
- [Publisher profile](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
