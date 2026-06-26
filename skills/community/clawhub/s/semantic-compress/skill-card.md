## Description: <br>
语义压缩 helps an agent build compression prompts that preserve key meaning while removing redundant text to reduce token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[licool88](https://clawhub.ai/user/licool88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to compress long conversation histories, articles, or documents into tighter prompts before sending them to an LLM. Review compressed output before relying on it, especially for factual, sensitive, or long-term-memory use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overpromise lossless or accuracy-preserving compression for text that still needs human or model judgment. <br>
Mitigation: Review compressed output against the source before relying on it for decisions, records, or downstream automation. <br>
Risk: Conversation histories can contain secrets or personal data before they are saved or sent through a compression workflow. <br>
Mitigation: Redact secrets and personal data before preserving compressed history in long-term memory or sharing it with another model. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/licool88/semantic-compress) <br>
- [README](README.md) <br>
- [System compression prompt](prompts/system-compress.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript examples; runtime helpers return prompt text and length estimates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a prompt for an external LLM rather than performing guaranteed lossless compression locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
