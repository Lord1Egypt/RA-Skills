## Description:

Transforms any flat prompt into a structured 8-layer XML prompt using RUNE's semantic engine for higher-quality AI responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsarac](https://clawhub.ai/user/mrsarac)

### License/Terms of Use:

MIT

## Use Case:

Developers and prompt authors use this skill to convert a plain prompt into a structured RUNE XML prompt with role, context, intent, governance, reasoning, capability, QA, and output layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Python code from a local external RUNE repository that may change independently of this release.

Mitigation: Use a trusted local RUNE checkout pinned to a reviewed commit before running the skill.

Risk: The skill sources a broad local secrets file to load RUNE_API_KEY.

Mitigation: Prefer an explicit environment variable or a dedicated credential file with restricted permissions.

Risk: Prompts may be sent through an external RUNE data flow that is not fully documented in the evidence.

Mitigation: Avoid confidential prompts until the runtime data flow and retention behavior are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrsarac/skills/rune-prompt-amplification)
- [Publisher profile](https://clawhub.ai/user/mrsarac)
- [RUNE skill homepage](https://github.com/neurabytelabs/rune-skill)
- [RUNE framework](https://github.com/neurabytelabs/rune)
- [RUNE playground](https://github.com/neurabytelabs/rune-playground)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [RUNE-amplified XML prompt emitted as plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+, a local RUNE repository, and RUNE_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
