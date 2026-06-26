## Description: <br>
Analyzes fixed-camera videos of an older adult's resting hand to report tremor frequency, pixel amplitude, affected side, risk level, and report links without replacing clinical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, elder-care providers, and developers use this skill to submit resting-hand videos or URLs for tremor screening, receive structured motion-analysis metrics and risk prompts, and query cloud-stored history reports. Results are intended as screening support and not as a substitute for professional neurological diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive elderly-care videos and account-linked health metadata are sent to remote services and stored in report history. <br>
Mitigation: Use only with informed consent for cloud processing and report storage; avoid sensitive signed or private video URLs and handle generated reports as health-related data. <br>
Risk: The skill silently creates or reuses local identities and tokens for account-linked cloud history. <br>
Mitigation: Review identity, token, workspace database, and report-retention handling before deployment; restrict access to the local workspace and associated cloud account history. <br>
Risk: The tremor risk output may be mistaken for clinical diagnosis. <br>
Mitigation: Present results as video motion-analysis indicators for screening support and route concerning results to qualified neurological review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-elderly-hand-tremor-detection-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON-formatted structured reports with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tremor frequency, pixel amplitude, rhythm consistency, affected side, risk level, alert text, medical follow-up prompt, and report export links.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
