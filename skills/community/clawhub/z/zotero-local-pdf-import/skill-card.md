## Description: <br>
通过 Zotero 本地连接器将用户指定的本地 PDF 文件或文件夹导入 Zotero 文库，并支持选择已有分类、列出分类和检查最近导入附件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, students, and knowledge workers use this skill to ask an agent to import local PDFs into Zotero through the local connector. It is useful for single-file imports, folder imports, imports into an existing Zotero collection, collection listing, and recent-attachment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes a user's Zotero library by importing selected PDFs. <br>
Mitigation: Confirm the Zotero port, target collection, PDF paths, folder path, and recursive setting before running imports. <br>
Risk: The doctor command may install the Python requests dependency automatically. <br>
Mitigation: Use a virtual environment or preinstall requests manually when tighter dependency control is required. <br>
Risk: Diagnostic and check output can expose document titles or local filesystem paths. <br>
Mitigation: Avoid sharing command output when local paths or document titles are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mxingchtongaelofficial2568/zotero-local-pdf-import) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require a user-provided Zotero local connector port and explicit PDF file or folder paths.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
