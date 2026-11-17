## Description:

SlonAide lets an agent query recording notes, retrieve transcripts and AI summaries, and set up an AiDeNote remote bridge for local OpenClaw access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajingmiao](https://clawhub.ai/user/ajingmiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who use SlonAide or AiDeNote use this skill to search and review recording notes, transcripts, AI-generated summaries, tags, and processing status from an OpenClaw agent. Users can also install and check a phone-to-local-OpenClaw bridge on macOS or Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bridge setup downloads and runs external installer code and creates an auto-starting tunnel service.

Mitigation: Install the bridge only when the user trusts SlonAide/AiDeNote and wants phone-to-local-OpenClaw connectivity; review installer URLs and service behavior before use.

Risk: Bridge setup passes API credentials to installer-controlled code and diagnostic output may expose key or token fragments.

Mitigation: Use a least-privilege API key, avoid sharing diagnostic output publicly, and rotate credentials if logs or terminal output may have exposed secrets.

Risk: Custom installer, API, tunnel, or relay URLs can redirect setup or traffic to endpoints outside the expected service.

Mitigation: Use the default service URLs unless the user controls the replacement endpoints.

## Reference(s):

- [ClawHub SlonAide Skill Page](https://clawhub.ai/ajingmiao/skills/slonaide)
- [SlonAide Web App](https://h5.slonaide.cn/)
- [AiDeNote Web App](https://h5.aidenote.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown-style text with command snippets and structured note summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include truncated transcripts, AI summaries, note metadata, bridge installation status, and diagnostic messages.]

## Skill Version(s):

3.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
