## Description: <br>
Bootstrap and maintain a personal LLM wiki: a persistent, compounding knowledge base of interlinked markdown pages that the agent writes and maintains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, researchers, and developers use this skill to create and maintain a local markdown knowledge base, ingest source material, answer questions from accumulated wiki pages, and audit the wiki for gaps or contradictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous ingest requests or an incorrect wiki root could lead the agent to update the wrong local wiki files. <br>
Mitigation: Choose the wiki root deliberately and review proposed writes during ingest, especially for broad requests such as ingesting an unspecified source. <br>
Risk: Generated wiki pages may contain outdated, contradictory, or unsourced claims. <br>
Mitigation: Use the skill's audit workflow to check contradictions, stale claims, missing citations, and pages marked as needing verification. <br>


## Reference(s): <br>
- [Wiki page template](artifact/templates/page.md) <br>
- [qmd local wiki search](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown files and plain-text responses, with optional tables, slide decks, or charts when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local wiki files under wiki/ while preserving raw source files under raw/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
