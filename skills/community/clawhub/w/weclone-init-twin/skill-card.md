## Description:

Scaffold a digital twin persona directory with markdown templates such as profile, state, persona examples, and guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xming521](https://clawhub.ai/user/xming521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize or refresh local digital-twin persona files before using a reply-generation workflow. It creates starter profile, state, reply example, and guardrail templates in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated persona files may contain private or sensitive personal details once filled in by the user.

Mitigation: Keep the generated ai_twin files private and leave sensitive fields blank unless they are truly needed.

Risk: Using force overwrite can replace existing persona files.

Mitigation: Use --force only when the user explicitly intends to regenerate or replace existing files.

Risk: Writing persona files into a directory controlled by untrusted users can expose or tamper with generated content.

Mitigation: Run the initializer only against directories the user trusts and controls.

## Reference(s):

- [weclone-init-twin ClawHub listing](https://clawhub.ai/xming521/skills/weclone-init-twin)
- [xming521 ClawHub profile](https://clawhub.ai/user/xming521)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown setup handoff with created file paths and next-step guidance; scaffolded persona files are Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates profile, state, persona_examples, and guardrails templates; supports English and Chinese templates and requires explicit approval before overwriting existing files.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
