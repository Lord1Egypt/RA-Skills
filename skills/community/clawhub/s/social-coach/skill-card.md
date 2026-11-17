## Description:

Social Coach helps users record dating and social interactions, review outcomes, generate respectful conversation practice, and track improvement without manipulative tactics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wnzzer](https://clawhub.ai/user/wnzzer)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a dating and social-growth coach that records invitations, interactions, conversation reviews, statistics, and mindset interventions. Agents use it to produce respectful guidance, markdown coaching responses, local record updates, and shell commands for maintaining JSONL history files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive dating, social, and emotional-history records locally.

Mitigation: Use a private storage path with restrictive permissions and avoid storing real names or identifying details.

Risk: The skill includes shell-based JSONL persistence patterns that can mishandle raw user text if not safely serialized.

Mitigation: Review write commands before execution and ensure user-provided text is safely encoded before it is persisted.

## Reference(s):

- [Field Guide](artifact/references/field-guide.md)
- [Analytics](artifact/references/analytics.md)
- [Mindset](artifact/references/mindset.md)
- [ClawHub Skill Page](https://clawhub.ai/wnzzer/skills/social-coach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline bash commands and JSON/JSONL record payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local profile and JSONL history files for social-coaching records.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
