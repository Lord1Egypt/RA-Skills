## Description: <br>
Smart Cost Tracker helps an agent estimate and report AI usage costs, budgets, trends, and local spending history when the user enables tracking or asks about spending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent users use this skill to track estimated model spend, review cost reports, set budget limits, and receive budget alerts while keeping spending history local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad spending and budget triggers may invoke the skill when the user only intended to discuss spending generally. <br>
Mitigation: Confirm whether cost tracking or reporting is intended before reading or updating the cost log for ambiguous spending questions. <br>
Risk: The skill may store or update spending records under ~/.openclaw/cost-log.json. <br>
Mitigation: Keep tracking user-controlled, disclose the local storage path, and tell users they can delete the file to clear history. <br>
Risk: Costs may be estimates when exact token counts are unavailable. <br>
Mitigation: Label approximated values as estimated and use exact token counts when the agent runtime provides them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, files] <br>
**Output Format:** [Markdown and plain text responses with local JSON cost-log updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces estimated costs unless exact token counts are available; writes spending history to ~/.openclaw/cost-log.json only when tracking is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
