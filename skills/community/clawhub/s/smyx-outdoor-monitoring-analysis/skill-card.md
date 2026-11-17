## Description:

Detects targets such as people, vehicles, non-motorized vehicles, and pets within target areas; supports batch image analysis, suitable for outdoor surveillance scenarios like courtyards, orchards, and farms. | 户外看护智能监测分析技能，检测目标区域内的人、车、非机动车、宠物等目标，支持批量图片分析，适用于庭院、果园、养殖场等户外区域看护场景

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Outdoor property owners, farm and orchard operators, and security teams use the skill to analyze surveillance images or videos, identify and count people, vehicles, and pets in target areas, assess possible intrusion risks, and review monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account and history behavior and privacy-sensitive data transfers have not been clarified in the security evidence.

Mitigation: Confirm what account and history data is used and where submitted media and results are sent or retained; avoid sending sensitive imagery until those details are clear.

Risk: The security evidence reports that an option presented as analysis-only may still run analysis.

Mitigation: Do not rely on that option to prevent processing; verify its behavior before use and treat it as an execution path until confirmed.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-outdoor-monitoring-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis results and Markdown report tables with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected-object classifications and counts, risk indications, recommendations, and report links; supports batch image analysis.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
