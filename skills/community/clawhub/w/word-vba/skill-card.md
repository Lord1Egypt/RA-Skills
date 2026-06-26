## Description: <br>
Uses Microsoft Word VBA and ActiveX through Python to read, write, format, merge, compare, and batch-process DOC and DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users can use this skill to automate Microsoft Word on Windows for DOC/DOCX reading, formatting, merging, template filling, batch replacement, table of contents generation, and document comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open and overwrite local Word files through Microsoft Word automation. <br>
Mitigation: Use trusted documents, set explicit new output paths, and back up originals before batch operations. <br>
Risk: Word automation depends on Windows, Microsoft Word, and pywin32, and unsupported environments can fail or leave Word sessions running. <br>
Mitigation: Run only on patched Windows systems with Microsoft Word installed, install a current pywin32 version, and close Word automation sessions after use. <br>


## Reference(s): <br>
- [Word Vba on ClawHub](https://clawhub.ai/jirboy/word-vba) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Word document paths and generated DOC/DOCX output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files mention 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
