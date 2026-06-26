## Description: <br>
Auto-wires new skills into core system by reading SKILL.md, AGENT.md, SOUL.md, and hooks, then injecting onboarding details into soul, memory, and agent files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard newly installed skills by extracting their triggers, rules, sections, and hooks, then preparing the agent's core registration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to write into core agent, soul, workspace, and memory files during onboarding. <br>
Mitigation: Require explicit user confirmation, show a visible diff before writes, keep trigger scope narrow, and provide a clear rollback path before installation or execution. <br>
Risk: The security scan reports a clean verdict but states that scanner concerns are unverified rather than proven because referenced artifact files were not found in its workspace. <br>
Mitigation: Review the actual package contents and file hashes before treating the release as approved for installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyber-bye/skill-onboarder) <br>
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and structured registration entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extraction summaries and idempotent registration updates for agent, soul, workspace, and memory files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
