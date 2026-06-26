## Description: <br>
Create and manage presentation slides using JSONL storage for deck building, theme application, and HTML or JSON export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, edit, organize, preview, and export local slide decks with themes, templates, speaker notes, and ordered slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Bash/Python helper runs locally and writes presentation content, including speaker notes, to ~/.slide/data.jsonl. <br>
Mitigation: Install only when local script execution and persistent local storage are acceptable, and avoid placing secrets or highly sensitive content in decks. <br>
Risk: Exported presentations can include business content copied from local deck records. <br>
Mitigation: Review generated HTML or JSON exports before sharing and delete local or exported files when the deck content should no longer persist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/slide) <br>
- [Publisher Profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, HTML, Shell commands, Files] <br>
**Output Format:** [Structured JSON to stdout, with optional self-contained HTML or JSON export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores deck and slide records locally in ~/.slide/data.jsonl.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
