## Description: <br>
Review and redline DOCX contracts paragraph by paragraph with tracked changes, clause-level risk analysis, and draft comment responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, procurement, privacy, security, and business reviewers use this skill to prepare paragraph-level DOCX contract redlines, clause-specific risk analysis, and draft responses to opponent comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes confidential contract text and writes sidecar outputs that can include contract text, comments, and proposed legal language. <br>
Mitigation: Run it only in an approved local environment for the contract data, control access to generated review JSON and DOCX files, and delete or archive outputs according to the user's data-handling policy. <br>
Risk: Generated redlines, risk reports, and comment responses may be legally or commercially incorrect if accepted without review. <br>
Mitigation: Have a qualified reviewer inspect the review JSON, tracked changes, and risk report before sharing or relying on the outputs. <br>
Risk: Materializing outputs can create amended files that may be confused with originals. <br>
Mitigation: Keep original contracts unchanged, write amended and report files to clearly named paths, and verify tracked changes are readable before use. <br>
Risk: The workflow depends on Python packages for DOCX and XML processing. <br>
Mitigation: Install dependencies only from trusted sources and use a controlled Python environment. <br>


## Reference(s): <br>
- [Contract Review JSON Schema](references/review-json-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChipmunkRPA/redline-contract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands, JSON review data, and generated DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a review JSON dataset, a tracked-changes amended DOCX, and a risk-report DOCX from user-selected contract files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
