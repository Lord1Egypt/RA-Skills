## Description:

uStack tracks upstream agent frameworks, analyzes changes, classifies portability, and generates adapted output for agent runtimes across Claude Code, Codex, OpenClaw, Gemini CLI, Cursor, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggie-security](https://clawhub.ai/user/aggie-security)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use uStack to monitor upstream agent-native frameworks, inspect changes, and produce portable update artifacts for their chosen agent runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted inputs or local manifests could cause writes outside the intended workspace or unintended shell command execution.

Mitigation: Use uStack only on trusted repositories, validate identifiers and manifests, and review shell-safe git invocation before installation or automation.

Risk: Generated Markdown may be published with misleading or unsafe content if it is not reviewed.

Mitigation: Review generated Markdown before publishing and avoid elevated-permission automated update jobs.

## Reference(s):

- [uStack ClawHub skill page](https://clawhub.ai/aggie-security/skills/ustack)
- [gstack upstream framework](https://github.com/garrytan/gstack)
- [AGI.security](https://agi.security)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Guidance]

**Output Format:** [CLI output plus JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .ustack manifests, analysis reports, and update pages in the local workspace.]

## Skill Version(s):

0.1.0 (source: release evidence, package.json, CHANGELOG, released 2026-04-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
