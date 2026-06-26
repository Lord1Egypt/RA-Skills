## Description: <br>
将论文和摘要保存到 Zotero 文库。需配置 ZOTERO_CREDENTIALS 环境变量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GottenZZP](https://clawhub.ai/user/GottenZZP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save paper metadata, abstracts, tags, AI-generated summaries, and optional arXiv PDFs into a Zotero library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ZOTERO_CREDENTIALS to write to a Zotero library. <br>
Mitigation: Use a Zotero API key with the minimum required permissions and keep the credential out of chats and logs. <br>
Risk: For arXiv URLs, the skill may download a PDF and upload it as a Zotero attachment. <br>
Mitigation: Review the target paper URL before execution and expect outbound network access to Zotero and arXiv when saving items. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GottenZZP/zotero-sholar) <br>
- [Zotero](https://www.zotero.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Plain text status messages with Zotero API writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS; arXiv URLs may trigger PDF download and Zotero attachment upload.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
