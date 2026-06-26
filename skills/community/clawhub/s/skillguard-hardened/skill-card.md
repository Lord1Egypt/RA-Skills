## Description: <br>
SkillGuard Hardened audits OpenClaw skills with local rules and optional Zenmux AI review, then recommends pass, warn, block, or quarantine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2404589803](https://clawhub.ai/user/2404589803) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill marketplace operators, and agent administrators use this skill to inspect installed or incoming OpenClaw skills before installation, update, or execution. It supports security review workflows that may quarantine, restore, or delete risky skills when explicitly configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run arbitrary commands, move skill directories, or delete skill directories. <br>
Mitigation: Install only when a high-privilege security management tool is needed, prefer quarantine over delete, avoid bulk auto-delete, and require explicit confirmation before destructive actions. <br>
Risk: Scanned skill content may be sent to a remote AI provider during AI auditing. <br>
Mitigation: Use a dedicated Zenmux key and review or disable remote AI auditing when scanning private or sensitive skills. <br>
Risk: Guarded execution and remote download flows can affect installation, update, and execution workflows. <br>
Mitigation: Use the guarded execution wrapper only for intended skill commands and verify remote Moltbook downloads before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2404589803/skillguard-hardened) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/2404589803) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples; runtime reports are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include pass, warn, block, or quarantine recommendations; deletion requires explicit force and confirmation flags.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
