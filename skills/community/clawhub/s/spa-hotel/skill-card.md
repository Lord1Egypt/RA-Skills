## Description: <br>
Book flights to spa hotels and wellness resort destinations, with support for related travel planning tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an agent for spa hotel and wellness resort flight options, compare routes, and receive booking-oriented Markdown results from live flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global npm CLI package for broad travel requests. <br>
Mitigation: Install a pinned @fly-ai/flyai-cli version in an isolated environment and require explicit approval before running npm i -g. <br>
Risk: Travel answers may be misleading if produced without live flyai CLI output. <br>
Mitigation: Require successful CLI execution and booking links before presenting travel options to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/spa-hotel) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI results for travel data and booking links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
