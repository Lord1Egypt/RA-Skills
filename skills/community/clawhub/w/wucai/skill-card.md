## Description:

WuCai lets an AI agent retrieve, summarize, and manage a user's WuCai web highlights, annotations, clipped articles, article notes, and diary entries through the WuCai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makediff](https://clawhub.ai/user/makediff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an AI agent to their WuCai personal knowledge base for searching highlights and articles, reviewing recent diary or clipping activity, answering questions from saved web context, and managing note or article state.

### Deployment Geography for Use:

Global, with WuCai account data isolated by the configured CN, EU, or US region.

## Known Risks and Mitigations:

Risk: A live WUCAI_API_TOKEN could be exposed if pasted into chat or stored insecurely.

Mitigation: Store the token in a protected environment or secret setting, avoid pasting it into chat, and rotate it if exposure is suspected.

Risk: The skill can update notes, append diary entries, change article statuses, and trash articles in a private knowledge base.

Mitigation: Require explicit user confirmation before allowing any write, status-change, or trash action.

Risk: Installing from a mutable raw URL can change the reviewed code path later.

Mitigation: Prefer the ClawHub release or a pinned version when installing.

## Reference(s):

- [WuCai API Reference](references/api-details.md)
- [WuCai Documentation](https://doc.wucai.site)
- [WuCai Global Site](https://wucainote.com)
- [ClawHub WuCai Skill Page](https://clawhub.ai/makediff/skills/wucai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text responses, with shell command invocations and JSON-backed API results when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WUCAI_API_TOKEN and can use WUCAI_REGION to select the CN, EU, or US WuCai region.]

## Skill Version(s):

26.3.37 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
