## Description:

Turn a serialized web novel into chapter-by-chapter webnovel audiobook audio with one consistent narrator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, publishers, and developers use this skill to produce chapter-by-chapter webnovel audiobook audio, optionally preserving one narrator voice across later chapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Beatra account capabilities beyond webnovel narration.

Mitigation: Install and authorize it only if you trust Beatra, review the requested account access, and avoid the raw call interface except for known Beatra narration, task, wallet, and upload tools.

Risk: The bundled client silently checks for and can install package updates by default.

Mitigation: Use the documented update controls, including `python3 scripts/mcp_client.py update --auto off`, if automatic updates are not acceptable for the deployment.

Risk: Voice cloning and text-to-speech calls can spend credits and may create duplicate work if retried incorrectly.

Mitigation: Confirm consent, voice choice, and live cost estimates before paid calls, then reuse the same frozen request identity only for recovery of uncertain submissions.

## Reference(s):

- [Webnovel serial-audio workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/webnovel-serial-audio)
- [Beatra skill homepage](https://beatra.ai/skills/webnovel-serial-audio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Beatra task identifiers, audio artifact references, durations, usage, and billing credit summaries when used with live Beatra tools.]

## Skill Version(s):

0.1.2 (source: manifest.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
