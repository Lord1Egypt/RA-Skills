## Description:

Analyzes writing style features and generates a Voice Profile configuration for capturing author style, creating Voice Profiles, and analyzing text characteristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing-tool users use this skill to analyze reference text and produce a reusable YAML Voice Profile for style-consistent novel or prompt workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional LLM analyzer can send up to 8,000 characters of user text to DashScope.

Mitigation: Use the documented local analyzer for sensitive text, and run the LLM analyzer only when the upload is intended and permitted under the provider's terms.

Risk: Dependencies are not pinned in requirements.txt.

Mitigation: Install in an isolated environment and pin or review dependency versions before production use.

Risk: Rule-based style metrics and rhetorical-device detection may be incomplete or inaccurate.

Mitigation: Review generated Voice Profiles before reuse and provide text samples of at least 500 characters as recommended by the skill documentation.

## Reference(s):

- [ClawHub Style Analyzer skill page](https://clawhub.ai/yuzhihui886/skills/style-analyzer)
- [DashScope chat completions endpoint used by optional LLM analyzer](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands]

**Output Format:** [YAML file plus terminal text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local analyzer writes voice profile, sentence, vocabulary, and rhythm metrics; the optional LLM analyzer writes a voice profile and analysis notes.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
