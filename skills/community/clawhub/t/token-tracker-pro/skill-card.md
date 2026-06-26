## Description: <br>
Tracks OpenClaw session token usage, summarizes daily, weekly, and cumulative consumption, and provides token-saving and model-selection suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longziruo-max](https://clawhub.ai/user/longziruo-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to monitor local token consumption, inspect usage history, export reports, and get practical suggestions for reducing token costs. It also supports optional local dashboard and shortcut workflows for repeated operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes local command execution paths through Node CLI wrappers. <br>
Mitigation: Install only from a trusted publisher, review the wrapper code before use, and avoid passing untrusted arguments to the global token-tracker command. <br>
Risk: Shortcut setup can persist changes to shell profile files or OS launcher locations. <br>
Mitigation: Run shortcut setup only after reviewing the generated changes and only on systems where persistent shortcut/profile edits are acceptable. <br>
Risk: Token history, exports, and dashboard views can include session-linked usage metadata. <br>
Mitigation: Treat exported reports and local dashboard access as sensitive, restrict local access, and clear or back up history according to the user's data-retention needs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/longziruo-max/token-tracker-pro) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [OpenClaw Integration Guide](artifact/INTEGRATION.md) <br>
- [Smart Recommendation Guide](artifact/SMART-RECOMMENDATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text reports, Markdown/JSON/CSV exports, TypeScript integration snippets, and local dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores token history locally and may expose session-linked usage metadata through exports or the local dashboard.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
