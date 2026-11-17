## Description:

Weeko CLI commands for bookmark management. Search, add, update, delete bookmarks. Create and organize groups. Batch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupy5](https://clawhub.ai/user/occupy5)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Weeko CLI bookmark and group management tasks, including search, creation, updates, deletion, and batch organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can delete bookmarks, groups, and batches of bookmarks, including group deletion that removes contained bookmarks.

Mitigation: Require explicit user confirmation and a reviewed target list before delete, group delete, or batch delete commands; use `--dry-run` where supported before making changes.

Risk: The skill depends on a mutable global `weeko-cli` package and the Weeko service.

Mitigation: Install only from trusted sources, pin or review the CLI version where possible, and confirm the Weeko service endpoint before use.

Risk: Weeko API keys may be stored locally or supplied through environment variables.

Mitigation: Keep API keys out of chat logs and shared transcripts, use least-privilege operational practices, and rotate credentials if exposure is suspected.

Risk: A custom `WEEKO_API_URL` can redirect CLI operations to an unexpected service.

Mitigation: Avoid custom API URLs unless the user controls and trusts the endpoint.

## Reference(s):

- [Weeko homepage](https://weeko.blog)
- [Weeko CLI repository](https://github.com/nicepkg/weeko)
- [weeko-cli npm package](https://www.npmjs.com/package/weeko-cli)
- [Bun runtime](https://bun.sh)
- [Command reference](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/occupy5/skills/weeko)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON, TOON, or pretty CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of Weeko CLI output formats, including JSON by default and TOON for token-efficient agent consumption.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
