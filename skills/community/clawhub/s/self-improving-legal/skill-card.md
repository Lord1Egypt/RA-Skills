## Description: <br>
Captures clause risks, compliance gaps, precedent shifts, contract deviations, regulatory changes, and litigation exposure to enable continuous legal operations improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal operations teams and agent users use this skill to capture reusable, process-level lessons from clause risks, compliance gaps, contract deviations, regulatory changes, precedent shifts, and litigation exposure. It is intended for legal-focused workspaces where persistent legal memory and promotion into playbooks, checklists, or risk registers are desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional hooks can run on every prompt and may add broad reminders into agent context. <br>
Mitigation: Enable hooks only in legal-focused workspaces, prefer project-local installation, and replace empty hook matchers with legal-specific triggers. <br>
Risk: Persistent legal learning files can influence future agent behavior if inaccurate, privileged, or overbroad entries are promoted. <br>
Mitigation: Keep .learnings out of source control unless reviewed, avoid privileged or confidential details, and require human approval before promoting entries into agent instruction files or generated skills. <br>


## Reference(s): <br>
- [OpenClaw Legal Integration](artifact/references/openclaw-integration.md) <br>
- [Legal Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Legal Entry Examples](artifact/references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-legal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, hook code, and generated markdown log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or guides creation of project-local legal learning files and optional hook reminders; persistent entries should be reviewed before promotion into agent instructions or reusable skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
