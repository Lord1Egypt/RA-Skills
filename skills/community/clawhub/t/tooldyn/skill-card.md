## Description: <br>
Intent-based tool selection for OpenClaw agents that recommends relevant tools for the latest user message and returns a short usage hint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Peter7397](https://clawhub.ai/user/Peter7397) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to choose a small, relevant tool set for a user request before calling tools. It is especially aimed at Feishu and Ollama-style setups where reducing tool context can improve reliability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent toward shell, file, and Feishu tools with broad keyword matching. <br>
Mitigation: Install only when intent-based tool selection is desired, and review or edit the mappings so sensitive tools such as exec, write, and Feishu management tools require explicit user intent. <br>
Risk: The README describes optional OpenClaw bundle patching for gateway-level filtering. <br>
Mitigation: Avoid applying the optional patch unless the exact change has been audited, tested, and can be rolled back. <br>


## Reference(s): <br>
- [Dynamic Tool on ClawHub](https://clawhub.ai/Peter7397/tooldyn) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Configuration, Shell commands] <br>
**Output Format:** [JSON object with recommended tool names, hint text, and a short explanatory message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keyword-based recommendations include exec by default and return at most 8 tool names.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, manifest.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
