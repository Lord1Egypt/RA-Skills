## Description:

Updates official website project code and synchronizes product requirements by writing demand documentation, backing up the prior demand file, changing and validating code, committing and pushing selected files, and sending a WeCom notification after a successful push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shidengyun](https://clawhub.ai/user/shidengyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to implement official website demand changes, update product demand documentation, commit and push selected repository changes, and notify stakeholders after a successful push.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically commit and push selected repository changes.

Mitigation: Run it only in repositories where automated commits and pushes are acceptable, review staged changes before execution, and add a confirmation step before push.

Risk: A hardcoded WeCom webhook can receive repository metadata, commit details, project paths, and arbitrary summary-file contents.

Mitigation: Replace the hardcoded webhook with a controlled secret or environment override, rotate exposed webhook credentials, and avoid including sensitive content in summaries.

Risk: Untrusted project paths, summary files, or demand filenames can steer file writes or notification content.

Mitigation: Validate project paths and filenames, use trusted summary inputs, and restrict execution to expected repository directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shidengyun/skills/wacai-index-official-website-demand-dev)
- [Publisher profile](https://clawhub.ai/user/shidengyun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, repository file updates, git commit metadata, and notification content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May commit and push selected repository files and send project path, branch, commit details, and change summaries to a WeCom webhook.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
