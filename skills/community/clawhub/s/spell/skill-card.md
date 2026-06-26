## Description: <br>
Log anything fast and find it later with search and export. Use when running lookups, checking entries, converting formats, generating summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other external users can use Spell to keep a local command-line log of short notes, lookup results, conversion inputs, generated snippets, and similar working text, then search recent entries or export retained data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spell saves user-entered text in plaintext local logs under ~/.local/share/spell, which can retain sensitive data longer than intended. <br>
Mitigation: Do not use Spell for passwords, tokens, regulated data, confidential work, or personal information unless local plaintext retention is acceptable. <br>
Risk: The release evidence notes that export and status behavior appears incorrectly wired in this version. <br>
Mitigation: Validate export and status commands in a disposable environment before relying on them for backup, reporting, or operational workflows. <br>


## Reference(s): <br>
- [Spell on ClawHub](https://clawhub.ai/bytesagain1/spell) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Plain text command-line output with local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/spell and can search or export retained logs.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
