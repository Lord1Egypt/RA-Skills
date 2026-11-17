## Description:

Generates Amap search links from user-provided place, location, or address names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaohong-test](https://clawhub.ai/user/zhaohong-test)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to convert place, location, or address requests into direct Amap search links, including separate links for multiple locations in one request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad location questions may be answered with an Amap search link instead of directions or factual context.

Mitigation: Use the skill for search-link generation and ask separately when directions or factual context are needed.

Risk: Place names with unusual characters may produce links that need URL encoding review.

Mitigation: Check generated links for unusual place-name input and percent-encode the query value when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaohong-test/skills/zhaohong-hello-world)
- [Amap search URL template](https://ditu.amap.com/search?query={keyword})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing generated Amap search links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns links only; no API key, credential, file access, code execution, persistence, or external API call is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
