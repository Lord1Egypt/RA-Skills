## Description: <br>
Export one or more Zeplin screen URLs into a structured layer tree with local assets and package the result as a zip file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sullivangu](https://clawhub.ai/user/sullivangu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to convert Zeplin screen links into local, prompt-ready exports for AI-driven UI implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Zeplin personal access tokens locally for project reuse. <br>
Mitigation: Use a least-privileged token, rotate or revoke it when finished, and delete ~/.zeplin-skill-config.json if token persistence is not desired. <br>
Risk: Exported zips, raw.json, assets, and layers_tree.html can contain proprietary design data. <br>
Mitigation: Treat generated exports as confidential design artifacts and share them only with intended recipients. <br>
Risk: Generated HTML is opened locally from design-derived content. <br>
Mitigation: Open generated HTML only from trusted Zeplin projects and trusted workspaces. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sullivangu/zeplin-to-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, markdown, shell commands, configuration] <br>
**Output Format:** [Zip package containing raw Zeplin JSON, a minified layer tree JSON file, previewable HTML, and local assets, plus a concise Markdown-style status reply.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store per-project Zeplin tokens locally and uses Zeplin screen URLs plus a personal access token to produce the export package.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
