## Description: <br>
Optimize OpenClaw workflows and reduce LLM API costs. Runs locally to reduce repeated context, unnecessary steps, and token waste with no workflow changes required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[immrlucky](https://clawhub.ai/user/immrlucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure Spectyra as a local model gateway that routes spectyra/* models through a companion service for workflow and token-cost optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently set spectyra/smart as the default route for future OpenClaw model traffic. <br>
Mitigation: Review the OpenClaw configuration after installation and remove the spectyra/smart default if that routing is not intended. <br>
Risk: The companion package may handle sensitive model prompts or credentials as part of local gateway routing. <br>
Mitigation: Inspect or verify @spectyra/local-companion before using the skill with sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/immrlucky/spectyra) <br>
- [Spectyra homepage](https://spectyra.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures OpenClaw model routing to a local companion service on 127.0.0.1:4111.] <br>

## Skill Version(s): <br>
1.0.25 (source: server release evidence, package.json, skill.json; SKILL.md frontmatter lists 1.0.24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
