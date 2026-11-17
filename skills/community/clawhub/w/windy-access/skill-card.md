## Description:

Windy Access helps agents pair with Windy Mail, Windy Chat, Windy Mind, and optional Eternitas identity by running the Windy CLI against supported local runtimes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sneakyfree](https://clawhub.ai/user/sneakyfree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw, Hermes Agent, Claude Code, or a generic local agent runtime to Windy services and manage pairing, status, refresh, and disconnect flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install mutable remote code and persist sensitive email, chat, LLM, and identity credentials in local agent configuration.

Mitigation: Prefer a pinned and verifiable CLI package over the curl-to-shell path, proceed only if Windy and the publisher are trusted, confirm which runtimes will be modified, and review how to disconnect or revoke credentials afterward.

Risk: Pairing credentials may grant access to external communication, model, and identity services.

Mitigation: Confirm the selected access tier and target runtimes before pairing, use status checks to inspect active credentials and expiration, and run the documented disconnect flow when access is no longer needed.

## Reference(s):

- [Windy Access on ClawHub](https://clawhub.ai/sneakyfree/skills/windy-access)
- [Windy Connect homepage](https://github.com/sneakyfree/windy-connect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides CLI-driven pairing and reports local runtime effects; the skill itself delegates writes to the Windy CLI.]

## Skill Version(s):

0.3.1 (source: server release evidence; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
