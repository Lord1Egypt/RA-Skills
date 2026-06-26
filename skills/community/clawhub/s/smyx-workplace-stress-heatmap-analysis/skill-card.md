## Description: <br>
Analyzes fixed-camera office video through a cloud workflow to produce anonymous, group-level workplace stress heatmaps, zone-level stress indicators, report links, and manager-facing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Facilities, HR, workplace operations, and smart-office teams can use this skill to submit office-area video or retrieve prior reports for group-level stress distribution review. The skill is intended for aggregate organizational-health monitoring and manager reference, not individual diagnosis, identification, profiling, or performance evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as anonymous group analysis, but release security evidence flags identity-linked cloud use, token/profile persistence, broad video ingestion, and mismatched health-analysis behavior. <br>
Mitigation: Complete a privacy and security review before installation; confirm what video is uploaded, whether individual health or face outputs are disabled, and how tokens, profiles, and historical reports are stored and accessed. <br>
Risk: Workplace video and stress-related outputs can affect employee privacy and workplace trust even when presented as aggregate heatmaps. <br>
Mitigation: Deploy only with documented employee notice and consent, strict role-based access to reports, minimum group-size thresholds, short retention periods, and a prohibition on individual performance or health decisions. <br>
Risk: The dependency list includes an unresolved yaml package name. <br>
Mitigation: Replace the yaml dependency with PyYAML or remove it before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/smyx-workplace-stress-heatmap-analysis) <br>
- [Workplace Stress Heatmap API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown report text with zone-level stress metrics, heatmap/report links, and operational recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and cloud API access; local video may be uploaded or a public video URL may be passed to the service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
