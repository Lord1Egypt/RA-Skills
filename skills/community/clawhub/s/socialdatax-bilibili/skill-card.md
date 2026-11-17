## Description:

Searches Bilibili videos and articles, analyzes content, comments, reactions, and creator activity, and can download videos locally on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to research Bilibili content and creators, analyze discussion and reactions, and save videos locally when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI instructions use an unpinned, changeable @latest package, which the security evidence identifies as a supply-chain and credential exposure risk.

Mitigation: Review and pin a specific package version, and verify its integrity before running it.

Risk: The CLI uses SOCIALDATAX_API_KEY, which could be exposed to an untrusted package or publisher.

Mitigation: Provide the key only to a package and publisher you trust, keep it in the documented private credential store, and never include it in logs or chat.

Risk: Online searches and lookups send keywords, content IDs, URLs, or share text to SocialDataX.

Mitigation: Avoid submitting sensitive search terms or content identifiers.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-bilibili)

## Skill Output:

**Output Type(s):** [API Calls, Text, Files]

**Output Format:** [Text responses and optional downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and lookup results depend on SocialDataX access; video files are saved locally only when requested.]

## Skill Version(s):

0.1.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
