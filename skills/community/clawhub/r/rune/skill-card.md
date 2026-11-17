## Description:

Self-improving AI memory system with intelligent context injection and adaptive learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebobloblaw](https://clawhub.ai/user/thebobloblaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Rune to give agents persistent memory, context injection, task recommendations, and adaptive workflow behavior across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent workflow hooks and changes OpenClaw workspace behavior.

Mitigation: Review the HEARTBEAT.md changes and generated workflow files before installation, and avoid --force unless the changes have already been checked.

Risk: Selected documents or extracted context can be sent to cloud AI providers when cloud engines are configured.

Mitigation: Prefer Ollama or local-only operation for sensitive files, and configure cloud API use only after reviewing the data flow.

Risk: The bundled uninstaller may not fully clean up current Rune artifacts.

Mitigation: After uninstalling, manually verify removal of Rune files, hooks, and local memory data that should no longer persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thebobloblaw/skills/rune)
- [README](README.md)
- [Security Information](SECURITY.md)
- [Integration Guide](INTEGRATION-GUIDE.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands, shell snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory guidance and installable workflow integration; runtime commands may create or update local files in the user's OpenClaw workspace.]

## Skill Version(s):

1.1.5 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
