## Description:

Use Serena-backed semantic code navigation and editing when working in existing software projects with non-trivial structure, especially multi-file repos where symbol-aware lookup and targeted edits are more reliable and token-efficient than brute-force file reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanclaw](https://clawhub.ai/user/juanclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to apply Serena's semantic project navigation, reference tracing, and symbol-scoped editing workflows in existing software repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow permits project-context shell execution or raw passthrough only as advanced escape hatches.

Mitigation: Review shell or passthrough actions before approval and prefer the normalized Serena tools for routine navigation and edits.

Risk: Ambiguous or failed semantic lookup can lead to edits that were not actually confirmed by Serena.

Mitigation: Disambiguate by path or additional lookup, explain Serena failures, and fall back to the smallest reliable file-based read or edit scope.

## Reference(s):

- [Integration patterns](references/integration-patterns.md)
- [ClawHub skill page](https://clawhub.ai/juanclaw/skills/serena-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with tool names, ordered workflows, and prompt patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for agents; it does not include executable code.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
