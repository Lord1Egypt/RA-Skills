## Description:

TokPortal helps agents create TikTok and Instagram accounts, distribute videos, upload content, and track analytics through TokPortal tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naybu256](https://clawhub.ai/user/naybu256)

### License/Terms of Use:


## Use Case:

External teams and developers use TokPortal to manage TikTok and Instagram account bundles, scheduled video distribution, uploads, and analytics from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger bulk account creation, uploads, publishing, and other credit-spending TokPortal actions.

Mitigation: Require explicit user approval for bulk creation, publishing, uploads, and credit-spending actions, and use account-level spending limits where available.

Risk: The skill requires a TokPortal API key and can retrieve delivered account credentials and verification codes.

Mitigation: Use a key with the minimum needed permissions, store it outside shared configuration files, and restrict credential or verification-code retrieval to approved workflows.

Risk: The recommended MCP server is installed from an external npm package.

Mitigation: Pin and review the tokportal-mcp package before running it, and update only after reviewing release changes.

## Reference(s):

- [TokPortal developer documentation](https://developers.tokportal.com)
- [TokPortal ClawHub skill listing](https://clawhub.ai/naybu256/skills/tokportal)
- [tokportal-mcp npm package](https://www.npmjs.com/package/tokportal-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions may spend TokPortal credits, publish social content, upload media, and retrieve delivered account credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
