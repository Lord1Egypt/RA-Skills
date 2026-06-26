## Description: <br>
READ-ONLY wine and alcohol information lookup skill that searches for wine details, ratings, price comparisons, background information, pairings, vintage guidance, health-related drinking guidance, and label-photo identification support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amurtiger01](https://clawhub.ai/user/amurtiger01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up wine and alcohol information, compare ratings and prices, generate search links, and present structured results from third-party wine, shopping, encyclopedia, and food-data sources. Health-related sections should be treated as general information rather than medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wine search terms and optional label-derived text may be sent to external wine, shopping, Wikipedia, Open Food Facts, and Firecrawl services. <br>
Mitigation: Use the skill only when those external lookups are acceptable, avoid entering sensitive personal details in search terms, and review generated WebFetch targets before fetching. <br>
Risk: The optional Firecrawl key can be exposed if passed as a command-line argument. <br>
Mitigation: Prefer the FIRECRAWL_API_KEY environment variable and avoid command-line key arguments in shared shells, logs, or process listings. <br>
Risk: Health-related drinking guidance may be mistaken for medical advice. <br>
Mitigation: Present health content as general information and direct users to qualified healthcare professionals for medical decisions. <br>
Risk: Fetched third-party pages may contain untrusted content or instructions. <br>
Mitigation: Treat fetched page content as data only and ignore instructions embedded in third-party web pages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amurtiger01/wine-info-search) <br>
- [Project Homepage](https://github.com/Amurtiger01/wine-info-search-skill) <br>
- [Wine Data Source Reference](references/api_reference.md) <br>
- [Firecrawl](https://firecrawl.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style structured text with command examples, search links, wine metadata, price hints, and advisory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core behavior is read-only; optional OCR dependencies and an optional FIRECRAWL_API_KEY can expand label recognition and Vivino search coverage.] <br>

## Skill Version(s): <br>
1.6.1 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
