## Description: <br>
Automated self-diagnostics: restarts crashed Ollama, repairs broken configs, verifies workspace integrity, and recovers from common failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to add local self-repair behavior to AI workspaces, including Ollama health checks, config repair, workspace file restoration, and scheduled routine execution. It is most relevant for controlled environments where autonomous repair actions are explicitly desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous repair behavior can modify local files and workspace state. <br>
Mitigation: Restrict workspacePath, backupPaths, requiredFiles, and requiredDirs before enabling repair cycles, and keep independent backups outside the managed workspace. <br>
Risk: Process and command helpers can start, stop, or execute local programs. <br>
Mitigation: Remove or hard-gate runCommand and killProcess unless a trusted operator has reviewed the exact commands and process names allowed. <br>
Risk: Hub mode combines localhost HTTP calls, LLM prompting, and scheduled callbacks into a continuously running automation loop. <br>
Mitigation: Enable hub mode only in controlled environments, keep Ollama endpoints local, and avoid exposing prompts, schedules, or configuration to untrusted input. <br>
Risk: Generic HTTP checks and arbitrary scheduled actions may broaden the skill beyond simple self-repair. <br>
Mitigation: Remove or tightly scope generic HTTP checks and custom scheduled callbacks to known internal targets and reviewed actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/self-repair-system) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation and JavaScript code that can emit JSON health reports and local repair logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform local file writes, process starts or stops, localhost HTTP checks, and scheduled callbacks when enabled by the user.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
