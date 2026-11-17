## Description:

Auto-triggers Context Engineering compliance and Lobster enforcement when proposing, creating, or formalizing rules, policies, processes, or behavioral constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to persist newly proposed rules, policies, and behavioral constraints into governance files, optionally creating Lobster enforcement workflows when the rule meets CR-012 criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers can cause persistent governance files to be changed without confirmation.

Mitigation: Enable the skill only where automatic rule persistence is desired, require human review before relying on new governance entries, and restrict allowed write destinations.

Risk: Rule text is treated as trusted input and can be written into Markdown or workflow configuration.

Mitigation: Review and sanitize rule names and descriptions before enabling generated docs or Lobster workflows.

Risk: Unsafe file or script handling may affect local agent configuration.

Mitigation: Run in a controlled workspace, review generated files before deployment, and avoid use until confirmation gates and destination allowlists are in place.

## Reference(s):

- [Rule Creation ClawHub release page](https://clawhub.ai/levineam/skills/rule-creation)
- [Context Engineering source post](https://x.com/koylanai/status/2025286163641118915)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON script results, governance-file entries, and optional Lobster workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append to governance files and generate workflow configuration when enforcement is available.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
