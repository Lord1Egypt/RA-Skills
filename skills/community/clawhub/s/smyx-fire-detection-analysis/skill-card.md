## Description:

Real-time detection of flames and smoke in video and image scenes. Suitable for fire early warning in industrial parks, forests, warehouses, and other locations. | 火情烟雾检测技能，实时检测视频/图片场景中的火焰、烟雾，适用于工业园区、森林、仓库等场所火情预警

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Fire safety teams can use this skill to analyze supplied images or video for flames and smoke, review detection reports, and query historical reports. Treat its results as supplementary warning information and have fire incidents confirmed by qualified responders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cloud analysis flow may mix users’ report accounts and may process footage despite an export-only option.

Mitigation: Wait until account isolation and export-only behavior are fixed; confirm report access and retention policies before using sensitive footage or a shared agent.

Risk: Stored tokens and API secrets may be difficult to remove or may be reused as account identifiers.

Mitigation: Confirm how stored tokens can be removed and verify that API secrets are not used as account identifiers.

Risk: Detection results could be treated as a definitive fire determination.

Mitigation: Use results only as supplementary fire-warning information and have suspected incidents confirmed by qualified responders.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-fire-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured detection reports; historical report lists can be presented as Markdown tables with report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include detected fire or smoke, location, confidence, severity, recommendations, and cloud report links.]

## Skill Version(s):

1.0.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
