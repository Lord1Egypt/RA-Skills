## Description: <br>
Summarize what is open, what changed, and what is due soon from a Campus Copilot snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local agent users use this skill to summarize already-exported Campus Copilot snapshots, including open work, recent changes, upcoming due items, and the site carrying the current workload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campus Copilot snapshots may contain private academic or operational information. <br>
Mitigation: Review and minimize snapshot contents before sharing them with an agent. <br>
Risk: Live browser automation could change the analysis boundary or expose fresh workspace data. <br>
Mitigation: Use imported snapshots or thin-BFF contract data unless the user explicitly requests live validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/read-only-workspace-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/xiaojiou176) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown summary or plain-language text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses provided snapshots or thin-BFF contract data; no live browser automation by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
