## Description: <br>
Import notes from pasted Logseq pages into a SlipBot slipbox by parsing page properties, extracting bullets as individual notes, adding parent context to nested bullets, and running SlipBot for each note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrswab](https://clawhub.ai/user/jrswab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
SlipBot users who keep notes in Logseq use this skill to convert pasted Logseq pages into persistent slipbox notes. It is intended for imports where the user can review a pre-import summary and note count before note creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted Logseq content may become persistent SlipBot notes that are later tagged or linked in the slipbox graph. <br>
Mitigation: Review the pre-import summary and note count carefully, and paste only content suitable for storage in the slipbox. <br>
Risk: Logseq tags and tag metadata are intentionally ignored during import. <br>
Mitigation: Confirm that SlipBot-generated tags are acceptable before proceeding with the import. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries, confirmations, import results, and per-note SlipBot import guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before creating notes; ignores Logseq tags and related tag metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
