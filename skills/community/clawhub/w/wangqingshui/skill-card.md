## Description:

A Chinese-language wrapper for the Mengpo narrative engine that helps agents generate and integrate reflective memory monologues and share-card copy while preserving the engine's call contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninebirds01-crypto](https://clawhub.ai/user/ninebirds01-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Mengpo-style emotional memory prose, share-card text, and integration guidance for a local WeChat mini-program narrative engine. It is most useful when the existing engine files are available and the goal is stable invocation rather than changing story logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional self-test script inspects local project modules and should only be run against the intended Mengpo narrative engine directory.

Mitigation: Review the copied script before execution and run it from the engine root that contains the expected utils/composer.js and data/*.js files.

Risk: The skill depends on the local engine's compose parameter order, five KEYMAP dimensions, relationship combinations, and semantic guard comments.

Mitigation: Run the documented guard self-test before release or upgrade, and treat failures as a signal to repair the engine contract before using the wrapper.

Risk: Generated memory content may be sensitive when saved through the app's expected local history feature.

Mitigation: Review local storage behavior and user-facing privacy expectations before deploying the skill in workflows that collect personal memories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ninebirds01-crypto/skills/wangqingshui)
- [Uploaded Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional local self-test steps; security evidence reports no hidden network access, credential handling, or automatic persistence beyond the app's expected local history feature.]

## Skill Version(s):

1.0.1 (source: server release metadata; uploaded SKILL.md frontmatter states 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
