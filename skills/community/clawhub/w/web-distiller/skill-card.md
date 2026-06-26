## Description: <br>
Fetch agent-ready cleaned Markdown from the Distiller API instead of relying on raw webpage fetches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardyen724-g](https://clawhub.ai/user/edwardyen724-g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn selected webpage URLs into cleaned, agent-ready content through Distiller. It is most useful when raw webpage fetches are too noisy or when an agent workflow needs Markdown, text, or JSON output from public pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected webpage URLs to an external Distiller service, which may expose sensitive or private browsing targets to that provider. <br>
Mitigation: Use the skill only with URLs that are appropriate for Distiller to process, and avoid submitting private or sensitive URLs unless the operator accepts that provider's processing. <br>
Risk: The skill relies on a Distiller API key and an operator-provided API base URL. <br>
Mitigation: Use a dedicated API key where possible, keep it out of shared logs and prompts, and confirm DISTILLER_API_BASE points to the intended HTTPS endpoint. <br>


## Reference(s): <br>
- [ClawHub Web Distiller Skill](https://clawhub.ai/edwardyen724-g/web-distiller) <br>
- [Distiller Service](https://webdistiller.dev) <br>
- [Distiller Dashboard](https://webdistiller.dev/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and optional Markdown, text, or JSON webpage output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DISTILLER_API_BASE and usually DISTILLER_API_KEY; defaults to POST /markdown and reserves POST /distill for paid Starter access.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
