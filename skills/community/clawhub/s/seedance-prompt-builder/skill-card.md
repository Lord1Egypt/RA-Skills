## Description:

Builds, rewrites, audits, and troubleshoots prompts for Doubao Seedance 2.0 video generation and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juneliu1999](https://clawhub.ai/user/juneliu1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, rewrite, audit, and troubleshoot Seedance 2.0 prompts for text-to-video, referenced video, video editing, video extension, track completion, storyboard, subtitle, speech, and multimodal asset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer Seedance prompts toward Chinese wording unless English is requested.

Mitigation: Review language requirements before use and explicitly request English-only prompts for English-only workflows.

Risk: Using reference-video phrasing for edit or extension tasks can route the task incorrectly.

Mitigation: Use direct edit or extension phrasing such as strictly edit videoN or extend videoN, and run the prompt audit or linter for routing conflicts.

Risk: Generated prompts may still lead to unwanted subtitles, logos, identity drift, style drift, or continuity jumps in downstream video generation.

Mitigation: Add explicit constraints, define subjects consistently, use suitable reference assets, and review generated outputs before publication.

## Reference(s):

- [Official Guide](references/official-guide.md)
- [Task Routing](references/task-routing.md)
- [Prompt Formulas](references/prompt-formulas.md)
- [Troubleshooting](references/troubleshooting.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text or Markdown prompts and audits, with optional JSON issue reports from the prompt linter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prefer Chinese wording for Seedance unless English is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
