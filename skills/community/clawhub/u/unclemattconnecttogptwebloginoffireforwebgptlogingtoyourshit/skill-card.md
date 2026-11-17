## Description:

Provides an explicit-invocation bridge for agents to use an already-authenticated local Codex ChatGPT login without copying credentials, while warning that prompt text is sent to the provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check local Codex ChatGPT login availability and send approved prompts through the authenticated provider without handling raw credentials. It is intended for explicit bridge or setup requests where the user accepts provider exposure for the prompt text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-controlled Codex runs may cause readable workspace files or environment values to be processed by the authenticated provider.

Mitigation: Use the skill from a clean, minimal working directory with a sanitized shell environment, and do not run ask on untrusted prompts or in projects containing secrets.

Risk: The ask and smoke commands send prompt text to the authenticated Codex/ChatGPT provider account.

Mitigation: Confirm the prompt is safe for provider processing before forwarding it, and remove passwords, API keys, cookies, private documents, regulated personal data, and other sensitive material.

Risk: The skill invokes a locally authenticated provider account.

Mitigation: Run status first to confirm bridge availability, and install or use the skill only when that authenticated-account behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/unclemattconnecttogptwebloginoffireforwebgptlogingtoyourshit)
- [Publisher profile](https://clawhub.ai/user/uncmatteth)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bridge supports status, smoke, and ask commands; ask and smoke send prompt text to the authenticated provider.]

## Skill Version(s):

1.420.69 (source: release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
