## Description: <br>
RFC Document Assistant helps agents look up, list, search, read, and summarize RFC documents for Internet protocol standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunrenyi](https://clawhub.ai/user/lunrenyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical agents use this skill to find RFC documents, inspect protocol specifications by number, search RFC content, and request concise AI-assisted summaries for protocol research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external x-cmd CLI, so installation introduces third-party supply-chain exposure. <br>
Mitigation: Prefer the Homebrew installation path or manually review the install script before execution. <br>
Risk: The curl-to-shell installer executes remote code before the user can review it. <br>
Mitigation: Avoid curl-to-shell on machines with sensitive data unless the user explicitly accepts that risk. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/lunrenyi/x-rfc) <br>
- [x-cmd Skill Repository](https://github.com/x-cmd/skill) <br>
- [x-cmd Installation Guide](data/install.md) <br>
- [x-cmd Release Downloads](https://github.com/x-cmd/release) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return RFC lookup commands, search examples, document excerpts, or summary guidance depending on the user's request.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
