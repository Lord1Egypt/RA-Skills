## Description: <br>
Cost-optimize AI agent operations by routing tasks to appropriate models based on complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigabit-eth](https://clawhub.ai/user/gigabit-eth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use SwitchBoard to choose lower-cost or higher-capability models for OpenClaw sessions and sub-agents based on task complexity, latency, context, and tool-use needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenRouter credentials and routed prompts may be exposed if users route secrets, private data, or sensitive work through free or unmoderated third-party models. <br>
Mitigation: Protect the OpenRouter key, set budget limits when available, review model privacy policies, and do not route API keys, passwords, or private PII through free or unmoderated models. <br>
Risk: The package metadata links do not clearly match this skill, so external repository or issue links may not be reliable provenance signals. <br>
Mitigation: Rely on the ClawHub publisher profile and server-resolved release evidence first, and verify external metadata before using it for support or trust decisions. <br>


## Reference(s): <br>
- [OpenRouter Models Reference](references/openrouter-models.md) <br>
- [OpenRouter Model Catalog Snapshot](references/openrouter-models.json) <br>
- [OpenRouter Documentation](https://openrouter.ai/docs) <br>
- [ClawHub skill page](https://clawhub.ai/gigabit-eth/router) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with configuration snippets and model-routing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key for non-default model routing; model prices and availability should be checked against provider documentation before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
