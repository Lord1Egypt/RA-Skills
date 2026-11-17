## Description:

Generate contextual follow-up suggestions after AI responses. Offers three next questions (Quick, Deep Dive, Related) when the user runs /smart-followups or asks for suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agents use this skill to generate three concise follow-up questions after an AI response, with quick, deeper, and related options. The agent can present the suggestions as text or as channel-supported buttons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documentation contains stale command references.

Mitigation: Use /smart-followups as the primary command and do not rely on older aliases.

Risk: Standalone CLI use can send recent conversation exchanges to the selected provider.

Mitigation: Avoid using the standalone CLI with sensitive conversations unless that provider use is acceptable.

Risk: API keys may be exposed if stored in shell startup files on shared or synced systems.

Mitigation: Store provider keys only in appropriate local secret handling for the deployment environment.

Risk: Manual uninstall instructions may include destructive file removal commands.

Mitigation: Verify the target path before running any rm -rf command.

## Reference(s):

- [ClawHub smart-followups page](https://clawhub.ai/robbyczgw-cla/skills/smart-followups)
- [OpenClaw](https://openclaw.com)
- [OpenRouter Privacy Policy](https://openrouter.ai/privacy)
- [Anthropic Privacy Policy](https://www.anthropic.com/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or numbered text with three follow-up questions; optional JSON/button payloads when supported by the channel or CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Quick, Deep Dive, and Related suggestions from recent conversation context.]

## Skill Version(s):

2.2.0 (source: frontmatter and changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
