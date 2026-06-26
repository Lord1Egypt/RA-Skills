## Description: <br>
Saves paper metadata, links, optional abstracts, AI-generated summaries, tags, and arXiv PDF attachments to a user's Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justin18chan](https://clawhub.ai/user/justin18chan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to add paper records and optional AI-generated notes to a Zotero library from command-line paper details. It is suited for literature collection workflows where an agent can gather citation metadata and then call the provided save script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zotero API key and can write new items to the user's Zotero library. <br>
Mitigation: Use the narrowest practical Zotero API permissions, keep ZOTERO_CREDENTIALS out of shared files and logs, and review the paper metadata before running the script. <br>
Risk: arXiv URLs may trigger automatic PDF download and upload as a Zotero attachment. <br>
Mitigation: Run the skill only for papers whose PDF attachment behavior is desired, and verify that the Zotero library has appropriate storage and sharing settings. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [ClawHub skill release](https://clawhub.ai/justin18chan/zotero-scholar-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and script status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes Zotero items through the Zotero API and may attach arXiv PDFs when the supplied URL is an arXiv abstract page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
