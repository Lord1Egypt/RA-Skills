## Description: <br>
Adds a Telegram private-chat footer with model, thinking-level, and context-usage details to OpenClaw replies, with dry-run preview, backup, syntax validation, rollback, and restart guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-joey](https://clawhub.ai/user/c-joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and developers use this skill to preview, apply, verify, and roll back a patch that appends model, thinking-level, and context-usage details to Telegram private-chat replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently patches OpenClaw live dist JavaScript files. <br>
Mitigation: Run the dry-run first, review the exact target files, use a controlled or staging instance, confirm backups, and test rollback before production use. <br>
Risk: The applied delivery-path patch reads local OpenClaw session records and exposes provider, model, thinking-level, and context details in Telegram private-chat replies. <br>
Mitigation: Use only on OpenClaw instances you control and confirm that disclosing these details in private-chat replies is acceptable for the deployment. <br>
Risk: Static marker and syntax checks do not prove the live Telegram send path was fixed. <br>
Mitigation: Perform a true gateway process restart and validate with an actual Telegram private-chat reply before considering the patch accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c-joey/telegram-footer-patch) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and patch/revert script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled scripts can modify OpenClaw dist JavaScript files, create timestamped backups, verify syntax with node --check, and restore from backups.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
