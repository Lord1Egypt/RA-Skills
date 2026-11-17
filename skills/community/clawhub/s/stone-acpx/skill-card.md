## Description:

Use the acpx CLI to run coding agents over the Agent Client Protocol (ACP) instead of PTY scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route coding work through ACP-compatible clients such as Codex, Claude Code, Gemini CLI, Pi, and OpenCode, and to inspect acpx commands, sessions, flags, workflows, and local runtime policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running npx acpx@latest may execute whatever acpx package version is current at that time.

Mitigation: Prefer the pinned plugin-local acpx runtime for normal use, and use npx acpx@latest only in an isolated, intentional upgrade-check context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/stone-acpx)
- [acpx upstream skill reference](https://raw.githubusercontent.com/openclaw/acpx/main/skills/acpx/SKILL.md)
- [acpx CLI documentation](https://raw.githubusercontent.com/openclaw/acpx/main/docs/CLI.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local binary-selection guidance and example acpx commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
