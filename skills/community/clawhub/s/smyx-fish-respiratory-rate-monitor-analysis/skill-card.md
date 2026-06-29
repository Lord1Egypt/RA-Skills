## Description: <br>
Analyzes aquarium camera images or videos to estimate fish gill opening and closing respiratory rate, classify abnormal breathing or hypoxia warning status, and return structured reports or historical report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium keepers, aquaculture operators, public aquarium staff, and laboratory teams use this skill to review close side-view fish media for respiratory rate, abnormal breathing alerts, and report history. The output supports monitoring and escalation guidance, not veterinary diagnosis or automated device control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium images, videos, or video URLs are processed by the publisher's cloud service. <br>
Mitigation: Use only media you are comfortable uploading, and confirm the publisher's upload, retention, deletion, and account-linking practices before using private footage. <br>
Risk: The skill may create local identity records and store backend tokens. <br>
Mitigation: Run it in an isolated workspace when possible, review retained data and token files, and remove local identity or credential artifacts when no longer needed. <br>
Risk: Respiratory-rate alerts are visual monitoring outputs and may be wrong when footage is unclear or context is missing. <br>
Mitigation: Treat alerts as decision support, verify water quality and fish condition independently, and involve qualified aquarium or veterinary support for urgent cases. <br>


## Reference(s): <br>
- [Fish respiratory rate monitor API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-respiratory-rate-monitor-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured text, Markdown tables, or JSON-style reports with respiratory rate fields, alert status, recommendations, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save results to a requested output file; historical report queries return cloud report listings and links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
