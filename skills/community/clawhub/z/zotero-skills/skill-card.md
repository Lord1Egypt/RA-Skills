## Description: <br>
Saves paper metadata, PDF links, tags, abstracts, and AI-generated summaries to a user's Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifenglei](https://clawhub.ai/user/lifenglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to add academic paper records to Zotero from command-line inputs, including optional abstracts, tags, summaries, and arXiv PDF attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zotero API key and writes metadata, summaries, tags, and attachments to a Zotero library. <br>
Mitigation: Use a minimally scoped Zotero API key, avoid exposing ZOTERO_CREDENTIALS in logs or shared shells, and review Zotero writes after execution. <br>
Risk: arXiv PDF attachment runs download and upload PDFs associated with the provided paper URL. <br>
Mitigation: Run only for paper URLs the user intends to store in Zotero and confirm the created Zotero record and attachment. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [ClawHub skill page](https://clawhub.ai/lifenglei/zotero-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown instructions with command-line examples; runtime output is terminal text and Zotero library updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS in userid:apiKey format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
