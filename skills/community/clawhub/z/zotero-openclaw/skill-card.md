## Description: <br>
Saves paper metadata, optional AI summaries, tags, and arXiv PDF attachments to a user's Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Little-Cat1](https://clawhub.ai/user/Little-Cat1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and knowledge workers use this skill to add paper records, summaries, tags, and available arXiv PDFs to their Zotero library from agent-provided bibliographic details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes user-provided paper metadata, summaries, tags, and attachments to a Zotero library. <br>
Mitigation: Review paper URLs, metadata, and AI-generated summaries before saving them. <br>
Risk: The skill uses a Zotero API key from the ZOTERO_CREDENTIALS environment variable. <br>
Mitigation: Use a Zotero API key with only the permissions needed and avoid exposing the credential in prompts, logs, or shared shell history. <br>
Risk: The helper depends on pyzotero and may download arXiv PDFs before attaching them to Zotero. <br>
Mitigation: Install pyzotero from a trusted Python environment and confirm downloaded PDFs come from expected paper URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Little-Cat1/zotero-openclaw) <br>
- [Zotero](https://www.zotero.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and parameter descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, pyzotero, and ZOTERO_CREDENTIALS formatted as userid:apiKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
