## Description: <br>
Generate contextual follow-up suggestions after AI responses, with three suggested next questions for quick clarification, deeper exploration, and related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users invoke this skill during a conversation to get three context-aware follow-up questions they can ask next. It is useful for chat workflows across supported messaging channels where users want quick next steps, deeper technical exploration, or related topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation context is used to generate suggestions and may be processed by the configured AI provider or optional external provider. <br>
Mitigation: Prefer the default OpenClaw-native mode and treat conversation context plus optional OpenRouter or Anthropic API keys as sensitive. <br>
Risk: Broad trigger phrases or auto-trigger behavior can produce suggestions more often than intended. <br>
Mitigation: Use /followups for explicit invocation and keep autoTrigger disabled unless suggestions after every response are intentionally desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/smart-followups) <br>
- [README.md](README.md) <br>
- [CHANNELS.md](CHANNELS.md) <br>
- [FAQ.md](FAQ.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown-style chat text, channel button payloads, numbered text lists, or JSON/text from the optional CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces three suggestions per request: Quick, Deep Dive, and Related. Default OpenClaw use requires Node and no extra API keys; optional standalone CLI/provider use can require OpenRouter or Anthropic keys.] <br>

## Skill Version(s): <br>
2.1.8 (source: server release, SKILL.md frontmatter, changelog released 2026-03-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
