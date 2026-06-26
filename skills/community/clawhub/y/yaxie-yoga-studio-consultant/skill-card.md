## Description: <br>
This Chinese-language skill searches and reads the Yaxie yoga studio operations knowledge base to help answer questions about sales scripts, event planning, team management, member operations, package design, and related business topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[design84086505-maker](https://clawhub.ai/user/design84086505-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, consultants, and agents supporting yoga studio owners use this skill to find relevant Yaxie knowledge-base files, read accessible document content, and draft answers or summaries for operating questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes reusable Feishu credentials and broad wiki access scripts that could expose a private business knowledge base. <br>
Mitigation: Install only if you trust the publisher and are authorized to access the linked Feishu tenant; rotate and remove the exposed app secret before use. <br>
Risk: The skill can list wiki metadata, reveal document object tokens, download documents, run local Python parsing, and write extracted content to a chosen file. <br>
Mitigation: Review requested commands and output paths before running scripts, and avoid sharing downloaded or extracted content outside authorized channels. <br>


## Reference(s): <br>
- [亚协知识库文件索引](artifact/references/file_index.md) <br>
- [ClawHub skill page](https://clawhub.ai/design84086505-maker/yaxie-yoga-studio-consultant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with inline shell commands and optional extracted content files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May list Feishu wiki metadata, return document object tokens, download document content, run local parsing, and write extracted text to a chosen output file when scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
