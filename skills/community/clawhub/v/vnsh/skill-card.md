## Description:

Securely share files using encrypted, expiring vnsh.dev links with the vnsh CLI for uploading and decrypting shared content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raullenchai](https://clawhub.ai/user/raullenchai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to share local files through encrypted, expiring vnsh.dev links and to decrypt received vnsh.dev links into local temporary files for review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local or agent-generated files to vnsh.dev and can fetch and decrypt vnsh URLs.

Mitigation: Require explicit approval before uploads or downloads, and avoid using it for secrets, private logs, credentials, or sensitive business data.

Risk: The installation guidance includes an unverified pipe-to-shell installer and an unpinned npx command.

Mitigation: Independently verify installation sources and pin or review CLI packages before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raullenchai/skills/vnsh)
- [vnsh website](https://vnsh.dev)
- [Publisher profile](https://clawhub.ai/user/raullenchai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands, plain-text vnsh URLs, and decrypted file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary decrypted files and expiring vnsh.dev share URLs.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
