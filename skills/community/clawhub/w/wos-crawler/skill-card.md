## Description: <br>
wos-crawler helps agents guide a Web of Science literature crawling workflow and batch PDF download workflow through a local web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grizzlyccc](https://clawhub.ai/user/grizzlyccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to guide Web of Science searches, export crawled literature metadata to Excel, and coordinate batch PDF downloads from configured sources. The release evidence notes that the referenced executable code is missing, so users should verify the complete source before relying on the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release describes WOS crawling and PDF downloading, but the referenced executable code is absent. <br>
Mitigation: Review the publisher-provided full source before installing or running the skill, and do not rely on the workflow until the missing script behavior can be inspected. <br>
Risk: The workflow may involve WOS or institutional credentials and persistent cookies. <br>
Mitigation: Do not enter credentials until cookie storage, deletion, and browser-profile controls are documented; use an isolated browser profile where possible. <br>
Risk: The workflow may contact external PDF services and perform bulk downloads. <br>
Mitigation: Confirm allowed sources, crawl limits, output paths, and organizational policy before enabling downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grizzlyccc/wos-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local Web UI launch, WOS search setup, Excel export, output directory selection, and PDF folder review.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
