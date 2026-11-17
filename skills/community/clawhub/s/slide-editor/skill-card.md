## Description:

A browser-based visual editor for HTML presentations that can inject an offline editor, expose agent-controllable slide editing APIs, and export edited HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtacheng](https://clawhub.ai/user/dtacheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation authors, and AI agents use this skill to add a browser-based editor to HTML presentations, manipulate slides and elements through a visual UI or JavaScript API, and export clean edited HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and open workflows create avoidable command-execution risk.

Mitigation: Review before installing, avoid curl|bash or PowerShell iex Bun installation commands, and avoid --open on files with untrusted names until the shell execution path is fixed.

Risk: Injected or exported presentations can be active JavaScript-bearing HTML documents.

Mitigation: Work on copies, inspect exported HTML before sharing, and open generated presentations only in trusted contexts.

Risk: The injector can modify the source presentation file in place.

Mitigation: Use a separate output path or a backup copy when editing valuable presentations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dtacheng/skills/slide-editor)
- [Publisher profile](https://clawhub.ai/user/dtacheng)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and JavaScript API examples; runtime output is edited or exported HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inject JavaScript into presentation HTML and may export active JavaScript-bearing HTML documents.]

## Skill Version(s):

0.2.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
