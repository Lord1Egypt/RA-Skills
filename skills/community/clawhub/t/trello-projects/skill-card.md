## Description: <br>
Manage Trello boards, lists, cards, comments, labels, checklists, and project workflows via the Trello API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Trello project workflows from an agent, including boards, lists, cards, comments, labels, checklists, members, organizations, Power-Ups, attachments, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to a Trello account through ClawLink. <br>
Mitigation: Install only when the user accepts ClawLink-brokered OAuth access and verify the Trello connection before making tool calls. <br>
Risk: Write-capable Trello actions can delete boards or organizations, archive lists, remove members, or create webhooks. <br>
Mitigation: Use preview and explicit confirmation before destructive or administrative actions, and verify IDs and scopes against the user's intended board, list, card, or workspace. <br>
Risk: Trello permissions and workspace membership determine which resources can be read or changed. <br>
Mitigation: Resolve board, list, card, member, and organization IDs from read operations before writes, and report permission or not-found errors directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/trello-projects) <br>
- [Trello API Documentation](https://developer.atlassian.com/cloud/trello/) <br>
- [Trello REST API Reference](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello Power-Ups](https://trello.com/power-ups) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, Trello tool selection guidance, preview-and-confirm workflows, and structured command examples for ClawLink-backed Trello actions.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
