## Description:

Assists Chinese-language QCC teams with preparing presentation PPTs, speaker notes, project-material checks, and pre-presentation review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

QCC practitioners and quality teams use this skill to prepare project presentation materials from provided QCC artifacts, including PPT outlines, speaker drafts, artifact inventories, and pre-presentation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect user-provided project directories, documents, spreadsheets, and images, which may contain sensitive quality or operational data.

Mitigation: Provide only the intended QCC project materials and review generated PPT, speech, and report content before sharing.

Risk: Workflow execution may fail if referenced scripts or templates are absent from the installed package.

Mitigation: Confirm required scripts, templates, Python 3.9+, and dependencies are available before running generation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-qcc-activity-assistant)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-qcc-activity-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with optional YAML outline content and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of PPTX, speech drafts, completeness reports, review reports, and archives when the required QCC materials and local resources are available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
