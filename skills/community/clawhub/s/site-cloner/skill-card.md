## Description: <br>
Clone any live website into a self-contained, dependency-free HTML file with all content, styles, fonts, and images extracted and preserved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michelle447](https://clawhub.ai/user/michelle447) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site builders use this skill to recreate a live website as a standalone HTML file, including assets, styling, and optional SPA bundle extraction. When requested, it can also guide deployment to nginx on a VPS or publication to a private GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone arbitrary websites, which may create copyright, terms-of-service, or brand misuse issues. <br>
Mitigation: Use it only for sites you own or have explicit permission to reproduce, and review cloned content before publishing. <br>
Risk: The artifact includes VPS deployment guidance with hard-coded infrastructure details and root-based remote commands. <br>
Mitigation: Replace all destinations and credentials, avoid root deployment, and confirm every remote write before execution. <br>
Risk: The artifact includes GitHub publishing guidance that can push copied content externally. <br>
Mitigation: Use private repositories unless publication is approved, and verify repository ownership, remotes, and content before pushing. <br>


## Reference(s): <br>
- [HTML Clone Template Guide](references/html-template.md) <br>
- [SPA Bundle Extraction Guide](references/spa-extraction.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell, HTML, CSS, JavaScript, SSH, nginx, and git command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths, image counts, GitHub URLs, and VPS URLs when those actions are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
