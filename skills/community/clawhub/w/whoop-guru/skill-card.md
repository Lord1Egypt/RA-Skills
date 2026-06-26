## Description: <br>
Whoop Guru helps agents retrieve WHOOP data, generate health summaries and charts, and produce LLM-assisted coaching, recovery, and training-plan guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect to WHOOP, review recovery, sleep, HRV, strain, workout, profile, and body data, and generate coaching summaries, charts, check-ins, and training plans. It is intended for fitness and wellness support, not medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive WHOOP recovery, sleep, HRV, workout, profile, and body data. <br>
Mitigation: Install only when the user accepts this data access, keep local data and token files protected, and delete local data or rotate credentials when uninstalling. <br>
Risk: Optional LLM analysis may send health summaries and prompts to a configured model provider. <br>
Mitigation: Configure an LLM only after reviewing the provider's data handling terms and avoid sending unnecessary personal health details. <br>
Risk: Recurring report and push scripts may rely on environment-specific paths, schedules, and user identifiers. <br>
Mitigation: Review and adjust script configuration before enabling scheduled or push-based workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/effeceee/whoop-guru) <br>
- [WHOOP API Reference](references/api.md) <br>
- [Health Data Analysis Guide](references/health_analysis.md) <br>
- [WHOOP API Application Guide](docs/whoop_api_guide.md) <br>
- [WHOOP Developer Platform](https://developer.whoop.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, generated reports, charts, JSON/local files, and training-plan text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use WHOOP OAuth credentials and optional user-configured LLM credentials; output can include sensitive health summaries derived from local WHOOP data.] <br>

## Skill Version(s): <br>
8.4.12 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
