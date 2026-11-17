## Description:

Turn Xiaohongshu parent FAQ notes into a 4 to 8 still answer set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education content creators use this skill to turn public Xiaohongshu parent questions and confirmed teaching facts into 4 to 8 answer stills. It guides an agent through slot planning, explicit approval before paid lookup or image work, result review, and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared Beatra account credential that can do more than this single still-image workflow.

Mitigation: Install only if Beatra is trusted, review the requested authorization scopes, and keep the credential in the private credential file rather than in chat, logs, command arguments, or environment variables.

Risk: The bundled client silently checks for and can install executable package updates.

Mitigation: Review the automatic-update behavior before installation and disable silent checks with `python3 scripts/mcp_client.py update --auto off` when local review is required before changes.

Risk: Local asset upload can expose an unintended file if the wrong asset is selected.

Mitigation: Inspect the selected file first and upload only the exact intended asset through the bundled client.

Risk: Paid lookup or generation work can be duplicated if a transport failure is retried with changed arguments or a new request identity.

Mitigation: Use the explicit approval cards, keep one opaque `client_request_id` per approved request, and retry only byte-identical arguments when delivery is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/xiaohongshu-parent-faq-stills)
- [Beatra package homepage](https://beatra.ai/skills/xiaohongshu-parent-faq-stills)
- [Parent FAQ still workflow](references/workflow.md)
- [Xiaohongshu parent FAQ lookup](references/parent-faq-lookup.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Tasks and results](references/tasks-and-results.md)
- [Installation and authentication](references/installation-and-auth.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead to Beatra social lookup, image generation, image transformation, image editing, asset upload, wallet, and task operations after the required user confirmations.]

## Skill Version(s):

0.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
