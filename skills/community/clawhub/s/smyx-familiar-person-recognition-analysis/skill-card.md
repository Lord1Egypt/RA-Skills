## Description: <br>
Identifies known acquaintances in images or videos by comparing detected faces against an enrolled face database and reporting identities and locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to enroll familiar faces and analyze uploaded images or videos for known-person matches in home or office monitoring workflows. Results are intended as operational recognition reports and not as legal identity verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive biometric images or videos and identity-linked report history may be sent to external Life Emergence endpoints. <br>
Mitigation: Use only when the publisher and endpoints are trusted, obtain consent for the people shown, and avoid regulated or legal identity-verification use without separate compliance controls. <br>
Risk: The skill silently creates or reuses identity state and stores authentication tokens locally. <br>
Mitigation: Run it in a controlled workspace, review local data retention before deployment, and restrict access to generated identity or token storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-familiar-person-recognition-analysis) <br>
- [Familiar person recognition API documentation](artifact/references/api_doc.md) <br>
- [Common analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands] <br>
**Output Format:** [Markdown or JSON recognition reports, with optional saved text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file or URL inputs for jpg, jpeg, png, mp4, avi, and mov media up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
