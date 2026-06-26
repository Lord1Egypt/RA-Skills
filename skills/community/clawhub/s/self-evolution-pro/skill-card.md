## Description: <br>
Self Evolution Pro helps agents record learnings, analyze root causes, maintain a knowledge graph, synchronize cross-session notes, and promote recurring patterns into reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent capture corrections, errors, feature requests, and recurring lessons, then review or promote them into guidance, skills, and ClawHub releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can preserve long-term self-learning notes and change future agent guidance. <br>
Mitigation: Require explicit review before saving sensitive content or promoting notes into instruction files; redact secrets and confidential project details from learning logs. <br>
Risk: Cross-session synchronization and spawned background agents can spread unreviewed learnings. <br>
Mitigation: Require manual approval before syncing sessions or spawning agents, and share only reviewed summaries. <br>
Risk: Scheduled reviews and generated-skill publishing may automate changes beyond the immediate task. <br>
Mitigation: Keep scheduled reviews approval-gated, and review and scan generated skills before publishing. <br>


## Reference(s): <br>
- [Self Evolution Pro ClawHub release](https://clawhub.ai/windy-001-crypto/self-evolution-pro) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reviews local learning, skill, and evolution files in the user's OpenClaw workspace when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
