## Description:

Soul Guardian is an AI-assisted counseling support skill for emotional distress, family and relationship issues, workplace stress, personal growth, anxiety, parenting, and related life topics, with local persistent memory and crisis-safety guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taohaowei](https://clawhub.ai/user/taohaowei)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke the skill in Claude Code to receive Chinese-language supportive conversation, reflection prompts, family-systems guidance, and crisis resource reminders for mental health and life stress topics. It is intended as AI support, not professional mental health care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates long-term plaintext mental-health records under ~/.counselor.

Mitigation: Use it only on a private, trusted machine; avoid git or cloud sync for ~/.counselor; inspect and delete records regularly.

Risk: Automatic activation on casual emotional statements can create sensitive records before the user has clearly intended a counseling session.

Mitigation: Prefer explicit /counselor invocation and review the local dossier after sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/taohaowei/skills/soul-guardian-counselor)
- [README](artifact/README.md)
- [Design Philosophy](artifact/docs/design.md)
- [Initialization Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown conversation with local Markdown file updates and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates plaintext records under ~/.counselor when used as designed.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
