## Description: <br>
Save and retrieve read-later links, articles, notes, and ideas in a local markdown reading list with status filtering and auto-tagging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoujackie0609](https://clawhub.ai/user/zhoujackie0609) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to maintain a local markdown-based reading list, save URLs or notes for later, search saved entries, and update item status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved entries may include secrets, confidential notes, private URLs, or internal references in a local markdown file. <br>
Mitigation: Avoid saving sensitive content unless local file storage is acceptable for the user's environment. <br>
Risk: User-provided URLs may be fetched for automatic tagging. <br>
Mitigation: Review URLs before saving private or internal links and disable or avoid fetching when network disclosure is a concern. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhoujackie0609/read-it-later) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown entries and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and updates entries in read-it-later.md, preferring a workspace file when present and otherwise using ~/read-it-later.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
