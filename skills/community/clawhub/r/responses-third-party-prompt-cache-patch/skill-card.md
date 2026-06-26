## Description: <br>
Patch an installed OpenClaw dist bundle so third-party OpenAI-compatible Responses endpoints keep prompt_cache_key and prompt_cache_retention instead of having them stripped. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsunheimat](https://clawhub.ai/user/tsunheimat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to apply, verify, and roll back a local bundle patch that preserves Responses prompt-cache hints for third-party OpenAI-compatible endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes directly into an installed OpenClaw dist bundle. <br>
Mitigation: Run the dry-run first, test with --root against a copied install or fixture, and keep the generated backups before restarting the gateway. <br>
Risk: The patch may be applied to a different OpenClaw install or bundle version than intended. <br>
Mitigation: Confirm the resolved OpenClaw root and target bundle before applying; use --root to select a specific installation. <br>
Risk: Gateway behavior does not change until the running service reloads the modified bundle. <br>
Mitigation: Restart the OpenClaw gateway only after confirming the patch or rollback completed and node --check passed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsunheimat/responses-third-party-prompt-cache-patch) <br>
- [Skill-provided source link](https://github.com/tsunheimat/openclaw-responses-prompt-cache-patch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline bash commands and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run, timestamped backups, syntax validation, rollback, and upgrade-aware reapply behavior.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
