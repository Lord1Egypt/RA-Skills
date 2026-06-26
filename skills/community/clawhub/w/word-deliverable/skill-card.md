## Description: <br>
Turn financial-services outputs into a polished Word deliverable. Use when the user wants an IC memo, customer memo, internal note, diligence summary, or banker-ready .docx built from this plugin's analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial-services teams use this skill to turn existing analysis outputs, notes, tables, and diligence materials into structured Word deliverables such as IC memos, customer memos, internal briefs, and diligence summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial materials may be passed to DOCX conversion or validation tools. <br>
Mitigation: Confirm that the referenced DOCX conversion and validation tools in the environment are trusted and permitted to process that data before use. <br>
Risk: Word memos can include incorrect hard numbers if they are not tied back to source material. <br>
Mitigation: For Chinese-market targets, source hard numbers from analysis or provenance files and run the documented delivery validation before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackdark425/word-deliverable) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown guidance for producing a real .docx deliverable, with routing preferences and validation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected agent output includes a .docx file, a short summary, and open assumptions or numbers requiring verification.] <br>

## Skill Version(s): <br>
0.9.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
