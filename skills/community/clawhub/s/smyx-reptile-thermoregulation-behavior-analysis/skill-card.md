## Description: <br>
Analyzes fixed-camera reptile enclosure videos to report basking and hiding zone dwell time, movement frequency, activity rhythm, thermal preference labels, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and reptile-care operators use this skill to analyze vivarium or breeding-enclosure video for thermal-zone usage, activity rhythm, and behavior-based warning signs. It supports structured reports and history queries for basking, hiding, cold-zone, and transition-zone behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reptile videos or URLs are sent to the LifeEmergence cloud service for analysis. <br>
Mitigation: Use the skill only with videos the user is authorized to upload, and disclose cloud processing before analysis. <br>
Risk: The skill maintains local identity or token state for cloud access. <br>
Mitigation: Review local identity and token files before installation and remove any stale or unintended API key values. <br>
Risk: History-report queries can run automatically when the user asks for past thermoregulation reports. <br>
Mitigation: Prefer explicit confirmation before querying historical reports, especially in shared or multi-user environments. <br>
Risk: Behavior analysis may be mistaken for veterinary diagnosis. <br>
Mitigation: Present outputs as behavior-based observations and environmental guidance only; keep disease confirmation and treatment decisions with qualified reptile veterinarians. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-reptile-thermoregulation-behavior-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports with report links; optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include thermal-zone dwell ratios, movement frequency, rhythm consistency, preference labels, alert levels, recommended actions, disclaimers, and cloud history-query results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
