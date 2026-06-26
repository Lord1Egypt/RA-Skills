## Description: <br>
Automates strain identification by parsing local SEQ or FASTA sequencing files, submitting sequences to online NCBI BLAST, preparing DingTalk table data, and drafting a Word identification report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-men](https://clawhub.ai/user/meta-men) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Laboratory users and developers use this skill to process local sequencing files, submit sequence data to NCBI BLAST, and create structured identification data plus a Word report draft. The output should be reviewed before operational, regulated, confidential, or clinical use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sequencing data is submitted to NCBI BLAST. <br>
Mitigation: Use only sequences your organization permits uploading to NCBI; avoid proprietary, clinical, regulated, or confidential samples unless approved. <br>
Risk: Identification output may be unreliable because the artifact appears to return hard-coded BLAST result fields. <br>
Mitigation: Treat the generated identification as a draft and verify results against real BLAST retrieval and expert review before use. <br>
Risk: The default Word report path can overwrite an existing report in the working folder. <br>
Mitigation: Run the skill in a dedicated folder or change the report path before execution. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/meta-men/strain-skill) <br>
- [Publisher profile](https://clawhub.ai/user/meta-men) <br>
- [NCBI BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON-style result with BLAST fields, DingTalk table data, and a Word report path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a .docx report from a supplied template; the default report filename may overwrite an existing file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
