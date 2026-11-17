## Description:

Reviews, evaluates, and provides structured feedback on master's and doctoral theses across multiple disciplines, covering academic quality, writing quality, formatting, data analysis, and academic integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Students, supervisors, and academic reviewers use this skill to convert a thesis document into Markdown and generate a structured review report with chapter-level findings, severity markers, discipline-specific checks, and prioritized revision guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently self-update during use, allowing review behavior to change without clear user approval.

Mitigation: Install and review a pinned version, or remove or disable the auto-update section before use.

Risk: Converted thesis text and review reports may be written beside sensitive or unpublished thesis documents.

Mitigation: Run the skill in a controlled working folder with appropriate access controls for thesis data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/thesis-reviewer)
- [Agent Skills format](https://agentskills.io)
- [OpenAI Codex sidecar](artifact/agents/openai.yaml)
- [Review checklist](artifact/checklist.md)
- [Review output template](artifact/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review reports and concise interactive guidance, with shell commands only for document conversion or skill maintenance steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces converted thesis Markdown and draft or final review Markdown files beside the source thesis document when used as described.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
