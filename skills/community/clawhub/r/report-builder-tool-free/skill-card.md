## Description: <br>
Summarizes existing daily Markdown reports into weekly or monthly reports, emphasizing outcomes, progress, duplicate-item consolidation, and explicit marking of missing dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users and lightweight work-reporting workflows use this skill to read daily Markdown reports and generate send-ready weekly or monthly summaries from the existing source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags inconsistent privacy and credential-handling guidance, which makes the skill unsuitable for sensitive work reports without review. <br>
Mitigation: Review before installing, use only report directories suitable for the active agent and configured LLM/API provider, and avoid exposing sensitive reports unless the environment is approved. <br>
Risk: The artifact includes broad environment-variable inspection guidance that may expose credential names or operational details. <br>
Mitigation: Avoid running the broad environment-variable check and inspect only the specific configuration values needed for the report workflow. <br>
Risk: The skill can write generated report files, so incorrect output paths or missing backups could overwrite or misplace reports. <br>
Mitigation: Confirm output paths and keep backups before allowing the agent to write generated weekly or monthly report files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/report-builder-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-style structured responses with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated weekly or monthly report files when the agent is allowed to use filesystem tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
