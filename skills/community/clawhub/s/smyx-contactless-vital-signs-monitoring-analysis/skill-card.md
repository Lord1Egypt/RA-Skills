## Description: <br>
Enables agents to run non-contact vital signs analysis from camera video, estimating heart rate, respiration rate, blood oxygen, and heart rate variability through cloud API analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit local or public video for non-contact health screening and to retrieve historical vital-sign reports. Results are for health reference and should not replace professional medical measurement or diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face video and health-related analysis requests are sent to the Life Emergence cloud service. <br>
Mitigation: Use the skill only with informed consent, avoid uploading sensitive videos when cloud processing is not acceptable, and treat outputs as health-reference information. <br>
Risk: Reports are linked to a persistent identifier such as a username or phone number. <br>
Mitigation: Use only the intended user's identifier, do not use another person's identifier, and confirm that report lookup is appropriate before querying history. <br>
Risk: Account tokens may be cached in local workspace data. <br>
Mitigation: Review and delete local workspace database or configuration data after use when token persistence is not desired. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-contactless-vital-signs-monitoring-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON text from API responses, with optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links to exported report images for historical reports.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
