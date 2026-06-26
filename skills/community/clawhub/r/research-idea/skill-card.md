## Description: <br>
Launches Clawdbot-native background sessions that research business ideas, write a markdown analysis, and return a verdict and summary to the active chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rqrqrqrq](https://clawhub.ai/user/rqrqrqrq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
ClawHub and Clawdbot users use this skill to turn an `Idea:` chat prompt into background research covering market, technical, business model, go-to-market, validation, and risk analysis. The skill is intended for users who want a practical markdown research report and concise verdict returned to their active chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business ideas may be confidential, and results are returned to the active chat. <br>
Mitigation: Use a private chat for sensitive ideas and confirm the active chat before triggering research. <br>
Risk: The skill stores generated research locally under `~/clawd/ideas/`. <br>
Mitigation: Delete generated sessions or files when the research is no longer needed. <br>
Risk: The background session uses web searches, so findings may depend on public, time-sensitive, or incomplete sources. <br>
Mitigation: Review cited findings before using the report for business decisions. <br>


## Reference(s): <br>
- [Research Idea on ClawHub](https://clawhub.ai/rqrqrqrq/research-idea) <br>
- [Idea Exploration Prompt Template](templates/idea-exploration-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research file with a concise chat summary and verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research is saved under `~/clawd/ideas/<slug>/research.md` and returned to the active chat.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
