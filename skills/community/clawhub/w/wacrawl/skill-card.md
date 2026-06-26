## Description: <br>
Read-only local archive and full-text search of macOS WhatsApp Desktop chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chasewebb](https://clawhub.ai/user/chasewebb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use Wacrawl to inspect and search a local macOS WhatsApp Desktop archive through the wacrawl CLI without writing back to WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private WhatsApp chat history and stores a local archive at ~/.wacrawl/wacrawl.db. <br>
Mitigation: Install only if you trust the wacrawl package, protect the archive as sensitive data, and consider whether local backups or scheduled imports should include it. <br>
Risk: Running wacrawl requires Full Disk Access for the terminal or automation environment. <br>
Mitigation: Grant Full Disk Access only to trusted runtimes, review whether scheduled imports are appropriate, and revoke access when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Wacrawl release](https://clawhub.ai/chasewebb/wacrawl) <br>
- [wacrawl project homepage](https://github.com/steipete/wacrawl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly return JSON from the wacrawl CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
