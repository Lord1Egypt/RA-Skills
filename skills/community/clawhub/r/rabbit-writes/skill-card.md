## Description:

Write, edit, or audit prose in a specific person's saved voice, or strip machine-writing patterns when there is no voice to apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, edit, audit, and rewrite prose in a configured voice while preserving source facts. It also reports machine-writing and prompt-injection patterns as signals, not proof of authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional model-backed rewrite mode can send selected document passages and a Rabbit-scoped credential to a configured endpoint.

Mitigation: Before using --apply-model, review .rabbit-model, base_url, and api_key_env, or provide an explicit trusted endpoint and credential.

Risk: Related host integration tooling can install persistent Claude Code hook and output-style behavior.

Mitigation: Review any hook or output-style installation separately, and prefer dry-run output before enabling host integration.

Risk: Machine-writing and authorship signals can produce false positives or be misused as attribution proof.

Mitigation: Use findings as pattern reports with quoted spans and fixes; do not use them for academic-integrity, hiring, or authorship decisions.

## Reference(s):

- [Rabbit Writes ClawHub page](https://clawhub.ai/whit3rabbit/skills/rabbit-writes)
- [Security notes](SECURITY.md)
- [Checklist](references/checklist.md)
- [Craft guidance](references/craft.md)
- [False positives guidance](references/false-positives.md)
- [Injection handling](references/injection.md)
- [Pattern catalog](references/patterns.md)
- [Voice guidance](references/voice.md)
- [Simplified Technical English guidance](references/ste.md)
- [rwlib API](scripts/rwlib/API.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with prose, findings, rewritten text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit files in place when the user asks for rewrite modes that support writing.]

## Skill Version(s):

0.5.0 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
