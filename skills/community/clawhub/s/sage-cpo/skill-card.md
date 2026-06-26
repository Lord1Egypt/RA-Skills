## Description: <br>
Sage CPO is an AI chief product officer for 1-30 person startup teams that helps pair on user insight, MVP definition, product-market fit, roadmaps, service productization, and persistent product memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, and small startup teams use this skill as a persistent product strategy partner for product discovery, prioritization, MVP planning, roadmap tradeoffs, packaging, pricing, and product operating-system cadence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite workspace agent instruction files and create persistent product memory. <br>
Mitigation: Review and back up AGENTS.md, CLAUDE.md, SOUL.md, IDENTITY.md, TOOLS.md, USER.md, and HEARTBEAT.md before running bootstrap scripts. <br>
Risk: The persistent ~/.sage memory can accumulate sensitive business or personal information. <br>
Mitigation: Avoid storing secrets, API keys, banking details, private links, or sensitive personal data in ~/.sage. <br>


## Reference(s): <br>
- [Sage CPO ClawHub listing](https://clawhub.ai/billzhuang6569/sage-cpo) <br>
- [CPO identity](references/cpo-identity.md) <br>
- [CPO product operating system](references/cpo-product-operating-system.md) <br>
- [CPO scenarios](references/cpo-scenarios.md) <br>
- [Sage DNA protocol](references/sage-dna-protocol.md) <br>
- [Write routing](references/write-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with optional shell commands and workspace memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update long-lived Sage memory files under ~/.sage and workspace agent identity files when the user runs the included scripts.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
