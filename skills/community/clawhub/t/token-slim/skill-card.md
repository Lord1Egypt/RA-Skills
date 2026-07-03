## Description: <br>
Guided token optimization for AI agent workspaces that audits project context files, estimates token savings, and guides cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use token-slim to reduce recurring context-token costs by scanning always-loaded workspace files, identifying bloat, and guiding safe cleanup. It supports first-time onboarding, on-demand rescans, dry-run previews, and optional concise-output configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change future agent behavior by modifying workspace agent configuration. <br>
Mitigation: Run scans in dry-run mode first, review exact config blocks before accepting changes, and create backups before modifying files. <br>
Risk: The optional tiktoken installer can run pip installation and fetch tokenizer cache data from external sources. <br>
Mitigation: Skip the installer in restricted environments or use heuristic counting; only run installation when pip access and external cache downloads are acceptable. <br>
Risk: Batch mode can apply multiple cleanup changes without per-item confirmation. <br>
Mitigation: Use confirm mode for normal operation and reserve batch mode for workspaces where every proposed change has already been reviewed or is trusted. <br>


## Reference(s): <br>
- [Token Saving Strategies](references/strategies.md) <br>
- [Mode A: First-time Setup](references/mode-a-onboarding.md) <br>
- [Mode B: On-demand Re-scan](references/mode-b-rescan.md) <br>
- [tiktoken](https://github.com/openai/tiktoken) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner supports dry-run and JSON modes; precise token counting depends on optional tiktoken availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
