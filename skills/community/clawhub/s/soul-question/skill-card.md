## Description: <br>
Soul Question generates deep, grounded questions from user-provided text by identifying cracks in the user's thinking, including contradictions, untested assumptions, value-behavior gaps, frame locks, avoidance, and meta-question signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyipeng1](https://clawhub.ai/user/chenyipeng1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to examine conversations, meeting notes, journals, strategy documents, and similar text for blind spots. The skill returns concise questions anchored to the supplied material rather than summaries, advice, or generic reflection prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste secrets, credentials, regulated personal data, confidential business information, or private third-party communications for analysis. <br>
Mitigation: Redact sensitive material first and only provide private third-party communications when you have permission to use them. <br>
Risk: Questions about personal journals, team dynamics, or sensitive topics may feel confrontational if phrased carelessly. <br>
Mitigation: Keep questions grounded in the supplied material, genuinely open, and respectful; avoid judgment, disguised advice, and unsupported claims. <br>
Risk: Thin or low-signal input can lead to shallow or unsupported questions. <br>
Mitigation: Ask for richer context when material is too short and decline to generate a question when no meaningful cognitive crack is supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyipeng1/soul-question) <br>
- [Declared project homepage](https://github.com/plaud/soul-question) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown heading followed by 0-3 direct questions and a short source citation for each question] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes no external calls, persistence, telemetry, or file writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
