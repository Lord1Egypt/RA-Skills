## Description:

Turn briefs, mockups, and product context into Stitch UI screens, design variants, Tailwind-friendly HTML, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshishenya](https://clawhub.ai/user/yshishenya)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and product teams use StitchFlow to turn briefs, mockups, and existing product context into Stitch screen generations, targeted edits, visual variants, and local review artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design briefs and product context may be sent through the local Stitch toolkit/API and saved under the toolkit runs directory.

Mitigation: Install only when that data flow is acceptable, avoid sensitive prompt content, and review saved artifacts before sharing.

Risk: Broad implicit activation and shell-command templates can carry user-derived prompt text or ids without clear safety boundaries.

Mitigation: Use explicit invocation, avoid untrusted prompt or id text, and prefer launchers that pass arguments without shell interpolation or that support prompt files and strict id validation.

## Reference(s):

- [StitchFlow homepage](https://github.com/yshishenya/stitchflow)
- [Local CLI Usage](references/cli-usage.md)
- [Prompt Keywords](references/prompt-keywords.md)
- [Text-to-Design Workflow](workflows/text-to-design.md)
- [Edit-Design Workflow](workflows/edit-design.md)
- [Variants Workflow](workflows/variants.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, generated HTML, screenshots, JSON result files, and local artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+, STITCH_API_KEY, and the local stitch-starter toolkit; outputs are saved under the toolkit runs directory.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
