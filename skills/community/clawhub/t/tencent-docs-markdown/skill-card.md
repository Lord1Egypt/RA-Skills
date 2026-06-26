## Description: <br>
腾讯文档 Markdown 技能，支持新建 Markdown 并写入内容、下载、删除、读取、更新、重命名等操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate Tencent Docs Markdown workflows, including creating, reading, downloading, updating, renaming, deleting, and inspecting Markdown documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires reusable Tencent Docs account cookies that function as sensitive account credentials. <br>
Mitigation: Use a dedicated automation account where possible, keep .cookies.json private, and run logout or delete the cookie file when finished. <br>
Risk: Update, delete, and rename operations can change or remove user documents. <br>
Mitigation: Verify the target document URL and title before proceeding, and avoid -y/--yes unless the operation has already been reviewed. <br>
Risk: Read and download operations can expose document content to the current agent session, terminal, or local files. <br>
Mitigation: Avoid using the skill with highly sensitive documents unless the execution environment and output handling are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/tencent-docs-markdown) <br>
- [Tencent Docs](https://docs.qq.com) <br>
- [Tencent Docs Desktop](https://docs.qq.com/desktop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python snippets; operations may return document URLs, metadata, document content, or local Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Docs account cookies for authenticated operations.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
