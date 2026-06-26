## Description: <br>
Customizes safety zones, identifies babies crawling out or approaching dangerous areas such as bedsides/windowsills, and immediately alerts to protect baby safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, guardians, and agents assisting home safety monitoring use this skill to submit baby/home monitoring videos or URLs to the LifeEmergence cloud service for virtual-fence crossing analysis, alerts, and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive baby or home monitoring media may be uploaded to the LifeEmergence cloud service. <br>
Mitigation: Use only media you are authorized to share, avoid unnecessary sensitive scenes, and confirm privacy and retention expectations before use. <br>
Risk: The skill creates or reuses a local identity and stores authentication tokens locally with limited user-facing controls. <br>
Mitigation: Run it in a controlled workspace, clear local data and tokens when decommissioning, and prefer a release with explicit account binding and token-clearing controls. <br>
Risk: Virtual-fence analysis is an auxiliary alert and may miss events or produce false alarms. <br>
Mitigation: Do not rely on it as the only safety mechanism; keep physical safeguards and direct human supervision in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-virtual-fence-intrusion-warning-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown or JSON analysis reports, history tables, cloud report links, and optional saved result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local mp4, avi, or mov files up to 10 MB, or a public video URL for cloud-side analysis.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
