## Description: <br>
This skill checks PDF, Word, and Excel files for sensitive or prohibited words from a built-in or external word library and highlights matches in yellow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[betty831221](https://clawhub.ai/user/betty831221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external reviewers, and document compliance teams use this skill to scan contracts and other business documents for configured sensitive terms, then produce highlighted copies for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected documents that may contain contracts, compliance records, or other sensitive business content. <br>
Mitigation: Run it only on documents the user intends to scan and handle the resulting highlighted copies according to the same confidentiality controls as the originals. <br>
Risk: A highlighted output file can overwrite a file with the same name in the selected output folder. <br>
Mitigation: Choose an explicit output folder and keep backups when processing important records. <br>
Risk: The built-in and external word lists may miss relevant terms or flag partial matches that require judgment. <br>
Mitigation: Review detected matches and update the external word library when the review policy requires additional terms. <br>


## Reference(s): <br>
- [Usage Guide](artifact/references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/betty831221/skills/sensitive-word-checker-cmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and highlighted document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces highlighted copies of supported input documents and console text reporting detected sensitive words.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
