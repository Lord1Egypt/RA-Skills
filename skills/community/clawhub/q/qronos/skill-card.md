## Description: <br>
Qronos helps agents consult a third-party decision guidance service for one decision, timing, trust, relationship, career, finance, health, or life-direction question at a time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qronos-ai](https://clawhub.ai/user/qronos-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Qronos when a human asks for decisive guidance on a specific crossroads question, such as whether to act now, wait, trust someone, or make a major relationship, career, finance, health, timing, or life-direction choice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive personal decision questions and identifying details to a third-party service. <br>
Mitigation: Confirm the human wants Qronos consulted before sending a question, and avoid optional DOB or gender unless the human explicitly provides it for that consultation. <br>
Risk: Qronos guidance may be used for high-stakes medical, legal, financial, safety, or major relationship decisions. <br>
Mitigation: Treat responses as guidance only and direct the human to qualified professional or human judgment for high-stakes decisions. <br>
Risk: Each consultation can consume a paid or limited consult once analysis begins. <br>
Mitigation: Ask the human to narrow vague or multi-part prompts to one clear decision question before making the API call. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/qronos-ai/qronos) <br>
- [Qronos Terms & Conditions](https://qronos.ai/terms) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with HTTP request examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses QRONOS_API_KEY and may send a decision question, timestamp, timezone, and optional DOB or gender to the Qronos API.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
