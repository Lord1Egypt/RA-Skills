## Description:

Usb is an offline reference tool that provides static USB guidance for devtools workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Usb to retrieve quick USB reference material, including overviews, quickstarts, troubleshooting, performance, security, migration, and cheatsheet guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill emits generic static reference text that may not match a user's specific USB environment, device, or policy requirements.

Mitigation: Treat the output as reference material and validate security, migration, and performance steps against local documentation before acting.

Risk: Some reference sections discuss credentials and configuration even though the artifact does not handle credentials or change systems.

Mitigation: Do not enter secrets into the skill, and review any credential or configuration guidance before applying it in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/usb)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text with Markdown-style headings and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static offline reference output; no external API calls, credentials, or network access are required.]

## Skill Version(s):

2.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
