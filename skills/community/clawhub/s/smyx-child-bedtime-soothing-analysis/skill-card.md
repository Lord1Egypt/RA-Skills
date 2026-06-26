## Description: <br>
Analyzes child bedroom night-time audio and video to identify bedtime distress, fear-of-dark behavior, nightmare wakeups, and out-of-bed safety events, then returns soothing actions and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, caregivers, and integrators use this skill to review child bedroom sleep-window media, identify distress or safety events, trigger age-sensitive soothing actions, and retrieve cloud history reports. It should be used only with explicit family consent and appropriate controls for child media and identity-linked records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive child bedroom audio/video and identity-linked sleep history through publisher remote services. <br>
Mitigation: Use only with explicit caregiver consent, account scoping, report access controls, retention limits, and clear disclosure to household members. <br>
Risk: The security review marked the release suspicious because media and cloud history controls are under-scoped for the sensitivity of the data. <br>
Mitigation: Review deployment settings before installation, avoid bundled fallback identifiers for real family data, and confirm retention, access, and deletion practices. <br>
Risk: Automated soothing guidance can be mistaken for medical or psychological assessment. <br>
Mitigation: Treat outputs as behavioral observations and automation suggestions only; use parent intervention and professional clinical resources for repeated or serious events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-child-bedtime-soothing-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables with optional JSON output from command-line API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id for analysis or history queries; outputs child sleep event classifications, observed audio/video signals, soothing actions, report links, and safety guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
