## Description: <br>
Analyzes child nighttime sleep video or audio to identify rollover frequency, crying, sleep talk, and possible restless sleep or nightmare alerts, then returns structured sleep-quality results and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents or guardians, and agents assisting them, use this skill to submit child sleep media or URLs for remote analysis of movement, crying, sleep talk, and sleep-quality indicators. The output is intended as a caregiving aid and not as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child bedroom audio, video, and report history are highly sensitive and may be processed by remote lifeemergence.com services. <br>
Mitigation: Use only with verified guardian consent, avoid unnecessarily sensitive recordings, and prefer a dedicated workspace or account for this skill. <br>
Risk: The skill silently manages identity, remote login or registration, local token storage, and cloud report retrieval. <br>
Mitigation: Review the configured services before use and delete the workspace data database or stored tokens when the skill is no longer needed. <br>
Risk: Sleep-quality and nightmare alerts can be mistaken for medical conclusions. <br>
Mitigation: Treat outputs as caregiving support only and consult qualified pediatric or sleep-medicine professionals for persistent concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-nightmare-rollover-detection-analysis) <br>
- [Skill API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [LifeEmergence skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files] <br>
**Output Format:** [Markdown text with structured JSON-style analysis results, report-list output, optional saved result files, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file paths or media URLs, cloud history queries, and basic, standard, or json detail modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
