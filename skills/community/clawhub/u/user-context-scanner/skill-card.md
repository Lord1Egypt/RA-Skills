## Description: <br>
Builds and maintains a local user profile by scanning OpenClaw memory files, detecting preferences and behavior patterns, and updating context from signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain personalization context for an OpenClaw agent by scanning local memories, storing evidence, calculating confidence, detecting contradictions, and generating follow-up quiz prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and maintain a detailed local profile from memory files and questionnaire answers. <br>
Mitigation: Install only when persistent personalization is intended, review the local memory contents before scanning, and periodically inspect or delete the generated profile and evidence files. <br>
Risk: Automatic signal-based updates may refresh the profile without clear per-update consent. <br>
Mitigation: Confirm how to disable automatic scans and signal processing before enabling the skill, and keep consent-oriented configuration such as requireConsentForPatterns enabled. <br>
Risk: Sensitive personal details may be retained in local evidence records. <br>
Mitigation: Avoid answering optional sensitive questions unless needed, keep sensitive-topic exclusion enabled where appropriate, and remove local evidence records that should not be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaoguoqiang-hub/user-context-scanner) <br>
- [Profile schema](references/profile-schema.md) <br>
- [Confidence calculation rules](references/confidence-calculation.md) <br>
- [Contradiction rules](references/contradiction-rules.md) <br>
- [Quiz examples](references/quiz-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, CLI output, JSON profile files, and JSONL evidence or signal records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local OpenClaw workspace profile, evidence, state, configuration, and signal files when executed.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
