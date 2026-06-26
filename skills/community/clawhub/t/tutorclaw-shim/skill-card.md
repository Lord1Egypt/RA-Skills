## Description: <br>
Offline fallback for TutorClaw. When the TutorClaw MCP server is unreachable, follow these PRIMM-Lite teaching instructions for Chapters 1-5 of the beginner programming course. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiktokmanagerhere889-coder](https://clawhub.ai/user/tiktokmanagerhere889-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and tutoring agents use this skill as an offline fallback for beginner programming lessons when the TutorClaw MCP server is unavailable. It guides Chapters 1-5 with a PRIMM-Lite flow that asks learners to predict code behavior before seeing or discussing the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learners may mistake offline fallback mode for the full TutorClaw service. <br>
Mitigation: Tell learners at the start of each conversation that offline mode is active and capabilities are limited. <br>
Risk: The skill could be asked for advanced content outside its stated coverage. <br>
Mitigation: Keep responses within Chapters 1-5 and direct Chapter 6+ requests to the full TutorClaw service. <br>
Risk: Static tutoring guidance can produce incorrect or misleading explanations if used without review. <br>
Mitigation: Review tutoring responses before relying on them for learner assessment; the security evidence reports no executable code, data access, persistence, or hidden privileges. <br>


## Reference(s): <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Release Page](https://clawhub.ai/tiktokmanagerhere889-coder/tutorclaw-shim) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown conversational tutoring responses with short code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute code, track learner progress, personalize exercises, or cover Chapter 6+ content.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
