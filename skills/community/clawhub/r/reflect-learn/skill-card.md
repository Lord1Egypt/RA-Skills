## Description: <br>
Self-improvement through conversation analysis that extracts learnings from corrections and success patterns, proposes updates to agent files, or creates new skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevengonsalvez](https://clawhub.ai/user/stevengonsalvez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Reflect to analyze conversations for durable learnings, review proposed agent or skill updates, and preserve approved behavior changes across future sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived learnings may preserve private content or secrets in local state or reflection files. <br>
Mitigation: Review proposed diffs and generated reflection files before approval, avoid approving learnings that contain secrets or private content, and consider setting REFLECT_STATE_DIR to a project-local or private location. <br>
Risk: Hook-based auto-reflection can write local files during context compaction. <br>
Mitigation: Keep auto-reflection disabled until the hook behavior and output locations are understood, and review hook configuration before enabling it. <br>
Risk: Bundled session logs may contain conversation history that users should evaluate before installation or redistribution. <br>
Mitigation: Review bundled logs before installing or sharing the release, and remove or avoid distributing logs that contain private data. <br>


## Reference(s): <br>
- [Signal Detection Patterns](references/signal_patterns.md) <br>
- [Agent Mappings Reference](references/agent_mappings.md) <br>
- [Skill Template Reference](references/skill_template.md) <br>
- [Reflect Hooks Integration](hooks/README.md) <br>
- [Learnings Schema](assets/learnings_schema.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with proposed diffs, shell commands, JSON hook output, YAML state, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Human approval is expected before applying proposed agent or skill changes.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
