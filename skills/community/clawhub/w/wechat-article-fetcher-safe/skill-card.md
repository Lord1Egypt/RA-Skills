## Description: <br>
Fetches accessible WeChat public-account articles with local Chrome and Puppeteer, extracting article text, metadata, and optional images to local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adgai115](https://clawhub.ai/user/adgai115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract content from accessible WeChat public-account article URLs into local Markdown, text, or HTML files for summarization, archiving, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool contacts WeChat article and image servers through a local headless browser. <br>
Mitigation: Use known article URLs and avoid running it from sensitive browsing contexts or networks. <br>
Risk: Extracted article content and downloaded images are written to local storage. <br>
Mitigation: Choose an appropriate output directory and review saved files before sharing or committing them. <br>
Risk: Dependency versions may change during installation without a lockfile. <br>
Mitigation: Pin dependencies or use a lockfile for reproducible installs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adgai115/wechat-article-fetcher-safe) <br>
- [Skill documentation](SKILL.md) <br>
- [Quick start README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, JSON] <br>
**Output Format:** [Markdown, plain text, HTML, and JSON image manifest files, with console status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves extracted article metadata, article content, and optional downloaded images locally.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
