## Description: <br>
Analyzes in-cabin driver face images or video for visual signs of facial flushing and abnormal sweating, then returns structured health-risk reminders and suggested driver or fleet actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, vehicle operators, and fleet teams use this skill to analyze driver-facing DMS camera media for visual flushing and sweat-abnormality indicators and to produce reminders, event records, or fleet-upload recommendations. Results are visual alerts only and should not be treated as medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Driver facial and health-related video may be sent to the publisher's cloud service. <br>
Mitigation: Use only with informed consent, applicable privacy-law review, and documented handling for uploads, stored fields, retention, deletion, and encryption. <br>
Risk: The skill includes identity handling, account login or registration, history lookup, and local token or profile persistence that are under-disclosed in the release evidence. <br>
Mitigation: Review publisher documentation and configuration before installation, including endpoint behavior, token storage protections, and confirmation flow for uploads and history queries. <br>
Risk: Visual flushing and sweat indicators can be affected by lighting, tinted windows, skin-tone variation, occlusion, and sensor channel quality. <br>
Mitigation: Treat results as driver-assistance alerts, require RGB camera input, verify deployment conditions, and avoid using outputs as medical diagnosis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-driver-flushing-sweat-detection-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with structured analysis fields, optional JSON detail, and optional output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can list cloud-hosted historical reports or save analysis output when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
