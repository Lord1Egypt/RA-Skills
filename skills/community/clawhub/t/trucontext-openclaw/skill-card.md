## Description:

TruContext OpenClaw gives OpenClaw agents a persistent-memory interface for remembering significant context, recalling prior knowledge, querying a knowledge graph, checking gaps, and managing entity nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alphacollectivellc](https://clawhub.ai/user/alphacollectivellc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users use this skill to persist important project memory across sessions and retrieve graph context before decisions, conversations, or entity updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may store agent context across sessions in TruContext.

Mitigation: Use the skill only where persistent storage is acceptable, and avoid sensitive projects until consent and deletion controls are clear.

Risk: Wrapper flaws could execute local code or select the wrong agent memory context.

Mitigation: Avoid running the wrapper from untrusted or oddly named directories, and ask the publisher to fix path handling and remove the first-agent fallback.

Risk: A compromised or unexpected TruContext toolchain could affect memory operations.

Mitigation: Prefer a pinned, verified installation of the TruContext tools before using the skill.

## Reference(s):

- [TruContext homepage](https://trucontext.ai)
- [ClawHub skill page](https://clawhub.ai/alphacollectivellc/skills/trucontext-openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the trucontext and python3 command-line tools.]

## Skill Version(s):

0.1.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
