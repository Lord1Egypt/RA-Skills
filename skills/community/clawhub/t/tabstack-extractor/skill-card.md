## Description: <br>
Extracts clean Markdown or schema-based JSON from web pages using the Tabstack API for jobs, news, products, and other structured content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noblepayne](https://clawhub.ai/user/noblepayne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn public or approved web pages into clean Markdown or schema-aligned JSON for analysis, archiving, and scraping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and extracted page content are processed by the external Tabstack API. <br>
Mitigation: Use the skill only for public or approved web pages, and avoid private intranet URLs, secrets, or regulated data unless Tabstack processing is approved. <br>
Risk: The Tabstack API key could be exposed through shell history, checked-in configuration, or shared logs. <br>
Mitigation: Store TABSTACK_API_KEY securely, prefer environment or approved secret storage, and do not commit credentials. <br>
Risk: The optional Babashka install path pipes a remote script into bash. <br>
Mitigation: Prefer Homebrew, Nix, or an inspected pinned release before running installer code. <br>
Risk: Automated extraction can conflict with site policies or overwhelm target sites. <br>
Mitigation: Respect site scraping policies and robots.txt, test with small batches first, and add delays for repeated requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/noblepayne/tabstack-extractor) <br>
- [Tabstack API Reference](references/api_reference.md) <br>
- [Schema Creation Guide](references/schema_guide.md) <br>
- [Job listing schema](references/job_schema.json) <br>
- [News article schema](references/news_schema.json) <br>
- [Simple article schema](references/simple_article.json) <br>
- [Tabstack extract JSON documentation](https://docs.tabstack.ai/api/extract-json-v-1) <br>
- [JSON Schema documentation](https://json-schema.org/learn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; API responses may be Markdown text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TABSTACK_API_KEY and an approved target URL; JSON extraction uses a supplied schema.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
