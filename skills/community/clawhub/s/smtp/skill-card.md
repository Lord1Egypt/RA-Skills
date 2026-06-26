## Description: <br>
Send, test, and debug SMTP mail flows with safe dry runs, provider-aware auth, and deliverability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, test, send, and debug outbound SMTP flows. It supports provider setup, TLS and auth diagnostics, canary sends, bounce interpretation, and deliverability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live SMTP actions can send message content, headers, recipients, and attachments to configured SMTP providers. <br>
Mitigation: Require explicit confirmation before any live send, external-recipient test, or multi-recipient action, and start with one approved canary inbox. <br>
Risk: SMTP credentials, tokens, recipient lists, or mail metadata could be retained in local notes. <br>
Mitigation: Use approved runtime secret sources, never store raw credentials under ~/smtp/, redact logs, and keep only the smallest reusable debugging evidence. <br>
Risk: A server acceptance response can be mistaken for final delivery. <br>
Mitigation: Treat queue acceptance as pending until bounce evidence, mailbox placement, spam-folder checks, or provider logs confirm the final state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/smtp) <br>
- [Skill homepage](https://clawic.com/skills/smtp) <br>
- [setup.md](artifact/setup.md) <br>
- [send-flow.md](artifact/send-flow.md) <br>
- [diagnostic-playbook.md](artifact/diagnostic-playbook.md) <br>
- [swaks-recipes.md](artifact/swaks-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local notes under ~/smtp/; credentials should come only from approved runtime secret sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
