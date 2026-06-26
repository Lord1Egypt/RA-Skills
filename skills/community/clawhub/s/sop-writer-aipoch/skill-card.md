## Description: <br>
Write GCP-compliant Standard Operating Procedures for labs and clinical sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical site, laboratory, and QA users can draft SOPs for sample processing, equipment calibration, safety procedures, and GCP compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unsafe output path could overwrite or place SOP files in an unintended location. <br>
Mitigation: Use an output path inside a disposable or project workspace and review the path before running the script. <br>
Risk: Sensitive clinical or patient content could be written into local output files without proper controls. <br>
Mitigation: Avoid regulated patient or clinical data unless authorized and appropriate data-handling controls are in place. <br>
Risk: Generated SOPs may be incomplete or unsuitable for regulated use without expert review. <br>
Mitigation: Treat generated SOPs as drafts and require qualified compliance review before operational use. <br>


## Reference(s): <br>
- [SOP Writer release page](https://clawhub.ai/aipoch-ai/sop-writer-aipoch) <br>
- [aipoch-ai publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text SOP document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the generated SOP to an output file and prints it to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
