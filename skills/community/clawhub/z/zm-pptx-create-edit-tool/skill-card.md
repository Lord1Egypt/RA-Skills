## Description:

ZM PPTX 创建与编辑工具 guides agents through creating, inspecting, and editing Microsoft PowerPoint PPTX decks, including layout and template mapping, placeholders, notes, charts, and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and presentation-producing agents use this skill when a PPTX deck is the main deliverable and slide layout, template fidelity, notes, comments, charts, extraction, editing, or visual QA matter. It helps the agent inventory the deck, map content to actual placeholders, preserve the deck's visual language, and verify the final file before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may overwrite or edit the wrong presentation file if input and output paths are ambiguous.

Mitigation: Confirm input and output PPTX paths before work begins and keep backups of important decks.

Risk: A deck can pass command or text extraction checks while still containing clipped text, overlap, weak contrast, or leftover placeholders.

Mitigation: Render, open, or visually inspect the actual deck output and perform at least one fix-and-verify cycle before delivery.

Risk: Generated slides may include unverified branding, logos, QR codes, data screenshots, or chart semantics.

Mitigation: Use only provided or verified assets and review generated slides visually before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/zm-pptx-create-edit-tool)
- [Skill Homepage](https://clawic.com/skills/zm-pptx-create-edit-tool)
- [AI Readiness Checklist](checklists/ai_readiness_checklist.md)
- [Minimum Required Fields](templates/minimum_required_fields.md)
- [Subagent Execution Prompt](templates/subagent_execution_prompt.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files]

**Output Format:** [Markdown status summaries, optional code or shell commands, and generated or modified PPTX files when the agent performs deck work.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final status should be PASS, NEEDS_REVISION, or BLOCKED, with visual or parsing verification for deck outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact SKILL.md frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
