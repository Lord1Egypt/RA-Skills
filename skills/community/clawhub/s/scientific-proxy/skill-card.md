## Description:

Scientific Proxy helps an agent scrape, test, and format public proxy nodes for common proxy clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtmpss](https://clawhub.ai/user/mtmpss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find public proxy nodes, test basic connectivity, and receive client-specific configuration output for tools such as Clash, V2Ray, Shadowrocket, and v2rayNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Traffic routed through free public proxy nodes may pass through operators the user does not know or trust.

Mitigation: Use only for low-sensitivity traffic and avoid banking, email, work accounts, or other sensitive logins.

Risk: The skill writes scraped and tested proxy details to local workspace files.

Mitigation: Review and remove generated proxy JSON files when they are no longer needed.

Risk: The skill attempts to suppress extra agent warnings and adds promotional or Telegram language-change messages.

Mitigation: Review the skill instructions before installation and treat unrelated promotional steps as nonessential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mtmpss/skills/scientific-proxy)
- [Publisher Profile](https://clawhub.ai/user/mtmpss)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational text with proxy configuration blocks and client setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scraped and tested proxy node details to local workspace JSON files.]

## Skill Version(s):

1.8.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
