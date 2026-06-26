## Description: <br>
Prepare and publish a local skill to ClawHub and GitHub using a workflow that keeps the local publish directory clean. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zackz2025](https://clawhub.ai/user/zackz2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare, clean, publish, and back up local agent skills on ClawHub and GitHub while preserving a minimal local publishing directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can expose sensitive content or unintended project details. <br>
Mitigation: Review the target directory, git diff, repository, account identity, version, changelog, and sensitive-content sweep before approving a release. <br>
Risk: Credential handling during GitHub or ClawHub publishing can expose long-lived tokens. <br>
Mitigation: Prefer browser login, SSH, or a credential manager, and do not paste or store long-lived tokens in chat or files. <br>
Risk: Git operations may overwrite or rewrite public repository history. <br>
Mitigation: Inspect remote state and require explicit confirmation before any force-push or destructive history operation. <br>


## Reference(s): <br>
- [Publish Checklist](references/publish-checklist.md) <br>
- [ClawHub Listing](https://clawhub.ai/zackz2025/publish-to-clawhub) <br>
- [Publisher Profile](https://clawhub.ai/user/zackz2025) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets and file-change recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits, publish commands, git commands, and safety checks for user review before execution.] <br>

## Skill Version(s): <br>
2.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
