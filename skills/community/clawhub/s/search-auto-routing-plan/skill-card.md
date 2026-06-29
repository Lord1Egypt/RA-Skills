## Description: <br>
Plan which search provider to use before multi-provider skills run by scoring query signals, choosing Serper, Tavily, Exa, Brave, or Firecrawl, defining fallback chains, and documenting the rationale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruti3](https://clawhub.ai/user/ruti3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan search-provider routing before running multi-provider search workflows. It helps select a primary provider, fallback chain, query phrasing, and quality checks without calling search APIs itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downstream executor skills may perform live searches, use API keys, or handle sensitive queries outside this planning skill. <br>
Mitigation: Review any downstream executor skill separately, especially when it performs live searches, uses API keys, or handles sensitive queries. <br>
Risk: A routing plan can recommend an unsuitable provider or fallback chain if query signals, constraints, or available providers are incomplete. <br>
Mitigation: Confirm the search goal, signal scores, constraints, and available providers before using the plan to drive execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruti3/skills/search-auto-routing-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with scoring tables, fallback steps, checklist items, and optional YAML executor hints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planning-only output; no API calls, network access, credentials, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
