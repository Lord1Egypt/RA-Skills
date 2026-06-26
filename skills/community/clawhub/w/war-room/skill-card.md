## Description: <br>
Multi-agent war room for brainstorming, system design, architecture review, product specs, business strategy, or other complex problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxkle1nz](https://clawhub.ai/user/maxkle1nz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, product builders, and strategy teams use War Room to run structured multi-agent planning sessions with specialist roles and adversarial review. The skill helps produce decision logs, specialist notes, consolidated blueprints, post-mortems, and concrete next-action plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may schedule recurring follow-up checks that outlive the user's immediate session expectations. <br>
Mitigation: Require explicit approval before scheduling follow-ups, show the user how to view or cancel scheduled jobs, and set clear stop conditions. <br>
Risk: The workflow may proactively open generated files with the operating system viewer. <br>
Mitigation: Ask for consent before opening files, restrict opened paths to the project war room workspace, and provide file paths as a non-opening alternative. <br>
Risk: Briefs, DNA files, and agent outputs may contain sensitive planning or business information. <br>
Mitigation: Use a dedicated workspace and avoid placing secrets, credentials, or sensitive personal data in war room files. <br>


## Reference(s): <br>
- [War Room ClawHub release](https://clawhub.ai/maxkle1nz/war-room) <br>
- [Agent Roles](references/agent-roles.md) <br>
- [DNA Template](references/dna-template.md) <br>
- [Wave Protocol](references/wave-protocol.md) <br>
- [Initialization Script](scripts/init_war_room.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, filesystem workspace structure, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates project-local war-rooms/<project>/ files and directories; generated session content depends on the selected specialist roles and user-provided brief.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
