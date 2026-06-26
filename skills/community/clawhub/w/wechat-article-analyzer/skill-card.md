## Description: <br>
Fetches user-provided WeChat public-account articles and generates structured analysis of the title, body text, timeline, stakeholders, facts, themes, quotes, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teenyboy](https://clawhub.ai/user/teenyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze a WeChat article URL and convert article content into timelines, stakeholder lists, extracted facts, themes, quotes, and shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches WeChat article URLs supplied by the user, and broad triggers could fetch a link the user did not intend to analyze. <br>
Mitigation: Run it on explicit WeChat article URLs and review automatic trigger behavior before enabling unattended use. <br>
Risk: Dependency hygiene issues in the Python runtime can affect network fetching or YAML handling. <br>
Mitigation: Use a controlled Python environment with pinned, current versions of requests and PyYAML. <br>
Risk: Generated Markdown, YAML, or JSON files may be written to paths selected at runtime. <br>
Mitigation: Review output paths and generated files before consuming reports or registering adapters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teenyboy/wechat-article-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration] <br>
**Output Format:** [Markdown reports, OpenCLI YAML adapter files, and JSON data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports or adapter files to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
