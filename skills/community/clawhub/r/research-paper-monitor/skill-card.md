## Description: <br>
Research Paper Monitor helps researchers track academic papers from sources such as arXiv, PubMed, CNKI, Google Scholar, IEEE Xplore, and Semantic Scholar, score papers against configured keywords, generate Chinese summaries, archive results, and optionally send Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wiltonMotta](https://clawhub.ai/user/wiltonMotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, graduate students, instructors, and research teams use this skill to monitor recent academic papers, filter them by research interests, generate Chinese summaries, and create local Markdown reports or optional notification digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification settings and external integration examples may expose sensitive webhook URLs, SMTP passwords, Zotero API keys, or research-profile data if copied into shared configuration files. <br>
Mitigation: Review notification settings before installation, treat webhook URLs and credentials as secrets, and avoid sharing or syncing ~/.openclaw/research-monitor/config.json unless its contents have been reviewed. <br>
Risk: The documentation includes Feishu webhook examples that should not be reused as live endpoints. <br>
Mitigation: Replace any documented webhook with a user-controlled endpoint or leave notifications disabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wiltonMotta/research-paper-monitor) <br>
- [Configuration Guide](references/configuration.md) <br>
- [Data Sources Guide](references/data-sources.md) <br>
- [Advanced Usage Guide](references/advanced-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON configuration, Markdown paper notes, daily or weekly digest Markdown files, and command-line usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When scripts are run, local configuration and paper records are written under user-configured paths such as ~/.openclaw/research-monitor and ~/.openclaw/research-papers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
