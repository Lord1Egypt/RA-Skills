## Description: <br>
Enables an agent to proactively send WeChat text messages and selected attachments through the wxclawbot CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lroolle](https://clawhub.ai/user/lroolle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and operators use this skill to send WeChat reminders, alerts, reports, and media or file notifications from an automated workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to send WeChat messages and attachments using configured bot credentials. <br>
Mitigation: Install only when this sending authority is intended, keep bot tokens and account files private, and require explicit approval before sending sensitive content. <br>
Risk: Messages or files can be sent to the wrong recipient or sent unintentionally during uncertain workflows. <br>
Mitigation: Verify the recipient before sending and use --dry-run for uncertain messages or attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lroolle/wxclawbot-send) <br>
- [wxclawbot-cli repository](https://github.com/lroolle/wxclawbot-cli) <br>
- [wxclawbot-cli npm package](https://www.npmjs.com/package/@claw-lab/wxclawbot-cli) <br>
- [Programmatic API reference](references/programmatic-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, TypeScript snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use --json for programmatic calls; supports dry-run previews and text, image, video, or file sends.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
