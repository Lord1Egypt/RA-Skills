## Description: <br>
Import local PDF files into Zotero from the command line on Windows/macOS/Linux via the Zotero local connector (127.0.0.1). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and Zotero users use this skill to import one or more local PDF files into an existing Zotero library or collection through Zotero Desktop's local connector. It also helps list collections and verify recent imported attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Zotero Desktop local communication and can import PDFs into the user's Zotero library. <br>
Mitigation: Confirm Zotero Desktop is open, local communication is intentionally enabled, the connector port is correct, and the target collection is selected before import. <br>
Risk: Recursive or folder imports can add more PDFs than the user intended. <br>
Mitigation: Use exact absolute paths, avoid recursive mode unless needed, and use selected file picks for partial folder imports. <br>
Risk: The doctor command may install the requests dependency automatically. <br>
Mitigation: Use a virtual environment or install requests manually before running the skill when dependency changes should be controlled. <br>
Risk: The check command can print Zotero item titles and local file paths. <br>
Mitigation: Run check only in environments where exposing recent attachment metadata and local paths is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mxingchtongaelofficial2568/zotero-local-import-en) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured CLI arguments for the bundled Zotero import tool and reports import, collection, doctor, or check results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
