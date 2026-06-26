## Description: <br>
Send Slybroadcast ringless voicemail campaigns from OpenClaw/LLMs using CLI or MCP, including AI voice generation (ElevenLabs or generic HTTP voice API) and campaign controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, operators, and developers use this skill to prepare and send Slybroadcast ringless voicemail campaigns from an agent workflow, including selecting recipients, choosing or generating audio, scheduling delivery, and checking campaign status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send voicemail campaigns and control campaign state, creating legal, cost, recipient, and reputational impact if used without authorization or review. <br>
Mitigation: Before any send or campaign-control action, require manual confirmation of recipients or list IDs, caller ID, message or audio source, schedule, cost or quota impact, and legal authorization to contact the recipients. <br>
Risk: Slybroadcast and ElevenLabs credentials, voicemail text, and voicemail audio may be exposed through prompts, logs, or public staging URLs. <br>
Mitigation: Store credentials securely, redact them from prompts and logs, and avoid placing sensitive voicemail audio or text in publicly reachable staging URLs. <br>
Risk: The security review notes high-impact sending authority without enough reviewed implementation detail for the local CLI or MCP behavior. <br>
Mitigation: Install only if you trust the local CLI or MCP implementation, inspect it before use, and require human approval for send and campaign-control actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Slybroadcast credentials; public audio staging and ElevenLabs credentials are optional depending on audio source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
