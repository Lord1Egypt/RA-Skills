## Description:

Patch an installed OpenClaw dist bundle so third-party OpenAI-compatible Responses endpoints keep prompt_cache_key and prompt_cache_retention instead of having them stripped.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsunheimat](https://clawhub.ai/user/tsunheimat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to patch a local OpenClaw installation so third-party OpenAI-compatible Responses endpoints retain prompt-cache hints. It is intended for local apply, dry-run verification, rollback, and upgrade-aware reapplication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits local OpenClaw installation files under dist/.

Mitigation: Run the dry-run first, confirm the selected OpenClaw root and bundle paths, and consider testing with --root on a copied fixture before applying to the active installation.

Risk: A changed or upgraded OpenClaw bundle may no longer match the expected patch point.

Mitigation: Use the script's target-shape checks and upgrade-aware messages; stop and inspect the new dist layout if the script reports an unexpected shape or missing target.

Risk: The patch or rollback only takes effect after the gateway reloads the modified bundle.

Mitigation: Keep the rollback script available and restart the OpenClaw gateway after apply or rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsunheimat/skills/responses-third-party-prompt-cache-patch)
- [Project link from skill documentation](https://github.com/tsunheimat/openclaw-responses-prompt-cache-patch)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown guidance with inline bash commands and bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, backup, syntax validation, auto-restore on failed patch validation, and rollback behavior.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
