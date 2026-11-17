## Description:

URL Manager helps agents save, organize, search, and share URLs and text notes through a hosted card-based knowledge library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piccolo123](https://clawhub.ai/user/piccolo123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to save web links or notes, organize them into personal or shared categories, search collections, and deliver curated collections through magic links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service can create an agent account and store saved URLs and metadata on ai.ocean94.com.

Mitigation: Inform the user before first use and avoid saving sensitive URLs or notes unless they accept the hosted-service terms.

Risk: The skill keeps a local bearer token for reuse across sessions.

Mitigation: Store the token with restricted file permissions, keep it out of logs and shared artifacts, and rotate it if exposure is suspected.

Risk: Generated magic links and invite links can grant access to card-based collections or shared categories.

Mitigation: Treat generated links and invite codes as secrets and share them only with intended recipients.

Risk: The documented recovery path clones a remote repository without a pinned revision.

Mitigation: Prefer the packaged artifact; if recovery is necessary, pin and verify the source before copying executable files.

Risk: Plaintext HTTP endpoints appear in the allowed endpoint list for local or private-network use.

Mitigation: Use the default HTTPS endpoint for real data and tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piccolo123/skills/url-manager)
- [URL Manager hosted service](https://ai.ocean94.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text responses with optional JSON command output and generated links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist a local bearer token and create hosted URL records through ai.ocean94.com.]

## Skill Version(s):

2.6.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
