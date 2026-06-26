## Description: <br>
Project-based skill isolation and management for configuring per-project skill sets with multi-source installation, version locking, caching, and automatic sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to isolate and synchronize project-specific OpenClaw skill configurations across registry, local, git, and URL sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project configuration can cause the skill to install or synchronize skills from registry, local, git, or URL sources. <br>
Mitigation: Review .openclaw-skills.json before syncing, especially in repositories you do not fully trust, and pin expected skill versions for shared or production projects. <br>
Risk: Automatic synchronization can install missing skills before a user has reviewed the project configuration. <br>
Mitigation: Disable auto-sync for untrusted projects and run synchronization manually after checking the configured skills and sources. <br>
Risk: The security scan reports possible shell-injected command execution from project configuration. <br>
Mitigation: Use a fixed version that validates skill names and executes commands with safe argument arrays, and do not force-install flagged skills without manual review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SuCriss/skill-isolator) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Tutorials](references/tutorials.md) <br>
- [FAQ](references/faq.md) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Example Configuration](references/example-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and Node.js shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or synchronize skills and update local cache state when users run the supplied scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
