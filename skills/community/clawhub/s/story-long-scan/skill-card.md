## Description: <br>
Story Long Scan analyzes ranking samples from Chinese long-form web fiction platforms, extracts market trends and genre signals, and helps produce topic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and market analysts use this skill to gather or inspect ranking data from Chinese web-novel platforms and turn repeated ranking patterns into genre trend reports and topic candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact external Chinese web-novel sites and drive a local browser/CDP session. <br>
Mitigation: Run it in a dedicated browser profile and network environment, and avoid logged-in sessions unless that access is intentional. <br>
Risk: The bundled publishing guidance includes platform-gaming advice about fake follows and ranking tactics. <br>
Mitigation: Review and remove that content before deployment in environments that require policy-compliant publishing guidance. <br>
Risk: The skill may write local Markdown report and topic-decision files. <br>
Mitigation: Run it from an expected workspace and review generated files before using them in a writing project. <br>


## Reference(s): <br>
- [Story Long Scan on ClawHub](https://clawhub.ai/worldwonderer/skills/story-long-scan) <br>
- [OpenClaw source metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Scan output format](references/scan-output-format.md) <br>
- [Topic decision guide](references/topic-decision.md) <br>
- [Genre trends reference](references/genre-trends.md) <br>
- [Reader profiling reference](references/reader-profiling.md) <br>
- [Publishing guide](references/publishing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown reports, Markdown decision files, shell commands, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local report files and topic-decision files; some collection modes may drive a local browser/CDP session.] <br>

## Skill Version(s): <br>
1.1.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
