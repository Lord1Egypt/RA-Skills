## Description: <br>
Robot Resources helps agents reduce LLM API costs with local model routing and compress web pages into token-optimized markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manuelsobrino](https://clawhub.ai/user/Manuelsobrino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and configure Robot Resources for lower-cost LLM routing and token-efficient web scraping. It is most relevant when API cost reduction, compressed web context, or OpenClaw provider setup is the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an external npm installer. <br>
Mitigation: Review the package source, exact install command, and requested setup changes before execution. <br>
Risk: The skill may install a persistent local proxy that reroutes AI traffic. <br>
Mitigation: Confirm the service name, listening port, affected agent configuration, logging behavior, and rollback steps before enabling it. <br>
Risk: The skill may use provider API keys and route requests that incur model-provider costs. <br>
Mitigation: Verify credential handling, provider selection, spend controls, and whether prompts and responses remain local before use. <br>
Risk: The signup flow may require GitHub OAuth or a generated claim URL. <br>
Mitigation: Have the human owner review the OAuth request, account ownership flow, and claim URL handling before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Manuelsobrino/robot-resources) <br>
- [Robot Resources homepage](https://robotresources.ai) <br>
- [Robot Resources full docs](https://robotresources.ai/llms-full.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service setup guidance, provider configuration, API key environment variables, and troubleshooting commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
