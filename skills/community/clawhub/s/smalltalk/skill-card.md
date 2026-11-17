## Description:

Interact with live Smalltalk images (Cuis or Squeak) to evaluate code, browse classes, view method source, define classes and methods, and query hierarchies and categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnmci](https://clawhub.ai/user/johnmci)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect, execute, and modify code in live Squeak or Cuis Smalltalk images. It also supports code explanation, comment audits, and SUnit test generation when configured with an LLM provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External LLM commands can send selected Smalltalk source code to Anthropic or OpenAI-compatible endpoints.

Mitigation: Use LLM commands only with trusted endpoints and avoid proprietary or secret code unless sharing is approved.

Risk: The skill can execute and modify code in a live Smalltalk image, including dev-mode changes and delete operations.

Mitigation: Use playground mode for disposable work and keep backups or snapshots before persistent dev-mode mutation.

Risk: Persistent background daemons keep VM state across tool calls.

Mitigation: Check daemon status and stop or restart daemons when the session no longer requires them.

Risk: Custom OpenAI-compatible endpoint settings can redirect code and prompts to a configured endpoint.

Mitigation: Set OPENAI_API_BASE only to trusted HTTPS endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnmci/skills/smalltalk)
- [Squeak Setup](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/SQUEAK-SETUP.md)
- [Clawdbot Setup](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/CLAWDBOT-SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, Smalltalk code, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute against a live Smalltalk image, start or use a persistent daemon, and file generated SUnit tests into the image.]

## Skill Version(s):

1.7.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
