## Description: <br>
Zero Token helps OpenClaw agents use a Free-Way fallback gateway so free-tier LLM providers can take over when a primary model fails or token budget is exhausted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtmpss](https://clawhub.ai/user/mtmpss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Zero Token to configure OpenClaw fallback behavior through a local Free-Way gateway when a primary LLM is unavailable or quota-limited. It is most relevant for agents where continuity matters and operators can manage provider API keys and data-routing choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be routed to third-party free-tier LLM providers during fallback, each with its own privacy and retention terms. <br>
Mitigation: Review the configured providers before use, avoid sensitive or regulated prompts unless all provider terms are acceptable, and inform operators and affected users when fallback providers may be used. <br>
Risk: The setup flow requires API keys and installs the third-party Free-Way gateway from a pinned external project. <br>
Mitigation: Review the setup script and pinned Free-Way commit before installing, and use disposable or free-tier provider keys rather than production credentials. <br>


## Reference(s): <br>
- [Zero Token ClawHub Page](https://clawhub.ai/mtmpss/zero-token) <br>
- [Zero Token Homepage](https://github.com/mtmpss/zero-token) <br>
- [Free-Way Gateway](https://github.com/GoDiao/Free-Way) <br>
- [I-Lang Protocol](https://ilang.ai) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Poor Man's Opus](https://github.com/mtmpss/poor-mans-opus) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup and operator guidance for configuring fallback LLM providers and API keys.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
