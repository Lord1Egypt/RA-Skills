## Description: <br>
Through fixed enclosure cameras, the skill analyzes turtle mouth and nasal videos for abnormally frequent open-mouth breathing, mucus, or nasal discharge and returns pneumonia risk warnings rather than a veterinary diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, turtle keepers, breeding facilities, and animal-care teams use this skill to submit turtle enclosure footage or video URLs for visual screening of open-mouth breathing, mucus, nasal discharge, posture, and related warning signals. The output should be treated as a visual risk report and prompt for environmental checks or professional reptile veterinary review, not as a diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends turtle footage, video URLs, account-linked identifiers, and report queries to the external lifeemergence.com service. <br>
Mitigation: Use it only when the user accepts the provider's retention and access controls; avoid sensitive household, clinic, or farm footage unless that sharing is appropriate. <br>
Risk: The skill can silently create or reuse a cloud-linked identity and may use local workspace identity data. <br>
Mitigation: Review workspace identity state before installation and avoid exposing account-linked identifiers in prompts, outputs, logs, or shared reports. <br>
Risk: The skill may create a local SQLite user/token cache for service access. <br>
Mitigation: Treat local cache files as sensitive, restrict workspace access, and remove cached credentials when the skill is no longer needed. <br>
Risk: The output concerns animal health and could be mistaken for a veterinary diagnosis or treatment plan. <br>
Mitigation: Keep outputs framed as visual risk screening; do not provide medication names, dosages, exact temperature therapy, or definitive disease diagnoses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-turtle-pneumonia-symptom-detection-analysis) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, JSON, Files] <br>
**Output Format:** [Markdown or JSON analysis report with warning level, observed indicators, recommended actions, disclaimer, and optional exported report link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an output file when requested and may query cloud-hosted historical reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
