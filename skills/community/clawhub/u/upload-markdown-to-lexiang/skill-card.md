## Description:

Uploads Markdown documents with local images and formulas to editable Tencent Lexiang pages, with local preflight, deterministic mixed text/image upload, and remote verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajaxhe](https://clawhub.ai/user/ajaxhe)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent skill authors use this skill to publish Markdown with local images, formulas, and portable callouts to Tencent Lexiang pages. It supports creating a new page or updating an existing entry after local preflight and remote verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved Lexiang personal tokens can be exposed if credential files are placed in shared or weakly protected locations.

Mitigation: Keep credential files in a private user-owned directory, avoid --credential-file or LEXIANG_UPLOAD_CREDENTIALS paths in shared directories, and rely on private credential storage where possible.

Risk: A personal Lexiang MCP token can create or update pages available to that account.

Mitigation: Install only when this uploader is needed, use the least-appropriate Lexiang account or profile for the task, and keep the token out of shared files and logs.

Risk: Using the wrong entry ID can overwrite an existing Lexiang page.

Mitigation: Run --dry-run first and verify --entry-id before updating an existing page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajaxhe/skills/upload-markdown-to-lexiang)
- [CLI Contract](references/cli-contract.md)
- [Lexiang personal credential page](https://lexiangla.com/ai/claw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with bash examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI API 1; successful uploads can return a Lexiang page URL and JSON status when --json is used.]

## Skill Version(s):

1.3.1 (source: frontmatter, README, CLI contract, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
