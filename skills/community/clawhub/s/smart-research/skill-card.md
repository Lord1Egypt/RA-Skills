## Description:

smart-research helps agents run multi-engine public web search, fetch pages through fallback readers, and return structured research results without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect public web search results, fetch selected pages, and consolidate them into structured research outputs for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External reader fallbacks can forward submitted URLs to third-party services.

Mitigation: Use the skill only for public, non-sensitive research unless third-party reader fallbacks are disabled or explicitly approved.

Risk: Unrestricted URL fetching can expose internal URLs, signed links, secrets, or regulated data if users submit them.

Mitigation: Add URL filtering or allowlists before use in environments where private hosts or sensitive links may be reachable.

Risk: The documented system-wide dependency installation can affect the host Python environment.

Mitigation: Install pinned dependencies in an isolated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xx235300/skills/smart-research)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Requirements](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, guidance]

**Output Format:** [Structured JSON or dict results, with optional Markdown search reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes result titles, URLs, snippets, source engines, fetch methods, timestamps, scores, fetched content, and error details when available.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
