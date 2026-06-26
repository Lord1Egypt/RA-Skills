## Description: <br>
Structured reasoning protocol for Claude that forces step-by-step analysis, self-critique, and confidence scoring before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other agent users use Thinkdeep when complex technical questions, trade-off decisions, code review, root-cause analysis, or risk assessment benefit from structured reasoning and explicit confidence checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured reasoning mode can make answers longer or include visible reasoning summaries and confidence ratings where concise output is required. <br>
Mitigation: Use Thinkdeep for complex questions and avoid activating it for simple transformations, factual lookups, or workflows that require minimal reasoning logs. <br>
Risk: The README installation example uses deep-think while the skill metadata and release slug use thinkdeep. <br>
Mitigation: Verify the ClawHub release slug before installation and prefer the server-resolved slug thinkdeep for this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiajiaoy/thinkdeep) <br>
- [Skill homepage](https://clawhub.ai/skills/thinkdeep) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured reasoning summaries and answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restatement, options, critiques, selected approach, confidence score, and uncertainty notes when the reasoning adds value.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter remains 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
