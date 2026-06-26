## Description: <br>
Academic paper discovery and evidence-oriented web search using a SerpApi/SearchAPI-compatible key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangnong598](https://clawhub.ai/user/huangnong598) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, faculty, and research-support agents use this skill to find scholarly papers, collect DOI and citation clues, verify candidate sources, and build initial literature-review shortlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search services and may expose confidential unpublished research topics or personal data. <br>
Mitigation: Use a dedicated API key and avoid submitting confidential unpublished research, personal data, or sensitive institutional details in queries. <br>
Risk: Scholar and web search results can contain incomplete, stale, or misleading citation and source information. <br>
Mitigation: Verify important papers against destination pages, DOI landing pages, publisher records, or institutional repositories before citing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangnong598/searchapi-scholar-search) <br>
- [SerpApi search endpoint](https://serpapi.com/search.json) <br>
- [Crossref Works API](https://api.crossref.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON search results with titles, authors, venue clues, years, links, snippets, DOI data, citation signals, verification hints, and query suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a SERPAPI_API_KEY or SEARCHAPI_API_KEY; Scholar searches may optionally enrich DOI data through Crossref.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
