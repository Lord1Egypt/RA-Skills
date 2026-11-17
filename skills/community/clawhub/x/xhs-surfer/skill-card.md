## Description:

Xhs Surfer automates Xiaohongshu browsing workflows, including search, content browsing, likes, comments, follows, and related account-session controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjlgod](https://clawhub.ai/user/xjlgod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run AI-assisted Xiaohongshu browsing sessions, search for topics, and optionally perform account interactions such as likes, comments, follows, and private-message checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate Xiaohongshu account actions including likes, comments, follows, marketing-oriented browsing, and private-message checks.

Mitigation: Require explicit user confirmation before interactive account actions and use a dedicated low-privilege account.

Risk: The release depends on an external PyPI package and browser automation, which can affect account state and local browser sessions.

Mitigation: Review or pin the package before use, install only in a controlled environment, and avoid sharing reusable cookies unless necessary.

Risk: Environment variables may include unrelated API keys during execution.

Mitigation: Run the skill with a minimal environment containing only the keys needed for the selected LLM provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjlgod/skills/xhs-surfer)
- [Project homepage](https://github.com/MTXAI/xhs_suffer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell code examples; runtime results are JSON-like status objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger browser automation and Xiaohongshu account actions when invoked by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
