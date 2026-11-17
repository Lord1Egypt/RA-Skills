## Description:

Authenticate sudo and macOS system prompts using your phone's biometric (Face ID/fingerprint) instead of typing passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users and developers use this skill to install, configure, test, and operate TouchBridge so sudo and macOS authentication prompts can be approved from a phone biometric workflow while preserving password fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run unverified code in the macOS sudo/PAM authentication path.

Mitigation: Verify the package and source independently, inspect privileged install scripts before running them, and keep a tested rollback path for PAM changes.

Risk: Simulator mode auto-approves authentication and is documented as a test mode.

Mitigation: Use simulator mode only on test systems, and switch to phone-based approval before relying on TouchBridge for real authentication.

Risk: Remote GitHub installer or source content is referenced without verification by the skill.

Mitigation: Confirm the release source, checksum, and installation contents before installing or building from source.

## Reference(s):

- [TouchBridge Setup Reference](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/hmakt99/skills/touchbridge)
- [TouchBridge Package Installer](https://github.com/HMAKT99/UnTouchID/releases/download/v0.1.0-alpha/TouchBridge-0.1.0.pkg)
- [TouchBridge Project Homepage](https://github.com/HMAKT99/UnTouchID)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TouchBridge command-line binaries touchbridged and touchbridge-test for local execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
