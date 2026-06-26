## Description: <br>
Identifies limb tremors, convulsions, stiffness, and gait abnormalities in video to support home risk monitoring for people with Parkinson's disease or epilepsy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care teams use this skill to submit home-monitoring video or image inputs for Parkinson's and epilepsy behavior analysis and to retrieve historical behavior-recognition reports. Results are assistive monitoring outputs and do not replace professional medical diagnosis or clinician judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive patient or household video and a user identifier may be sent to the publisher's cloud service. <br>
Mitigation: Use only with clear consent from people in the footage, submit the minimum necessary media, and install only if the publisher cloud service is acceptable for the data. <br>
Risk: The security review flags under-disclosed account, token, and report-history behavior. <br>
Mitigation: Review bundled configuration before deployment, remove or replace shared api-key or open-id values, and use dedicated credentials for production use. <br>
Risk: Health-oriented analysis output may be mistaken for clinical diagnosis. <br>
Mitigation: Treat results as assistive monitoring information and require professional medical review for diagnosis, treatment changes, or urgent care decisions. <br>


## Reference(s): <br>
- [Parkinson's and Epilepsy Behavior Recognition API Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown or JSON text containing structured behavior-recognition reports, historical report lists, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file or public URL inputs, requires an open-id for analysis and history queries, and supports optional file output.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
