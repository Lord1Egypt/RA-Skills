## Description: <br>
Find and book theme park tickets for destinations such as Disney, Universal Studios, Happy Valley, and Chimelong, with real-time availability, pricing, express pass options, and related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search theme park ticket options and related travel services through the flyai CLI, then present booking-ready Markdown results with links sourced from CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI, creating a persistent system change. <br>
Mitigation: Review and approve the npm install manually, verify the @fly-ai/flyai-cli package, and consider running the skill in a contained environment. <br>
Risk: Booking links, prices, and availability come from flyai/Fliggy output and should not be treated as independent travel advice. <br>
Mitigation: Verify booking links, prices, and terms directly before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/theme-park) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the data source; results should include Book links when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
