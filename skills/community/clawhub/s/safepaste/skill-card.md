## Description: <br>
Safepaste checks OpenClaw prompts, configuration snippets, and tips against a user's actual setup before applying them, with auto-detection, compatibility analysis, exact modification previews, safe apply, and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocanome](https://clawhub.ai/user/rocanome) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use Safepaste to review proposed prompt, skill, cron, model-routing, and configuration changes against their local setup before adding them. It helps identify conflicts, redundant guidance, cost implications, permission expansions, and safer modified versions before any apply action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and can modify sensitive OpenClaw setup files. <br>
Mitigation: Review the exact diff and confirm the backup path before approving any apply action. <br>
Risk: The skill makes broad local/privacy claims while analysis may use the configured LLM provider and local usage state may be stored. <br>
Mitigation: Install only if that data flow is acceptable for the workspace, and treat privacy claims as dependent on the active agent and provider configuration. <br>


## Reference(s): <br>
- [Safepaste homepage](https://clawmentor.ai/safepaste) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose exact changes, show diffs, create backups, apply approved changes, and provide rollback guidance.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
