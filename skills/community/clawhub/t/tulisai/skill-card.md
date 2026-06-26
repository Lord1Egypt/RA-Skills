## Description: <br>
Manages BangunAI Blog content workflows and MDX authoring with BangunAI conventions, including Obsidian-like callouts, Mermaid diagrams, LaTeX, wikilinks, backlinks, and graph views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwirx](https://clawhub.ai/user/dwirx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content authors use this skill to create, update, inspect, and verify BangunAI Blog MDX content across writing, articles, reading notes, daily notes, and special pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows can overwrite special page files such as about.mdx and now.mdx. <br>
Mitigation: Require explicit approval before overwriting special pages and review generated MDX before publishing. <br>
Risk: The documented workflows include file deletion, commits, and pushes that can publish or remove content. <br>
Mitigation: Require explicit approval before deleting posts, committing, or pushing changes. <br>
Risk: Generated MDX can contain incorrect frontmatter, links, diagrams, or embedded components. <br>
Mitigation: Validate frontmatter, preview rendered MDX, and run the documented verification workflow before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dwirx/tulisai) <br>
- [README.md](README.md) <br>
- [INTEGRATION.md](INTEGRATION.md) <br>
- [EXAMPLES.md](EXAMPLES.md) <br>
- [BangunAI Blog repository](https://github.com/dwirx/BangunAI-Blog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MDX templates and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces content-management instructions and MDX-oriented file updates for a specific BangunAI Blog workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
