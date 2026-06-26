## Description: <br>
Spark Context Monitor estimates current conversation token usage, shows used and remaining tokens with a progress bar, and suggests when to start or compact a session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to check how much of the active chat context has been consumed, estimate remaining capacity, and decide when to start a new session or compact context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill estimates token usage from conversation text, so results may differ from platform token accounting. <br>
Mitigation: Treat the report as a planning aid and rely on platform-native usage statistics when exact billing or limit decisions are required. <br>
Risk: The skill needs access to current conversation text to estimate usage. <br>
Mitigation: Invoke it intentionally, such as with /token, and deploy it only where local session inspection is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/spark-context-monitor) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status report with token counts, percentage, progress bar, and threshold-based recommendation text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token counts are estimates based on current session history and model-window assumptions; the skill does not report platform-authoritative token accounting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
