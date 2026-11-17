## Description:

Office Reader helps an agent read local Word, Excel, PowerPoint, PDF, Markdown, text, CSV, JSON, YAML, and HTML files and return extracted content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to inspect local document and data files they explicitly provide, including Office files, PDFs, and common text formats. It is useful for extracting readable content, summarizing document contents, and producing structured text, JSON, or Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local file paths supplied by the user, so it can expose document contents to the agent session.

Mitigation: Use it only with files intended for agent access and avoid passing sensitive paths unless that access is approved.

Risk: The release evidence notes a missing office-reader.ps1 implementation.

Mitigation: Review or obtain the script implementation before relying on scripted document parsing.

Risk: Dependency installation guidance is unpinned.

Mitigation: Install dependencies in a virtual environment and pin package versions for repeatable use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-office-reader)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, JSON, or Markdown, with PowerShell command examples where script execution is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may be limited by a maximum line count, with the documented default of 1000 lines.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
