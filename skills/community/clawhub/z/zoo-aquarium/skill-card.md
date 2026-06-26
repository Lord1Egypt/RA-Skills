## Description: <br>
Find zoos, aquariums, safari parks, and wildlife sanctuaries, with related travel search support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find zoo, aquarium, safari, wildlife, and related travel options through flyai CLI results, then receive concise Markdown recommendations with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install @fly-ai/flyai-cli globally before use. <br>
Mitigation: Approve installation only after verifying trust in the package and restrict CLI execution to explicit zoo, aquarium, safari, or attraction-search requests. <br>
Risk: The skill may persist raw user travel queries in .flyai-execution-log.json. <br>
Mitigation: Avoid entering sensitive personal travel details and review or delete the local execution log after use. <br>
Risk: Travel recommendations can be incomplete or unavailable when flyai CLI results fail or return no booking link. <br>
Mitigation: Use only results with detailUrl booking links and report failures instead of substituting unsupported knowledge. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the data source and should not expose raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
