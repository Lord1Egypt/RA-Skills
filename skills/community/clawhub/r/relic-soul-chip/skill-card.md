## Description: <br>
One soul, many agents. Persistent AI personality and cross-agent memory sync via pure Markdown files. Zero deps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucioliu](https://clawhub.ai/user/lucioliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain local Markdown-based personality, user preference, memory, skill, project, and session records across supported agent hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent startup anchor and cross-agent memory sync can retain or move personal memories and raw conversations across systems with inconsistent consent wording. <br>
Mitigation: Review the anchor before manually pasting it, avoid storing secrets or full raw conversations unless explicitly desired, and confirm where host memory sync writes so deletion and rollback are clear. <br>
Risk: The skill performs an optional GitHub version check during session startup. <br>
Mitigation: Disable or block the version check for offline or restricted-network use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucioliu/relic-soul-chip) <br>
- [Agent Router](artifact/AGENT.md) <br>
- [Upload Soul Guide](artifact/docs/upload-soul.md) <br>
- [Load Soul Guide](artifact/docs/load-soul.md) <br>
- [Resonate Soul Guide](artifact/docs/resonate-soul.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions and plain-text anchor content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill that guides local Markdown file reads and writes under ~/relic/brain/ and displays anchor text for manual user copy-paste.] <br>

## Skill Version(s): <br>
2.1.1 (source: evidence.json release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
