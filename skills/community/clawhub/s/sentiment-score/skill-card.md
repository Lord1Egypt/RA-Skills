## Description: <br>
Analyze text sentiment on a scale from -1 (negative) to +1 (positive) using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators can use this skill to score submitted text for positive, negative, or neutral sentiment and receive a numeric sentiment score. It supports CLI-style text processing and an HTTP server mode for integration into agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server mode exposes an unauthenticated network endpoint that can use the installer's OpenAI key. <br>
Mitigation: Prefer CLI mode, or bind the server to localhost and place it behind authentication before making it reachable. <br>
Risk: Submitted text may be sent to OpenAI and can create usage costs on the configured API key. <br>
Mitigation: Use only with text that is appropriate for the configured OpenAI account, and monitor API usage and billing. <br>
Risk: The deploy command references a remote Expanso deployment URL. <br>
Mitigation: Verify the Expanso tooling and deployment URL before running remote deployment commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aronchick/sentiment-score) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON sentiment result with score, label, confidence, and metadata; Markdown usage guidance with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores range from -1 to +1; labels are positive, negative, or neutral.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
