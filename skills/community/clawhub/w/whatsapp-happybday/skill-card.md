## Description: <br>
Monitor WhatsApp groups to dynamically detect people who should be congratulated. It identifies keywords (e.g., "birthday", "congratulations") and the person's name using a score-based system, then automatically sends a random customizable congratulatory message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero-astro](https://clawhub.ai/user/zero-astro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor WhatsApp groups for birthday or congratulatory messages and, when configured, send a generated congratulatory reply through wacli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously read WhatsApp group chats and send messages from the user's account. <br>
Mitigation: Keep BIRTHDAY_SIMULATE=true during testing, use the skill only in groups where participants have agreed to automated monitoring, and avoid sensitive chats. <br>
Risk: Weak scoping can allow the monitor to inspect or act across more groups than intended. <br>
Mitigation: Do not enable scheduled execution or real sending unless the deployment scope is acceptable; prefer adding a group allowlist before production use. <br>
Risk: Command execution through shell=True creates command-injection exposure. <br>
Mitigation: Prefer a safer implementation that removes shell=True and passes command arguments without shell interpolation before enabling real sending. <br>
Risk: Automated birthday detection can produce false positives and unwanted posts. <br>
Mitigation: Tune BIRTHDAY_MIN_MESSAGES and BIRTHDAY_CONFIDENCE_THRESHOLD, maintain the skip list, and require approval before each real WhatsApp message when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zero-astro/whatsapp-happybday) <br>
- [Project homepage from clawdis metadata](https://github.com/zero-astro/whatsapp-happybday) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and script console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can read local WhatsApp data through wacli, write JSON state, and send WhatsApp messages when simulation mode is disabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
