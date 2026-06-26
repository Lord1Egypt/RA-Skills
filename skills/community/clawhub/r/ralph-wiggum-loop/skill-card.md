## Description: <br>
Runs an iterative Generator, Critic, Fixer, and Verifier loop through LM Studio to improve code or text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to run a local LM Studio-backed loop that reviews, rewrites, and verifies code or text with configurable prompts, model selection, iteration limits, and output format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive code or text may be sent to an untrusted model endpoint if LMSTUDIO_URL is pointed away from localhost. <br>
Mitigation: Keep LMSTUDIO_URL on localhost unless the remote endpoint and model are intentionally trusted, and avoid processing secrets. <br>
Risk: Generated or rewritten code may be incorrect, insecure, or unsuitable for production use. <br>
Mitigation: Review, test, and security-check generated output before using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/ralph-wiggum-loop) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples; runtime output is plain text code or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local LM Studio OpenAI-compatible endpoint; max iterations defaults to 3 and output can be written to stdout or a file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
