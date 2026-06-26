## Description: <br>
Extracts paper information from citation text, paper links, or social-media posts and helps save the resulting metadata, notes, and supported PDFs to a Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auto-dog](https://clawhub.ai/user/auto-dog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to turn shared paper citations, academic links, or social-media article links into Zotero library entries. It can prepare metadata, summaries, tags, source notes, and arXiv PDF attachments through the bundled Zotero helper script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Zotero credentials that can write to a user's library. <br>
Mitigation: Use a Zotero API key with the minimum permissions needed and store it only in the documented macOS Keychain entry or ZOTERO_CREDENTIALS environment variable. <br>
Risk: User-provided paper or social-media links may produce ambiguous metadata, notes, or PDF attachments. <br>
Mitigation: Review generated Zotero metadata, notes, and attachments before saving when a source link is ambiguous or private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auto-dog/social-media-scholar) <br>
- [Zotero](https://www.zotero.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Zotero item creation through the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Zotero journalArticle items, notes, tags, and arXiv PDF attachments when executed with user credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
