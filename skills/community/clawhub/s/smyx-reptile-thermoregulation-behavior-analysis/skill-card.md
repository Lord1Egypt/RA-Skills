## Description: <br>
Through fixed enclosure cameras, the skill analyzes reptile behavior videos to report movement frequency, dwell duration, thermal-zone preference, activity rhythm, and alerts for abnormal basking, hiding, shuttling, or immobility patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and reptile keepers use this skill to analyze fixed-camera vivarium videos, generate thermal-zone utilization reports, and receive environment-focused guidance without disease diagnosis or medication advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends reptile enclosure videos or video URLs, user identifiers, and report-history queries to a third-party cloud service. <br>
Mitigation: Use the skill only with trusted publisher accounts, user authorization, and videos that are acceptable to transmit to the SMYX/LifeEmergence cloud service. <br>
Risk: The local workspace database may cache account tokens or related account state. <br>
Mitigation: Treat the workspace as sensitive, restrict local access, and clear cached credentials before sharing or archiving the environment. <br>
Risk: The skill asks for open-id/user identifiers and also exposes an API-key parameter, which can be confused during setup. <br>
Mitigation: Keep API keys separate from user identifiers, avoid placing secrets in open-id fields, and review configuration files before execution. <br>
Risk: Behavior reports may influence animal-care decisions while the artifact states it is not a disease diagnosis or medication advisor. <br>
Mitigation: Use results as behavior and environment guidance only, verify enclosure conditions directly, and consult a qualified reptile veterinarian for health concerns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-reptile-thermoregulation-behavior-analysis) <br>
- [Primary API Documentation](artifact/references/api_doc.md) <br>
- [Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured JSON-like report content, with optional shell commands and saved text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include thermal-zone dwell ratios, transition counts, rhythm signals, preference labels, alert level, recommended actions, history listings, and export links when returned by the cloud service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
