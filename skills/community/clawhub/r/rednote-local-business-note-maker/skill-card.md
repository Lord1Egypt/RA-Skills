## Description:

Create a Xiaohongshu local business post or REDnote local business post from storefront photos, service images, a merchant brief, or brand references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, local business marketers, and agents use this skill to plan and generate a three-slide REDnote or Xiaohongshu local-business discovery note from a storefront photo, service image, merchant brief, or brand reference. It helps produce visit-oriented visuals, title ideas, caption beats, fact checks, and tags while keeping business claims limited to user-supplied facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared Beatra device authorization that can spend credits and access broader media capabilities than this REDnote workflow requires.

Mitigation: Install only if the publisher is trusted, review the Beatra approval scopes, monitor paid confirmations, and revoke the device from the Beatra Console when no longer needed.

Risk: The bundled client can silently self-update executable package files.

Mitigation: Consider disabling silent checks with `python3 scripts/mcp_client.py update --auto off` and review updates before continued use.

Risk: Uploaded storefront, service, or brand-reference media may contain sensitive local business details.

Mitigation: Avoid uploading sensitive local files and confirm that business facts, claims, and embedded text are user supplied before generation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/rednote-local-business-note-maker)
- [Beatra skill page](https://beatra.ai/skills/rednote-local-business-note-maker)
- [Local-business note planning](artifact/references/local-business-note-planning.md)
- [Local-business workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [MCP connection](artifact/references/mcp-connection.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, image artifacts, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured prompts, confirmations, command examples, artifact links, and returned task facts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ordered image artifact references, task IDs, dimensions, resolved model, and net charged credits when returned by Beatra.]

## Skill Version(s):

0.1.1 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
