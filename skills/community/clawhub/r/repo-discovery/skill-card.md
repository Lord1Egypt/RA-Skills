## Description: <br>
Repository Discovery helps agents inspect an unfamiliar GitHub repository and produce a structured briefing of its architecture, technology stack, dependencies, features, configuration, development workflow, and testing strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigd0g](https://clawhub.ai/user/pigd0g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill when starting work in a new or unfamiliar repository, preparing technical due diligence, or creating repository documentation for future development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect environment and configuration files while documenting repository setup, which can expose sensitive values if real secrets are read or copied. <br>
Mitigation: Instruct the agent not to read real .env files or copy secret values, and require confirmation before creating or overwriting REPO_DISCOVERY.md. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown file named REPO_DISCOVERY.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured repository briefing with sections for purpose, technology stack, dependencies, architecture, features, configuration, development workflow, testing strategy, observations, and unknowns.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
