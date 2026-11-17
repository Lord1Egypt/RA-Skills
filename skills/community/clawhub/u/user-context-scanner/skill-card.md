## Description:

User Context Scanner builds and maintains a local user profile by scanning OpenClaw memory, extracting preferences and behavior patterns, updating confidence scores, detecting contradictions, and generating clarification questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain a local, structured user profile from memory files and direct answers so agents can adapt responses to user preferences, habits, values, and unresolved contradictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build a persistent profile from private OpenClaw memory and user answers.

Mitigation: Install and run it only when the user intentionally wants local profiling, and review the generated profile and evidence files regularly.

Risk: Plaintext profile, evidence, state, configuration, and signal files may contain personal details.

Mitigation: Restrict workspace access, avoid storing secrets or sensitive personal details, and delete generated .soul files when profiling is no longer needed.

Risk: Automatic memory scanning may infer personal details without clear consent or scope.

Mitigation: Keep scanning scope narrow, require explicit user consent for pattern updates, and disable or adjust memory scanning before use in shared or sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoguoqiang-hub/skills/user-context-scanner)
- [Confidence calculation rules](references/confidence-calculation.md)
- [Contradiction detection rules](references/contradiction-rules.md)
- [User profile schema](references/profile-schema.md)
- [Quiz interaction examples](references/quiz-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [CLI text output, JSON profile and evidence files, Markdown guidance, and signal-style status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local profile, evidence, state, and configuration files under the OpenClaw workspace.]

## Skill Version(s):

0.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
