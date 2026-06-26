## Description: <br>
Provides Ziwei Doushu charting data and interpretation guidance for agents using the MyFate AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[letswinone888](https://clawhub.ai/user/letswinone888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to collect birth details, call MyFate AI charting endpoints, and turn Ziwei Doushu chart data into clear fortune-analysis guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth date, birth time, gender, and related chart parameters are sent to skill.myfate.ai. <br>
Mitigation: Use the skill only with user consent, review the provider's privacy terms, and avoid persisting exact birth details unless the user explicitly requests it. <br>
Risk: The API may require paid quota or recharge before continued use. <br>
Mitigation: Tell users when quota is exhausted, direct them to the provider homepage for billing actions, and resume only after they confirm they want to continue. <br>


## Reference(s): <br>
- [MyFate AI skill homepage](https://skill.myfate.ai) <br>
- [ClawHub skill listing](https://clawhub.ai/letswinone888/ziwei-doushu-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline curl examples and API response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MYFATE_AI_API_KEY environment variable and curl for API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
