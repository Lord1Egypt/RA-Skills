## Description: <br>
Saves academic paper metadata, optional summaries, tags, and available arXiv PDFs to a Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mozisword](https://clawhub.ai/user/Mozisword) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers can use this skill to send paper records and related notes from an agent workflow into their Zotero library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime script contradicts the documented ZOTERO_CREDENTIALS setup and contains a credential-looking string. <br>
Mitigation: Change credential lookup to ZOTERO_CREDENTIALS and revoke or rotate any exposed Zotero key before installing or running the skill. <br>
Risk: The skill can perform persistent writes to a Zotero library, including creating items, adding AI-generated summary notes, and uploading arXiv PDF attachments. <br>
Mitigation: Run only with a Zotero account and API key intended for this workflow, review requested paper data before execution, and confirm created records in Zotero. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [ClawHub release page](https://clawhub.ai/Mozisword/zotero-myscholar) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell command examples and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS; may create Zotero items, notes, and uploaded PDF attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
