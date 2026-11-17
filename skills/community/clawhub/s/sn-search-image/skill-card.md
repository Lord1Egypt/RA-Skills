## Description:

Google-backed image discovery via Serper.dev that returns image URLs, page URLs, titles, and source domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find candidate image assets and collect image/page metadata from Serper.dev without building a custom search client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Serper API key can be sent to an environment-selected server if SERPER_BASE_URL is changed.

Mitigation: Run the skill only in environments where SERPER_BASE_URL is unset, fixed to https://google.serper.dev, or allowlisted by policy.

Risk: Raw result JSON can be written to arbitrary paths through --save-json.

Mitigation: Use --save-json only with a known safe temporary path and avoid writing into sensitive or shared directories.

Risk: Image results are external candidate metadata and may be inaccurate, unavailable, or unsuitable for the intended use.

Mitigation: Review returned image URLs, page URLs, titles, source domains, and applicable usage rights before using any result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-image)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Serper.dev API endpoint](https://google.serper.dev)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Formatted text, URL lists, or raw JSON from the Serper image search response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SERPER_API_KEY; supports country and language bias through --gl and --hl.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
