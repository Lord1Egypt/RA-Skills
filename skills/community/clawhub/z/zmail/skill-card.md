## Description: <br>
zmail helps agents sync email over IMAP into a local maildir and SQLite FTS index, then search, read threads, inspect contacts and attachments, and answer mailbox questions through its CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cirne](https://clawhub.ai/user/cirne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation engineers, and agent users use zmail to give an assistant controlled access to a local email index for mailbox search, message review, contact lookup, attachment inspection, and synthesized answers about mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires IMAP mailbox credentials and an OpenAI API key for setup and LLM-backed features. <br>
Mitigation: Use app-specific mailbox credentials, protect the local ~/.zmail directory and backups, and rotate credentials if they are exposed. <br>
Risk: LLM-backed commands such as ask, inbox, and enriched contact lookup can send email-derived text to OpenAI or other providers. <br>
Mitigation: Use those commands only when the mailbox owner accepts that data flow; use local search, read, thread, who, and attachment primitives when provider calls are not acceptable. <br>
Risk: Shell command construction around email text can introduce command-injection risk. <br>
Mitigation: Invoke zmail with argument arrays or careful quoting, and do not paste untrusted mail text into sh -c command strings. <br>
Risk: Local cleanup can delete cached mail, indexes, credentials, and extracted local-only artifacts under ZMAIL_HOME. <br>
Mitigation: Treat setup --clean --yes as a local destructive operation, confirm backups and expected state first, and resync from IMAP afterward when needed. <br>


## Reference(s): <br>
- [ClawHub zmail release page](https://clawhub.ai/cirne/zmail) <br>
- [zmail project homepage](https://github.com/cirne/zmail) <br>
- [Canonical docs and discovery](references/CANONICAL-DOCS.md) <br>
- [OpenClaw skill requirements](https://docs.openclaw.ai/tools/creating-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI-oriented configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to commands that return JSON, text tables, mailbox summaries, message content, thread context, contacts, and attachment metadata.] <br>

## Skill Version(s): <br>
0.1.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
