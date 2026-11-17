## Description:

Query the Unofficial Urban Dictionary API for slang definitions. Use when asked to define slang/phrases, fetch random Urban Dictionary entries, browse by letter/new, or get entries by author/date. Supports endpoints /api/search, /api/random, /api/browse, /api/author, and /api/date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougbtv](https://clawhub.ai/user/dougbtv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up slang terms, random entries, browse views, author entries, or date-filtered entries from the Unofficial Urban Dictionary API and return concise definitions with examples and ratings when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms and related query parameters are sent to unofficialurbandictionaryapi.com.

Mitigation: Use the skill only when external slang lookup requests are acceptable, and avoid sending sensitive or private terms.

Risk: Returned slang definitions may include offensive or NSFW content.

Mitigation: Report results neutrally, limit output to relevant entries, and avoid adding extra offensive language beyond what is necessary to answer the user.

## Reference(s):

- [Unofficial Urban Dictionary API base endpoint](https://unofficialurbandictionaryapi.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls]

**Output Format:** [Markdown summaries and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default reporting shows the top 3-5 entries with term, short definition, example, ratings, and permalink when present.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
