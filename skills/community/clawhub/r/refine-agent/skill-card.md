## Description:

REFINE is an adaptive skill engine for structured session diagnostics, local error-pattern memory, feedback capture, and optional system prompt patch synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use REFINE to capture sanitized diagnostic labels and exception summaries across sessions, then review locally generated prompt-patch guidance for recurring failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local diagnostics may contain feedback labels and exception-message text.

Mitigation: Avoid passing secrets, raw prompts, customer data, or attacker-controlled error text into the skill; review local diagnostics before reuse.

Risk: Stored error messages can influence generated system prompt patch guidance.

Mitigation: Human-review and sanitize generated patch_body content before adding it to any system prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dttnpole-commits/skills/refine-agent)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Python return values and plain text or Markdown patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local diagnostic memory and, in PRO mode, produce patch_body text for human review before prompt use.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
