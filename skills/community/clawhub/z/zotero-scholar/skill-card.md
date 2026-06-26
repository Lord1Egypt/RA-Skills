## Description: <br>
Save academic papers with metadata, PDF links, and AI summaries to a Zotero library using credentials set in ZOTERO_CREDENTIALS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GottenZZP](https://clawhub.ai/user/GottenZZP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and agents that assist with literature workflows use this skill to create Zotero entries from paper metadata, optional abstracts, tags, AI summaries, and arXiv PDF links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zotero API key that can write to the user's library. <br>
Mitigation: Use the narrowest practical Zotero key permissions and keep ZOTERO_CREDENTIALS out of logs, shared shell history, and public configuration. <br>
Risk: Generated summaries and attached PDFs may be incomplete, incorrect, or unsuitable for citation without review. <br>
Mitigation: Review Zotero notes, metadata, tags, and PDF attachments before relying on them in research or publication workflows. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [ClawHub skill page](https://clawhub.ai/GottenZZP/zotero-scholar) <br>
- [Publisher profile](https://clawhub.ai/user/GottenZZP) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, Zotero library entries] <br>
**Output Format:** [Markdown guidance with command-line arguments and text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes paper metadata, optional notes, tags, and arXiv PDF attachments to Zotero through the user's API credentials.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
