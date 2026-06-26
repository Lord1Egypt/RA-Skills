## Description: <br>
See where your AI money goes by tracking AI spending across OpenAI, Anthropic, Google, and other providers with breakdowns, budget tracking, and waste detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, and AI tool users can import exported provider billing data, analyze cross-provider spend, track budgets, detect costly model usage, and generate local reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Billing exports and generated JSON or HTML reports can contain sensitive spending and usage information. <br>
Mitigation: Use trusted billing exports only, keep generated reports out of shared folders and repositories, and review dashboards before sharing. <br>
Risk: The security evidence reports that generated HTML includes imported fields before the project escapes them. <br>
Mitigation: Treat HTML dashboards as sensitive local files and avoid opening or sharing dashboards generated from untrusted billing exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/token-books) <br>
- [README](artifact/README.md) <br>
- [Limitations](artifact/LIMITATIONS.md) <br>
- [Configuration example](artifact/config_example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, generated JSON analysis, and local HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-supplied billing exports locally and may produce sensitive JSON or HTML reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
