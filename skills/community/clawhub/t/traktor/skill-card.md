## Description: <br>
Extract all assets and content from websites including images, SVGs, fonts, videos, and page structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to collect website assets and page metadata from one or more authorized URLs for analysis, design reference, or local archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraped URLs and generated filenames may be placed into shell commands without clear sanitization. <br>
Mitigation: Review generated curl commands before execution and sanitize or quote URLs, filenames, and output paths. <br>
Risk: The skill downloads website assets and writes files into the current workspace. <br>
Mitigation: Run it only against sites you are authorized to scrape, keep URL batches small, and use a disposable or clearly scoped workspace. <br>
Risk: The workflow relies on browser automation through the claude-in-chrome MCP server. <br>
Mitigation: Use a logged-out or separate browser profile and confirm the browser extension is expected before running extraction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorukardahan/traktor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown progress and summary text with bash commands, JSON manifests, and downloaded asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates asset directories, page-content JSON, asset URL catalogs, and an asset manifest in the current workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
