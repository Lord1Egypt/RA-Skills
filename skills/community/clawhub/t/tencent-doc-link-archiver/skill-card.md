## Description: <br>
Extracts Tencent Docs links from user-provided text, downloads the documents serially to a Desktop/Tencent Docs folder, and updates an Excel ledger with the archived links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pufanuzhu-hash](https://clawhub.ai/user/pufanuzhu-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive Tencent Docs links they provide by exporting local document copies and maintaining a dated spreadsheet ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded documents and the link ledger may contain business, personal, or regulated data that remains on disk. <br>
Mitigation: Review source documents before archiving and remove local files or ledger entries when retention is no longer appropriate. <br>
Risk: Some Tencent Docs links may fail because of permissions, rate limits, or unavailable export capability. <br>
Mitigation: Process each link independently and report failures without stopping the rest of the batch. <br>
Risk: Non-Tencent links in mixed user input could be archived unintentionally. <br>
Mitigation: Filter input to docs.qq.com links only and ignore other URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pufanuzhu-hash/tencent-doc-link-archiver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown feedback report, downloaded document files, and an Excel ledger] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes only docs.qq.com links, handles downloads serially, and stores files under the user's Desktop/Tencent Docs folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
