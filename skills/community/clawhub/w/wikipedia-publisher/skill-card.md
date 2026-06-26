## Description: <br>
Drafts, reviews, de-risks, and can publish Wikipedia or Wikidata content with a conservative, policy-safe workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colto111](https://clawhub.ai/user/colto111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Editors, developers, and content teams use this skill to prepare Wikipedia articles, sandbox drafts, Wikidata starter statements, citation cleanup, source-quality reviews, notability checks, and COI-sensitive rewrites before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live publishing can modify wiki pages when MediaWiki credentials are supplied. <br>
Mitigation: Use dry-run mode first, prefer sandbox or Draft pages, verify the API endpoint and page title, and use dedicated wiki or bot credentials rather than a primary account. <br>
Risk: Citation enrichment contacts source URLs from the user's environment. <br>
Mitigation: Run citation fetching only on public URLs you are comfortable contacting and review fetched metadata before using it in a draft. <br>
Risk: Weak sourcing, promotional tone, or conflict-of-interest content can lead to rejected or misleading wiki pages. <br>
Mitigation: Run source hygiene, notability, tone, and deletion-risk checks, then remove unsupported or promotional claims before publishing. <br>


## Reference(s): <br>
- [Wikipedia Publisher README](README.md) <br>
- [Citation Guidelines](references/citation-guidelines.md) <br>
- [Publishing Workflow](references/workflow.md) <br>
- [Wikipedia Publishing Red Flags](references/red-flags.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/colto111/wikipedia-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with proposed wiki text, citation templates, command examples, and optional text or JSON-style review reports from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run publishing steps and review notes; live publishing requires user-provided MediaWiki credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
