## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pntrivedy](https://clawhub.ai/user/pntrivedy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture corrections, command failures, missing capabilities, knowledge gaps, and reusable practices as structured project memory. It supports later review, promotion into agent instructions, and extraction of high-value learnings into reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived details in project learning files, which may expose sensitive, customer, personal, or secret data if committed or shared. <br>
Mitigation: Keep .learnings local or review entries before committing, and redact secrets plus customer or personal data before saving or sharing them. <br>
Risk: Promoting logged learnings into agent instruction files can affect future agent behavior with incorrect or unreviewed guidance. <br>
Mitigation: Require explicit human review before editing CLAUDE.md, AGENTS.md, Copilot instructions, or creating new skills from logged content. <br>
Risk: Global prompt or tool hooks can capture reminders across more interactions than intended. <br>
Mitigation: Enable hooks only for projects where durable learning capture is desired, and avoid global hook configuration unless every prompt should be covered. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pntrivedy/self-improving-agent-1-0-1) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Entry examples](artifact/references/examples.md) <br>
- [Hook setup guide](artifact/references/hooks-setup.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown learning, error, and feature-request entries with optional shell commands and hook configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates .learnings markdown files and may propose promotion into CLAUDE.md, AGENTS.md, Copilot instructions, or extracted skill files after review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
