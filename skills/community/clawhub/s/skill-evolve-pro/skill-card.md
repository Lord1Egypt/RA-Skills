## Description:

Skill Evolve Pro analyzes failed skill trajectories, generates targeted skill-document edits, gates proposed changes, and can parse session state into rollout evidence for iterative skill improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to improve agent skill documents from failed rollout or session-state evidence. It produces candidate patches, validation results, and update guidance before active skill files are changed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill can send skill and session data to DeepSeek.

Mitigation: Use only non-sensitive skills and rollout data, redact private session state before use, and confirm that external-provider processing is approved.

Risk: The security review reports an exposed DeepSeek key in the release artifact.

Mitigation: Rotate the exposed key, remove hard-coded secrets, and supply API credentials through environment variables.

Risk: The security review reports that model-generated changes can be persisted to active skill files without enforcing the documented user confirmation.

Mitigation: Require manual diff review and explicit approval before allowing the skill to overwrite any active SKILL.md.

## Reference(s):

- [ClawHub Skill Evolve Pro listing](https://clawhub.ai/pengpengliu1212-art/skills/skill-evolve-pro)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text reports with JSON-like patch data, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to SKILL.md and write rollout or state files when run with configured workspace paths.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
