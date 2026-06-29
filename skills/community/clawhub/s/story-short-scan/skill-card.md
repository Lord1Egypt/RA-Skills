## Description: <br>
Scans short-form web fiction rankings across platforms such as Zhihu Yanyan, Qimao, Heiyan, and Dianzhong to identify current genre, emotion, and topic signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and content strategists use this skill to collect or inspect short-form fiction market samples and turn them into ranking reports, trend hypotheses, topic candidates, risk thresholds, and follow-up validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in browser collection can expose authenticated platform access or unrelated browser-session data to the agent. <br>
Mitigation: Use an isolated Chrome profile and accounts limited to the target collection task; prefer public-page or user-supplied data modes when authenticated collection is not required. <br>
Risk: The Heiyan collection path uses an admin token to query a management backend. <br>
Mitigation: Run that mode only with intentional authorization, limit collection scope, and review generated files for sensitive data before sharing. <br>
Risk: Short-form fiction market signals can become stale quickly. <br>
Mitigation: Require each report to state the sample date, trend confidence, and next rescan time before treating recommendations as current. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/worldwonderer/skills/story-short-scan) <br>
- [Publisher Profile](https://clawhub.ai/user/worldwonderer) <br>
- [Declared OpenClaw Source](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Real Market Data Reference](references/real-market-data.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown reports with optional generated Markdown data files and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include sample date, trend confidence, and a recommended rescan time.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
