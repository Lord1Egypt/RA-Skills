## Description: <br>
Routes prompts to Venice.ai models by classifying complexity, selecting a cost tier, and supporting streaming, web search, private-only mode, function calling, budget controls, and reasoning mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PlusOne](https://clawhub.ai/user/PlusOne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send prompts through Venice.ai while controlling model tier, cost, privacy posture, tool calling, web search, and conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prompt, conversation, or tool data can leave the machine or appear in output when sent through the router. <br>
Mitigation: Use a dedicated Venice API key with spending limits and do not pass secrets through prompts, conversation files, or tool arguments unless that disclosure is acceptable. <br>
Risk: The private-only privacy promise is not reliably enforced according to the security evidence. <br>
Mitigation: Avoid relying on private-only mode for confidential workloads until the model-selection issue is fixed and review the selected model before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PlusOne/venice-router) <br>
- [Venice.ai Router OpenClaw source](https://github.com/PlusOne/venice.ai-router-openclaw) <br>
- [Venice.ai](https://venice.ai) <br>
- [Venice.ai API Docs](https://docs.venice.ai) <br>
- [OpenClaw](https://github.com/PlusOne/openclaw) <br>
- [Venice.ai Model Reference](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Plain text or Markdown responses, optional JSON for classification and routing metadata, and streamed terminal output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports model-tier controls, web search, tool definitions, conversation files, session IDs, and budget status output.] <br>

## Skill Version(s): <br>
1.5.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
