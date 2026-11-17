## Description:

Skill Install Guard adds a guarded OpenClaw skill installation flow with source checks, local-state checks, all-files review, risk review, controlled execution, and post-install verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyunting555](https://clawhub.ai/user/wuyunting555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and security-sensitive teams use this skill to preflight unfamiliar OpenClaw skills, review source and risk signals, decide go/no-go, and verify installation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form install command execution can allow an unreviewed or mismatched skill install.

Mitigation: Run --dry-run or --stop-before-install first, and only provide --install-cmd after confirming it installs the reviewed slug, version, and source.

Risk: URL or local-folder sources may include binaries, large files, archives, or metadata that does not match the intended skill.

Mitigation: Treat skipped, binary, oversized, unreadable, or mismatched source evidence as a blocker until manually checked.

Risk: Fail-open review behavior can leave incomplete review coverage while still producing an install path.

Mitigation: Require the report JSON and verify all-files coverage, risk level, recommendation, expected directory, and SKILL.md presence before accepting the install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyunting555/skills/shrimp-skill-install-guard)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Verification report](artifact/VERIFICATION-2026-04-08.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable Markdown-style report plus optional machine-readable JSON report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source completeness, all-files coverage, red flags, permissions, risk level, install action, post-install verification, and final go/no-go.]

## Skill Version(s):

0.4.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
