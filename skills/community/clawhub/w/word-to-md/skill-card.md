## Description:

Convert Word documents (.docx and .doc) to clean Markdown using the MinerU API and mineru-open-api CLI, preserving headings, lists, tables, images, and code blocks where supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to convert Word documents into Markdown for Git repositories, static sites, blogs, and documentation migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion workflow relies on mineru-open-api and the MinerU service, so selected Word document contents may leave the local machine.

Mitigation: Use the skill only for documents approved for that provider, and avoid sensitive, proprietary, or regulated files unless organizational review permits it.

Risk: Installing mineru-open-api globally can affect the user's command-line environment.

Mitigation: Prefer a pinned or project-local installation when environment isolation or reproducibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veeicwgy/skills/word-to-md)
- [MinerU API token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and concise Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create output directories such as ~/MinerU-Skill/<name>_<hash>/ when following the artifact workflow.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
