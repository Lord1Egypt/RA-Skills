## Description: <br>
AI-powered pet eye anomaly detection from close-up facial images or video that flags redness, abnormal tearing or tear stains, and pupil or cornea opacity for early health screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners, boarding centers, and veterinary triage teams use this skill to analyze close-up pet eye media, retrieve related cloud reports, and produce visual-risk alerts with practical follow-up guidance. Results are visual screening support and should not be treated as a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet images, videos, and report history are processed by the publisher's cloud service and may be associated with a local identity. <br>
Mitigation: Use the skill only with media you are comfortable sending to the service, avoid sensitive household media or internal URLs, and confirm account and retention practices before broader deployment. <br>
Risk: The skill can silently create or reuse an account identity and store service tokens in a local SQLite database. <br>
Mitigation: Run it in a contained workspace, restrict access to local storage, and review token handling before using it in shared or regulated environments. <br>
Risk: Eye-health findings are visual screening outputs and may be incomplete or misleading for medical decisions. <br>
Mitigation: Treat results as triage guidance only and direct users to a veterinarian for diagnosis or urgent symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-eye-anomaly-detection-analysis) <br>
- [Pet eye anomaly API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports, with optional saved text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include anomaly classifications, health guidance, history-report tables, and report links returned by the vendor cloud service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
