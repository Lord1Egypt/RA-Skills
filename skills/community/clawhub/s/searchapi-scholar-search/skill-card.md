## Description:

Academic Paper Search helps agents find, shortlist, review, and verify scholarly papers and related source evidence using SerpApi-backed Google Scholar and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangnong598](https://clawhub.ai/user/huangnong598)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, faculty, and developers use this skill to build initial literature pools, verify paper metadata, check DOI/source clues, and locate publisher or repository pages before downstream citation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-boundary risk: this version can send a SEARCHAPI_API_KEY value to SerpApi.

Mitigation: Use only a SerpApi key with this version, avoid setting SEARCHAPI_API_KEY unless provider routing is fixed, and rotate any SearchAPI key that may already have been used.

Risk: Search terms and DOI-enrichment titles are sent to external services.

Mitigation: Avoid confidential, unpublished, regulated, or personally sensitive research topics unless disclosure to those services is acceptable.

Risk: Review-paper detection, DOI enrichment, cited-by counts, and search snippets can be incomplete or misleading.

Mitigation: Verify important claims on destination pages and treat the output as leads for review, deduplication, and citation formatting rather than final truth.

## Reference(s):

- [Academic Paper Search ClawHub release](https://clawhub.ai/huangnong598/skills/searchapi-scholar-search)
- [huangnong598 publisher profile](https://clawhub.ai/user/huangnong598)
- [SerpApi search endpoint](https://serpapi.com/search.json)
- [Crossref Works API endpoint](https://api.crossref.org/works)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text summaries or structured JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes titles, authors, venue and year clues, best links, citation counts, DOI or DOI URLs when available, paper-type heuristics, verification hints, and query suggestions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
