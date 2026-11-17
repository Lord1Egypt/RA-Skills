## Description:

Read Figma design context from Multica issue figma_urls without Figma MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianyu-cursor](https://clawhub.ai/user/xianyu-cursor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repair agents use this skill when Multica issue data includes Figma URLs and they need grounded design context before changing UI code. It collects Figma node data, screenshots, style information, Code Connect clues, and artifact summaries for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Issue metadata can steer artifact writes and deletion outside the intended output folder.

Mitigation: Use the skill only with trusted Multica issue JSON until path handling is fixed, and review generated artifact paths before relying on the output.

Risk: The skill reads Figma credentials and contacts Figma APIs.

Mitigation: Use least-privilege Figma credentials, keep tokens out of logs and repair notes, and review generated artifacts for accidental credential exposure.

Risk: The skill writes .multica artifacts and updates .git/info/exclude in the repair repository.

Mitigation: Run it in a controlled repair workspace and confirm .multica/figma-context/ and .multica/tmp/ remain uncommitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xianyu-cursor/skills/templates)
- [Output Schema](references/output-schema.md)
- [Repair Expert Usage](references/repair-expert-usage.md)
- [Code Connect Rules](references/code-connect-rules.md)
- [Node Expansion Rules](references/node-expansion-rules.md)
- [Style Extraction Checklist](references/style-extraction-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, CSS, image, and manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Figma context artifacts are intended for local repair workflow review and should not be committed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact manifest reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
