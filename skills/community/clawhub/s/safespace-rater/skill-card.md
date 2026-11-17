## Description:

Use when users need to audit local OpenClaw skills, generate trust scores, and optionally publish those scores to SafeSpace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vpn2004](https://clawhub.ai/user/vpn2004)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit local OpenClaw skills, generate security and trust scores, save concise audit reports, and optionally submit reputation ratings to SafeSpace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can automatically download, build, and execute a mutable external Go binary when normal commands are run.

Mitigation: Use a preinstalled, trusted safespace-rater binary through SAFESPACE_RATER_BIN, or review and pin the remote module before allowing automatic installation.

Risk: Audit reports, ratings, pending uploads, and optional LLM fallback data may leave the local machine.

Mitigation: Run local-only audits with dry-run settings when upload is not intended, and review report contents before enabling submissions or LLM fallback.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown audit reports and pending upload queue files under the user's SafeSpace directory.]

## Skill Version(s):

1.3.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
