## Description: <br>
Analyzes pet grooming images or videos by sending local files or URLs to a remote service and returning coat condition, shed-hair, grooming effectiveness, hairball risk, and historical report outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet-care developers, smart-grooming operators, and caretakers use this skill to submit grooming-area media and receive structured observations about matting, shed hair volume, grooming effectiveness, hairball risk, and prior reports for care reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet media, URLs, and report queries are sent to remote services and may be associated with identity-linked report history. <br>
Mitigation: Install only where remote processing is acceptable, avoid submitting sensitive media, and review the configured service endpoints before use. <br>
Risk: The skill can silently create or reuse internal identity state and persist returned tokens in the local workspace. <br>
Mitigation: Run it in a controlled workspace, restrict access to local skill files, and remove local credential state when it is no longer needed. <br>
Risk: Hairball risk and grooming observations may be mistaken for veterinary advice. <br>
Mitigation: Use outputs as grooming-care reference only and consult a veterinarian for medical diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-grooming-effectiveness-analysis) <br>
- [Grooming analysis API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [Markdown or JSON analysis reports, with optional saved text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local image/video file paths or network URLs and can list cloud-backed historical grooming reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
