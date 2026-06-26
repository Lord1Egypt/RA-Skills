## Description: <br>
Suggest reusable skills from recurring patterns in local memory files. Human review gate, drafts only to skills/_pending/, local-first runner with optional external fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Skillminer to scan local OpenClaw memory files for recurring work patterns, review candidate skills, and draft accepted candidates into a pending skills directory for human review before promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent local memory files, which may contain private or sensitive user content. <br>
Mitigation: Install only in workspaces where local memory scanning is acceptable, and review generated candidates before accepting or promoting them. <br>
Risk: Setting FORGE_RUNNER=claude sends prompt data to Anthropic's API. <br>
Mitigation: Leave FORGE_RUNNER unset to use the default local OpenClaw runner unless external processing has been explicitly approved. <br>
Risk: Server security evidence reports that documented token redaction should not be relied on until missing pattern data and output-scrubbing gaps are fixed. <br>
Mitigation: Treat redaction as defense in depth, avoid storing secrets in memory files, and inspect local state, review, and draft outputs before sharing or promoting them. <br>
Risk: Generated skill drafts could encode incorrect, misleading, or over-broad guidance. <br>
Mitigation: Keep the human review gate: accept, reject, defer, or silence candidates manually, and scan drafts before moving them from skills/_pending/ into live skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robbyczgw-cla/skillminer) <br>
- [Publisher Profile](https://clawhub.ai/user/robbyczgw-cla) <br>
- [README](README.md) <br>
- [User Guide](USER_GUIDE.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, SKILL.md drafts, JSON state, shell command output, and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft skills are written under skills/_pending/ for human review; local state and review artifacts are written under state/.] <br>

## Skill Version(s): <br>
0.5.3 (source: server evidence, frontmatter, skill.json, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
