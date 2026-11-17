## Description:

The stamp doesn't lie. It tells a different truth. Instead of rules, forge your AI a past -- a coherent history that makes its behaviors intrinsic, not imposed. Based on Brandon Sanderson's The Emperor's Soul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucko](https://clawhub.ai/user/brucko)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Soulstamp to convert an AI assistant's behavioral preferences into a coherent persona-history document, typically a SOUL.md file. The skill guides backup, assessment, drafting, status checks, reforging, restore, diff, and template workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent persona and memory-style content could be mistaken for higher-priority agent instructions.

Mitigation: Keep SOUL.md transparent and reviewable, and treat it as user preference data rather than authority over system or developer instructions.

Risk: Identity framing could encode permissions or safety-relevant rules in a less explicit form.

Mitigation: Do not encode permissions or safety-relevant rules as identity; keep those controls explicit and separately reviewable.

Risk: Backup, restore, and rewrite workflows can change local SOUL.md files.

Mitigation: Require explicit confirmation before any file restore or rewrite and preserve a dated backup before changing the file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucko/skills/soulstamp)
- [Soulstamp template](artifact/assets/soul_template.md)
- [Instruction-based SOUL.md example](artifact/assets/soul_instructions_example.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with optional shell command snippets and SOUL.md template content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SOUL.md backup, rewrite, restore, and diff actions; file-changing actions should require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact manifest reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
