## Description:

Work Work helps users format, check, and refine Chinese academic literature reviews, reference lists, and Word documents according to Chinese academic standards.

This skill is for research and development only.

## Publisher:

[xf280230439-netizen](https://clawhub.ai/user/xf280230439-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and academic writers use this skill to check literature reviews, validate citation and reference consistency, configure formatting rules, and generate Chinese academic Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-opening generated Word documents can launch shell behavior with user-influenced filenames.

Mitigation: Avoid untrusted or unusual filenames and disable or remove auto-open behavior before running the Word-generation path.

Risk: Deep reference verification can share reference metadata with Crossref.

Mitigation: Use --deep-check only when external metadata lookup is acceptable for the document being checked.

Risk: Filtering or renumbering references can change academic source lists and citation mappings.

Mitigation: Back up source files and manually review filtered or renumbered references before relying on the results.

## Reference(s):

- [Workwork Features Checklist](references/features_checklist.md)
- [Workwork Workflow Guide](references/workflow_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/xf280230439-netizen/skills/work-work)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, inline shell commands, YAML configuration, and generated Word documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts write report files or Word documents; reference filtering and renumbering workflows can modify source files.]

## Skill Version(s):

3.3.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
