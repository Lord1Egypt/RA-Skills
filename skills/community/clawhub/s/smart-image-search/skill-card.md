## Description:

Searches multiple image engines from a text query, ranks candidates for relevance and quality, and returns a best image, candidate links, source pages, or ready-to-open search links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumu-0922](https://clawhub.ai/user/mumu-0922)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find image results for people, characters, brands, memes, wallpapers, avatars, logos, and other visual reference requests. It is intended to return a strong match when confidence is high and candidate links or search URLs when confidence is lower.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-search terms are sent to external providers including Bing, Baidu, and Sogou.

Mitigation: Avoid private or sensitive queries and run the skill in an environment with restricted network egress when appropriate.

Risk: The skill may automatically download third-party image files with weak network and file-size safeguards.

Mitigation: Review before installing, use temporary-file cleanup, and add URL validation and download-size limits before high-trust use.

## Reference(s):

- [Confidence](references/confidence.md)
- [Entity Consistency](references/entity-consistency.md)
- [Entity Gating](references/entity-gating.md)
- [Intent Routing](references/intent-routing.md)
- [Official Sources](references/official-sources.md)
- [Official Whitelist](references/official-whitelist.md)
- [Parameters](references/parameters.md)
- [Quality Filtering](references/quality-filtering.md)
- [Relevance](references/relevance.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands]

**Output Format:** [Markdown responses with links, JSON from helper scripts, and local image files when download succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May attach downloaded image files or provide multiple candidate links when confidence is not high.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
