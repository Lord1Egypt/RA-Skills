## Description:

Generate high-quality, customizable AI prompts for creative writing, problem-solving, education, business, programming, Flutter development, and game development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helal-muneer](https://clawhub.ai/user/helal-muneer)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, educators, and business users use this skill to turn rough goals into structured prompts with role, task, context, constraints, and output expectations. It is especially useful for Flutter app and game development prompt templates, while also covering general writing, planning, learning, and marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts and downstream AI-generated code may be incomplete or unsafe for security-sensitive workflows such as authentication, payments, analytics, ads, or token handling.

Mitigation: Treat generated prompts and resulting code as drafts; review and test security-sensitive outputs before production use.

Risk: The artifact includes strong security claims that are broader than the visible Markdown-only implementation proves.

Mitigation: Use the Claw scan verdict and local artifact behavior as the security baseline, not unsupported claims in documentation.

Risk: Prompt templates can include user-provided context that may contain sensitive information.

Mitigation: Use placeholders for secrets and avoid placing passwords, API keys, personal data, or confidential business information in generated prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helal-muneer/skills/smart-prompt-generator)
- [README](artifact/README.md)
- [Flutter app templates](artifact/flutter_app_templates.md)
- [Flutter game templates](artifact/flutter_game_templates.md)
- [Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown prompt templates with optional code-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated prompts should be reviewed before use, especially for security-sensitive app or game features.]

## Skill Version(s):

1.0.0 (source: CHANGELOG.md, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
