## Description: <br>
A deep-research skill for the SIAS Multi-Agent System that helps agents analyze FOIA requests, NGO networks, public funding, local database findings, and web sources for Cologne and NRW research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iggyswelt](https://clawhub.ai/user/iggyswelt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and agents working in the SIAS/Rheingold environment use this skill to structure investigations into FOIA correspondence, NGO networks, funding flows, and related public records. It guides database checks, source validation, contradiction handling, and concise reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist investigative findings, mail contents, and personal data to SIAS database tables. <br>
Mitigation: Install only in the intended SIAS/Rheingold environment, restrict database permissions to the required tables, and define retention and deletion rules before use. <br>
Risk: The artifact instructs agents to send critical findings to a fixed Telegram recipient. <br>
Mitigation: Disable or rewrite the Telegram notification rule and require explicit user approval before any external notification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iggyswelt/sias-research-v1) <br>
- [SIAS Project](https://github.com/iggyswelt/SIAS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with SQL snippets, command examples, source labels, confidence levels, and follow-up questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database write guidance for configured SIAS tables and recommendations for reviewing contradictory sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
