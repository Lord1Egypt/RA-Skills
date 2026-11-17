## Description:

Render Mermaid diagrams as colored ASCII or Unicode text directly in terminals and Python applications without external rendering services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to render Mermaid diagrams in terminal-native contexts such as SSH sessions, CI logs, documentation generation, TUI applications, and Python workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer writes files under ~/.termaid and may overwrite or conflict with existing local Termaid examples or configuration.

Mitigation: Review or back up existing ~/.termaid files before running the installer.

Risk: The install flow resolves the Termaid package from the package index at install time.

Mitigation: Install in a virtual environment or other low-privilege context and pin and verify the Termaid package version for stronger supply-chain hygiene.

## Reference(s):

- [ClawHub Termaid skill page](https://clawhub.ai/smallnest/skills/termaid)
- [Termaid GitHub repository](https://github.com/fasouto/termaid)
- [Termaid PyPI package](https://pypi.org/project/termaid/)
- [Termaid online demo](https://termaid.com)
- [Mermaid.js documentation](https://mermaid.js.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python examples, configuration snippets, and terminal diagram text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ASCII-only or Unicode terminal output and optional colorized output when Termaid extras are installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
