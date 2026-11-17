## Description:

解卦——四象合参·象推演系统。基于梅花易数+六爻为主体、六壬/奇门为辅助触发、类象知识库展开的符号推演 Skill。不做吉凶判断，展开丰富可能性，启发用户自主决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrryjoke](https://clawhub.ai/user/henrryjoke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with OpenClaw-compatible agents to generate symbolic hexagram interpretation reports for reflection and decision support. It emphasizes multiple possibilities and user judgment rather than deterministic fortune-telling verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to store feedback and preferences on disk and potentially in global agent memory.

Mitigation: Install only when local and global memory storage are acceptable, and avoid including private relationship, health, financial, legal, or third-party details in feedback.

Risk: The skill can steer users toward detailed external feedback submissions through GitHub issue links.

Mitigation: Treat external feedback links as public or semi-public submissions and avoid sharing sensitive personal details.

Risk: Hexagram interpretations may be mistaken for deterministic advice.

Mitigation: Keep outputs framed as possible symbolic interpretations, preserve the non-deterministic disclaimer, and encourage users to apply their own judgment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henrryjoke/skills/sitiantai-xiangtuie)
- [Project homepage](https://github.com/henrryjoke/sitiantai-xiangtuie)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with structured sections, optional code snippets, and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask clarifying questions, execute bundled Python calculation scripts, and adapt report language to the user's input language.]

## Skill Version(s):

0.9.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
