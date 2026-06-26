## Description: <br>
Detects strangers near minors in surveillance images or videos, returns structured safety analysis, and can list prior warning reports from the configured cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to analyze home, school, childcare, or similar monitoring media for stranger proximity risks around minors and to retrieve prior alert reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends surveillance images or videos and account-linked report queries to a configured external service. <br>
Mitigation: Use only with media the operator is authorized to upload, and confirm consent, retention, and deletion expectations before use. <br>
Risk: The security summary says the skill creates or reuses local identity and token state automatically and can retrieve cloud history. <br>
Mitigation: Review the configured service, isolate the workspace where practical, and remove local identity or token state when the release is no longer needed. <br>
Risk: The skill is intended for safety-video analysis, but its output should not be treated as a substitute for professional security response. <br>
Mitigation: Use results as decision support, keep human review in the workflow, and follow emergency procedures when a real safety issue is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-stranger-approach-warning-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Common AI API Error Reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis text with optional report links and saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local media paths, remote media URLs, report listing, detail levels, and optional file output.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence; artifact frontmatter says 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
