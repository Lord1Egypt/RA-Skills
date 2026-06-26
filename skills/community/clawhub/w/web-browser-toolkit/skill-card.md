## Description: <br>
OpenClaw Web Browser helps agents fetch web pages, extract structured data, monitor changes, and use aviation-focused collection presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to collect web content, extract page data into structured JSON, monitor pages for changes, and recommend related official documents for aviation and regulatory research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch external web pages and save collected content locally. <br>
Mitigation: Use dedicated output directories and avoid sensitive logged-in pages unless local artifacts are acceptable. <br>
Risk: Monitoring can be scheduled to run continuously. <br>
Mitigation: Enable cron or recurring monitors only for specific targets you intend to check continuously. <br>
Risk: Web collection may be inappropriate for some target sites or content. <br>
Mitigation: Review target-site rules and scope collection to sites and pages you are permitted to access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkbeomjun-gkgkgk/web-browser-toolkit) <br>
- [README](README.md) <br>
- [Aviation presets](references/aviation_presets.json) <br>
- [CSS selector guide](references/selector_guide.md) <br>
- [Official document recommender knowledge base](sub-skills/doc-recommender/references/doc_knowledge_base.json) <br>
- [Official document recommender keyword mapping](sub-skills/doc-recommender/references/keyword_mapping.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus JSON collection, monitoring, diff, and recommendation outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local collection outputs, monitor snapshots, diffs, alerts, and recommendation files when the included scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
