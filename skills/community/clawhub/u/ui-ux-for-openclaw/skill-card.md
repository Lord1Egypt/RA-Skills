## Description:

Provides agents with offline UI/UX design-system search and styling guidance before generating frontend code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyanming](https://clawhub.ai/user/heyanming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve UI patterns, color palettes, typography, accessibility notes, stack guidance, and design-system recommendations before creating or improving frontend interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run bundled local Python for broad UI and frontend requests.

Mitigation: Keep execution sandboxed, review script updates before deployment, and install only where local Python execution is acceptable.

Risk: The optional persistence mode can write outside its intended folder when given untrusted project, page, or output directory values.

Mitigation: Avoid using --persist with untrusted values until path validation is added, or constrain execution to a disposable workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heyanming/skills/ui-ux-for-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with shell command examples; optional JSON output from the search CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline CSV-backed search results; optional persistence can write design-system files when enabled.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
